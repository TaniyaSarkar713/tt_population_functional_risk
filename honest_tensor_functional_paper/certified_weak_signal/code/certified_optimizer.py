"""Global residual optimization on the complete 2 x ... x 2 rank-one ball.

The domain is continuous, not a finite list of candidate means. Branch bounds
cover every factor angle and signed amplitude. Every scan support is included.
Complexity is exponential. Returned certificates use ordinary double precision
with conservative guards, not formally verified interval arithmetic.
"""
import heapq
import itertools
import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize


def cos_bounds(lo, hi):
    lo, hi = np.asarray(lo), np.asarray(hi)
    lower, upper = np.minimum(np.cos(lo), np.cos(hi)), np.maximum(np.cos(lo), np.cos(hi))
    upper = np.where(np.ceil(lo / (2 * np.pi)) <= np.floor(hi / (2 * np.pi)), 1., upper)
    lower = np.where(np.ceil((lo - np.pi) / (2 * np.pi)) <= np.floor((hi - np.pi) / (2 * np.pi)), -1., lower)
    return lower, upper


def multiply_bounds(al, ah, bl, bh):
    values = np.array([al * bl, al * bh, ah * bl, ah * bh])
    return values.min(axis=0), values.max(axis=0)


def rank_one(parameters):
    tensor = np.asarray(parameters[0])
    for angle in parameters[1:]:
        tensor = np.multiply.outer(tensor, [np.cos(angle), np.sin(angle)])
    return tensor


@dataclass
class Cell:
    lower: np.ndarray
    upper: np.ndarray
    residual_lower: float
    target_lower: float
    target_upper: float


class BinaryRankOneOptimizer:
    """Full residual criterion, arbitrary loading, known Gaussian noise.

    Tucker/TT caps must all equal one. Only mode size two is implemented.
    The projective circle net has mesh at most 1/(2K); antipodal product
    directions are redundant because scan contractions are absolute values.
    """

    def __init__(self, observation, loading, M, tau=1., alpha=.05):
        z, loading = np.asarray(observation, float), np.asarray(loading, float)
        if z.ndim < 3 or z.shape != (2,) * z.ndim or loading.shape != z.shape:
            raise ValueError('Require matching binary tensors of order at least three.')
        if not np.isfinite(z).all() or not np.isfinite(loading).all():
            raise ValueError('Inputs must be finite.')
        if not np.isfinite([M, tau, alpha]).all() or M <= 0 or tau <= 0 or not 0 < alpha < 1:
            raise ValueError('Require finite M,tau > 0 and 0 < alpha < 1.')
        self.K, self.M, self.tau, self.alpha = z.ndim, float(M), float(tau), float(alpha)
        self.z, self.loading = z, loading
        count = math.ceil(np.pi * self.K)
        self.angles = np.vstack([np.zeros((1, self.K)), np.full((1, self.K), np.pi / 2),
                                np.array(list(itertools.product(np.pi * np.arange(count) / count,
                                                                repeat=self.K)))])
        self.levels = np.r_[np.ones(2, dtype=int), np.full(count ** self.K, 2, dtype=int)]
        self.directions = np.array([rank_one(np.r_[1., a]).ravel() for a in self.angles])
        counts = {1: 2, 2: count ** self.K}
        self.thresholds = np.array([tau * np.sqrt(2 * np.log(4 * counts[s] / alpha))
                                    for s in self.levels])
        self.y = np.einsum('ij,j->i', self.directions, z.ravel(), optimize=False)
        self.guard = 1e-10 * (1 + M + np.linalg.norm(z) + np.linalg.norm(loading) * M)
        self.best_parameters = np.zeros(self.K + 1)
        self.best_residual = self.objective(self.best_parameters)
        self.inner_lower, self.inner_upper = math.inf, -math.inf
        self.evaluations = 0

    def objective(self, parameters):
        amplitudes = parameters[0] * np.prod(np.cos(parameters[1:] - self.angles), axis=1)
        return float(max(0., np.max(np.abs(self.y - amplitudes) - self.thresholds)))

    def _witness(self, parameters):
        value = self.objective(parameters)
        if value < self.best_residual:
            self.best_residual, self.best_parameters = value, parameters.copy()
        # Never expand feasibility by a positive numerical tolerance.
        if value == 0.:
            target = float(np.sum(rank_one(parameters) * self.loading))
            self.inner_lower, self.inner_upper = min(self.inner_lower, target), max(self.inner_upper, target)

    def seed(self, local=True):
        """Feasible witnesses accelerate the search; they never supply a lower bound."""
        starts = []
        for angles in itertools.product((0., np.pi / 4, np.pi / 2), repeat=self.K):
            unit = rank_one(np.r_[1., angles])
            amplitude = np.clip(np.sum(self.z * unit), -self.M, self.M)
            parameters = np.r_[amplitude, angles]
            self._witness(parameters)
            self._amplitude_witnesses(np.asarray(angles))
            starts.append((self.objective(parameters), parameters))
        self._witness(np.zeros(self.K + 1))
        if local and self.best_residual > 0:
            for _, parameters in sorted(starts, key=lambda item: item[0])[:3]:
                result = minimize(self.objective, parameters, method='Powell',
                                  bounds=[(-self.M, self.M)] + [(0., np.pi)] * self.K,
                                  options={'maxiter': 150, 'xtol': 1e-8, 'ftol': 1e-9})
                self._witness(result.x)

    def _amplitude_witnesses(self, angles):
        """Exact linear feasibility along fixed factors, useful for endpoint witnesses."""
        products = np.prod(np.cos(angles - self.angles), axis=1)
        lower, upper = -self.M, self.M
        active = np.abs(products) > 1e-14
        # Tiny contractions are checked again by _witness, never accepted on faith.
        if np.any(np.abs(self.y[~active]) > self.thresholds[~active]):
            return
        left = (self.y[active] - self.thresholds[active]) / products[active]
        right = (self.y[active] + self.thresholds[active]) / products[active]
        lower, upper = max(lower, np.minimum(left, right).max()), min(upper, np.maximum(left, right).min())
        if lower <= upper:
            for amplitude in (lower, (lower + upper) / 2, upper):
                self._witness(np.r_[amplitude, angles])

    def cell(self, lower, upper, endpoints=False):
        center = (lower + upper) / 2
        self._witness(center)
        if endpoints:
            self._amplitude_witnesses(center[1:])
        pl, ph = np.ones(len(self.y)), np.ones(len(self.y))
        for k in range(self.K):
            dl, dh = cos_bounds(lower[k + 1] - self.angles[:, k], upper[k + 1] - self.angles[:, k])
            pl, ph = multiply_bounds(pl, ph, dl, dh)
        pl, ph = multiply_bounds(pl, ph, lower[0], upper[0])
        distance = np.maximum(np.maximum(pl - self.y, self.y - ph), 0.)
        residual_lower = max(0., float(np.max(distance - self.thresholds)) - self.guard)

        # Tensor-entry interval arithmetic supplies arbitrary-loading bounds.
        tl, th = np.asarray(lower[0]), np.asarray(upper[0])
        for k in range(self.K):
            cl, ch = cos_bounds(lower[k + 1], upper[k + 1])
            sl, sh = cos_bounds(lower[k + 1] - np.pi / 2, upper[k + 1] - np.pi / 2)
            tl, th = multiply_bounds(tl[..., None], th[..., None], np.array([cl, sl]), np.array([ch, sh]))
        target_lower = np.minimum(self.loading * tl, self.loading * th).sum()
        target_upper = np.maximum(self.loading * tl, self.loading * th).sum()
        # Intersect with the center Lipschitz bound and the norm-only bound.
        target = float(np.sum(rank_one(center) * self.loading))
        radius = min(2 * self.M, (upper[0] - lower[0]) / 2 +
                     self.M * np.sum(upper[1:] - lower[1:]) / 2)
        norm_l = np.linalg.norm(self.loading)
        target_lower = max(target_lower, target - radius * norm_l, -self.M * norm_l) - self.guard
        target_upper = min(target_upper, target + radius * norm_l, self.M * norm_l) + self.guard
        self.evaluations += 1
        return Cell(lower, upper, residual_lower, float(target_lower), float(target_upper))

    def root(self, endpoints=False):
        return self.cell(np.r_[-self.M, np.zeros(self.K)],
                         np.r_[self.M, np.full(self.K, np.pi)], endpoints)

    def split(self, cell, endpoints=False):
        widths = (cell.upper - cell.lower) * np.r_[1., np.full(self.K, self.M)]
        k = int(np.argmax(widths))
        mid = (cell.lower[k] + cell.upper[k]) / 2
        upper, lower = cell.upper.copy(), cell.lower.copy()
        upper[k], lower[k] = mid, mid
        return self.cell(cell.lower.copy(), upper, endpoints), self.cell(lower, cell.upper.copy(), endpoints)

    def minimize_residual(self, tolerance=.1, max_nodes=10000):
        """Return a rank-one incumbent and a global absolute optimality gap."""
        if tolerance <= 0 or max_nodes < 1:
            raise ValueError('Require a positive tolerance and node budget.')
        self.seed()
        root = self.root()
        queue, serial = [(root.residual_lower, 0, root)], 0
        processed = 0
        while queue and processed < max_nodes:
            global_lower = min(self.best_residual, queue[0][0])
            if self.best_residual - global_lower <= tolerance:
                break
            _, _, cell = heapq.heappop(queue)
            if cell.residual_lower >= self.best_residual:
                continue
            for child in self.split(cell):
                if child.residual_lower < self.best_residual:
                    serial += 1
                    heapq.heappush(queue, (child.residual_lower, serial, child))
            processed += 1
        lower = min(self.best_residual, queue[0][0]) if queue else self.best_residual
        return dict(lower=float(lower), upper=float(self.best_residual), gap=float(self.best_residual - lower),
                    certified_to_tolerance=bool(self.best_residual - lower <= tolerance),
                    parameters=self.best_parameters.tolist(), nodes=processed, active_cells=len(queue),
                    scan_directions=len(self.y), tolerance=tolerance,
                    arithmetic='float64 with conservative guards; not formal interval arithmetic')

    def project_interval(self, tolerance=.1, max_nodes=10000):
        """Outer endpoints contain the ideal confidence-set projection at any stop.

        Inner endpoints are actual feasible witnesses. A budget stop is explicit;
        an unresolved gap never licenses reporting inner endpoints as an interval.
        """
        if tolerance <= 0 or max_nodes < 1:
            raise ValueError('Require a positive tolerance and node budget.')
        self.seed(local=False)
        root = self.root(endpoints=True)
        queue, serial, terminal = [], 0, []

        def priority(cell):
            return max(self.inner_lower - cell.target_lower, cell.target_upper - self.inner_upper)

        if root.residual_lower <= 0:
            heapq.heappush(queue, (-priority(root), serial, root))
        processed = 0
        while queue and processed < max_nodes:
            _, _, cell = heapq.heappop(queue)
            if priority(cell) <= tolerance:
                terminal.append(cell)
                continue
            for child in self.split(cell, endpoints=True):
                if child.residual_lower <= 0:
                    serial += 1
                    heapq.heappush(queue, (-priority(child), serial, child))
            processed += 1
        retained = terminal + [entry[2] for entry in queue]
        empty = not retained and not np.isfinite(self.inner_lower)
        if empty:
            return dict(lo=0., hi=0., empty_certified=True, certified_to_tolerance=True,
                        endpoint_gap=0., nodes=processed, active_cells=0, scan_directions=len(self.y))
        lo = min([c.target_lower for c in retained] + [self.inner_lower])
        hi = max([c.target_upper for c in retained] + [self.inner_upper])
        gap = max(self.inner_lower - lo, hi - self.inner_upper)
        return dict(lo=float(lo), hi=float(hi), inner_lo=float(self.inner_lower) if np.isfinite(self.inner_lower) else None,
                    inner_hi=float(self.inner_upper) if np.isfinite(self.inner_upper) else None,
                    empty_certified=False, endpoint_gap=float(gap) if np.isfinite(gap) else None,
                    certified_to_tolerance=bool(gap <= tolerance), nodes=processed,
                    active_cells=len(queue), scan_directions=len(self.y),
                    arithmetic='float64 with conservative guards; not formal interval arithmetic')
