"""Independent finite corroborations of new bounds and approximation coverage."""
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.stats import norm

from methods import inner, mode_apply, project_modes, tangent_loading
from run_experiments import proportion

ROOT = Path(__file__).resolve().parents[1]


def main():
    rng = np.random.default_rng(2026091108)
    projector_errors, bias_ratios = [], []
    for K in [3, 4]:
        for rank in [1, 2]:
            for _ in range(50):
                p = 4
                true_spaces, pilot_spaces, errors = [], [], []
                for k in range(K):
                    u, _ = np.linalg.qr(rng.normal(size=(p, rank)))
                    v, _ = np.linalg.qr(u + .2 * rng.normal(size=(p, rank)))
                    q = np.einsum('ij,kj->ik', v, v, optimize=False)
                    true_spaces.append(u)
                    pilot_spaces.append(q)
                    errors.append(np.linalg.norm((np.eye(p) - q) @ u, ord=2))
                mean = rng.normal(size=(rank,) * K)
                for k, u in enumerate(true_spaces):
                    mean = mode_apply(mean, u, k)
                loading = rng.normal(size=(p,) * K)
                loading /= np.linalg.norm(loading)
                tangent = tangent_loading(loading, pilot_spaces)
                repeat = tangent_loading(tangent, pilot_spaces)
                projector_errors.append(np.linalg.norm(repeat - tangent))
                witness = rng.normal(size=loading.shape)
                assert abs(inner(loading, tangent_loading(witness, pilot_spaces)) - inner(tangent, witness)) < 1e-10
                pair_error = np.sqrt(sum((errors[k] * errors[l]) ** 2 for k in range(K) for l in range(k + 1, K)))
                residual = mean - tangent_loading(mean, pilot_spaces)
                assert np.linalg.norm(residual) <= np.linalg.norm(mean) * min(1, pair_error) + 1e-10
                certificate = np.linalg.norm(mean) * np.linalg.norm(loading - tangent) * min(1, pair_error)
                actual = abs(inner(loading - tangent, mean))
                assert actual <= certificate + 1e-10
                bias_ratios.append(actual / max(certificate, 1e-30))
    assert max(projector_errors) < 1e-10

    tail_checks = 0
    for p in [1, 2, 4, 8, 64, 512]:
        for K in [3, 4, 6]:
            for beta in [.01, .05, .125]:
                h = np.array([s * np.log(np.e * p / s) + K * s * np.log(1 + 4 * K) for s in range(1, p + 1)])
                b = np.ceil(np.maximum(9, (h + np.log(p / beta)) / np.log(2))).astype(int)
                b += (b % 2 == 0)
                assert np.all(b >= 9) and np.all(b % 2 == 1)
                assert np.sum(np.exp(h - b * np.log(2))) <= beta * (1 + 1e-10)
                for t in [0, .1, 1, 10, 100]:
                    lhs = (1 + t / (4 * np.sqrt(2 * b))) ** (-b)
                    rhs = (1 + t / (12 * np.sqrt(2))) ** (-9)
                    assert np.all(lhs <= rhs * (1 + 1e-10))
                    tail_checks += len(b)
    moment = quad(lambda t: 2 * t * (1 + t / (12 * np.sqrt(2))) ** -9, 0, np.inf)[0]
    assert abs(moment - 72 / 7) < 1e-8

    mixture_pairs, largest_second = 0, 0.0
    for p in range(2, 10):
        for s in range(1, min(p, 4) + 1):
            for M in [.1, 1, 10]:
                supports = list(itertools.combinations(range(p), s))
                b = min(M / np.sqrt(s), np.sqrt(np.log1p(p / (4 * s * s))))
                second = 0.0
                for S in supports:
                    for T in supports:
                        second += np.exp(b * b * len(set(S) & set(T)))
                        mixture_pairs += 1
                second /= len(supports) ** 2
                assert second <= np.exp(.25) * (1 + 1e-10)
                largest_second = max(largest_second, second)

    shifted_checks = 0
    p, q, K = 6, 2, 3
    base = np.zeros((p,) * K)
    base[0, 0, 0], base[1, 1, 1] = 2, 1
    for _ in range(100):
        factor = rng.uniform(size=p - q)
        block = np.einsum('i,j,k->ijk', factor, factor, factor, optimize=False)
        block *= .7 / np.linalg.norm(block)
        alternative = base.copy()
        alternative[q:, q:, q:] = block
        assert abs(np.linalg.norm(alternative) ** 2 - np.linalg.norm(base) ** 2 - .7 ** 2) < 1e-12
        for mode in range(K):
            assert np.linalg.matrix_rank(np.moveaxis(alternative, mode, 0).reshape(p, -1)) <= 3
        increment = sum(alternative[(i,) * K] - base[(i,) * K] for i in range(p)) / np.sqrt(p)
        normalized_block = sum(block[(i,) * K] for i in range(p - q)) / np.sqrt(p - q)
        assert abs(increment - np.sqrt((p - q) / p) * normalized_block) < 1e-12
        shifted_checks += 1

    approximation = []
    p, K, M, repetitions = 4096, 4, 64.0, 1000
    lam = np.sqrt(2 * np.log(2 * p / .05))
    nl_radius = M ** (2 / K) * (2 * lam) ** (1 - 2 / K) / np.sqrt(p)
    for eta in [0, .1, .5, 2]:
        for signal in ['zero', 'coordinate', 'diffuse']:
            base = np.zeros(p)
            if signal == 'coordinate': base[0] = M
            if signal == 'diffuse': base[:] = M / p ** (K / 2)
            # Perturbation eta * L_flat has Frobenius norm eta and rank p.
            diagonal = base + eta / np.sqrt(p)
            target = diagonal.sum() / np.sqrt(p)
            radii = [nl_radius + eta, M / np.sqrt(p) + eta, norm.ppf(.975)]
            selected = int(np.argmin(radii))
            covered, uninflated = [], []
            for _ in range(repetitions):
                data = diagonal + rng.normal(size=p)
                thresholded = np.sum(np.sign(data) * np.maximum(np.abs(data) - lam, 0)) / np.sqrt(p)
                center = [thresholded, 0.0, data.sum() / np.sqrt(p)][selected]
                covered.append(abs(center - target) <= radii[selected])
                uninflated.append(abs(thresholded - target) <= nl_radius)
            approximation.append(dict(p=p, K=K, M=M, eta=eta, signal=signal,
                                      coverage=proportion(covered), uninflated_coverage=proportion(uninflated),
                                      length=2 * radii[selected], selected=['inflated_threshold', 'structural', 'direct'][selected]))
    (ROOT / 'results/approximate_ranks.json').write_text(json.dumps(approximation, indent=2) + '\n')
    result = dict(status='PASS', scope='Finite mathematical corroboration, not a formal proof or minimax-optimizer experiment',
                  seed=2026091108, projector_and_bias_cases=len(bias_ratios),
                  maximum_projector_error=float(max(projector_errors)), maximum_bias_ratio=float(max(bias_ratios)),
                  mom_tail_comparisons=tail_checks, mom_normalized_second_moment=moment,
                  growing_rank_support_pairs=mixture_pairs, largest_mixture_second_moment=largest_second,
                  shifted_block_checks=shifted_checks, approximation_configurations=len(approximation),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (ROOT / 'results/theory_checks.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
