"""Finite attempts to falsify the new inequalities; not formal proof verification."""
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.special import digamma, gammaln, logsumexp
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
SEED = 20260911


def rate(K, p, M, tau):
    ell = math.log(math.e * p)
    x = M / (tau * math.sqrt(ell))
    multiplier = min(x, 1 + max(0, math.log(x)), ell) if K == 3 else min(x, 1)
    return tau * math.sqrt(ell / p) * multiplier


def harmonic(m):
    return float(digamma(m + 1) + np.euler_gamma)


def hard_target(K, p, M, tau):
    coordinate = min(M, tau * math.sqrt(math.log1p(p / 4))) / math.sqrt(p)
    if K != 3:
        return coordinate, 1
    x = M / (tau * math.sqrt(math.log(math.e * p)))
    m = max(1, int(min(p ** 0.25, x * x))) if x > 1 else 1
    b = min(M / math.sqrt(27 * m), tau * math.sqrt(math.log1p(p / (4 * m * m))) / math.sqrt(27))
    cubic = b * harmonic(m) / math.sqrt(p)
    return max(coordinate, cubic), m


def mode_product(A, U, k):
    return np.moveaxis(np.tensordot(U, A, axes=(1, k)), 0, k)


def tensor_product(factors):
    result = factors[0]
    for factor in factors[1:]:
        result = np.multiply.outer(result, factor)
    return result


def random_tensor(rng, K, p, rank, kind):
    if kind == 'tucker':
        A = rng.normal(size=(rank,) * K)
        for k in range(K):
            Q = np.linalg.qr(rng.normal(size=(p, rank)))[0]
            A = mode_product(A, Q, k)
    else:
        cores = [rng.normal(size=(1 if k == 0 else rank, p, 1 if k == K - 1 else rank)) for k in range(K)]
        A = cores[0][0]
        for core in cores[1:]:
            A = np.tensordot(A, core, axes=(-1, 0))
        A = A[..., 0]
    return A / np.linalg.norm(A)


def main():
    rng = np.random.default_rng(SEED)
    grid = []
    sum_ratios = []
    for K in (3, 4, 6):
        for p in (1, 2, 3, 16, 255, 256, 1024, 4096, 65536):
            s = np.arange(1, p + 1, dtype=float)
            ell = math.log(math.e * p)
            for x in np.logspace(-6, 6, 121):
                M = float(x * math.sqrt(ell))
                target_rate = rate(K, p, M, 1)
                terms = np.minimum(x * s ** (-K / 2), s ** (-(K - 1) / 2))
                multiplier = min(x, 1 + max(0, math.log(x)), ell) if K == 3 else min(x, 1)
                sum_ratio = float(terms.sum() / multiplier)
                assert sum_ratio <= (4 if K == 3 else 3) + 1e-11
                delta, m = hard_target(K, p, M, 1)
                lower_ratio = delta / target_rate
                assert lower_ratio >= (1 / (5 * math.sqrt(135)) if K == 3 else 1 / math.sqrt(5)) - 1e-12
                assert math.isclose(rate(K, p, 7 * M, 7), 7 * target_rate, rel_tol=1e-12)
                sum_ratios.append(sum_ratio)
                grid.append(dict(K=K, p=p, M=M, tau=1, x=float(x), rate=target_rate,
                                 lower_target=delta, lower_ratio=lower_ratio, support=m,
                                 sum_ratio=sum_ratio))

    # Exact dense tensors and unfolding ranks, independently of the rate formulas.
    geometry_count = 0
    geometry_max_ratio = 0.0
    for K in (3, 4):
        for p in (3, 4, 5):
            for kind in ('tucker', 'tt'):
                for _ in range(20):
                    M = float(np.exp(rng.uniform(-4, 4)))
                    A = M * random_tensor(rng, K, p, 2, kind)
                    B = M * random_tensor(rng, K, p, 2, kind)
                    delta = A - B
                    ordered = np.sort(np.abs(np.array([delta[(i,) * K] for i in range(p)])))[::-1]
                    J2 = 4 ** (K - 1)
                    envelope = 2 * J2 ** ((K - 1) / 2) * M * np.arange(1, p + 1) ** (-K / 2)
                    geometry_max_ratio = max(geometry_max_ratio, float(np.max(ordered / envelope)))
                    assert np.all(ordered <= envelope * (1 + 1e-11))
                    if kind == 'tucker':
                        unfoldings = [np.moveaxis(delta, k, 0).reshape(p, -1) for k in range(K)]
                    else:
                        unfoldings = [delta.reshape(p ** k, -1) for k in range(1, K)]
                    assert all(np.linalg.matrix_rank(U, tol=1e-8 * M) <= 4 for U in unfoldings)
                    geometry_count += 1

    # Signed nonuniform loading: exact full tensors, common targets, and likelihoods.
    mixtures = []
    for p in (2, 4, 6, 8):
        for d in range(1, p + 1):
            weights = np.arange(1, p + 1, dtype=float) ** -0.7
            weights *= np.where(np.arange(p) % 2, -1, 1)
            weights /= np.linalg.norm(weights)
            for m in range(1, min(d, 3) + 1):
                supports = list(itertools.combinations(range(d), m))
                X = np.zeros((len(supports), p))
                for i, support in enumerate(supports):
                    X[i, list(support)] = np.arange(1, m + 1) ** (-1 / 3)
                for M in (0.03, 1.0, 30.0):
                    b = min(M / math.sqrt(27 * m), math.sqrt(math.log1p(d / (4 * m * m)) / 27))
                    contraction = np.zeros(p)
                    contraction[:d] = abs(weights[d - 1]) / weights[:d]
                    tensors = np.array([b * tensor_product([v * contraction, v, v]) for v in X])
                    means = tensors.reshape(len(supports), -1)
                    # Explicit reductions avoid platform BLAS floating-point flag artifacts.
                    dots = np.einsum('ia,ja->ij', means, means, optimize=False)
                    original_dots = b * b * np.einsum('ia,ja->ij', X, X, optimize=False) ** 3
                    assert np.isfinite(dots).all() and np.isfinite(original_dots).all()
                    assert np.all(dots <= original_dots + 1e-12)
                    assert np.all(np.linalg.norm(means, axis=1) <= M + 1e-12)
                    actual_targets = np.einsum('ni,i->n', np.array([[T[i, i, i] for i in range(p)] for T in tensors]), weights)
                    expected_target = abs(weights[d - 1]) * b * harmonic(m)
                    assert np.allclose(actual_targets, expected_target, atol=1e-12)
                    second_moment = float(np.mean(np.exp(dots)))
                    assert second_moment <= math.exp(0.25) + 1e-12
                    mixtures.append(dict(p=p, d=d, m=m, M=M, support_pairs=len(supports) ** 2,
                                         common_target=expected_target, second_moment=second_moment))

    # Exact Gaussian union bound uses normal tails and binomial counts, rather than
    # the exponential tail bound used in the written proof.
    tail_checks = []
    beta = 1 / 8
    for K in (3, 4, 6):
        for p in (1, 2, 8, 64, 1024):
            s = np.arange(1, p + 1, dtype=float)
            lam = np.sqrt(2 * (s * np.log(math.e * p / s) + K * s * math.log(1 + 4 * K) + math.log(2 * p / beta)))
            log_count = gammaln(p + 1) - gammaln(s + 1) - gammaln(p - s + 1) + K * s * math.log(1 + 4 * K)
            for slack in (0, 0.1, 1, 3, 10, 30):
                log_union = float(logsumexp(math.log(2) + log_count + norm.logsf(lam + slack)))
                claimed = math.log(beta) - slack * slack / 2
                assert log_union <= claimed + 1e-9
                tail_checks.append(dict(K=K, p=p, slack=slack, log_union=log_union, log_bound=claimed))

    # Orthogonal loading reduction checked in unequal ambient dimensions.
    rotation_errors = []
    for m in (1, 2, 3):
        for _ in range(20):
            factors = [rng.normal(size=m) for _ in range(3)]
            A = tensor_product(factors)
            signs = rng.choice([-1, 1], size=m)
            bases = [np.linalg.qr(rng.normal(size=(m + k + 1, m)))[0] for k in range(3)]
            ambient = A
            for k, Q in enumerate(bases):
                ambient = mode_product(ambient, Q, k)
            loading = sum(signs[i] * tensor_product([Q[:, i] for Q in bases]) for i in range(m)) / math.sqrt(m)
            actual = float(np.sum(ambient * loading))
            expected = float(np.sum(signs * np.array([A[i, i, i] for i in range(m)])) / math.sqrt(m))
            rotation_errors.append(abs(actual - expected))
            assert np.isclose(np.linalg.norm(ambient), np.linalg.norm(A))
            assert np.isclose(np.linalg.norm(loading), 1)
            assert math.isclose(actual, expected, abs_tol=1e-10)

    result = dict(status='PASS', seed=SEED,
                  interpretation='Finite algebraic/numerical checks, not formal proof verification or minimax-estimator simulations.',
                  rate_grid_configurations=len(grid), min_lower_target_to_rate=min(row['lower_ratio'] for row in grid),
                  max_normalized_sum=max(sum_ratios), random_doubled_cap_differences=geometry_count,
                  max_ordered_norm_envelope_ratio=geometry_max_ratio, weighted_mixture_configurations=len(mixtures),
                  weighted_support_pairs=sum(row['support_pairs'] for row in mixtures),
                  max_weighted_mixture_second_moment=max(row['second_moment'] for row in mixtures),
                  residual_tail_checks=len(tail_checks), rotated_loading_checks=len(rotation_errors),
                  max_rotation_target_error=max(rotation_errors),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (ROOT / 'results').mkdir(exist_ok=True)
    (ROOT / 'results/theory_checks.json').write_text(json.dumps(result, indent=2) + '\n')
    (ROOT / 'results/rate_grid.json').write_text(json.dumps(grid, indent=2) + '\n')
    (ROOT / 'results/weighted_mixtures.json').write_text(json.dumps(mixtures, indent=2) + '\n')
    (ROOT / 'results/residual_tails.json').write_text(json.dumps(tail_checks, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
