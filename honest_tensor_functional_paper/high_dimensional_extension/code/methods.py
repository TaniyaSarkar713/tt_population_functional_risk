"""High-dimensional intervals and finite loading/rank envelopes.

The growing-cap interval is minimax for r >= c sqrt(p). The pointwise
interval is honest without separation; its proved pointwise optimality
requires the strong saturated Tucker regime in theory/results.md.
"""
import math

import numpy as np
from scipy.linalg import svd
from scipy.stats import norm


def _bounds(M, tau, alpha):
    if not np.isfinite([M, tau, alpha]).all() or M <= 0 or tau <= 0 or not 0 < alpha < 1:
        raise ValueError('Require finite M,tau > 0 and 0 < alpha < 1.')


def _rank(p, rank):
    if int(rank) != rank or not 1 <= rank <= p:
        raise ValueError('Require an integer supplied cap between one and p.')
    return int(rank)


def growing_cap_interval(diagonal, M, rank, tau=1., alpha=.05):
    """O(p) coordinate accesses; valid for the full Tucker/TT cap class.

    rank is the smallest supplied constrained-unfolding cap, truncated at p.
    The off-diagonal observations are unused, rather than assumed absent.
    """
    diagonal = np.asarray(diagonal, float)
    if diagonal.ndim != 1 or not len(diagonal) or not np.isfinite(diagonal).all():
        raise ValueError('Supply a finite nonempty diagonal observation vector.')
    _bounds(M, tau, alpha)
    p, rank = len(diagonal), _rank(len(diagonal), rank)
    structural = M * np.sqrt(rank / p)
    direct = norm.isf(alpha / 2) * tau
    observed = float(np.sum(diagonal) / np.sqrt(p))
    center, radius, selected = ((0., structural, 'structural') if structural <= direct
                                else (observed, direct, 'direct'))
    return dict(lo=center - radius, hi=center + radius, width=2 * radius,
                selected=selected, estimate=0. if structural <= tau else observed,
                mse_upper=min(structural ** 2, tau ** 2),
                rate=min(structural, tau), coordinate_accesses=p)


def growing_lower(p, rank, M, tau=1., alpha=.05):
    _bounds(M, tau, alpha)
    rank = _rank(p, rank)
    target = min(M * np.sqrt(rank / p),
                 tau * rank / np.sqrt(p) * np.sqrt(np.log1p(p / (4 * rank * rank))))
    coefficient = 1 - 2 * alpha - .5 * np.sqrt(np.expm1(.25))
    if coefficient <= 0:
        raise ValueError('Confidence level does not give a positive mixture coefficient.')
    return dict(target=float(target), length_lower=float(coefficient * target),
                mse_lower=float(target ** 2 * (1 - .5 * np.sqrt(np.expm1(.25))) / 8))


def fixed_cap_rate(p, M, tau=1., order=3):
    ell = np.log(np.e * p)
    x = M / (tau * np.sqrt(ell))
    factor = min(x, 1 + max(0., np.log(x)), ell) if order == 3 else min(x, 1.)
    return float(tau * np.sqrt(ell / p) * factor)


def dyadic_envelope(weights, M, tau=1., order=3, rank=1, alpha=.05):
    """Finite diameter of ideal block fits, not an implementation of those fits.

    Assumes uniform Tucker mode caps rank. Constants are retained explicitly.
    Signed weights are sorted by absolute value. Also includes structural and
    direct choices chosen using deterministic diameter bounds.
    """
    weights = np.sort(np.abs(np.asarray(weights, float)))[::-1]
    if weights.ndim != 1 or not len(weights) or not np.isfinite(weights).all():
        raise ValueError('Supply a nonempty finite vector.')
    _bounds(M, tau, alpha)
    if int(order) != order or order < 3:
        raise ValueError('Require tensor order at least three.')
    rank = _rank(len(weights), rank)
    J2 = float((2 * rank) ** (order - 1))
    P2, Q2 = 2 * J2 ** ((order - 1) / 2), 4 * J2 ** (order / 2)
    blocks, start, index, diameter, profile = [], 0, 0, 0., 0.
    exponent = 1.5 if order == 3 else .5
    while start < len(weights):
        end = 1 if index == 0 else min(2 ** index, len(weights))
        block = weights[start:end]
        size = len(block)
        s = np.arange(1, size + 1, dtype=float)
        # Work in log probabilities to avoid underflow for a large block index.
        log_inverse_alpha = np.log(1 / alpha) + (index + 1) * np.log(2)
        thresholds = tau * np.sqrt(2 * (s * np.log(np.e * size / s)
                                   + order * s * np.log(1 + 4 * order)
                                   + np.log(2 * size) + log_inverse_alpha))
        bound = float(np.sum(block * np.minimum(P2 * M, Q2 * thresholds) * s ** (-order / 2)))
        diameter += bound
        profile += block[0] * (index + 1) ** exponent
        blocks.append(dict(start=start, stop=end, error_budget=float(alpha / 2 ** (index + 1)),
                           diameter=bound, maximum_weight=float(block[0])))
        start, index = end, index + 1
    structural = 2 * M * np.linalg.norm(weights[:rank])
    direct = 2 * norm.isf(alpha / 2) * tau * np.linalg.norm(weights)
    return dict(block_diameter=diameter, structural_diameter=float(structural),
                direct_diameter=float(direct), upper_diameter=float(min(diameter, structural, direct)),
                profile_H=float(profile), blocks=blocks)


def _project_mode(tensor, basis, mode):
    if basis is None:  # Full ambient mode space.
        return tensor
    moved = np.moveaxis(tensor, mode, 0)
    reduced = np.einsum('ir,i...->r...', basis, moved, optimize=False)
    projected = np.einsum('ir,r...->i...', basis, reduced, optimize=False)
    return np.moveaxis(projected, 0, mode)


def project_modes(tensor, bases, omit=None):
    for k, basis in enumerate(bases):
        if k != omit:
            tensor = _project_mode(tensor, basis, k)
    return tensor


def flat_loading(p, order):
    result = np.zeros((p,) * order)
    ids = np.arange(p)
    result[(ids,) * order] = 1 / np.sqrt(p)
    return result


def pilot_bound(p, order, tau, delta):
    return float(2 * np.sqrt(2) * tau * np.sqrt(2 * ((p + p ** (order - 1)) * np.log(9)
                                                  + np.log(2 * order / delta))))


def pointwise_interval(observation, M, rank, rng, tau=1., alpha=.05,
                       return_loading=False):
    """Equal-diagonal interval using economy SVDs and a rank/dimension error budget.

    Honest on the complete unseparated equal-mode Tucker cap class. The
    supplied cap is retained even if the observed signal appears lower rank.
    rng supplies independent artificial Gaussian noise, not extra observations.
    """
    z = np.asarray(observation, float)
    if z.ndim < 3 or len(set(z.shape)) != 1 or min(z.shape) < 1 or not np.isfinite(z).all():
        raise ValueError('Require a finite equal-mode tensor of order at least three.')
    _bounds(M, tau, alpha)
    p, order = z.shape[0], z.ndim
    rank = _rank(p, rank)
    delta = alpha * rank / (8 * p)
    eta = pilot_bound(p, order, tau, delta)
    auxiliary = tau * rng.normal(size=z.shape)
    pilot, validation = z + auxiliary, z - auxiliary
    bases, errors = [], []
    max_right_entries = 0
    for k in range(order):
        if rank == p:
            bases.append(None); errors.append(0.)
            continue
        matrix = np.moveaxis(pilot, k, 0).reshape(p, -1)
        # Full right singular matrices would have p^(2K-2) entries. Economy
        # SVD uses p^K, which is only the size of the explicit input tensor.
        u, singular, vh = svd(matrix, full_matrices=False, check_finite=False)
        max_right_entries = max(max_right_entries, vh.size)
        bases.append(u[:, :rank].copy())
        denominator = singular[rank - 1] - eta
        errors.append(min(1., 2 * eta / denominator) if denominator > 0 else 1.)
        del u, vh
    loading = flat_loading(p, order)
    joint = project_modes(loading, bases)
    tangent = -(order - 1) * joint
    for k in range(order):
        tangent += project_modes(loading, bases, omit=k)
    discarded = loading - tangent
    angle = min(1., np.sqrt(sum(errors[k] ** 2 * errors[l] ** 2
                               for k in range(order) for l in range(k + 1, order))))
    bias = float(M * np.linalg.norm(discarded) * angle)
    tangent_norm = float(np.linalg.norm(tangent))
    q = norm.isf((alpha / 2 - delta) / 2)
    structural = M * np.sqrt(rank / p)
    radii = [bias + q * np.sqrt(2) * tau * tangent_norm, q * np.sqrt(2) * tau, structural]
    choice = int(np.argmin(radii))
    ids = np.arange(p)
    diagonal_index = (ids,) * order
    centers = [float(np.sum(tangent * validation)),
               float(np.sum(validation[diagonal_index]) / np.sqrt(p)), 0.]
    lo, hi = centers[choice] - radii[choice], centers[choice] + radii[choice]
    direct_center = float(np.sum(z[diagonal_index]) / np.sqrt(p))
    direct_radius = norm.isf(alpha / 4) * tau
    lo, hi = max(lo, direct_center - direct_radius, -structural), min(hi, direct_center + direct_radius, structural)
    if lo > hi:
        lo = hi = 0.
    result = dict(lo=float(lo), hi=float(hi), width=float(hi - lo), bias=bias,
                  selected=['tangent', 'split_direct', 'structural'][choice],
                  tangent_norm=tangent_norm, angle_bounds=list(map(float, errors)),
                  eta=eta, pilot_failure_budget=delta,
                  max_right_svd_entries=max_right_entries, input_entries=z.size,
                  full_right_svd_entries=p ** (2 * order - 2) if rank < p else 0)
    if return_loading:
        result['tangent_loading'] = tangent
    return result


def pointwise_amplitude_bound(p, rank, tau=1., order=3, alpha=.05):
    rank = _rank(p, rank)
    delta = alpha * rank / (8 * p)
    eta = pilot_bound(p, order, tau, delta)
    return max(4 * eta, eta ** 2 * np.sqrt(p) / tau)
