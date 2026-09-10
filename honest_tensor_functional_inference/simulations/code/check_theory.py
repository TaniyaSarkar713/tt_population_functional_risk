"""Numerical counterexample searches for key identities; not proof substitutes."""
import json
from pathlib import Path
import numpy as np
from scipy.stats import binom
from intervals import radii


def mode_product(A, U, k):
    return np.moveaxis(np.tensordot(U, A, axes=(1, k)), 0, k)


def diagonal(A):
    idx = np.arange(min(A.shape))
    return A[(idx,) * A.ndim]


def run():
    rng = np.random.default_rng(20260909)
    x = np.linspace(-8, 8, 1001)[:, None]
    e = np.linspace(-1, 1, 101)[None, :]
    soft = np.sign(x + e) * np.maximum(np.abs(x + e) - 1, 0)
    scalar_violation = np.max(np.abs(soft - x) - np.minimum(np.abs(x), 2))
    assert scalar_violation < 1e-12
    ratios = {"tucker": [], "tt": []}
    tt_norm_errors = []
    for K in (2, 3, 4, 5):
        for _ in range(30):
            p, r = 4, 2
            core = rng.normal(size=(r,) * K)
            A = core
            for k in range(K):
                U = np.linalg.qr(rng.normal(size=(p, r)))[0]
                A = mode_product(A, U, k)
            J = r ** (K - 1)
            bound = J ** (1 - 1 / K) * np.linalg.norm(A) ** (2 / K)
            ratios["tucker"].append(np.sum(np.abs(diagonal(A)) ** (2 / K)) / bound)

            cores = []
            for k in range(K - 1):
                prev = 1 if k == 0 else r
                Q = np.linalg.qr(rng.normal(size=(prev * p, r)))[0]
                cores.append(Q.reshape(prev, p, r))
            cores.append(rng.normal(size=(r, p, 1)))
            A = cores[0][0]
            for G in cores[1:]:
                A = np.tensordot(A, G, axes=(-1, 0))
            A = A[..., 0]
            prefix = np.ones(1)
            for G in cores:
                prefix = prefix @ np.sum(G**2, axis=1)
            tt_norm_errors.append(abs(prefix.item() - np.linalg.norm(A)**2))
            bound = J ** (1 - 1 / K) * np.linalg.norm(A) ** (2 / K)
            ratios["tt"].append(np.sum(np.abs(diagonal(A)) ** (2 / K)) / bound)
    assert max(tt_norm_errors) < 1e-10
    assert max(ratios["tucker"] + ratios["tt"]) <= 1 + 1e-12
    mixture_max = 0.0
    for p in (1, 2, 3, 8, 32, 128):
        j = np.arange(p + 1)
        exact = np.sum(binom.pmf(j, p, 0.5) * np.exp((2*j-p)**2 / (16*p)))
        assert exact <= np.sqrt(8 / 7) + 1e-12
        mixture_max = max(mixture_max, float(exact))
    # Rank-one equality examples check the exponent without the slack rank factor.
    for K in (2, 3, 4, 6):
        for s in (1, 3, 10):
            a = 0.7
            lhs = s * (a / s**(K/2))**(2/K)
            assert np.isclose(lhs, a**(2/K))
        p = 8192
        h = radii(K, p, 1 / np.sqrt(p)).nonlinear
        predicted = p**(-0.5) * (8*np.log(40*p)/p)**((K-2)/(2*K))
        assert np.isclose(h, predicted)
    # Verify the reverse diagonal-image construction, including signed entries.
    image_error = 0.0
    for K in (2, 3, 4, 5):
        raw = rng.normal(size=5)
        a = raw * (0.7 / np.sum(np.abs(raw)**(2/K))**(K/2))
        factors = [np.sign(a)*np.abs(a)**(1/K)] + [np.abs(a)**(1/K)]*(K-1)
        A = factors[0]
        for f in factors[1:]:
            A = np.multiply.outer(A, f)
        image_error = max(image_error, float(np.max(np.abs(diagonal(A)-a))))
        assert np.isclose(np.linalg.norm(A), 0.7)
    assert image_error < 1e-12
    result = {"status": "PASS", "seed": 20260909,
              "scalar_grid_points": int(x.size * e.size),
              "random_tensors_per_format": len(ratios["tt"]),
              "max_diagonal_bound_ratio": {k: max(v) for k, v in ratios.items()},
              "max_tt_squared_weight_error": max(tt_norm_errors),
              "max_exact_mixture_second_moment": mixture_max,
              "mixture_bound": float(np.sqrt(8/7)),
              "exact_diagonal_image_max_error": image_error,
              "interpretation": "Supplementary numerical checks, not proof verification"}
    dest = Path(__file__).resolve().parents[1] / "results" / "theory_checks.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
