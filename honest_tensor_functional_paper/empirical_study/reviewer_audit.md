# Empirical reviewer audit

This audit distinguishes completed simulation evidence from requirements that cannot be settled by the experiments. Final counts and numerical findings are in `report.md` and `results/analysis_audit.json`.

## Major scientific limitations

1. **General minimax computation is still unavailable.** The full high-dimensional residual/block optimizer is not implemented. The binary continuous rank-one optimizer is exponential and has recorded endpoint gaps. Diagonal thresholding, analytic envelopes, solver successes at mode size two and runtime slopes do not replace the missing algorithm.
2. **The pointwise positive regime is deliberately extreme.** Strong saturated diagonal means test the actual P1 sufficient condition; they do not show practical weak-signal efficiency or optimal signal thresholds. The logarithmic signal sweep, unsaturated caps, rotated factors and weak extra components are essential negative/contextual comparisons. The regular-signal comparator and oracle can be much shorter.
3. **Pointwise interval midpoints are not risk-certified estimators.** The preserved `{0}` replacement for empty interval intersections causes large squared errors at nonzero means. This does not contradict the expected-length theorem, but prevents interpreting its interval midpoint as a sharp general estimator. Both outcomes and the interpretation are retained.
4. **Monte Carlo precision is unequal.** Full tensors at p=64 have 150 replicates; solver cases have only 30. Those counts are adequate for computational/rough-coverage diagnostics, not fine size certification. One unusually low p=64 direct-Gaussian coverage realization is not removed. The independently registered S13 diagnostic is separate from the primary result.
5. **No real-data execution claim.** R01 remains pending a dataset and defensible scientific loading/sampling/noise model. The application audit is not a substitute for the attachment's requested analysis. Forcing an image/LLM/fluorescence array into the model would not satisfy the requirement.
6. **Intermediate caps and general loading geometry remain open.** S12 exposes upper/lower gaps rather than supplies matching rates. Its diagonal-mixture lower bound can be weaker than existing fixed-cap lower bounds. S07's all-budget bounds are deterministic calculations and do not empirically attain the power-profile theorem.
7. **Finite-grid pointwise slopes are not exact exponent validation.** The observed slopes -.474 and -.179 differ from limiting references -.5 and -.25 by more than Monte Carlo error. A post-hoc true-subspace intersection calculation matches the observed mean lengths within two Monte Carlo standard errors and explains finite-dimension curvature. It is an analytic approximation, not a new estimated-subspace theorem or a substitute for a wider asymptotic study.

## Baselines, fairness and uncertainty

- Strong baselines include direct Gaussian inference (optimal in a known regime), structural intervals, calibrated diagonal thresholding, the Xu–Chen–Han tensor PCA procedure, the preceding separated selector and unavailable-information oracles. The PCA comparator is a checked local reimplementation, not official author software. Two simultaneous iterations, HOSVD initialization, fitted-core tangent variance and known/plugin noise variants are documented; no truth-assisted initialization is used.
- Paired methods use the same data and supplied bounds. Split ablations share the same auxiliary noise. Optimal-support/direction oracles are explicitly labeled and do not count as deployable methods. Comparators' out-of-domain failures are not portrayed as theorem contradictions.
- Results include 90/95/99% coverage, Wilson intervals, length/loss standard errors, paired differences, type-I/power curves and normal diagnostics only for relevant pivots. For t3 noise, infinite fourth moments preclude a finite-variance squared-loss MCSE; the final table marks that limitation.
- The large cheap scalar draw count cannot be pooled into high precision for the expensive full-tensor cases. Three confidence levels and several node budgets on one observation are not independent draws. No extrema-over-configurations estimate uniform worst-case coverage over an infinite parameter class.
- The global solver run spans substantial host scheduling/inactive time; its case-level elapsed times should not be read as portable CPU benchmarks. S11 makes a separate fixed-thread, repeated-call timing and traced-allocation comparison. Traced allocations exclude preallocated inputs and untraced native workspace, and hardware is not an isolated benchmark server.

## Interpretation safeguards

The study can detect coding/calibration mistakes and illustrate proved mechanisms, including costs and failures. It cannot prove a minimax lower bound, an impossibility theorem, uniform honesty over a continuous class or a universal computational lower bound. A passed Bonferroni coverage screen is only a limited diagnostic. No universal CLT is claimed for nonlinear interval midpoints. Gaussian covariance, finite-variance replication, mean-zero noise, supplied caps, supplied approximation allowance and independently chosen loading are kept distinct.

The two additional suites are explicitly registered after a requirements/calibration audit, before their execution. They do not overwrite or pool away primary outcomes. Complete raw endpoints, estimator errors, numerical statuses and seed rules are available, including unfavorable cases and unresolved certificates.

## Before a submission or application

- Obtain independent review of the mathematical claims and of the local published-method implementation.
- Increase repetitions for any largest-dimension or solver coverage statement that must distinguish deviations of one or two percentage points.
- Develop and evaluate a justified application with immutable raw data, independent sampling units, fixed target, defensible calibration and leakage-free preprocessing.
- Resolve the general optimizer, arbitrary-profile, intermediate-cap and complete pointwise questions before making broader claims. Any estimator repair for the empty-intersection sentinel needs its own stated risk analysis.

Simulation execution, analytic calculations, raw-result verification and report/figure checks are separate evidence categories in this stage. Earlier drafts and saved results are preserved rather than pooled or silently rewritten.
