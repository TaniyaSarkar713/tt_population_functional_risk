# Adversarial review of the scientific extension

14 September 2026. Internal self-review, not an independent referee report. The preceding review and its resolutions are preserved; the full 19-item registry is continued in `issue_registry.csv`.

## T01: General efficient minimax computation

Assessment: the broad concern is still valid. The general cap-valid SVD implementation supports arbitrary tensors/loadings and TT cuts, and P4 is a constant-entry optimal pointwise procedure for a prescribed minor. Neither controls the ideal residual objective globally or attains the diffuse weak-signal minimax rate. Numerical loading envelopes are not confidence sets. The exponential binary optimizer is untouched. Status: PARTIALLY RESOLVED; the requested general algorithm remains a SUBMISSION RISK for any broad computational claim.

## T02: Intermediate caps

Assessment: D2's exact-diagonal assumption is stronger than low tensor rank. Its rate follows classical sparse Gaussian functional theory and is not advertised as a new sparse minimax theorem. Its finite-sample interval is implemented with explicit bias and variance bounds. Deliberate application to the diagonal of a dense rank-one tensor has zero coverage, confirming why it cannot fill the general gap. Status: PARTIALLY RESOLVED; the general intermediate-cap problem remains FUTURE WORK for a focused paper and a SUBMISSION RISK for the broad goals.

## T03: Arbitrary loading profiles

Assessment: AB1 genuinely uses every orthogonal weight and all budgets. The proof explicitly absorbs dimension-dependent confidence allocation into prefix thresholds, preventing a hidden extra logarithm. Its Abel ratio inequality is deterministic, while statistical constants still depend on fixed caps/order. AB2 checks all three cubic budget branches and excludes critical exponents. Lower mixtures remain full-data alternatives with controlled norm/ranks after signed contraction. The calculation is an advance over fixed-power decay, but exact arbitrary profiles and nonorthogonal loading tensors remain open. Status: PARTIALLY RESOLVED. Independent proof/priority assessment is a REMAINING SUBMISSION TASK.

## T04/F04: Pointwise inference and scalar risk

Assessment: P2 must use the pre-intersection center. Its broad direct guard bounds losses on bad pilot events without assuming independence between the pilot and original direct scalar. Its smaller pilot error budget makes those losses negligible at the intended scale. P3's TT lower perturbation preserves all bond dimensions through a bridge matrix, not just one unfolding rank. Its Tucker projector is correctly described as the first-order product-space projector rather than the exact rank-r tangent. Pointwise minimax squared risk without a neighborhood would be zero; the local two-point lower criterion is stated explicitly. P4 separately supplies second-order length at a zero-tangent point with a safe denominator fallback and a matching rotated alternative. Its general ratio idea is classical; the claimed advance is the restricted tensor consequence.

Remaining limitations: strong/aligned saturated points in P3, one prespecified axis/minor family in P4, conservative signal conditions, arbitrary weak/undersaturated/higher-order geometry and unknown favorable minor selection. The scalar theorem is not asserted for P4's empty-intersection midpoint. Status: F04 RESOLVED with a new stronger extension; T04 PARTIALLY RESOLVED. Full pointwise claims would be a SUBMISSION RISK.

## D01/T05: Real-data analysis and calibration

Assessment: real analysis was executed, not postponed for an unspecified dataset. Protocol and target were fixed before raw observations were downloaded. The explicit sampling-model amendment preceded contrast computation and reflects separately recruited groups, not observed effect size. All 122 subjects are retained; within-person trials are not independent sampling units. The target is a clipped, quality-filtered recorded response at fixed channels/sample indices, not an unclipped latent response or clinical effect. Exact population rank is never asserted from a fitted pilot. B1/B1a calibrates the signed projection residual independently and keeps the wide interval.

Remaining limitations: the archive does not establish family-level independence or representative sampling; case/control mixture weights describe this study, not disease prevalence. Error/missing trials may be informative for latent responses, which are not the target. The approximate t interval excludes zero, but the finite-sample interval does not. The tensor correction spans the full target range and gives no precision advantage. Status: D01 PARTIALLY RESOLVED as an original-model application requirement; the bounded-data execution itself is complete. Independence/selection and lack of model-specific validation are explicit SUBMISSION RISKS for a strong application claim, acceptable limitations for a cautious demonstration.

## Simulation and implementation audit

The main design includes zero, weak, strong and undersaturated tensors, new dense TT core/loading geometry, all-cap exact-diagonal cases, deliberate model violation, bounded projection-bias correction and rank-one minor scaling. All methods retain the same known noise calibration and supplied caps within their stated Gaussian scenarios. Direct scalar rows use their own Gaussian intervals; an initial summary attachment error was corrected from saved direct errors before reporting, with generator correction recorded. Other scalar ablations share the proposed interval and new calibration; they are not exact historical R1 reruns. Rare midpoint losses, empty intervals and wide finite-sample bounds remain visible.

Coverage screening is reported with binomial uncertainty and family multiplicity; a non-rejection is not proof. Curves show proxy calculations or finite observations as labeled. The main grid intentionally uses sufficient, very strong signals and does not discover an optimal transition. The new work reuses existing sparse and empirical Bernstein theory with attribution. Primary references are linked; an exhaustive literature/priority search has not been performed.

## Presentation and preservation audit

The report and technical supplement are separate from the prior submission, so new theorems do not silently alter the previous 59-result dependency chain. Root README and requirements identify the current stage, new versus saved checks, file organization and outstanding science. A float/long-table interaction initially clipped one plot in the report; the report now places complete vector figures and their captions on dedicated pages. Horizontal and vertical page bounds, figure vector content and readable previews are checked in final validation. The 2,733-file starting baseline is compared by hash; only the authorized root status documents should differ.

## Final readiness assessment

Correctness: supplied derivations are internally checked and no known unresolved proof step is labeled PROVED. Proof completeness: seven result groups and the fixed-stratum corollary have explicit arguments, with the original flat-loading theorem as a named dependency. Assumptions and limitations: explicit. Simulations: new methods and negative boundaries tested, but no general minimax optimizer run exists. Empirical fairness: direct baselines and different sampling assumptions labeled. Real-data validity: conditional on the stated subject sampling model; no verified family independence or Gaussian low-rank population assertion. Reproducibility: source, configurations, individual outcomes, data transformation, provenance and rebuild commands retained.

Verdict **C: additional scientific work required for the expanded goals**. The main progress is mathematical and implemented, but does not resolve all four broad open theory problems or establish a precision-gaining original-model application. The preceding focused manuscript's B assessment is preserved as an assessment of that narrower contribution. No new fundamental identifiability contradiction was found; there is no reason to abandon the research direction. Independent proof review and novelty/priority assessment remain necessary before selecting a final submission scope.
