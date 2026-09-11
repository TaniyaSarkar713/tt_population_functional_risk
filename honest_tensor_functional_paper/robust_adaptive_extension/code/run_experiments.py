"""Seeded coverage, cost and failure-mode experiments for the new procedures."""
import hashlib
import json
import os
import platform
import time
from pathlib import Path

os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np
import scipy
from scipy.stats import beta, norm

from methods import (adaptive_interval, inner, mom_parameters, pilot_envelope,
                     robust_scan_errors, small_full_nets, surrogate_interval)

ROOT = Path(__file__).resolve().parents[1]
SEED = 2026091107


def proportion(values):
    values = np.asarray(values, dtype=bool)
    n, k = len(values), int(values.sum())
    return dict(successes=k, repetitions=n, rate=k / n,
                mcse=float(np.sqrt(k / n * (1 - k / n) / n)),
                ci95=[float(beta.ppf(.025, k, n - k + 1)) if k else 0.0,
                      float(beta.ppf(.975, k + 1, n - k)) if k < n else 1.0])


def noise(rng, shape, kind):
    if kind == 'gaussian':
        return rng.normal(size=shape)
    if kind == 'rademacher':
        return rng.choice([-1.0, 1.0], size=shape)
    if kind == 'correlated_gaussian':
        return np.sqrt(.5) * rng.normal(size=shape) + np.sqrt(.5 / np.prod(shape)) * rng.normal()
    if kind == 'student_t3':
        return rng.standard_t(3, size=shape) / np.sqrt(3)
    if kind == 'rare_outliers':
        epsilon = .0001
        return (np.sqrt(.1) * rng.normal(size=shape)
                + (rng.random(shape) < epsilon) * rng.choice([-1.0, 1.0], size=shape)
                * np.sqrt(.9 / epsilon))
    raise ValueError(kind)


def adaptive_experiment(rng, repetitions=500):
    rows = []
    p, K = 8, 3
    shape = (p,) * K
    eta = float(pilot_envelope(shape)[0])
    flat = np.zeros(shape)
    for i in range(p):
        flat[(i,) * K] = 1 / np.sqrt(p)
    off = np.zeros(shape)
    off[0, 1, 2] = 1
    for kind in ['gaussian', 'rademacher', 'correlated_gaussian']:
        for loading_name, loading in [('diagonal', flat), ('general', np.sqrt(.91) * flat + .3 * off)]:
            for rank, strength in [(0, 0)] + [(r, s) for r in [1, 2] for s in [.25, 3, 100, 1000]]:
                mean = np.zeros(shape)
                amplitude = strength * eta
                for i in range(rank):
                    mean[(i,) * K] = amplitude
                M = 1.1 * amplitude * np.sqrt(rank) if rank else 100 * eta
                target = inner(loading, mean)
                covered, recovered, projected, widths, biases, errors, times = [], [], [], [], [], [], []
                for _ in range(repetitions):
                    pilot = mean + noise(rng, shape, kind)
                    second = mean + noise(rng, shape, kind)
                    start = time.perf_counter()
                    fit = adaptive_interval(pilot, second, loading, M, gaussian=kind != 'rademacher')
                    times.append(time.perf_counter() - start)
                    covered.append(fit['lo'] <= target <= fit['hi'])
                    recovered.append(fit['ranks'] == [rank] * K)
                    projected.append(fit['selected'] == 'projected')
                    widths.append(fit['width'])
                    biases.append(fit['bias'])
                    errors.append((fit['center'] - target) ** 2)
                q = norm.ppf(.98) if kind != 'rademacher' else np.sqrt(2 * np.log(50))
                rows.append(dict(noise=kind, loading=loading_name, p=p, K=K, rank=rank,
                                 strength_over_eta=strength, amplitude=amplitude, M=M, eta=eta,
                                 theorem_assumptions=rank == 0 or strength > 2,
                                 coverage=proportion(covered), rank_recovery=proportion(recovered),
                                 projected_selection=proportion(projected), mean_length=float(np.mean(widths)),
                                 length_mcse=float(np.std(widths, ddof=1) / np.sqrt(repetitions)),
                                 length_to_direct=float(np.mean(widths) / (2 * q)),
                                 mean_bias_certificate=float(np.mean(biases)),
                                 center_rmse=float(np.sqrt(np.mean(errors))), median_seconds=float(np.median(times))))
    return rows


def loading_experiment(rng, repetitions=1000):
    rows = []
    K = 4
    for kind in ['gaussian', 'rademacher']:
        for p in [256, 4096]:
            M = np.sqrt(p)
            for epsilon in [0, .03, .3]:
                a = np.sqrt(1 - epsilon ** 2)
                for signal in ['coordinate', 'diffuse', 'off_diagonal']:
                    diagonal = np.zeros(p)
                    if signal == 'coordinate':
                        diagonal[0] = M
                    elif signal == 'diffuse':
                        diagonal[:] = M / p ** (K / 2)
                    off_mean = M if signal == 'off_diagonal' else (M / p ** (K / 2) if signal == 'diffuse' else 0)
                    target = a * diagonal.sum() / np.sqrt(p) + epsilon * off_mean
                    covered, omitted, widths, errors, times = [], [], [], [], []
                    for _ in range(repetitions):
                        data = diagonal + noise(rng, (p,), kind)
                        off_data = off_mean + float(noise(rng, (), kind))
                        start = time.perf_counter()
                        center, radius, naive_center, naive_radius, selected = surrogate_interval(
                            data, off_data, M, epsilon, K=K, gaussian=kind == 'gaussian')
                        times.append(time.perf_counter() - start)
                        covered.append(abs(center - target) <= radius)
                        omitted.append(abs(naive_center - target) <= naive_radius)
                        widths.append(2 * radius)
                        errors.append((center - target) ** 2)
                    rows.append(dict(noise=kind, p=p, K=K, M=float(M), epsilon=epsilon, signal=signal,
                                     coverage=proportion(covered), uncorrected_coverage=proportion(omitted),
                                     length=float(widths[0]), center_rmse=float(np.sqrt(np.mean(errors))),
                                     selected=['surrogate_plus_residual', 'direct', 'structural'][selected],
                                     median_seconds=float(np.median(times))))
    return rows


def robust_experiment(rng, repetitions=400):
    nets, shape = small_full_nets()
    n = 128
    counts = {s: len(v) for s, v in nets.items()}
    parameters = mom_parameters(counts, n)
    rows = []
    for kind in ['gaussian', 'rademacher', 'student_t3', 'rare_outliers']:
        robust_pass, gaussian_pass, ratios, excesses, timings = [], [], [], [], []
        for _ in range(repetitions):
            # Treat n as independent replicate index, never as a tensor mode.
            replicates = noise(rng, (n,) + shape, kind)
            start = time.perf_counter()
            result = robust_scan_errors(replicates, nets, parameters)
            timings.append(time.perf_counter() - start)
            robust_pass.append(result['robust_pass'])
            gaussian_pass.append(result['gaussian_pass'])
            ratios.append(result['threshold_ratio'])
            excesses.append(result['excess'] ** 2)
        rows.append(dict(noise=kind, p=2, K=3, n=n, full_scan=True,
                         directions=counts, parameters=parameters,
                         finite_variance_assumptions=True, gaussian_proxy_one_valid=kind in ['gaussian', 'rademacher'],
                         robust_envelope=proportion(robust_pass), sample_mean_gaussian_envelope=proportion(gaussian_pass),
                         maximum_threshold_ratio=float(max(ratios)),
                         mean_excess_squared_over_tau_squared=float(n * np.mean(excesses)),
                         median_seconds=float(np.median(timings))))
    return rows


def main():
    rng = np.random.default_rng(SEED)
    results = ROOT / 'results'
    start = time.perf_counter()
    for name, run in [('adaptive_intervals', adaptive_experiment), ('general_loadings', loading_experiment), ('robust_full_scan', robust_experiment)]:
        rows = run(rng)
        (results / (name + '.json')).write_text(json.dumps(rows, indent=2) + '\n')
        print(name, 'completed:', len(rows), flush=True)
    sources = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__), ROOT / 'code/methods.py']}
    record = dict(seed=SEED, seconds=time.perf_counter() - start, sources=sources,
                  environment=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
                                   platform=platform.platform(), blas_threads=os.environ['OPENBLAS_NUM_THREADS']))
    (results / 'experiment_run.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
