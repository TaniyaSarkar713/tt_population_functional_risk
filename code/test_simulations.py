#!/usr/bin/env python3
"""Fast deterministic checks for the simulation implementation."""

import numpy as np

from run_simulations import (
    bernoulli_kl,
    fit_logistic_offset,
    rank_one_tt_atom,
    run_access_experiment,
    run_misordering_experiment,
    tangent_geometry,
    tt_dimension,
)


def test_dimensions() -> None:
    mode_sizes = (4, 4, 4, 4)
    for rank in (1, 2, 3):
        raw, gauge, dimension = tt_dimension(mode_sizes, rank)
        record, _, tangent = tangent_geometry(mode_sizes, rank, seed=100 + rank)
        assert raw - gauge == dimension
        assert record["numerical_jacobian_rank"] == dimension
        assert tangent.shape == (4**4, dimension)


def test_bernoulli_kl() -> None:
    q = np.array([0.2, 0.5, 0.8])
    assert np.allclose(bernoulli_kl(q, q), 0.0)
    assert np.all(bernoulli_kl(q, 1.0 - q) >= 0.0)


def test_exact_soft_labels() -> None:
    rng = np.random.default_rng(7)
    design = rng.normal(size=(300, 6))
    target = np.full(300, 0.5)
    theta = fit_logistic_offset(
        design, np.zeros(300), target, init=np.full(6, 0.2)
    )
    assert np.linalg.norm(theta) < 1e-7

    access = run_access_experiment(
        dimension=2, reps=2, multipliers=(8,), seed=11
    )
    assert set(access["regime"]) == {
        "stochastic_teacher",
        "exact_soft_labels_correct",
        "exact_soft_labels_misspecified",
    }


def test_exact_rank_one_tt_misordering() -> None:
    tensor_h = rank_one_tt_atom((2, 2, 2, 2), coordinate=0)
    tensor_l = rank_one_tt_atom((2, 2, 2, 2), coordinate=1)
    assert np.isclose(np.linalg.norm(tensor_h), 1.0)
    assert np.isclose(np.linalg.norm(tensor_l), 1.0)
    assert np.isclose(np.vdot(tensor_h, tensor_l), 0.0)

    result = run_misordering_experiment()
    assert np.all(result["rho_H"] / result["rho_L"] == result["metric_condition_number"])
    assert np.all(
        result["squared_frobenius_error_candidate_A"]
        < result["squared_frobenius_error_candidate_B"]
    )
    assert np.all(
        result["functional_risk_candidate_A"]
        > result["functional_risk_candidate_B"]
    )
    assert np.all(result["condition_inequality_holds"])
    assert np.all(result["frobenius_selected"] == "A")
    assert np.all(result["functional_selected"] == "B")
    assert np.allclose(
        result["risk_improvement_factor"],
        result["functional_risk_candidate_A"]
        / result["functional_risk_candidate_B"],
    )
    # Exact nonlinear KL remains close to, but is not replaced by, its local
    # quadratic approximation at t=0.5.
    assert np.all(result["risk_improvement_factor"] > 1.0)
    assert not np.allclose(
        result["risk_improvement_factor"],
        result["local_quadratic_improvement_factor"],
        rtol=1e-5,
    )


if __name__ == "__main__":
    test_dimensions()
    test_bernoulli_kl()
    test_exact_soft_labels()
    test_exact_rank_one_tt_misordering()
    print("All simulation checks passed.")
