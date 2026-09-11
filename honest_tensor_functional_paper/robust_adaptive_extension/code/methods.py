"""Finite-sample interval implementations; no exhaustive minimax optimizer."""
import itertools
import math

import numpy as np
from scipy.stats import norm


def inner(a, b):
    return float(np.sum(a * b))


def mode_apply(a, matrix, mode):
    moved = np.moveaxis(a, mode, 0)
    out = np.einsum('ij,j...->i...', matrix, moved, optimize=False)
    return np.moveaxis(out, 0, mode)


def project_modes(a, projectors, omit=None):
    for k, projector in enumerate(projectors):
        if k != omit:
            a = mode_apply(a, projector, k)
    return a


def tangent_loading(loading, projectors):
    joint = project_modes(loading, projectors)
    return sum(project_modes(loading, projectors, omit=k)
               for k in range(loading.ndim)) - (loading.ndim - 1) * joint


def pilot_envelope(shape, v=1.0, delta=0.01):
    dimension = math.prod(shape)
    return np.array([2 * v * np.sqrt(2 * ((p + dimension // p) * np.log(9)
                     + np.log(2 * len(shape) / delta))) for p in shape])


def adaptive_interval(pilot, second, loading, M, v1=1.0, v2=1.0,
                      alpha=0.05, delta=0.01, gaussian=True):
    """Honest only on the mode-gap class sigma_min > 2 * pilot_envelope.

    Requires independent pilot/second errors; Gaussian artificial splitting
    is valid with the increased noise scales. Rank caps are not inputs.
    """
    eta = pilot_envelope(pilot.shape, v1, delta)
    projectors, ranks, errors = [], [], []
    for k, p in enumerate(pilot.shape):
        matrix = np.moveaxis(pilot, k, 0).reshape(p, -1)
        u, singular, _ = np.linalg.svd(matrix, full_matrices=False)
        rank = int(np.sum(singular > eta[k]))
        ranks.append(rank)
        if rank:
            projectors.append(np.einsum('ij,kj->ik', u[:, :rank], u[:, :rank], optimize=False))
            errors.append(min(1.0, 2 * eta[k] / (singular[rank - 1] - eta[k])))
    if min(ranks) == 0:
        return dict(lo=0.0, hi=0.0, width=0.0, ranks=ranks, bias=0.0,
                    tangent_norm=0.0, selected='zero', center=0.0)
    tangent = tangent_loading(loading, projectors)
    remainder = loading - tangent
    error2 = sum((errors[k] * errors[l]) ** 2
                 for k in range(len(errors)) for l in range(k + 1, len(errors)))
    bias = M * np.linalg.norm(remainder) * min(1.0, np.sqrt(error2))
    q = norm.ppf(1 - (alpha - delta) / 2) if gaussian else np.sqrt(2 * np.log(2 / (alpha - delta)))
    norm_l, norm_t = np.linalg.norm(loading), np.linalg.norm(tangent)
    radii = [bias + q * v2 * norm_t, q * v2 * norm_l, M * norm_l]
    selected = int(np.argmin(radii))
    center = [inner(tangent, second), inner(loading, second), 0.0][selected]
    lo = max(center - radii[selected], -M * norm_l)
    hi = min(center + radii[selected], M * norm_l)
    if lo > hi:
        lo = hi = 0.0
    return dict(lo=float(lo), hi=float(hi), width=float(hi - lo), ranks=ranks,
                bias=float(bias), tangent_norm=float(norm_t),
                selected=['projected', 'direct', 'structural'][selected], center=center)


def surrogate_interval(diagonal, off_entry, M, epsilon, K=4, alpha=0.05,
                       gaussian=True):
    """Rank-one class; L = sqrt(1-eps^2) L_flat + eps U_off.

    U_off is a known off-diagonal unit product atom. No full tensor is needed
    after these contractions have been obtained. Selection is deterministic.
    """
    p = len(diagonal)
    a = np.sqrt(1 - epsilon ** 2)
    lam = np.sqrt(2 * np.log(4 * p / alpha))
    q_res = norm.ppf(1 - alpha / 4) if gaussian else np.sqrt(2 * np.log(4 / alpha))
    q_dir = norm.ppf(1 - alpha / 2) if gaussian else np.sqrt(2 * np.log(2 / alpha))
    radius_nl = M ** (2 / K) * (2 * lam) ** (1 - 2 / K) / np.sqrt(p)
    center_nl = np.sum(np.sign(diagonal) * np.maximum(np.abs(diagonal) - lam, 0)) / np.sqrt(p)
    norm_bound = min(M, M * (a / np.sqrt(p) + epsilon))
    radii = [a * radius_nl + epsilon * q_res, q_dir, norm_bound]
    centers = [a * center_nl + epsilon * off_entry,
               a * np.sum(diagonal) / np.sqrt(p) + epsilon * off_entry, 0.0]
    choice = int(np.argmin(radii))
    return centers[choice], radii[choice], a * center_nl, a * radius_nl, choice


def small_full_nets(K=3):
    """Complete sphere-net support scan for p=2 (all support levels)."""
    shape = (2,) * K
    singletons = np.zeros((2, 2 ** K))
    singletons[0, 0] = singletons[1, -1] = 1
    count = int(np.ceil(2 * np.pi * K))
    angle = 2 * np.pi * np.arange(count) / count
    circle = np.stack([np.cos(angle), np.sin(angle)], axis=1)
    directions = []
    for indices in itertools.product(range(count), repeat=K):
        a = circle[indices[0]]
        for i in indices[1:]:
            a = np.multiply.outer(a, circle[i])
        directions.append(a.ravel())
    return {1: singletons, 2: np.asarray(directions)}, shape


def mom_parameters(counts, n, sigma=1.0, beta=0.05):
    parameters = {}
    levels = len(counts)
    for s, count in counts.items():
        b = int(np.ceil(max(9, np.log(count * levels / beta) / np.log(2))))
        b += (b % 2 == 0)
        if n < 2 * b:
            raise ValueError('Insufficient independent replicates for all requested directions')
        k = n // b
        parameters[s] = dict(b=b, k=k, threshold=4 * sigma / np.sqrt(k))
    return parameters


def robust_scan_errors(replicates, nets, parameters):
    """Return full-net median and Gaussian sample-mean envelope diagnostics."""
    flat = replicates.reshape(len(replicates), -1)
    mean = np.mean(flat, axis=0)
    max_excess, gaussian_pass, ratio = 0.0, True, 0.0
    for s, directions in nets.items():
        cfg = parameters[s]
        blocks = flat[:cfg['b'] * cfg['k']].reshape(cfg['b'], cfg['k'], -1).mean(axis=1)
        values = np.einsum('bd,ud->bu', blocks, directions, optimize=False)
        medians = np.median(values, axis=0)
        maximum = float(np.max(np.abs(medians)))
        max_excess = max(max_excess, maximum - cfg['threshold'])
        ratio = max(ratio, maximum / cfg['threshold'])
        sample_means = np.einsum('d,ud->u', mean, directions, optimize=False)
        bound = np.sqrt(2 * np.log(2 * len(directions) * len(nets) / 0.05) / len(flat))
        gaussian_pass &= bool(np.max(np.abs(sample_means)) <= bound)
    return dict(excess=max_excess, robust_pass=max_excess == 0.0,
                gaussian_pass=gaussian_pass, threshold_ratio=ratio)
