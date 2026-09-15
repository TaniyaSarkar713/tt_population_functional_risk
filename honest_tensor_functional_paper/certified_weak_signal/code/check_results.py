"""Independent finite checks for global bounds and mathematical certificates."""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

from certified_optimizer import BinaryRankOneOptimizer, cos_bounds, rank_one
from loading_and_adaptation import (cap_safe_tangent_interval, pilot_envelopes,
                                    project, residual_certificate, unfold, weighted_axis_lower)

ROOT = Path(__file__).resolve().parents[1]


def main():
    started = time.time()
    rng = np.random.default_rng(2026091101)
    counts = {}
    with np.errstate(all='raise'):
        for _ in range(1000):
            lo = rng.uniform(-10, 10)
            hi = lo + rng.uniform(0, 10)
            left, right = cos_bounds(lo, hi)
            values = np.cos(np.linspace(lo, hi, 53))
            assert values.min() >= left - 1e-13 and values.max() <= right + 1e-13
        counts['cosine_ranges'] = 1000
        loading = rng.normal(size=(2, 2, 2))
        z = rng.normal(size=(2, 2, 2))
        optimizer = BinaryRankOneOptimizer(z, loading, 3, .4)
        for _ in range(150):
            ends = np.sort(rng.uniform(size=(2, 4)), axis=0)
            lower = np.r_[-3., 0., 0., 0.] + ends[0] * np.r_[6., np.pi, np.pi, np.pi]
            upper = np.r_[-3., 0., 0., 0.] + ends[1] * np.r_[6., np.pi, np.pi, np.pi]
            cell = optimizer.cell(lower, upper)
            for _ in range(12):
                parameters = rng.uniform(lower, upper)
                tensor = rank_one(parameters)
                target = np.sum(tensor * loading)
                objective = max(0., max(abs(np.sum(u.reshape(z.shape) * (z - tensor))) - t
                                       for u, t in zip(optimizer.directions, optimizer.thresholds)))
                assert cell.residual_lower <= objective + 1e-10
                assert cell.target_lower <= target <= cell.target_upper
        counts['box_containment_points'] = 1800

        flat = np.zeros((2, 2, 2)); flat[0, 0, 0] = flat[1, 1, 1] = 1 / np.sqrt(2)
        atom = np.zeros_like(flat); atom[0, 0, 0] = 1.
        optimizer = BinaryRankOneOptimizer(8 * atom, flat, 2, .3)
        fitted = optimizer.minimize_residual(.01, 500)
        exact = max(0., 8 - 2 - optimizer.thresholds[0])
        assert fitted['lower'] <= exact + 1e-10 <= fitted['upper'] + 1e-9
        assert fitted['certified_to_tolerance']
        optimizer = BinaryRankOneOptimizer(np.zeros_like(flat), flat, 2, 1.)
        full_projection = optimizer.project_interval(.1, 5000)
        assert full_projection['lo'] <= -np.sqrt(2) and full_projection['hi'] >= np.sqrt(2)
        assert full_projection['certified_to_tolerance']
        optimizer = BinaryRankOneOptimizer(np.zeros_like(flat), flat, 2, 1.)
        stopped = optimizer.project_interval(.0001, 1)
        assert not stopped['certified_to_tolerance']
        assert stopped['lo'] <= -np.sqrt(2) and stopped['hi'] >= np.sqrt(2)
        optimizer = BinaryRankOneOptimizer(20 * flat, flat, 30, .2)
        empty = optimizer.project_interval(.1, 1000)
        assert empty['empty_certified']
        incompatible = optimizer.minimize_residual(.1, 3000)
        assert incompatible['lower'] > 0 and incompatible['certified_to_tolerance']
        # A different finite angular/amplitude enumeration supplies upper witnesses.
        for _ in range(400):
            candidate = np.r_[rng.uniform(-30, 30), rng.uniform(0, np.pi, 3)]
            assert optimizer.objective(candidate) >= incompatible['lower'] - 1e-9
        counts['optimizer_contract_cases'] = 5

        for _ in range(120):
            weights = np.sort(rng.uniform(.05, 1., 8))[::-1]
            M, tau = rng.uniform(.05, 4), rng.uniform(.2, 2)
            result = weighted_axis_lower(weights, M, tau)
            d, delta = result['support'], result['delta']
            pi = np.array(result['probabilities'])
            means = np.diag(delta / weights[:d])
            gram = np.einsum('ik,jk->ij', means, means, optimize=False) / tau ** 2
            chi = np.sum(pi[:, None] * pi[None, :] * np.expm1(gram))
            assert abs(chi - result['chi_square']) < 1e-10
            assert chi <= .25 + 1e-9 and np.max(np.linalg.norm(means, axis=1)) <= M + 1e-10
            assert np.allclose(means @ weights[:d], delta)
        counts['weighted_mixture_identities'] = 120
        assert weighted_axis_lower([0, 0], 1)['length_lower'] == 0

        for _ in range(250):
            shape = (3, 4, 2)
            mean, noise, loading = [rng.normal(size=shape) for _ in range(3)]
            pilot = mean + noise
            eta = [np.linalg.svd(unfold(noise, k), compute_uv=False)[0] for k in range(3)]
            ranks = tuple(rng.integers(0, p + 1) for p in shape)
            projected, bias, _ = residual_certificate(pilot, loading, np.linalg.norm(mean), ranks, eta)
            actual = abs(np.sum((loading - projected) * mean))
            assert actual <= bias + 1e-9
        counts['unseparated_bias_certificates'] = 250

        for index in range(180):
            cap = 1 + index % 3
            actual_rank = index % (cap + 1)
            mean = np.zeros((3, 3, 3))
            for j in range(actual_rank):
                mean[j, j, j] = [.1, 10., 10000.][(index + j) % 3]
            loading, noise = rng.normal(size=mean.shape), rng.normal(size=mean.shape)
            pilot = mean + noise
            M = max(1., 1.1 * np.linalg.norm(mean))
            result = cap_safe_tangent_interval(pilot, mean, loading, M, (cap,) * 3)
            eta = pilot_envelopes(mean.shape, 1., .01)
            qs = []
            for k in range(3):
                assert np.linalg.svd(unfold(noise, k), compute_uv=False)[0] <= eta[k]
                u, _, _ = np.linalg.svd(unfold(pilot, k), full_matrices=True)
                q = np.eye(3) if cap == 3 else np.einsum('ij,kj->ik', u[:, :cap], u[:, :cap], optimize=False)
                qs.append(q)
                if actual_rank:
                    truth = np.eye(3)[:, :actual_rank]
                    error = np.linalg.svd(np.einsum('ij,jk->ik', np.eye(3) - q, truth, optimize=False), compute_uv=False)[0]
                    assert error <= result['angle_bounds'][k] + 1e-10
            tangent = -2 * project(loading, qs)
            for k in range(3):
                tangent += project(loading, [np.eye(3) if j == k else q for j, q in enumerate(qs)])
            bias = abs(np.sum((loading - tangent) * mean))
            assert bias <= result['bias'] + 1e-8
        counts['cap_safe_tangent_certificates'] = 180

    summary = dict(seed=2026091101, passed=True, checks=counts,
                   optimizer_examples=dict(analytic_fit=fitted, full_class_projection=full_projection,
                                           budget_stop=stopped, incompatible_fit=incompatible, empty_projection=empty),
                   seconds=time.time() - started,
                   source_hashes={name: hashlib.sha256((ROOT / 'code' / name).read_bytes()).hexdigest()
                                  for name in ['check_results.py', 'certified_optimizer.py', 'loading_and_adaptation.py']})
    (ROOT / 'results/checks.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(dict(passed=True, checks=counts, seconds=summary['seconds']), indent=2))


if __name__ == '__main__':
    main()
