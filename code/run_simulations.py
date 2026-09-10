#!/usr/bin/env python3
"""Reproducible simulations for the TT population functional-risk paper.

The experiments are deliberately theorem-aligned rather than LLM-scale:
1. verify that a generic TT contraction Jacobian has raw-minus-gauge rank;
2. estimate a correctly specified Bernoulli teacher in a TT horizontal tangent
   and check the d/(2n) conditional-KL law;
3. contrast stochastic teacher samples with exact soft labels;
4. show the possible Frobenius/functional ranking reversal; and
5. verify an approximation-plus-estimation oracle in a Gaussian tangent model.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-tt-risk")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.special import expit, xlogy

# Accelerate/BLAS combinations on some macOS builds leave floating-point flags
# set after SVD and then emit spurious warnings on a later finite matrix product.
# Every optimizer and every saved table is checked for finite values below.
np.seterr(over="ignore", divide="ignore", invalid="ignore")


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"


def tt_shapes(mode_sizes: tuple[int, ...], rank: int) -> list[tuple[int, int, int]]:
    ranks = (1,) + (rank,) * (len(mode_sizes) - 1) + (1,)
    return [
        (ranks[j], mode_sizes[j], ranks[j + 1])
        for j in range(len(mode_sizes))
    ]


def random_tt_cores(
    mode_sizes: tuple[int, ...], rank: int, rng: np.random.Generator
) -> list[np.ndarray]:
    cores = [rng.normal(size=shape) for shape in tt_shapes(mode_sizes, rank)]
    # Keep contractions numerically moderate without changing generic ranks.
    for j, core in enumerate(cores):
        cores[j] = core / np.sqrt(core.shape[0] * core.shape[1])
    return cores


def tt_contract(cores: list[np.ndarray]) -> np.ndarray:
    value = cores[0][0, :, :]
    for core in cores[1:]:
        value = np.tensordot(value, core, axes=([-1], [0]))
    return np.squeeze(value, axis=-1)


def pack_cores(cores: list[np.ndarray]) -> np.ndarray:
    return np.concatenate([core.ravel() for core in cores])


def unpack_cores(vector: np.ndarray, shapes: list[tuple[int, int, int]]) -> list[np.ndarray]:
    cores: list[np.ndarray] = []
    start = 0
    for shape in shapes:
        size = int(np.prod(shape))
        cores.append(vector[start : start + size].reshape(shape))
        start += size
    if start != vector.size:
        raise ValueError("Core vector has the wrong length.")
    return cores


def tt_jacobian(
    cores: list[np.ndarray], step: float = 1e-6
) -> tuple[np.ndarray, np.ndarray]:
    """Finite-difference Jacobian of the contracted tensor by raw cores."""
    shapes = [core.shape for core in cores]
    packed = pack_cores(cores)
    base = tt_contract(cores).ravel()
    jac = np.empty((base.size, packed.size))
    for j in range(packed.size):
        plus = packed.copy()
        minus = packed.copy()
        plus[j] += step
        minus[j] -= step
        jac[:, j] = (
            tt_contract(unpack_cores(plus, shapes)).ravel()
            - tt_contract(unpack_cores(minus, shapes)).ravel()
        ) / (2.0 * step)
    return base, jac


def tt_dimension(mode_sizes: tuple[int, ...], rank: int) -> tuple[int, int, int]:
    shapes = tt_shapes(mode_sizes, rank)
    raw = int(sum(np.prod(shape) for shape in shapes))
    gauge = (len(mode_sizes) - 1) * rank**2
    return raw, gauge, raw - gauge


def tangent_geometry(
    mode_sizes: tuple[int, ...], rank: int, seed: int
) -> tuple[dict[str, float], np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    cores = random_tt_cores(mode_sizes, rank, rng)
    tensor, jac = tt_jacobian(cores)
    singular_values = np.linalg.svd(jac, compute_uv=False)
    # Central differences leave gauge-null singular values near 1e-11 here;
    # the non-null values are separated by at least four orders of magnitude.
    tol = singular_values[0] * 1e-8
    numerical_rank = int(np.sum(singular_values > tol))
    raw, gauge, theory_dim = tt_dimension(mode_sizes, rank)
    if numerical_rank != theory_dim:
        raise RuntimeError(
            f"Numerical tangent rank {numerical_rank} != TT dimension {theory_dim}."
        )
    left, _, _ = np.linalg.svd(jac, full_matrices=False)
    tangent = left[:, :numerical_rank]
    tensor = tensor / np.linalg.norm(tensor) * 0.35
    record = {
        "order": len(mode_sizes),
        "mode_size": mode_sizes[0],
        "tt_rank": rank,
        "ambient_dimension": int(np.prod(mode_sizes)),
        "raw_core_count": raw,
        "gauge_dimension": gauge,
        "theoretical_quotient_dimension": theory_dim,
        "numerical_jacobian_rank": numerical_rank,
        "smallest_nonzero_jacobian_sv": float(singular_values[numerical_rank - 1]),
    }
    return record, tensor, tangent


def bernoulli_kl(q: np.ndarray, p: np.ndarray) -> np.ndarray:
    eps = np.finfo(float).eps
    p = np.clip(p, eps, 1.0 - eps)
    q = np.clip(q, eps, 1.0 - eps)
    value = xlogy(q, q / p) + xlogy(1.0 - q, (1.0 - q) / (1.0 - p))
    return np.maximum(value, 0.0)


def logistic_objective(
    theta: np.ndarray, design: np.ndarray, offset: np.ndarray, target: np.ndarray
) -> float:
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        eta = offset + design @ theta
    if not np.all(np.isfinite(eta)):
        return float("inf")
    return float(np.sum(np.logaddexp(0.0, eta) - target * eta))


def fit_logistic_offset(
    design: np.ndarray,
    offset: np.ndarray,
    target: np.ndarray,
    init: np.ndarray | None = None,
    max_iter: int = 60,
    tolerance: float = 1e-9,
) -> np.ndarray:
    """Newton fit for Bernoulli outcomes or fractional soft labels."""
    d = design.shape[1]
    theta = np.zeros(d) if init is None else np.asarray(init, dtype=float).copy()
    ridge = 1e-9
    for _ in range(max_iter):
        with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
            eta = offset + design @ theta
        if not np.all(np.isfinite(eta)):
            raise FloatingPointError("Non-finite linear predictor in logistic fit.")
        prob = expit(eta)
        gradient = design.T @ (prob - target)
        if np.linalg.norm(gradient) <= tolerance * max(1.0, float(design.shape[0])):
            break
        weight = np.maximum(prob * (1.0 - prob), 1e-7)
        with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
            hessian = design.T @ (weight[:, None] * design) + ridge * np.eye(d)
        if not np.all(np.isfinite(hessian)):
            raise FloatingPointError("Non-finite Hessian in logistic fit.")
        step = np.linalg.solve(hessian, gradient)
        step_norm = np.linalg.norm(step)
        if not np.isfinite(step_norm):
            raise FloatingPointError("Non-finite Newton step in logistic fit.")
        if step_norm <= tolerance * (1.0 + np.linalg.norm(theta)):
            break
        if step_norm > 10.0:
            step *= 10.0 / step_norm
        old_value = logistic_objective(theta, design, offset, target)
        scale = 1.0
        while scale > 1e-6:
            proposal = theta - scale * step
            if logistic_objective(proposal, design, offset, target) <= old_value:
                theta = proposal
                break
            scale *= 0.5
        else:
            break
    return theta


def gaussian_tangent_draws(
    n: int,
    tangent: np.ndarray,
    tensor: np.ndarray,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Draw tangent design and correlated base logit without materializing X."""
    coefficient = tangent.T @ tensor
    residual_sq = max(float(tensor @ tensor - coefficient @ coefficient), 0.0)
    design = rng.normal(size=(n, tangent.shape[1]))
    offset = design @ coefficient
    if residual_sq > 1e-14:
        offset += np.sqrt(residual_sq) * rng.normal(size=n)
    return design, offset


def run_tt_rate_experiment(
    geometries: dict[int, tuple[np.ndarray, np.ndarray]],
    reps: int,
    multipliers: tuple[int, ...],
    seed: int,
) -> pd.DataFrame:
    rows: list[dict[str, float]] = []
    master = np.random.default_rng(seed)
    for rank, (tensor, tangent) in geometries.items():
        d = tangent.shape[1]
        test_rng = np.random.default_rng(seed + 1000 + rank)
        test_design, test_offset = gaussian_tangent_draws(12000, tangent, tensor, test_rng)
        test_q = expit(test_offset)
        for multiplier in multipliers:
            n = multiplier * d
            risks = []
            for _ in range(reps):
                rng = np.random.default_rng(master.integers(0, 2**32 - 1))
                design, offset = gaussian_tangent_draws(n, tangent, tensor, rng)
                q = expit(offset)
                outcome = rng.binomial(1, q)
                theta = fit_logistic_offset(design, offset, outcome)
                test_p = expit(test_offset + test_design @ theta)
                risks.append(float(np.mean(bernoulli_kl(test_q, test_p))))
            rows.append(
                {
                    "tt_rank": rank,
                    "quotient_dimension": d,
                    "n": n,
                    "n_over_d": multiplier,
                    "replications": reps,
                    "mean_population_kl": np.mean(risks),
                    "se_population_kl": np.std(risks, ddof=1) / np.sqrt(reps),
                    "n_risk_over_d": n * np.mean(risks) / d,
                }
            )
    return pd.DataFrame(rows)


def run_access_experiment(
    dimension: int, reps: int, multipliers: tuple[int, ...], seed: int
) -> pd.DataFrame:
    rows: list[dict[str, float | str]] = []
    master = np.random.default_rng(seed)
    test_rng = np.random.default_rng(seed + 1)
    test_x = test_rng.normal(size=(30000, dimension))
    nonlinear_test_logit = 0.65 * (
        np.sum(test_x**2, axis=1) - dimension
    ) / np.sqrt(2.0 * dimension)
    nonlinear_test_q = expit(nonlinear_test_logit)
    base_test_p = np.full(test_x.shape[0], 0.5)
    base_test_risk = float(np.mean(bernoulli_kl(nonlinear_test_q, base_test_p)))
    for multiplier in multipliers:
        n = multiplier * dimension
        black_box_risks = []
        exact_correct_risks = []
        exact_misspecified_excess = []
        for _ in range(reps):
            rng = np.random.default_rng(master.integers(0, 2**32 - 1))
            x = rng.normal(size=(n, dimension))

            stochastic_y = rng.binomial(1, 0.5, size=n)
            theta_black = fit_logistic_offset(x, np.zeros(n), stochastic_y)
            black_p = expit(test_x @ theta_black)
            black_box_risks.append(
                float(np.mean(bernoulli_kl(np.full(test_x.shape[0], 0.5), black_p)))
            )

            init = rng.normal(scale=0.1, size=dimension)
            theta_soft = fit_logistic_offset(
                x, np.zeros(n), np.full(n, 0.5), init=init
            )
            soft_p = expit(test_x @ theta_soft)
            exact_correct_risks.append(
                float(np.mean(bernoulli_kl(np.full(test_x.shape[0], 0.5), soft_p)))
            )

            nonlinear_logit = 0.65 * (
                np.sum(x**2, axis=1) - dimension
            ) / np.sqrt(2.0 * dimension)
            nonlinear_q = expit(nonlinear_logit)
            theta_miss = fit_logistic_offset(x, np.zeros(n), nonlinear_q)
            miss_p = expit(test_x @ theta_miss)
            total = float(np.mean(bernoulli_kl(nonlinear_test_q, miss_p)))
            exact_misspecified_excess.append(total - base_test_risk)

        for regime, values in [
            ("stochastic_teacher", black_box_risks),
            ("exact_soft_labels_correct", exact_correct_risks),
            ("exact_soft_labels_misspecified", exact_misspecified_excess),
        ]:
            rows.append(
                {
                    "regime": regime,
                    "dimension": dimension,
                    "n": n,
                    "n_over_d": multiplier,
                    "replications": reps,
                    "mean_excess_kl": np.mean(values),
                    "se_excess_kl": np.std(values, ddof=1) / np.sqrt(reps),
                    "n_risk_over_d": n * np.mean(values) / dimension,
                }
            )
    return pd.DataFrame(rows)


def rank_one_tt_atom(
    mode_sizes: tuple[int, ...], coordinate: int
) -> np.ndarray:
    """Return an orthonormal coordinate atom with TT rank one.

    The outer product of one-hot mode factors is represented exactly by TT
    cores of shape ``(1, mode_size, 1)``.  Distinct coordinates therefore give
    Frobenius-orthogonal, equal-budget rank-one TT tensors.
    """
    if not mode_sizes or coordinate < 0 or any(coordinate >= m for m in mode_sizes):
        raise ValueError("The requested coordinate must exist in every mode.")
    atom = np.array(1.0)
    for mode_size in mode_sizes:
        factor = np.zeros(mode_size)
        factor[coordinate] = 1.0
        atom = np.multiply.outer(atom, factor)
    return atom


def run_misordering_experiment(
    condition_numbers: tuple[float, ...] = (2, 4, 8, 16, 32),
    a: float = 0.8,
    b: float = 1.0,
    t: float = 0.5,
    mode_sizes: tuple[int, ...] = (2, 2, 2, 2),
) -> pd.DataFrame:
    """Evaluate the exact Bernoulli-KL rank-one TT misordering example.

    The teacher is ``t * (a T_H + b T_L)``.  Candidate A retains ``T_L`` and
    drops ``a T_H``; candidate B retains ``T_H`` and drops ``b T_L``.  Thus A
    has smaller squared Frobenius error because ``a < b``.  Prompts equal the
    two orthonormal TT atoms with probabilities ``rho_H`` and ``rho_L``.  The
    ratio ``rho_H / rho_L`` is also the local conditional-information condition
    ratio.  Exact population risks, rather than their quadratic expansions, are
    reported below.
    """
    if not (0.0 < a < b and t > 0.0):
        raise ValueError("The construction requires 0 < a < b and t > 0.")
    if any(condition <= (b / a) ** 2 for condition in condition_numbers):
        raise ValueError(
            "Each information condition ratio must make rho_H*a^2 > rho_L*b^2."
        )

    tensor_h = rank_one_tt_atom(mode_sizes, coordinate=0)
    tensor_l = rank_one_tt_atom(mode_sizes, coordinate=1)
    if not (
        np.isclose(np.linalg.norm(tensor_h), 1.0)
        and np.isclose(np.linalg.norm(tensor_l), 1.0)
        and np.isclose(np.vdot(tensor_h, tensor_l), 0.0)
    ):
        raise RuntimeError("The rank-one TT atoms are not Frobenius orthonormal.")

    teacher = t * (a * tensor_h + b * tensor_l)
    candidate_a = t * b * tensor_l
    candidate_b = t * a * tensor_h
    error_a = teacher - candidate_a
    error_b = teacher - candidate_b
    frobenius_norm_a = float(np.linalg.norm(error_a))
    frobenius_norm_b = float(np.linalg.norm(error_b))
    squared_frobenius_a = float(np.vdot(error_a, error_a).real)
    squared_frobenius_b = float(np.vdot(error_b, error_b).real)

    prompts = (tensor_h, tensor_l)
    teacher_probabilities = np.array(
        [expit(float(np.vdot(teacher, prompt).real)) for prompt in prompts]
    )
    candidate_a_probabilities = np.array(
        [expit(float(np.vdot(candidate_a, prompt).real)) for prompt in prompts]
    )
    candidate_b_probabilities = np.array(
        [expit(float(np.vdot(candidate_b, prompt).real)) for prompt in prompts]
    )
    conditional_kl_a = bernoulli_kl(
        teacher_probabilities, candidate_a_probabilities
    )
    conditional_kl_b = bernoulli_kl(
        teacher_probabilities, candidate_b_probabilities
    )

    rows: list[dict[str, float | str | int | bool]] = []
    for condition_number in condition_numbers:
        rho_h = condition_number / (1.0 + condition_number)
        rho_l = 1.0 / (1.0 + condition_number)
        weights = np.array([rho_h, rho_l])
        exact_risk_a = float(weights @ conditional_kl_a)
        exact_risk_b = float(weights @ conditional_kl_b)
        quadratic_risk_a = rho_h * (t * a) ** 2 / 8.0
        quadratic_risk_b = rho_l * (t * b) ** 2 / 8.0
        if not (
            squared_frobenius_a < squared_frobenius_b
            and exact_risk_a > exact_risk_b > 0.0
        ):
            raise RuntimeError("The requested exact metric reversal did not occur.")
        rows.append(
            {
                "metric_condition_number": float(condition_number),
                "rho_H": rho_h,
                "rho_L": rho_l,
                "teacher_scale_t": t,
                "teacher_amplitude_a": a,
                "teacher_amplitude_b": b,
                "tt_order": len(mode_sizes),
                "tt_mode_size": mode_sizes[0],
                "tt_rank_candidate_A": 1,
                "tt_rank_candidate_B": 1,
                # Retain the original column names, now as actual norms.
                "frobenius_error_candidate_A": frobenius_norm_a,
                "frobenius_error_candidate_B": frobenius_norm_b,
                "squared_frobenius_error_candidate_A": squared_frobenius_a,
                "squared_frobenius_error_candidate_B": squared_frobenius_b,
                # These original risk columns now contain exact population KL.
                "functional_risk_candidate_A": exact_risk_a,
                "functional_risk_candidate_B": exact_risk_b,
                "quadratic_risk_candidate_A": quadratic_risk_a,
                "quadratic_risk_candidate_B": quadratic_risk_b,
                "frobenius_selected": "A",
                "functional_selected": "B",
                "condition_inequality_holds": bool(rho_h * a**2 > rho_l * b**2),
                "risk_improvement_factor": exact_risk_a / exact_risk_b,
                "local_quadratic_improvement_factor": (
                    quadratic_risk_a / quadratic_risk_b
                ),
            }
        )
    return pd.DataFrame(rows)


def run_oracle_experiment(reps: int, seed: int) -> pd.DataFrame:
    dimensions = np.array([13, 36, 69, 112])
    ambient = 180
    index = np.arange(1, ambient + 1)
    smoothness = 0.8
    theta = 1.4 * index ** (-(smoothness + 0.5))
    rows = []
    rng = np.random.default_rng(seed)
    for n in (200, 500, 1000, 2000, 5000):
        approximation = np.array(
            [np.sum(theta[d:] ** 2) for d in dimensions], dtype=float
        )
        oracle_curve = approximation + dimensions / n
        oracle_risk = float(np.min(oracle_curve))
        oracle_dimension = int(dimensions[np.argmin(oracle_curve)])
        selected_risks = []
        selected_dimensions = []
        for _ in range(reps):
            observation = theta + rng.normal(scale=1.0 / np.sqrt(n), size=ambient)
            # Mallows/SURE criterion, up to an additive constant independent of d.
            criteria = np.array(
                [np.sum(observation[d:] ** 2) + 2.0 * d / n for d in dimensions]
            )
            chosen = int(dimensions[np.argmin(criteria)])
            estimate = np.zeros(ambient)
            estimate[:chosen] = observation[:chosen]
            selected_risks.append(float(np.sum((estimate - theta) ** 2)))
            selected_dimensions.append(chosen)
        rows.append(
            {
                "n": n,
                "replications": reps,
                "oracle_dimension": oracle_dimension,
                "mean_selected_dimension": np.mean(selected_dimensions),
                "oracle_approximation_plus_estimation": oracle_risk,
                "mean_selected_risk": np.mean(selected_risks),
                "se_selected_risk": np.std(selected_risks, ddof=1) / np.sqrt(reps),
                "selected_to_oracle_ratio": np.mean(selected_risks) / oracle_risk,
            }
        )
    return pd.DataFrame(rows)


def save_figures(
    rate: pd.DataFrame,
    access: pd.DataFrame,
    misordering: pd.DataFrame,
    oracle: pd.DataFrame,
) -> None:
    plt.style.use("seaborn-v0_8-whitegrid")

    fig, ax = plt.subplots(figsize=(6.2, 4.3))
    rank_styles = {
        1: {"marker": "o", "linestyle": "-"},
        2: {"marker": "s", "linestyle": "--"},
        3: {"marker": "^", "linestyle": ":"},
    }
    for rank, group in rate.groupby("tt_rank"):
        x = group["quotient_dimension"] / group["n"]
        ax.errorbar(
            x,
            group["mean_population_kl"],
            yerr=1.96 * group["se_population_kl"],
            marker=rank_styles[int(rank)]["marker"],
            linestyle=rank_styles[int(rank)]["linestyle"],
            capsize=2,
            label=f"TT rank {rank}",
        )
    xref = np.linspace(0, (rate["quotient_dimension"] / rate["n"]).max(), 100)
    ax.plot(xref, 0.5 * xref, "k--", label=r"$d/(2n)$")
    ax.set_xlabel(r"Gauge-adjusted dimension / queries, $d_{\mathrm{TT}}/n$")
    ax.set_ylabel("Population conditional KL")
    ax.legend(frameon=True)
    fig.tight_layout()
    fig.savefig(FIGURES / "tt_rate.png", dpi=220)
    fig.savefig(FIGURES / "tt_rate.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.2, 4.3))
    access_styles = {
        "stochastic_teacher": {"marker": "o", "linestyle": "-"},
        "exact_soft_labels_correct": {"marker": "s", "linestyle": "--"},
        "exact_soft_labels_misspecified": {"marker": "^", "linestyle": ":"},
    }
    access_labels = {
        "stochastic_teacher": "stochastic teacher samples",
        "exact_soft_labels_correct": "exact soft labels (correct specification)",
        "exact_soft_labels_misspecified": "exact soft labels (misspecified)",
    }
    for regime, group in access.groupby("regime"):
        ax.plot(
            group["n_over_d"],
            group["mean_excess_kl"],
            marker=access_styles[regime]["marker"],
            linestyle=access_styles[regime]["linestyle"],
            label=access_labels[regime],
        )
    ax.set_yscale("symlog", linthresh=1e-10)
    ax.set_xlabel(r"Prompts per coordinate, $n/d$")
    ax.set_ylabel("Population excess KL")
    ax.legend(frameon=True, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "access_regimes.png", dpi=220)
    fig.savefig(FIGURES / "access_regimes.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.2, 4.3))
    ax.plot(
        misordering["metric_condition_number"],
        misordering["risk_improvement_factor"],
        marker="o",
        label="exact Bernoulli KL",
    )
    ax.plot(
        misordering["metric_condition_number"],
        misordering["local_quadratic_improvement_factor"],
        marker="s",
        linestyle="--",
        label="local quadratic prediction",
    )
    ax.axhline(1.0, color="black", linewidth=0.8, linestyle=":")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=2)
    ax.set_xlabel(r"Information condition ratio, $\rho_H/\rho_L$")
    ax.set_ylabel("KL of Frobenius choice / KL of functional choice")
    ax.legend(frameon=True)
    fig.tight_layout()
    fig.savefig(FIGURES / "metric_misordering.png", dpi=220)
    fig.savefig(FIGURES / "metric_misordering.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.2, 4.3))
    ax.plot(oracle["n"], oracle["mean_selected_risk"], marker="o", label="selected")
    ax.plot(
        oracle["n"],
        oracle["oracle_approximation_plus_estimation"],
        marker="s",
        linestyle="--",
        label="oracle curve",
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Queries, n")
    ax.set_ylabel("Squared functional tangent risk")
    ax.legend(frameon=True)
    fig.tight_layout()
    fig.savefig(FIGURES / "oracle_adaptation.png", dpi=220)
    fig.savefig(FIGURES / "oracle_adaptation.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="Use a short smoke-test run.")
    parser.add_argument("--seed", type=int, default=20260907)
    args = parser.parse_args()

    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    rate_reps = 12 if args.quick else 80
    access_reps = 15 if args.quick else 100
    oracle_reps = 300 if args.quick else 3000
    multipliers = (8, 16, 32, 64)
    mode_sizes = (4, 4, 4, 4)

    geometry_rows = []
    geometries: dict[int, tuple[np.ndarray, np.ndarray]] = {}
    for rank in (1, 2, 3):
        record, tensor, tangent = tangent_geometry(
            mode_sizes, rank, args.seed + 17 * rank
        )
        geometry_rows.append(record)
        geometries[rank] = (tensor, tangent)
    geometry = pd.DataFrame(geometry_rows)
    rate = run_tt_rate_experiment(
        geometries, rate_reps, multipliers, args.seed + 100
    )
    access = run_access_experiment(20, access_reps, multipliers, args.seed + 200)
    misordering = run_misordering_experiment()
    oracle = run_oracle_experiment(oracle_reps, args.seed + 300)

    for name, frame in {
        "geometry": geometry,
        "rate": rate,
        "access": access,
        "misordering": misordering,
        "oracle": oracle,
    }.items():
        numeric = frame.select_dtypes(include=[np.number]).to_numpy()
        if not np.all(np.isfinite(numeric)):
            raise FloatingPointError(f"Non-finite value in {name} results.")

    geometry.to_csv(RESULTS / "tt_geometry.csv", index=False)
    rate.to_csv(RESULTS / "tt_rate.csv", index=False)
    access.to_csv(RESULTS / "access_regimes.csv", index=False)
    misordering.to_csv(RESULTS / "metric_misordering.csv", index=False)
    oracle.to_csv(RESULTS / "oracle_adaptation.csv", index=False)
    save_figures(rate, access, misordering, oracle)

    summary = {
        "mode": "quick" if args.quick else "full",
        "seed": args.seed,
        "geometry_all_match": bool(
            np.all(
                geometry["theoretical_quotient_dimension"]
                == geometry["numerical_jacobian_rank"]
            )
        ),
        "mean_n_risk_over_d": float(rate["n_risk_over_d"].mean()),
        "exact_correct_max_risk": float(
            access.loc[
                access["regime"] == "exact_soft_labels_correct", "mean_excess_kl"
            ].max()
        ),
        "oracle_ratio_mean": float(oracle["selected_to_oracle_ratio"].mean()),
        "misordering_all_reversed": bool(
            np.all(
                (misordering["frobenius_selected"] == "A")
                & (misordering["functional_selected"] == "B")
                & misordering["condition_inequality_holds"]
            )
        ),
        "misordering_min_exact_improvement": float(
            misordering["risk_improvement_factor"].min()
        ),
        "misordering_max_exact_improvement": float(
            misordering["risk_improvement_factor"].max()
        ),
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
