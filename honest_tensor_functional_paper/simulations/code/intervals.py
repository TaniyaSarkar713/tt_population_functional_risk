"""Intervals in T2. Parameters are supplied outer bounds, not estimates."""
from dataclasses import dataclass
import numpy as np
from scipy.stats import norm


@dataclass(frozen=True)
class Radii:
    threshold: float
    nonlinear: float
    gaussian: float
    structural: float
    selected: str


def radii(K, p, tau, M=1.0, rank_cap=1, alpha=0.05, multiplier=1.0):
    """Equal dimensions, equal positive diagonal weights, equal rank caps.

    For these caps J_Tucker=J_TT=rank_cap**(K-1).
    """
    if K < 2 or p < 1 or tau <= 0 or M <= 0 or not 0 < alpha < 1:
        raise ValueError("Invalid model parameters")
    if not 1 <= rank_cap <= p or int(rank_cap) != rank_cap:
        raise ValueError("Rank cap must be an integer in [1,p]")
    if multiplier < 1:
        raise ValueError("The proved threshold multiplier must be at least one")
    q = 2.0 / K
    J = rank_cap ** (K - 1)
    lam = multiplier * tau * np.sqrt(2 * np.log(2 * p / alpha))
    nl = J ** (1 - q / 2) * M**q * (2 * lam) ** (1 - q) / np.sqrt(p)
    gauss = norm.ppf(1 - alpha / 2) * tau
    structural = M * np.sqrt(rank_cap / p)
    choices = {"nonlinear": nl, "gaussian": gauss, "structural": structural}
    return Radii(lam, nl, gauss, structural, min(choices, key=choices.get))


def centers(diagonal, threshold):
    """Each row is one replicate of the observed diagonal."""
    diagonal = np.asarray(diagonal)
    if diagonal.ndim != 2:
        raise ValueError("Expected a replication-by-coordinate matrix")
    p = diagonal.shape[1]
    soft = np.sign(diagonal) * np.maximum(np.abs(diagonal) - threshold, 0)
    return {"nonlinear": soft.sum(axis=1) / np.sqrt(p),
            "gaussian": diagonal.sum(axis=1) / np.sqrt(p),
            "structural": np.zeros(diagonal.shape[0])}
