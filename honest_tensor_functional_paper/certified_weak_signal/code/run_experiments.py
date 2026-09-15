"""Small global-optimizer benchmarks and original-experiment coverage checks."""
import hashlib
import importlib.util
import json
import platform
import time
from collections import Counter
from pathlib import Path

import numpy as np
import scipy
from scipy.stats import norm

from certified_optimizer import BinaryRankOneOptimizer, rank_one
from loading_and_adaptation import single_observation_interval, weighted_axis_lower

ROOT = Path(__file__).resolve().parents[1]


def wilson(successes, n):
    q = norm.isf(.025)
    center = (successes / n + q * q / (2 * n)) / (1 + q * q / n)
    radius = q / (1 + q * q / n) * np.sqrt(successes / n * (1 - successes / n) / n + q * q / (4 * n * n))
    return [float(center - radius), float(center + radius)]


def save(name, value):
    (ROOT / 'results' / name).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def optimizer_experiments(rng):
    flat = np.zeros((2, 2, 2)); flat[0, 0, 0] = flat[1, 1, 1] = 1 / np.sqrt(2)
    loading = rng.normal(size=flat.shape); loading /= np.linalg.norm(loading)
    cases = [('zero', np.zeros_like(flat), 2., 1.),
             ('weak_dense', rank_one([.8, .4, .9, 1.2]), 2., 1.),
             ('boundary_atom', rank_one([2., 0., 0., 0.]), 2., 1.),
             ('strong_dense', rank_one([15., .4, .9, 1.2]), 20., .3)]
    rows = []
    for name, mean, M, tau in cases:
        for label, L in [('flat', flat), ('arbitrary', loading)]:
            started = time.time()
            covered, certified, widths, gaps, nodes = 0, 0, [], [], []
            records = []
            target = float(np.sum(mean * L))
            for _ in range(40):
                z = mean + tau * rng.normal(size=mean.shape)
                optimizer = BinaryRankOneOptimizer(z, L, M, tau)
                result = optimizer.project_interval(tolerance=.2 * tau, max_nodes=600)
                success = result['lo'] <= target <= result['hi']
                covered += success
                certified += result['certified_to_tolerance']
                widths.append(result['hi'] - result['lo'])
                if result.get('endpoint_gap') is not None:
                    gaps.append(result['endpoint_gap'])
                nodes.append(result['nodes'])
                records.append(dict(covered=bool(success), **result))
            rows.append(dict(case=name, loading=label, M=M, tau=tau, target=target, repetitions=40,
                             covered=int(covered), coverage_wilson_95=wilson(covered, 40),
                             certified_to_tolerance=int(certified), mean_width=float(np.mean(widths)),
                             mean_endpoint_gap=float(np.mean(gaps)) if gaps else None,
                             mean_nodes=float(np.mean(nodes)), seconds=time.time() - started, trials=records))
            print('optimizer', name, label, 'covered', covered, '/ 40; certified', certified, flush=True)
    return rows


def adaptation_experiments(rng):
    old_path = ROOT.parent / 'robust_adaptive_extension/code/methods.py'
    spec = importlib.util.spec_from_file_location('preserved_methods', old_path)
    old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
    p, shape = 4, (4, 4, 4)
    flat = np.zeros(shape)
    for i in range(p):
        flat[(i,) * 3] = 1 / np.sqrt(p)
    rows = []
    for amplitude, extra, cap in [(0., 0., 1), (.5, 0., 1), (2., 0., 1),
                                  (2000., 0., 1), (2000., .5, 2), (2000., 0., 2),
                                  (200000., 0., 1), (200000., 0., 2)]:
        mean = np.zeros(shape); mean[0, 0, 0] = amplitude; mean[1, 1, 1] = extra
        M = max(2., 1.05 * np.linalg.norm(mean))
        target = float(np.sum(mean * flat))
        covered, old_covered, width, old_width, selections, zero_width = 0, 0, [], [], Counter(), 0
        started = time.time()
        for _ in range(1000):
            z = mean + rng.normal(size=shape)
            result = single_observation_interval(z, flat, M, (cap,) * 3, rng)
            covered += result['lo'] <= target <= result['hi']
            zero_width += result['width'] == 0.
            width.append(result['width']); selections[result['selected']] += 1
            # The previous method is deliberately applied outside its gap class
            # for the weak cases, using a separate correctly scaled split.
            auxiliary = rng.normal(size=shape)
            comparator = old.adaptive_interval(z + auxiliary, z - auxiliary, flat, M,
                                              v1=np.sqrt(2), v2=np.sqrt(2))
            old_covered += comparator['lo'] <= target <= comparator['hi']
            old_width.append(comparator['width'])
        rows.append(dict(amplitude=amplitude, weak_extra=extra, supplied_mode_cap=cap, M=float(M),
                         repetitions=1000, covered=int(covered), coverage_wilson_95=wilson(covered, 1000),
                         mean_width=float(np.mean(width)), zero_width_count=int(zero_width),
                         pilot_choices=dict(selections), old_covered=int(old_covered),
                         old_coverage_wilson_95=wilson(old_covered, 1000), old_mean_width=float(np.mean(old_width)),
                         comparator_scope='Previous method requires separation; weak cases deliberately violate it.',
                         seconds=time.time() - started))
        print('adaptation', amplitude, extra, cap, 'covered', covered, '/ 1000;', dict(selections), flush=True)
    return rows


def loading_experiments():
    rows = []
    for m in [4, 16, 64]:
        for profile in ['flat', 'power', 'spike']:
            w = {'flat': np.ones(m), 'power': np.arange(1, m + 1) ** (-.75),
                 'spike': np.r_[1., np.full(m - 1, .03)]}[profile]
            w /= np.linalg.norm(w)
            for M in [.2, np.sqrt(m), 10 * np.sqrt(m)]:
                rows.append(dict(m=m, profile=profile, M=float(M),
                                 small_budget_rate=float(M * np.max(w)) if M <= 1 else None,
                                 **weighted_axis_lower(w, M)))
    return rows


def main():
    started, seed = time.time(), 2026091102
    source_hashes = {name: hashlib.sha256((ROOT / 'code' / name).read_bytes()).hexdigest()
                     for name in ['run_experiments.py', 'certified_optimizer.py', 'loading_and_adaptation.py']}
    rng = np.random.default_rng(seed)
    optimizer = optimizer_experiments(rng)
    save('optimizer_experiments.json', dict(seed=seed, cases=optimizer))
    adaptation = adaptation_experiments(rng)
    save('adaptation_experiments.json', dict(seed=seed, cases=adaptation))
    save('loading_bounds.json', dict(cases=loading_experiments()))
    save('run_manifest.json', dict(seed=seed, seconds=time.time() - started,
                                  python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
                                  source_hashes=source_hashes))
    print('All experiments completed.', flush=True)


if __name__ == '__main__':
    main()
