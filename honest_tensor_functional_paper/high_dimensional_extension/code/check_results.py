"""Independent finite checks for the new matched regimes and algorithm."""
import hashlib
import itertools
import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.special import logsumexp
from scipy.stats import hypergeom

from methods import (dyadic_envelope, flat_loading, growing_cap_interval,
                     growing_lower, pointwise_amplitude_bound, pointwise_interval,
                     project_modes)

ROOT = Path(__file__).resolve().parents[1]


def profile_constant(beta, order):
    exponent = 1.5 if order == 3 else .5
    stop = max(1, int(np.ceil(2 * exponent / (beta * np.log(2)))))
    j = np.arange(1, stop + 1)
    total = 1 + np.sum(2. ** (-beta * (j - 1)) * (j + 1) ** exponent)
    next_term = 2. ** (-beta * stop) * (stop + 2) ** exponent
    ratio = 2. ** (-beta) * ((stop + 3) / (stop + 2)) ** exponent
    assert ratio < 1
    return float(total + next_term / (1 - ratio))


def main():
    started = time.time()
    rng = np.random.default_rng(2026091201)
    counts, ratios = {}, []
    for p in [1, 4, 16, 64, 256, 1024]:
        for r in sorted({min(p, int(np.ceil(np.sqrt(p)))), p, max(1, p // 4)}):
            for M in [.01, .5, 2., 100.]:
                result = growing_lower(p, r, M)
                b = result['target'] * np.sqrt(p) / r
                h = np.arange(max(0, 2 * r - p), r + 1)
                log_second = logsumexp(hypergeom.logpmf(h, p, r, r) + b * b * h)
                assert log_second <= .25 + 1e-8
                assert b * np.sqrt(r) <= M + 1e-10
                if r >= np.sqrt(p):
                    rate = min(M * np.sqrt(r / p), 1.)
                    assert result['target'] >= rate / (2 * np.sqrt(1.25)) - 1e-10
                    ratios.append(result['target'] / rate)
    counts['exact_hypergeometric_moments'] = 4 * sum(len({min(p, int(np.ceil(np.sqrt(p)))), p, max(1, p // 4)}) for p in [1, 4, 16, 64, 256, 1024])

    for p in [4, 16, 64]:
        for r in [1, int(np.sqrt(p)), p]:
            M = 3.
            a = np.zeros((p, p, p))
            for i in range(r):
                a[i, i, i] = M / np.sqrt(r)
            target = np.sum(a * flat_loading(p, 3))
            assert np.isclose(target, M * np.sqrt(r / p))
            result = growing_cap_interval(np.diagonal(a, axis1=0, axis2=1)[np.arange(p), np.arange(p)], M, r)
            assert result['lo'] <= target <= result['hi']
    counts['attained_structural_bounds'] = 9

    counts['dyadic_profiles_and_tail_bounds'] = 0
    for m in [1, 8, 128, 4096]:
        for beta in [.1, .25, .75, 2.]:
            for order in [3, 4]:
                weights = np.arange(1, m + 1) ** (-beta)
                result = dyadic_envelope(weights, 100., order=order)
                assert result['profile_H'] <= profile_constant(beta, order) + 1e-10
                assert sum(x['stop'] - x['start'] for x in result['blocks']) == m
                assert sum(x['error_budget'] for x in result['blocks']) <= .05
                counts['dyadic_profiles_and_tail_bounds'] += 1

    for trial in range(60):
        p, cap = 4, 1 + trial % 3
        actual = trial % (cap + 1)
        a = np.zeros((p,) * 3)
        for i in range(actual):
            a[i, i, i] = [.1, 10., 100000.][(trial + i) % 3]
        M = max(2., 1.1 * np.linalg.norm(a))
        z = a + rng.normal(size=a.shape)
        result = pointwise_interval(z, M, cap, rng, return_loading=True)
        bias = abs(np.sum((flat_loading(p, 3) - result['tangent_loading']) * a))
        assert bias <= result['bias'] + 1e-7
        assert result['max_right_svd_entries'] <= z.size
        assert result['pilot_failure_budget'] == .05 * cap / (8 * p)
        assert result['width'] <= 2 * 2.241402727604945 + 1e-9
    counts['pointwise_bias_and_allocation_cases'] = 60

    # Independently compare basis contraction with explicit projector matrices.
    for _ in range(50):
        tensor = rng.normal(size=(3, 4, 5))
        bases = [np.linalg.qr(rng.normal(size=(p, 2)))[0] for p in tensor.shape]
        expected = tensor.copy()
        for k, u in enumerate(bases):
            q = np.einsum('ir,jr->ij', u, u, optimize=False)
            moved = np.moveaxis(expected, k, 0)
            expected = np.moveaxis(np.einsum('ij,j...->i...', q, moved, optimize=False), 0, k)
        assert np.allclose(project_modes(tensor, bases), expected, atol=1e-11)
    counts['economy_projection_equivalences'] = 50

    for p, s, order in [(5, 2, 3), (6, 2, 4), (7, 3, 3)]:
        beta, strength = 1 / (2 * order), .005
        weights = np.arange(1, p + 1, dtype=float) ** (-beta)
        tensors = []
        for support in itertools.combinations(range(p), s):
            x = np.zeros(p); x[list(support)] = 1 / np.sqrt(s)
            tensor = strength * weights[-1] / weights * x
            for _ in range(order - 1):
                tensor = np.multiply.outer(tensor, x)
            target = sum(weights[i] * tensor[(i,) * order] for i in range(p))
            assert np.isclose(target, strength * weights[-1] * s ** (1 - order / 2))
            assert np.linalg.norm(tensor) <= strength + 1e-12
            tensors.append(tensor.ravel())
        tensors = np.asarray(tensors)
        gram = np.einsum('id,jd->ij', tensors, tensors, optimize=False)
        for degree in [1, 2, 3]:
            partial = sum(float(np.mean(gram ** d)) / math.factorial(d) for d in range(1, degree + 1))
            mu = s * s / p
            B = strength ** 2 * (order * degree) ** order / s ** order
            assert B < 1 and partial <= mu * np.exp(mu) * B / (1 - B)
    counts['weighted_low_degree_moments'] = 9

    # Exact aligned strong means validate the target geometry behind P1.
    strong = []
    for p, cap in [(8, 1), (8, 3), (16, 1), (16, 4)]:
        amplitude = 8 * pointwise_amplitude_bound(p, cap)
        a = np.zeros((p,) * 3)
        support = rng.choice(p, size=cap, replace=False)
        for i in support:
            a[i, i, i] = amplitude * rng.choice([-1., 1.]) * rng.uniform(1., 1.5)
        result = pointwise_interval(a, 1.1 * np.linalg.norm(a), cap, rng)
        assert result['selected'] == 'tangent'
        assert abs(result['tangent_norm'] - np.sqrt(cap / p)) < 1e-5
        strong.append(dict(p=p, cap=cap, width=result['width'], rate=np.sqrt(cap / p)))
    counts['strong_pointwise_geometry'] = 4
    summary = dict(passed=True, seed=2026091201, checks=counts,
                   growing_target_ratio_range=[float(min(ratios)), float(max(ratios))],
                   strong_examples=strong, seconds=time.time() - started,
                   source_hashes={name: hashlib.sha256((ROOT / 'code' / name).read_bytes()).hexdigest()
                                  for name in ['methods.py', 'check_results.py']})
    (ROOT / 'results/checks.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
