# Internal proof audit

The stage supplies six theorems and four propositions with ten complete proofs in [the appendix](../paper/robust_adaptive_proofs.tex). This audit identifies potential failure points; it is not independent mathematical review.

| Potential error | Resolution or remaining scope |
|---|---|
| Transfer Gaussian lower bounds to every sub-Gaussian law | Lower bounds are for the unknown-law family containing Gaussian noise. A scalar Rademacher counterexample disproves a universal per-law transfer. |
| Use coordinatewise tails for dense product contractions | Require a joint directional proxy or a covariance operator bound for replicates. A shared-sign tensor disproves marginal sufficiency. |
| Treat medians as a linear tensor estimate | Each direction has its own median. Confidence constraints and feasible differences do not require one representing tensor. |
| Ignore exponential net cardinality in robust calibration | Block counts contain the logarithm of every support/direction count and a level allocation. Full scans require the stated replicate budget. |
| Infer squared risk from fixed-probability median coverage | Prove the common polynomial excess tail and integrate it: the normalized second-moment constant is $72\beta/7$. |
| Confuse within-replicate dependence with across-replicate dependence | Covariance control allows the former; independent blocks require the latter to be absent. |
| Use same-data rank selection without a joint event | All unfolding ranks are recovered on one simultaneous operator-norm event, only on the stated separated class. |
| Ignore projection bias | The interval includes a second-order certificate from observed singular values; a direct fallback is selected from the pilot alone. |
| Bound the sum of mixed tensor projections incorrectly | Mutually orthogonal products yield the pairwise squared residual bound; each discarded component appears in at least one pair. |
| Identify the product-space projector with the exact Tucker tangent projector | The new projector is explicitly defined and can be larger at ranks above one; no exact manifold efficiency is claimed. |
| Infer Gaussian independence merely from uncorrelated artificial splits | The artificial splitting claim is restricted to jointly Gaussian noise. Independent replicate groups are required otherwise. |
| Claim rank recovery implies efficient precision | Experiments show otherwise: the certificate is conservative and selects the direct interval at moderate signal strength. |
| Extend separated coverage to weak extra components | Twelve deliberate violations give zero coverage. A shifted-mixture lower bound supplies a separate mathematical obstruction. |
| Call mode ranks TT bond ranks | The positive adaptive result concerns Tucker mode ranks. Its use on TT tensors still requires those mode-gap conditions. |
| Lose the norm budget under a shifted lower prior | Disjoint tensor blocks make Frobenius squares additive; use the exact remaining budget $\sqrt{M^2-\|A_0\|_F^2}$. |
| Interpret convex-hull failure as all-algorithm hardness | The lower bound requires honesty on the entire larger convex parameter class. Convex subroutines within other procedures are not ruled out. |
| Drop arbitrary loading residuals | Observe their contraction and add a separately calibrated noise radius; use a union bound, not an independence assertion. |
| Reuse fixed-cap asymptotics for growing or unknown caps | Finite upper constants remain explicit; a new rank-dependent lower bound and the no-cap endpoint delimit the relaxation. |
| Claim approximate-rank risk from interval length alone | The new approximation result asserts sharp expected length only. |

## Verification evidence

Saved checks independently examine projection idempotence/self-adjointness, second-order bias bounds, median-tail comparisons and integration, exact growing-rank mixture second moments, and shifted norms/ranks/targets. Random finite checks cannot prove universal statements. Prior-stage hashes are verified; that stage is not modified.

The original tensor expansion, full scan, and harmonic mixture remain dependencies. The source contains their proofs, but they still warrant external review. The new arguments use elementary Gaussian likelihoods, directional concentration, Chebyshev/binomial bounds, singular-value variational bounds, and orthogonal projection identities. Broad novelty is not claimed for median-of-means, subspace projection, common-target testing, or confidence-set inversion.
