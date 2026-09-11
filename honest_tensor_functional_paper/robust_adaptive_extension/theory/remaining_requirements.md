# Requirements after robustness and adaptation work

This ledger supersedes the previous report for the new stage. **Resolved** means a complete supplied proof within the stated scope, not independent verification.

| Requested area | New result | Still missing |
|---|---|---|
| Efficient minimax intervals | Structural solution in the small-budget regime; direct/structural solution for a certified constant product overlap; proof that honesty on a full convex outer class loses the weak-signal improvement | Efficient minimax solution for the original high-dimensional, diffuse-loading, weak-signal class; interval-specific computational hardness |
| General loading geometry | Honest orthogonal-surrogate plus residual construction for arbitrary known loadings; prescribed block upper bounds; sharp constant-overlap regime | Sharp minimax geometry for all unequal weights or arbitrary loading tensors |
| Actual-rank adaptation | Nonzero-baseline lower bound; rank-free polynomial SVD/projection interval with a bias certificate on a separated Tucker-mode class | Uniform unseparated rank adaptation; optimal pointwise lengths; TT bond-rank selection and its optimal geometry |
| Non-Gaussian observations | Same full-scan/MSE upper rates under a joint sub-Gaussian proxy; family-wise minimax lower bounds | Universal lower bound for each fixed law (false in general); calibration from only marginal coordinate assumptions (insufficient) |
| Finite variance | Matching full-data rates over iid replicate laws with known covariance upper bound and enough replicates; directional-median excess-tail proof | Practical exact optimizer; weaker sufficient replicate counts; unknown covariance scale and dependence across replicates |
| Approximate low rank | Sharp Gaussian interval length $\min(\tau,\mathfrak r_K+\eta)$ for a supplied Frobenius allowance | New all-budget MSE result for this approximate class; data-estimated allowance |
| Growing or absent caps | Existing finite upper constants remain explicit; new rank-dependent lower bound; no-cap norm-ball rate $\min(M,\tau)$ | Matching growing-cap factors; a vanishing improvement without any rank restriction (false in general) |

## Experiment audit

The earlier report mainly checked analytic formulas. This stage runs 106 configurations with 76,600 Monte Carlo repetitions:

- 54 adaptive interval configurations, including 12 explicit violations of spectral separation; no supplied ranks passed to the algorithm.
- 36 efficient arbitrary-loading corrections, including a deliberately uncorrected comparator.
- Four complete small full-net noise-envelope experiments under Gaussian, sign, Student, and rare-outlier errors.
- 12 approximate-rank interval experiments with full-rank perturbations and an uninflated comparator.

Each result reports the appropriate error/coverage event. Exact binomial intervals are included; coverage minima are descriptive across configurations and are not simultaneous coverage certificates. A pass of a noise envelope is not reported as an experiment of the exact minimax confidence-set optimizer.

## Next work with a concrete success criterion

1. **Moderate-signal adaptive precision:** sharpen the second-order loading-specific bias bound enough to select projection before the extremely strong regime. Check valid coverage and shorter expected length over a fixed common-model grid.
2. **Weak-signal computation:** retain enough nonconvex structure to avoid the full-convex-hull lower bound while obtaining outer confidence certificates in polynomial time. Numerical convergence of an unconstrained local optimizer is insufficient.
3. **General weights:** determine when prescribed-block upper bounds match a multiscale mixture lower bound. Supply a matching expression or a demonstrated gap; do not label the current sandwich minimax.
4. **Robust optimizer:** implement certified confidence-set extrema in a small full-data problem before scaling. The current complete net implementation stops at the simultaneous noise constraints.
5. **Comparison/application:** implement a published regular-signal comparator only under compatible observations and loading assumptions; validate the actual noise/replication design of any application before claiming transfer.

Do not remove the separation, covariance, independent-replicate, or supplied-norm assumptions based on the successful simulations. The explicit counterexamples explain why several such removals are impossible.
