# Reviewer-style idea evaluation

Date: 7 September 2026  
Decision: **Accept with major revisions as a theory project; not yet submission-ready**  
Best current target: **JRSS-B or JASA Theory and Methods**

## One-line thesis

The publishable object is not “loss-aware tensor compression.” It is a sharp statistical theory for estimating and selecting one TT-compressed nonlinear conditional generator under population teacher-relative KL, with complexity determined by restricted functional information on the classical TT gauge quotient and with the teacher access model fixed explicitly.

## Five-dimension assessment

| Dimension | Score / 10 | Assessment |
|---|---:|---|
| Higher | 8 | Replaces weight reconstruction by the population conditional law that deployment actually uses; proves when the two orderings differ. |
| Faster | 5 | The statistical result supports rank selection, but it does not yet prove a faster globally convergent TT optimizer. |
| Stronger | 8 | Gives upper and lower rates, exact local constants, an access-model counterexample, and a rank-boundary impossibility result. |
| Cheaper | 7 | Identifies the query/resource frontier and supports least-cost feasible selection, conditional on stable fitting. |
| Broader | 7 | Applies to conditional generators with frozen nonlinear blocks and multiple environments; full-transformer and long-sequence extensions remain open. |

## Lifecycle and feasibility

- Current stage: theorem-complete working draft with theorem-aligned synthetic evidence.
- Remaining scientific work: sharper rank-dependent atlas constants, a global verification of the off-chart separation condition, an optimizer that provably localizes to the regular chart, and open-model falsification experiments. An independent proof audit of the present regular theorem package has been completed.
- Expected effort for a strong statistics submission: roughly 9–15 months for one theory lead plus one systems/LLM collaborator.
- Student capability match: unknown. The project needs comfort with empirical processes, Le Cam/Assouad theory, quotient manifolds, tensor networks, and LLM evaluation. This is a red flag for a solo student without an advisor who covers at least two of those areas.

## Fatal-flaw audit

| Potential fatal flaw | Status | Resolution or remaining burden |
|---|---|---|
| A universal \(d_{TT}/n\) lower bound is false after changing teacher access | Resolved in formulation | Main theorem uses finite stochastic teacher queries. White-box access gives zero risk for a feasible teacher; an identifiable logistic soft-label experiment gives a second exact-recovery counterexample. |
| Gauge dimension may exceed functional dimension | Resolved conditionally | Require restricted information on horizontal tangent; otherwise state the rate using functional rank/spectrum. |
| Tensor-network oracle inequalities already exist | Live novelty constraint | Michel–Nouy (Bernoulli 2022) is the strongest collision. Novelty must come from frozen nonlinear conditional-law geometry and the matching access-specific lower experiment. |
| Matching low-rank adaptation rates already exist | Live novelty constraint | Arunan (2026) blocks any broad “first matching low-rank neural rate” claim. |
| A fixed-stratum lower bound does not match an arbitrary pointwise oracle infimum | Resolved in claims | Prove modelwise matching and a smooth information-normal approximation shell. Keep the adaptive calculation as a separate exact Gaussian-sequence benchmark; do not claim a universal union lower bound. |
| Singular lower-rank strata destroy uniform charts | Resolved conditionally | Main theorem uses compact rank-separated strata; rank-boundary impossibility is stated separately. |
| Generic smooth \(d\)-parameter likelihood theory looks classical | Still critical | Submission must make the TT quotient entropy, nonlinear block identifiability, normal tube, and rank-stratum behavior mathematically substantive. |
| Nonconvex training may not attain the ERM | Open | Keep optimization error explicit; either certify local convergence or frame the theorem as statistical rather than computational. |
| Bounded sequence log likelihood is unrealistic | Open | Current theorem is for finite/truncated outputs. A martingale/subexponential extension would materially strengthen the paper. |
| Same-data certification is generic stability theory | Resolved in positioning | Keep as secondary and do not claim priority over LTT, Pareto Testing, PAC-Bayes, or data-reuse methods. |
| Synthetic evidence may not predict LLM behavior | Open empirical gate | Require held-out rank-order improvement on at least two open model families before a submission claims practical impact. |

## Paradigm-shift probe

The conceptual shift is from “compress a known matrix accurately” to “estimate the best resource-constrained conditional law for an unknown deployment distribution under a specified teacher-query channel.” This shift exposes three phase changes that weight approximation hides:

1. quotient dimension versus visible functional dimension;
2. stochastic-query noise versus exact-soft-label design identifiability; and
3. risk adaptation versus exact rank recovery near singular strata.

That is potentially field-shaping if the results extend beyond one artificial block. Without the nonlinear identifiability and access boundary, it collapses to a classical parametric likelihood argument.

## Venue verdict

- **JRSS-B / JASA:** plausible after sharpening the remaining TT-specific constants and completing convincing open-model falsification tests.
- **Biometrika:** plausible if the paper is shortened around the access phase change and sharp local quotient theory.
- **Annals of Statistics:** presently too application-specific. An Annals version likely needs a general theory for stratified unions of tensor-network quotient models with adaptive effective dimension.
- **ML conference:** possible with strong LLM experiments, but the present value is primarily statistical theory.

## Go/no-go gates

Proceed only if all three gates pass:

1. The restricted functional information of the chosen compressed blocks is stable and not numerically collapsed across prompt resamples.
2. Conditional-KL or Jacobian-pullback ranking improves held-out capability/risk ordering over Frobenius, spectral, activation-reconstruction, and contemporary loss-aware baselines.
3. A practical optimizer approaches the predicted approximation–estimation curve in a frozen nonlinear transformer block.

If gate 1 fails, pivot to effective-rank theory. If gate 2 fails, retain the access-model/statistical theory but drop the performance-improvement claim. If gate 3 fails, present a lower-bound/diagnostic paper rather than an algorithmic one.
