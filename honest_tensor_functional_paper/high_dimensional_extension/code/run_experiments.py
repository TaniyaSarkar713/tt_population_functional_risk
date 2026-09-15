"""New high-dimensional interval experiments; no old simulation suite is rerun."""
import hashlib
import json
import platform
import time
from collections import Counter
from pathlib import Path

import numpy as np
import scipy
from scipy.stats import norm

from methods import (dyadic_envelope, fixed_cap_rate, growing_cap_interval,
                     growing_lower, pointwise_amplitude_bound, pointwise_interval)

ROOT = Path(__file__).resolve().parents[1]


def wilson(covered, n):
    q = norm.isf(.025)
    center = (covered / n + q * q / (2 * n)) / (1 + q * q / n)
    radius = q / (1 + q * q / n) * np.sqrt(covered / n * (1 - covered / n) / n + q * q / (4 * n * n))
    return [float(center - radius), float(center + radius)]


def save(name, data):
    (ROOT / 'results' / name).write_text(json.dumps(data, indent=2, allow_nan=False) + '\n')


def growing_experiments(rng):
    rows = []
    for p in [64, 1024, 16384]:
        for r in [int(np.ceil(np.sqrt(p))), min(p, 4 * int(np.ceil(np.sqrt(p))))]:
            for structural_scale in [.25, 2., 8.]:
                M = structural_scale * np.sqrt(p / r)
                for signal in ['zero', 'boundary']:
                    mean = np.zeros(p)
                    if signal == 'boundary':
                        mean[:r] = M / np.sqrt(r)
                    target = float(np.sum(mean) / np.sqrt(p))
                    n, covered, lengths, losses = 200, 0, [], []
                    started = time.time()
                    for _ in range(n):
                        result = growing_cap_interval(mean + rng.normal(size=p), M, r)
                        covered += result['lo'] <= target <= result['hi']
                        lengths.append(result['width']); losses.append((result['estimate'] - target) ** 2)
                    lower = growing_lower(p, r, M)
                    rows.append(dict(p=p, cap=r, M=float(M), signal=signal, target=target, repetitions=n,
                                     covered=int(covered), coverage_wilson_95=wilson(covered, n),
                                     mean_length=float(np.mean(lengths)), empirical_mse=float(np.mean(losses)),
                                     theoretical_mse_upper=result['mse_upper'], length_lower=lower['length_lower'],
                                     minimax_rate=result['rate'], seconds=time.time() - started,
                                     simulated_coordinates='Only the diagonal used by this exact O(p)-access procedure.'))
        print('Growing-cap experiments completed at p =', p, flush=True)
    return rows


def pointwise_experiments(rng):
    rows = []
    cases = []
    for p, n in [(8, 200), (16, 120), (32, 60), (64, 20)]:
        for r in [1, int(np.ceil(np.sqrt(p)))]:
            cases.append((p, r, 'strong_saturated', 8., n))
    cases.extend([(8, 1, 'weak', 0., 500), (8, 3, 'strong_lower_rank', 8., 200),
                  (8, 3, 'strong_plus_weak', 8., 200), (16, 1, 'dense_rank_one', 0., 200)])
    for p, cap, case, multiplier, n in cases:
        amplitude = multiplier * pointwise_amplitude_bound(p, cap)
        mean = np.zeros((p,) * 3)
        if case == 'strong_saturated':
            for i in range(cap):
                mean[i, i, i] = amplitude
        elif case in ['strong_lower_rank', 'strong_plus_weak']:
            mean[0, 0, 0] = amplitude
            if case == 'strong_plus_weak':
                mean[1, 1, 1] = .5
        elif case == 'weak':
            mean[0, 0, 0] = .5
        else:
            vector = np.arange(1, p + 1, dtype=float) ** (-.3)
            vector /= np.linalg.norm(vector)
            mean = np.sqrt(p) * np.einsum('i,j,k->ijk', vector, vector, vector, optimize=False)
        M = max(np.sqrt(p), 1.1 * np.linalg.norm(mean))
        ids = np.arange(p)
        target = float(np.sum(mean[ids, ids, ids]) / np.sqrt(p))
        covered, widths, selections, runtimes, biases, ratios = 0, [], Counter(), [], [], []
        for _ in range(n):
            z = mean + rng.normal(size=mean.shape)
            started = time.time()
            result = pointwise_interval(z, M, cap, rng)
            runtimes.append(time.time() - started)
            covered += result['lo'] <= target <= result['hi']
            widths.append(result['width']); selections[result['selected']] += 1
            biases.append(result['bias']); ratios.append(result['tangent_norm'])
        rows.append(dict(p=p, cap=cap, case=case, amplitude=amplitude, M=float(M), repetitions=n,
                         covered=int(covered), coverage_wilson_95=wilson(covered, n),
                         mean_length=float(np.mean(widths)), length_standard_error=float(np.std(widths, ddof=1) / np.sqrt(n)),
                         pointwise_rate=float(np.sqrt(cap / p)) if case == 'strong_saturated' else None,
                         mean_bias=float(np.mean(biases)), mean_tangent_norm=float(np.mean(ratios)),
                         choices=dict(selections), mean_seconds=float(np.mean(runtimes)),
                         input_entries=result['input_entries'], max_right_svd_entries=result['max_right_svd_entries'],
                         previous_full_right_entries=result['full_right_svd_entries'],
                         pilot_failure_budget=result['pilot_failure_budget']))
        print('Pointwise', p, cap, case, 'coverage', covered, '/', n, dict(selections), flush=True)
    return rows


def loading_calculations():
    rows = []
    for m in [64, 1024, 16384]:
        for beta in [.1, .25, .5, 1.]:
            w = np.arange(1, m + 1, dtype=float) ** (-beta)
            w /= np.linalg.norm(w)
            for order in [3, 4]:
                for M in [.1, 1., np.sqrt(m), 1e6]:
                    result = dyadic_envelope(w, M, order=order)
                    rows.append(dict(m=m, beta=beta, order=order, M=float(M), largest_weight=float(w[0]),
                                     sharp_rate=float(w[0] * min(M, 1.)),
                                     envelope_ratio=float(result['upper_diameter'] / (w[0] * min(M, 1.))),
                                     profile_ratio=float(result['profile_H'] / w[0]),
                                     upper_diameter=result['upper_diameter'],
                                     block_count=len(result['blocks'])))
    adaptation = []
    for p in [64, 1024, 16384, 1048576]:
        for order in [3, 4]:
            lower = growing_lower(p, int(np.ceil(np.sqrt(p))), np.sqrt(p))
            rate = fixed_cap_rate(p, np.sqrt(p), order=order)
            adaptation.append(dict(p=p, order=order, outer_length_lower=lower['length_lower'],
                                   fixed_cap_oracle_rate=rate, lower_to_oracle_rate_ratio=lower['length_lower'] / rate))
    return dict(loading_cases=rows, adaptation_obstructions=adaptation)


def main():
    seed, started = 2026091202, time.time()
    hashes = {name: hashlib.sha256((ROOT / 'code' / name).read_bytes()).hexdigest()
              for name in ['run_experiments.py', 'methods.py']}
    rng = np.random.default_rng(seed)
    save('growing_caps.json', dict(seed=seed, cases=growing_experiments(rng)))
    save('pointwise.json', dict(seed=seed, cases=pointwise_experiments(rng)))
    save('loading_rates.json', loading_calculations())
    save('run_manifest.json', dict(seed=seed, source_hashes=hashes, python=platform.python_version(),
                                  numpy=np.__version__, scipy=scipy.__version__, seconds=time.time() - started))
    print('Experiment run complete.', flush=True)


if __name__ == '__main__':
    main()
