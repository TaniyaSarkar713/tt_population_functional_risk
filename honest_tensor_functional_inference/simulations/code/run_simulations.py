"""Exact marginal Monte Carlo experiments for the prespecified protocol."""
import argparse
import csv
import hashlib
import json
import platform
import time
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import beta, norm
from intervals import centers, radii

ROOT = Path(__file__).resolve().parents[1]
SEED = 20260909


def configurations():
    configs = []
    for K in (2, 3, 4, 6):
        for p in (128, 512, 2048, 8192):
            lam = radii(K, p, p**-0.5).threshold
            configs.append(dict(experiment="core", K=K, p=p, n=p, cap=1,
                                amplitude=0.0, support=1, noise="gaussian"))
            for amplitude in (0.02, 0.2, 1.0):
                near = int(np.clip(round((amplitude / lam)**(2/K)), 1, p))
                for support in sorted({1, p, near}):
                    configs.append(dict(experiment="core", K=K, p=p, n=p,
                                        cap=1, amplitude=amplitude, support=support,
                                        noise="gaussian"))
    for p in (512, 2048, 8192):
        near = max(1, round((1 / radii(3, p, p**-0.5).threshold)**(2/3)))
        for support in sorted({1, near}):
            for epsilon in (0, 0.001, 0.01, 0.1, 0.5):
                configs.append(dict(experiment="weak_rank", K=3, p=p, n=p,
                                    cap=2, epsilon=epsilon, support=support,
                                    noise="gaussian"))
    for ratio in (0.25, 1, 4, 16):
        for multiplier in (1, 1.5):
            configs.append(dict(experiment="noise_level", K=3, p=2048,
                                n=int(2048*ratio), cap=1, amplitude=0.2,
                                support=3, multiplier=multiplier, noise="gaussian"))
    for noise in ("gaussian", "student_t3", "variance_contamination", "correlated"):
        configs.append(dict(experiment="assumption_stress", K=3, p=512, n=512,
                            cap=1, amplitude=0.0, support=1, noise=noise))
    return configs


def signal(config):
    K, p, s = config["K"], config["p"], config["support"]
    a = np.zeros(p)
    oracle_diagonal = None
    if config["experiment"] == "weak_rank":
        epsilon = config["epsilon"]
        a[:s] = np.sqrt(1-epsilon**2) / s**(K/2)
        a[s:2*s] = epsilon / s**(K/2)
    else:
        amplitude = config["amplitude"]
        a[:s] = amplitude / s**(K/2)
        if config["experiment"] == "core" and amplitude > 0:
            oracle_diagonal = np.zeros(p)
            oracle_diagonal[:s] = s**(-K/2)
    return a, oracle_diagonal


def random_noise(rng, shape, kind):
    if kind == "gaussian":
        return rng.normal(size=shape)
    if kind == "student_t3":
        return rng.standard_t(3, size=shape) / np.sqrt(3)
    if kind == "variance_contamination":
        g = rng.normal(size=shape)
        return g * np.where(rng.random(shape) < 0.05, 10.0, 1.0)
    if kind == "correlated":
        return np.sqrt(0.8)*rng.normal(size=shape) + np.sqrt(0.2)*rng.normal(size=(shape[0], 1))
    raise ValueError(kind)


def summarize(errors, halfwidth):
    N = len(errors)
    success = int(np.sum(np.abs(errors) <= halfwidth * (1 + 1e-12)))
    coverage = success / N
    lo = 0.0 if success == 0 else beta.ppf(0.025, success, N-success+1)
    hi = 1.0 if success == N else beta.ppf(0.975, success+1, N-success)
    return dict(repetitions=N, coverage=coverage,
                coverage_mcse=np.sqrt(coverage*(1-coverage)/N),
                coverage_ci_lower=lo, coverage_ci_upper=hi,
                mean_length=2*halfwidth, length_mcse=0.0,
                bias=float(errors.mean()), bias_mcse=float(errors.std(ddof=1)/np.sqrt(N)),
                rmse=float(np.sqrt(np.mean(errors**2))))


def simulate(config, repetitions, batch=128):
    encoded = json.dumps(config, sort_keys=True).encode()
    digest = hashlib.sha256(encoded).digest()
    stream = [SEED] + list(np.frombuffer(digest[:16], dtype="<u4"))
    rng = np.random.default_rng(np.random.SeedSequence(stream))
    p, K = config["p"], config["K"]
    tau = config["n"]**-0.5
    rad = radii(K, p, tau, rank_cap=config["cap"],
                multiplier=config.get("multiplier", 1))
    a, oracle_diagonal = signal(config)
    psi = a.sum() / np.sqrt(p)
    errors = {name: [] for name in ("nonlinear", "gaussian", "structural", "selected")}
    widths = {name: getattr(rad, name) for name in ("nonlinear", "gaussian", "structural")}
    widths["selected"] = widths[rad.selected]
    if oracle_diagonal is not None:
        c = oracle_diagonal.sum() / np.sqrt(p)
        widths["known_direction_oracle"] = norm.ppf(0.975)*tau*abs(c)
        errors["known_direction_oracle"] = []
        leftover = np.sqrt(max(0.0, 1-np.dot(oracle_diagonal, oracle_diagonal)))
    for start in range(0, repetitions, batch):
        size = min(batch, repetitions-start)
        g = random_noise(rng, (size, p), config["noise"])
        estimates = centers(a[None, :] + tau*g, rad.threshold)
        estimates["selected"] = estimates[rad.selected]
        if oracle_diagonal is not None:
            projected = g @ oracle_diagonal + leftover*rng.normal(size=size)
            estimates["known_direction_oracle"] = c*(config["amplitude"] + tau*projected)
        for name, center in estimates.items():
            errors[name].append(center - psi)
    return [{**config, "config_id": hashlib.sha256(encoded).hexdigest()[:12],
             "tau": tau, "truth": psi, "threshold": rad.threshold,
             "selected_method": rad.selected, "method": name,
             "in_model": config["noise"] == "gaussian",
             **summarize(np.concatenate(values), widths[name])}
            for name, values in errors.items()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repetitions", type=int, default=2000)
    args = parser.parse_args()
    if args.repetitions < 2:
        raise ValueError("At least two replications are needed")
    configs = configurations()
    dest = ROOT / "results"
    dest.mkdir(exist_ok=True)
    (dest / "configurations.json").write_text(json.dumps(configs, indent=2)+"\n")
    start = time.monotonic()
    rows = []
    for i, config in enumerate(configs):
        rows.extend(simulate(config, args.repetitions))
        if (i+1) % 20 == 0 or i+1 == len(configs):
            print(f"Completed {i+1}/{len(configs)} configurations", flush=True)
    columns = sorted({key for row in rows for key in row})
    with (dest / "summary.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    files = sorted(Path(__file__).parent.glob("*.py"))
    manifest = dict(seed=SEED, configurations=len(configs), rows=len(rows),
                    repetitions_per_configuration=args.repetitions,
                    elapsed_seconds=time.monotonic()-start,
                    completed_utc=datetime.now(timezone.utc).isoformat(),
                    python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
                    platform=platform.platform(),
                    code_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
                    result_sha256=hashlib.sha256((dest/"summary.csv").read_bytes()).hexdigest(),
                    experiment="Exact marginal of full Gaussian tensor mean; stress rows excluded")
    (dest / "run_manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
