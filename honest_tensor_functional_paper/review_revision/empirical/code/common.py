"""Reproducible case-local seeds, paired records, and Monte Carlo uncertainty."""
import hashlib
import importlib.util
import json
import time
from pathlib import Path

import numpy as np
from scipy.stats import norm
from numerics import coverage_events

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[1]
LEVELS = np.array([.10, .05, .01])
SEED = 2026091203


def module(name, relative):
    import sys
    spec = importlib.util.spec_from_file_location(name, PROJECT / relative)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value


high = module('emp_high', 'high_dimensional_extension/code/methods.py')
old = module('emp_old', 'robust_adaptive_extension/code/methods.py')
diag = module('emp_diag', 'simulations/code/intervals.py')
global_fit = module('emp_global', 'certified_weak_signal/code/certified_optimizer.py')


def rng_for(case, trial=0, stream=0):
    digest = hashlib.sha256(str(case).encode()).digest()
    ident = int.from_bytes(digest[:4], 'little')
    return np.random.default_rng(np.random.SeedSequence([SEED, ident, trial, stream]))


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + '\n')


def mean_se(x):
    x = np.asarray(x, float)
    return float(np.mean(x)), float(np.std(x, ddof=1) / np.sqrt(len(x))) if len(x) > 1 else 0.


def wilson(k, n):
    z = norm.isf(.025)
    center = (k / n + z*z/(2*n)) / (1+z*z/n)
    rad = z / (1+z*z/n) * np.sqrt(k/n*(1-k/n)/n+z*z/(4*n*n))
    return [float(center-rad), float(center+rad)]


def save_intervals(case, names, endpoints, estimates, target, seconds=None,
                   scope=None, extra=None):
    """Arrays: endpoints B x methods x levels x 2; estimates B x methods."""
    endpoints, estimates = np.asarray(endpoints), np.asarray(estimates)
    B, methods = estimates.shape
    assert endpoints.shape == (B, methods, len(LEVELS), 2)
    assert np.isfinite(endpoints).all() and np.isfinite(estimates).all()
    assert np.all(endpoints[..., 0] <= endpoints[..., 1])
    seconds = np.zeros((B, methods)) if seconds is None else np.asarray(seconds)
    widths = endpoints[..., 1] - endpoints[..., 0]
    covered = coverage_events(endpoints, target)
    rejected = (endpoints[..., 0] > 0) | (endpoints[..., 1] < 0)
    errors = estimates - target
    rows = []
    for j, name in enumerate(names):
        mse, mse_se = mean_se(errors[:, j] ** 2)
        bias, bias_se = mean_se(errors[:, j])
        sec, sec_se = mean_se(seconds[:, j])
        for a, alpha in enumerate(LEVELS):
            hits = int(covered[:, j, a].sum())
            length, length_se = mean_se(widths[:, j, a])
            paired_width, paired_width_se = mean_se(widths[:, j, a] - widths[:, 0, a])
            paired_cov, paired_cov_se = mean_se(covered[:, j, a].astype(float) - covered[:, 0, a])
            paired_loss, paired_loss_se = mean_se(errors[:, j]**2 - errors[:, 0]**2)
            rows.append(dict(case=case['id'], suite=case['suite'], method=name, alpha=float(alpha),
                             repetitions=B, target=float(target), covered=hits, coverage=hits/B,
                             coverage_mcse=float(np.sqrt(hits/B*(1-hits/B)/B)),
                             coverage_wilson_95=wilson(hits, B), length=length, length_se=length_se,
                             mse=mse, mse_se=mse_se, bias=bias, bias_se=bias_se,
                             reject_count=int(rejected[:, j, a].sum()), rejection=float(rejected[:, j, a].mean()),
                             rejection_wilson_95=wilson(int(rejected[:, j, a].sum()), B),
                             seconds=sec, seconds_se=sec_se,
                             paired_reference=names[0], paired_length=paired_width,
                             paired_length_se=paired_width_se, paired_coverage=paired_cov,
                             paired_coverage_se=paired_cov_se, paired_mse=paired_loss,
                             paired_mse_se=paired_loss_se,
                             guarantee=(scope or {}).get(name, 'finite_sample'),
                             estimator_id=('interval_companion' if name=='pointwise' else 'threshold_95' if name in ['threshold_selected','threshold_raw'] else name+'_scalar'),
                             estimator_alpha=.05 if name in ['pointwise','threshold_selected','threshold_raw'] else None,
                             coverage_policy='four_endpoint_ulps',status='NEEDS CHECK'))
    metadata = dict(case=case, methods=names, alpha=LEVELS.tolist(), target=float(target),
                    extra=extra or {}, records=rows)
    raw = ROOT / 'results' / (case['id'] + '.npz')
    np.savez_compressed(raw, endpoints=endpoints, estimates=estimates, seconds=seconds,
                        target=target, alpha=LEVELS, methods=np.array(names))
    write_json(raw.with_suffix('.json'), metadata)
    return rows


def symmetric(center, radius):
    center, radius = np.broadcast_arrays(center, radius)
    return np.stack((center-radius, center+radius), axis=-1)


def load_cases(suite=None):
    cases = json.loads((ROOT/'configs/cases.json').read_text())['cases']
    return [c for c in cases if suite is None or c['suite'] == suite]


def hashes():
    paths = list((ROOT/'code').glob('*.py')) + list((ROOT/'configs').glob('*.json'))
    paths += [ROOT/'simulation_design.md', ROOT/'theorem_experiment_map.md', ROOT/'experiment_registry.md']
    paths += [Path(m.__file__) for m in [high, old, diag, global_fit]]
    return {str(p.relative_to(PROJECT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
