"""Loading-sensitive mixture bounds and separation-free projection intervals."""
import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm


def weighted_axis_lower(weights, M, tau=1., alpha=.05, chi_budget=.25):
    """Full-data lower bound from an optimized common-target axis mixture.

    This is a lower bound for the full tensor class, not a matching rate for
    general loadings. Orthogonal product loading weights are required.
    """
    weights = np.sort(np.abs(np.asarray(weights, float)))[::-1]
    if not np.isfinite(weights).all() or not np.isfinite([M, tau, alpha, chi_budget]).all() or M <= 0 or tau <= 0 or not 0 < alpha < .25:
        raise ValueError('Invalid weights, norm/noise bounds, or confidence level.')
    if not 0 < chi_budget < 4 * (1 - 2 * alpha) ** 2:
        raise ValueError('Chi-square budget must give a positive length coefficient.')
    weights = weights[weights > 0]
    best = dict(delta=0., length_lower=0., chi_square=0., support=0, probabilities=[])
    for d in range(1, len(weights) + 1):
        w = weights[:d]

        def reciprocals(delta):
            x = (delta / (tau * w)) ** 2
            with np.errstate(over='ignore', under='ignore', divide='ignore', invalid='ignore'):
                return np.exp(-x) / (-np.expm1(-x))

        hi = tau * w[0] * np.sqrt(np.log1p(d * chi_budget))
        root = brentq(lambda scale: 1 / reciprocals(scale * hi).sum() - chi_budget,
                      0., 1. + 1e-12, xtol=1e-13) * hi
        delta = min(M * w[-1], root)
        rec = reciprocals(delta)
        chi = 1. / rec.sum()
        lower = delta * (1 - 2 * alpha - .5 * np.sqrt(chi))
        if lower > best['length_lower']:
            best = dict(delta=float(delta), length_lower=float(lower), chi_square=float(chi),
                        support=d, probabilities=(rec / rec.sum()).tolist())
    return best


def unfold(tensor, mode):
    return np.moveaxis(tensor, mode, 0).reshape(tensor.shape[mode], -1)


def mode_apply(tensor, matrix, mode):
    moved = np.moveaxis(tensor, mode, 0)
    return np.moveaxis(np.tensordot(matrix, moved, axes=(1, 0)), 0, mode)


def project(tensor, projectors):
    result = tensor.copy()
    for k, q in enumerate(projectors):
        result = mode_apply(result, q, k)
    return result


def pilot_envelopes(shape, tau, delta):
    """Simultaneous unfolding operator-norm bounds, valid for all mean tensors."""
    size, order = int(np.prod(shape)), len(shape)
    return np.array([2 * tau * np.sqrt(2 * ((p + size // p) * np.log(9) +
                     np.log(2 * order / delta))) for p in shape])


def residual_certificate(pilot, loading, M, ranks, eta, decompositions=None):
    """Certify discarded functional bias, without a gap or true-rank assertion."""
    if decompositions is None:
        decompositions = [np.linalg.svd(unfold(pilot, k), full_matrices=True)
                          for k in range(pilot.ndim)]
    projectors, d = [], []
    for k, rank in enumerate(ranks):
        u, s, _ = decompositions[k]
        if rank < 0 or rank > pilot.shape[k]:
            raise ValueError('Invalid projection rank.')
        projectors.append(np.einsum('ij,kj->ik', u[:, :rank], u[:, :rank], optimize=False))
        # Full ambient projector discards exactly nothing, even for wide modes.
        d.append(0. if rank == pilot.shape[k] else (s[rank] if rank < len(s) else 0.) + eta[k])
    projected = project(loading, projectors)
    residual = loading - projected
    # I - product(Q_k) = sum_k product_{l<k}(Q_l) (I-Q_k).
    prefix, nuclear_bound = loading.copy(), 0.
    for k, q in enumerate(projectors):
        piece = prefix - mode_apply(prefix, q, k)
        nuclear_bound += d[k] * np.linalg.svd(unfold(piece, k), compute_uv=False).sum()
        prefix = mode_apply(prefix, q, k)
    bias = min(M * np.linalg.norm(residual), nuclear_bound)
    return projected, float(bias), dict(ranks=list(map(int, ranks)), discarded_operator_bounds=list(map(float, d)))


def unseparated_interval(pilot, validation, loading, M, tau1=1., tau2=1., alpha=.05, delta=.01):
    """Polynomial interval, honest over the entire supplied Frobenius ball.

    Pilot and validation noise must be independent iid Gaussian tensors with
    known scales. Rank candidates are selected on the pilot. Coverage does not
    imply sharp rank adaptation or weak-signal minimax length.
    """
    pilot, validation, loading = map(lambda x: np.asarray(x, float), (pilot, validation, loading))
    if pilot.ndim < 2 or pilot.shape != validation.shape or pilot.shape != loading.shape:
        raise ValueError('Require matching tensors.')
    if not all(np.isfinite(x).all() for x in (pilot, validation, loading)):
        raise ValueError('Inputs must be finite.')
    if not np.isfinite([M, tau1, tau2, alpha, delta]).all() or M <= 0 or tau1 <= 0 or tau2 <= 0 or not 0 < delta < alpha < 1:
        raise ValueError('Invalid model bounds or error budgets.')
    eta = pilot_envelopes(pilot.shape, tau1, delta)
    decompositions = [np.linalg.svd(unfold(pilot, k), full_matrices=True) for k in range(pilot.ndim)]
    ranks = {tuple(0 for _ in pilot.shape), tuple(1 for _ in pilot.shape), tuple(pilot.shape)}
    for multiplier in (.5, 1., 2.):
        ranks.add(tuple(int(np.sum(s > multiplier * eta[k])) for k, (_, s, _) in enumerate(decompositions)))
    quantile, norm_l = norm.isf((alpha - delta) / 2), np.linalg.norm(loading)
    candidates = []
    for rank in sorted(ranks):
        projected, bias, metadata = residual_certificate(pilot, loading, M, rank, eta, decompositions)
        radius = bias + quantile * tau2 * np.linalg.norm(projected)
        candidates.append((float(radius), projected, bias, metadata))
    radius, projected, bias, metadata = min(candidates, key=lambda item: item[0])
    center = float(np.sum(projected * validation))
    lo, hi = max(-M * norm_l, center - radius), min(M * norm_l, center + radius)
    if lo > hi:
        lo = hi = 0.
    return dict(lo=float(lo), hi=float(hi), width=float(hi - lo), radius=radius,
                bias=bias, projected_norm=float(np.linalg.norm(projected)), **metadata)


def cap_safe_tangent_interval(pilot, validation, loading, M, mode_caps,
                              tau1=1., tau2=1., alpha=.05, delta=.01):
    """Honest for all signals below supplied mode caps, without separation.

    The retained dimension is the supplied cap, not an estimated true rank.
    An unresolved singular value sets the angle bound to one, never to zero.
    The same second-order bias argument then remains valid for weak signals.
    """
    pilot, validation, loading = map(lambda x: np.asarray(x, float), (pilot, validation, loading))
    if pilot.ndim < 3 or pilot.shape != validation.shape or pilot.shape != loading.shape:
        raise ValueError('Require matching tensors of order at least three.')
    if not all(np.isfinite(x).all() for x in (pilot, validation, loading)):
        raise ValueError('Inputs must be finite.')
    if not np.isfinite([M, tau1, tau2, alpha, delta]).all() or M <= 0 or tau1 <= 0 or tau2 <= 0 or not 0 < delta < alpha < 1:
        raise ValueError('Invalid model bounds or error budgets.')
    if len(mode_caps) != pilot.ndim or any(int(r) != r or not 1 <= r <= p for r, p in zip(mode_caps, pilot.shape)):
        raise ValueError('Supply positive integer mode caps no larger than mode sizes.')
    eta = pilot_envelopes(pilot.shape, tau1, delta)
    projectors, errors = [], []
    for k, (p, cap) in enumerate(zip(pilot.shape, mode_caps)):
        cap = int(cap)
        u, singular, _ = np.linalg.svd(unfold(pilot, k), full_matrices=True)
        if cap == p:
            projectors.append(np.eye(p)); errors.append(0.)
            continue
        projectors.append(np.einsum('ij,kj->ik', u[:, :cap], u[:, :cap], optimize=False))
        smallest = singular[cap - 1] if cap <= len(singular) else 0.
        denominator = smallest - eta[k]
        errors.append(min(1., 2 * eta[k] / denominator) if denominator > 0 else 1.)
    joint = project(loading, projectors)
    tangent = -(pilot.ndim - 1) * joint
    for k in range(pilot.ndim):
        tangent += project(loading, [np.eye(pilot.shape[j]) if j == k else q
                                     for j, q in enumerate(projectors)])
    residual = loading - tangent
    angle = min(1., np.sqrt(sum(errors[k] ** 2 * errors[l] ** 2
                               for k in range(pilot.ndim) for l in range(k + 1, pilot.ndim))))
    bias = float(M * np.linalg.norm(residual) * angle)
    q, norm_l = norm.isf((alpha - delta) / 2), np.linalg.norm(loading)
    radii = [bias + q * tau2 * np.linalg.norm(tangent), q * tau2 * norm_l, M * norm_l]
    choice = int(np.argmin(radii))
    center = [float(np.sum(tangent * validation)), float(np.sum(loading * validation)), 0.][choice]
    lo, hi = max(-M * norm_l, center - radii[choice]), min(M * norm_l, center + radii[choice])
    if lo > hi:
        lo = hi = 0.
    return dict(lo=float(lo), hi=float(hi), width=float(hi - lo), radius=float(radii[choice]),
                bias=bias, angle_bounds=list(map(float, errors)), projected_norm=float(np.linalg.norm(tangent)),
                selected=['tangent', 'direct', 'structural'][choice], caps=list(map(int, mode_caps)))


def single_observation_interval(observation, loading, M, mode_caps, rng, tau=1., alpha=.05):
    """Original one-tensor experiment, with correctly scaled artificial split.

    A simultaneous direct interval on the original observation limits the
    length; dependence is handled by allocating alpha/2 to each interval.
    """
    observation, loading = np.asarray(observation, float), np.asarray(loading, float)
    auxiliary = tau * rng.normal(size=observation.shape)
    split = cap_safe_tangent_interval(observation + auxiliary, observation - auxiliary,
                                     loading, M, mode_caps, tau1=np.sqrt(2) * tau,
                                     tau2=np.sqrt(2) * tau, alpha=alpha / 2, delta=alpha / 8)
    center = float(np.sum(loading * observation))
    direct_radius = norm.isf(alpha / 4) * tau * np.linalg.norm(loading)
    lo, hi = max(split['lo'], center - direct_radius), min(split['hi'], center + direct_radius)
    if lo > hi:
        lo = hi = 0.
    return dict(**{k: v for k, v in split.items() if k not in ('lo', 'hi', 'width')},
                lo=float(lo), hi=float(hi), width=float(hi - lo), direct_radius=float(direct_radius))
