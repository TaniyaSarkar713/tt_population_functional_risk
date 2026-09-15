# Scientific dependency and assumption audit

The complete prior review and its eight component documents were read before revisions; `logs/review_read_manifest.json` records them. The prior 59-result audit found no central theorem counterexample or missing essential proof step. This revision preserves those 59 statements/rates and assembles their full supplied derivations in one technical supplement. R1 is new and PROVED by the pathwise argument in `scalar_companion.md`. “PROVED” is an internal checked-proof status, not formal verification or external review.

## Dependency chains checked after revision

| Main claim | Assumptions → mechanism → result | Revision assessment |
|---|---|---|
| Fixed-cap all-budget length | Known isotropic Gaussian scale, fixed order/caps, flat loading → canonical expansion and doubled caps → norm and scan bounds on each ordered coordinate → cubic split harmonic sum / higher-order summability | No rate change. Preserve the inner minimum before summation. Lower bound is under the full tensor likelihood, not the diagonal marginal. |
| All-budget squared risk | Same class → approximate residual fit with deterministic noise-scale tolerance → excess-tail control and integration | No rate change. Do not replace this estimator by a fixed-confidence midpoint. |
| Growing-cap G1 | Minimum constrained cap at least c sqrt(p) → sparse diagonal mixture with overlap H → structural/direct matching | Constants are uniform in ranks here, not in the fixed-cap theorem. No claim that intermediate caps match. |
| Fixed-decay W2 | Fixed beta>0, fixed caps → dyadic block fits and summable weight envelope → largest-atom lower bound | Constants diverge as beta decreases to zero; ideal fits remain unimplemented generally. |
| Adaptation A1/G2 | Fixed positive caps versus growing outer class → same fixed-cap order / growing-class lower bound at shared zero | No contradiction: the fixed-cap constants are not rank-uniform. A universal positive growing-cap adaptation claim would be false. |
| Strong pointwise P1 | Saturated diagonal Tucker mean, a large relative to eta and eta² sqrt(p)/tau, norm comparability → pilot angles and second-order bias → length bound plus delta=alpha r/(8p) failure term | Length theorem unchanged. Explicit conditions remain in the main theorem. Not a TT or general nonsaturated result. |
| R1 | Known scalar Gaussian noise scale, supplied valid structural range, intersection with direct and structural intervals → pathwise error at most tau|g|+d → unconditional risk bound | New scalar output and proof. No extra signal assumption. Does not upgrade P1 to pointwise minimax MSE. |
| Whole-replicate corruption | Independent clean replicates, known marginal contraction variance, known c, enough blocks and n → Chebyshev plus bounded corrupted-block count → median envelope | Directly tested in V03, including correlated coordinates and t3. Deliberate cap violation fails. No sharp contamination-minimax conclusion. |
| Independent scale calibration | Gaussian full replicates, orthogonal prescribed contractions, n≥2 → independent mean and residual chi-square → conditional selection plus delta | Directly tested in V04, including small degrees of freedom. No same-data general-noise plug-in theorem. |

## Restrictive assumptions investigated rather than hidden

1. **Identifiability.** In the full Gaussian location experiment, equal laws imply equal means, and hence equal linear targets. Factor equivalence does not change this target. No new factor-identification condition is needed.
2. **Known norm/caps.** The structural and bias radii use these supplied bounds. V01 now holds M fixed while changing the signal and compares on the same draws with the norm-comparable branch. A larger M can retain honesty but worsen length. An underestimated cap or structural range invalidates the supplied-class guarantee; such cases are flagged, not used as evidence against R1.
3. **Gaussianity.** It supplies the exact likelihood identity and artificial-split independence. Joint sub-Gaussian envelopes can replace it for some upper bounds. Marginal sub-Gaussianity cannot calibrate the full scan. Gaussian lower bounds transfer to a family containing Gaussians, not automatically to every individual non-Gaussian law.
4. **Independent replicates.** Required for block concentration and chi-square residual separation. Perfectly dependent repeats need not reduce uncertainty with n. No arbitrary-dependence extension is asserted. Existing counterexamples are retained in the supplement.
5. **Loading structure.** Orthogonal loading factors support independent contractions and block reductions. L1 treats arbitrary loading in small budgets; W2 allows the stated residual perturbation. Neither removes the general large-budget geometry or computational problem.
6. **Pointwise saturation, signal and norm comparability.** Saturation excludes unused weak rank in the coordinate family; signal controls pilot angles; norm comparability turns M times the second-order angle term into the pointwise scale. Dropping all three and preserving the same local rate is contradicted by shifted weak-component mixtures. The conservative sufficient SNR is not shown necessary.
7. **Unknown noise scale.** The finite Gaussian replicate refinement is available and now tested. For general unknown directional scales or selected loadings, the relevant simultaneous or independent calibration is still missing. Replacing these assumptions by a naive plug-in is empirically invalid in the small-n Gaussian check.

## Open-problem investigations and precise stopping points

**T01, general computation.** The ideal confidence projection has exponentially many support/net constraints and a nonconvex fit. C1 requires feasible candidates and a global objective certificate; a small local gradient or favorable local optimizer value does not establish that contract. Holding all other quantities fixed in V02 gives seven successful endpoint certificates out of 600 and retains 593 unresolved searches. The tested binary model cannot resolve the general high-dimensional problem. Low-degree polynomial risk separation is a restricted result; a general efficient-testing obstruction still needs an explicit hypothesis and reduction.

**T02, intermediate caps.** Re-examining the existing sparse mixture yields the all-r lower scale

$$\min\{M\sqrt{r/p},\tau r p^{-1/2}\sqrt{\log(1+p/(4r^2))}\}.$$

The structural/direct upper scale is $\min\{M\sqrt{r/p},\tau\}$. They match at $r\gtrsim\sqrt p$ but can be widely separated below it. Fixed-cap residual constants depend polynomially on canonical rank complexity and cannot be silently treated as uniform. The preserved intermediate-cap grid reports the actual bracket; fitting simulated coverage would not prove a missing lower or upper rate. No new matching theorem is asserted.

**T03, arbitrary profiles.** The dyadic upper functional $\sum_j a_j(j+1)^{\nu_K}$ is sufficient for fixed decay, while largest-atom and flat-block alternatives provide lower bounds. For slowly varying or dimension-dependent profiles these are not equivalent in general. Summing separate block risks via Minkowski may be loose, and a general matching mixture must respect the common global norm budget and full tensor likelihood. Neither a numerical envelope evaluation nor a binary loading study settles this issue.

**T04, complete pointwise theory.** The support-oracle direction supplies the P1 lower scale under norm slack; the upper bound uses saturation and strong pilot accuracy. R1 corrects a different issue, unconditional scalar risk. It has order min(h²,tau²), which can exceed tau² r/p. Thus it does not close pointwise minimax squared risk, characterize all geometries or prove optimal SNR. G2 already rules out a blanket adaptation claim on its growing outer classes.

**T05, broader robustness.** Available independent-scale and bounded-row refinements are implemented and tested. Unknown arbitrary covariance, dependence across replicates, selected loadings, and estimated approximation allowances require new calibration or a different experiment. These remain explicit future work rather than unsupported generalizations.

## Propagation check

The rate in the abstract, main Theorem 1, analytic Figure 1, interpretation and discussion is the all-budget rate. The squared-risk theorem refers to residual fitting; the public scalar method refers only to R1. P1 continues to be a length theorem. Historical intermediate rates are technical ingredients in the supplement. Every affected saved interval case was reevaluated, all corrected tables and ten archived-study figures regenerated, and six new figures generated from checked data or explicitly labeled analytic formulas. Neither old experiments nor the prior review are overwritten.
