# Simulation study of honest tensor-functional intervals

Status: PASSED; completed simulation results, 2026-09-13. Real-data execution remains pending a dataset and justified sampling model. The open theoretical problems are unchanged.

The study executed **1,084,640 Monte Carlo data sets** in **318 stochastic configurations**, plus **84 analytic-only configurations** (402 statistical/envelope configurations total). A separate 18-setting runtime study is excluded from these coverage counts. The initial registry had 351 configurations and 824,640 data sets; a separately registered requirements/calibration follow-up added 51 configurations and 260,000 data sets. There are 2,160 binary optimizer solves on 240 shared data sets, not that many independent coverage observations. All summaries, raw per-trial endpoints/errors, seeds and numerical statuses are retained.

The main findings are rate-scale shortening in the regimes with executable guarantees, a substantial precision cost for conservative pointwise correction, severe failures under incorrectly supplied assumptions, and remaining computational gaps. Simulations do not prove minimax optimality, uniform honesty, or impossibility.

## Design and checks

The design, theorem map and initial registry were written before implementation/execution. Gaussian sample-mean experiments use tau=1/sqrt(n). Scalar/diagonal sufficient observations are generated exactly for methods that use only those contractions; full tensors are generated for projection and optimization. Procedures share observations, and split ablations share the same valid artificial Gaussian split. Supplied bounds are not selected using truth after seeing a realization. Signal construction uses truth only to define the prescribed parameter class and explicitly labeled oracles.

The study uses 329 known-answer checks, including 36 equivalence checks against the preserved cap-valid implementation, exact Tucker tangent-Jacobian variance checks, noiseless reconstruction, net calibration and model membership. Final analysis independently recomputes all interval coverages and mean widths, verifies all configuration/source hashes and preserves 330 earlier files unchanged. Python/NumPy/SciPy versions and single-thread settings are in the run manifests.

| Suite | Registered cases | MC data sets | Summary rows |
| --- | --- | --- | --- |
| S01 | 54 | 270,000 | 486 |
| S02 | 44 | 44,000 | 660 |
| S03 | 8 | 2,900 | 144 |
| S04 | 28 | 14,000 | 588 |
| S05 | 10 | 50,000 | 60 |
| S06 | 15 | 7,500 | 90 |
| S07 | 168 | 420,000 | 504 |
| S08 | 8 | 240 | 120 |
| S09 | 11 | 11,000 | 99 |
| S10 | 5 | 5,000 | 90 |
| S12 | 50 | 250,000 | 600 |
| S13 | 1 | 10,000 | 3 |


Cheap cases use B=5,000, giving nominal 95% coverage MCSE .00308. Full-tensor B is 500, 300 or 150, with nominal MCSE .00975, .01258 or .01780. Solver B=30 gives .03979. Wilson intervals are retained even at 0/100% coverage. Mean lengths, losses and paired differences have uncertainty summaries. Squared-loss Monte Carlo standard errors are not claimed for t3 noise, whose fourth moment is infinite. Aggregate timing from the prolonged host session includes scheduling/inactive periods; separate S11 calls provide the computational comparison.

## Coverage and rate validation

The table gives descriptive ranges over tested parameters, not confidence bounds for worst-case coverage over a continuum. All 90%, 95% and 99% levels are in the full tables. The predeclared family-wise lower-coverage screen includes 2526 in-scope rows and flagged 0 at Bonferroni cutoff 1.98e-05. Lack of a flag is not proof of uniform coverage and does not hide the individual low-coverage case discussed below.

| Suite | Method | In-scope cases | 95% coverage range | B per case |
| --- | --- | --- | --- | --- |
| S01 | growing | 54 | 0.944–1.000 | 5000–5000 |
| S02 | threshold_selected | 44 | 1.000–1.000 | 1000–1000 |
| S03 | pointwise | 8 | 0.920–0.993 | 150–500 |
| S04 | pointwise | 26 | 0.940–0.986 | 500–500 |
| S05 | calibrated | 9 | 0.949–1.000 | 5000–5000 |
| S06 | directional_mom | 12 | 1.000–1.000 | 500–500 |


| Curve | Observed slope | MC slope SE | Reference |
| --- | --- | --- | --- |
| G1 fixed-M structural length vs p | -0.2500 | deterministic | -0.25 |
| G1 noise-branch length vs n | -0.5000 | deterministic | -0.5 |
| G1 noise-branch RMSE vs n | -0.4980 | 0.0023 | -0.5 |
| P1 length vs p: cap 1 | -0.4745 | 0.0053 | -0.5 |
| P1 length vs p: cap ceil(sqrt(p)) | -0.1791 | 0.0071 | -0.25 |
| Threshold raw length vs p, K=3 (log factor retained) | -0.1526 | deterministic | -0.1667 |
| Threshold raw length vs p, K=4 (log factor retained) | -0.2289 | deterministic | -0.25 |


Log-regression slopes are descriptive finite-grid diagnostics. Mean-length error bars vanish for deterministic-radius procedures, so their fitted slopes partly check formulas, not stochastic attainment. The noise-branch RMSE and full-tensor expected-length slopes use observed losses/lengths with Monte Carlo uncertainty. Threshold reference exponents exclude the displayed logarithmic correction. See `tables/summary.csv` for length/rate, squared-loss/rate-squared and paired differences.

The P1 slopes do not equal their limiting references over p=8–64: the fixed-cap slope is about -0.474 and the growing-cap slope about -0.179. These departures exceed the reported Monte Carlo slope errors, which do not account for finite-dimension curvature. We do not label this exact exponent validation. A post-hoc diagnostic freezes the fitted subspaces at their true values and the singular values at the prescribed amplitude. If the resulting tangent and direct radii are h and d, their center difference is N(0,tau^2), and the intersection length is max(0,min(2min(h,d),h+d-abs(W))). Integrating this expression predicts the finite-dimension clipping effect. All eight approximate mean-length predictions are within two observed Monte Carlo standard errors; the integral formula is independently checked by quadrature. This is an explanatory approximation using unavailable true geometry, not a new theorem for estimated subspaces.

| p | Cap | Observed length / rate | Frozen-subspace length / rate | Difference in MCSE |
| --- | --- | --- | --- | --- |
| 8 | 1 | 7.578 | 7.478 | 1.95 |
| 8 | 3 | 6.271 | 6.310 | -0.93 |
| 16 | 1 | 7.807 | 7.770 | 0.75 |
| 16 | 4 | 6.840 | 6.877 | -0.69 |
| 32 | 1 | 7.857 | 7.908 | -0.74 |
| 32 | 6 | 7.038 | 7.175 | -1.77 |
| 64 | 1 | 8.009 | 7.974 | 0.43 |
| 64 | 8 | 7.277 | 7.476 | -1.50 |


## Pointwise precision and an estimator failure

| p | Cap | Method | 95% coverage [Wilson CI] | Mean length ± MCSE |
| --- | --- | --- | --- | --- |
| 16 | 1 | direct | 0.962 [0.941, 0.976] | 3.92 ± 0 |
| 16 | 1 | pointwise | 0.982 [0.966, 0.991] | 1.95 ± 0.012 |
| 16 | 1 | xch_known | 0.944 [0.920, 0.961] | 0.98 ± 0 |
| 16 | 1 | oracle | 0.944 [0.920, 0.961] | 0.98 ± 0 |
| 16 | 4 | direct | 0.962 [0.941, 0.976] | 3.92 ± 0 |
| 16 | 4 | pointwise | 0.978 [0.961, 0.988] | 3.42 ± 0.027 |
| 16 | 4 | xch_known | 0.954 [0.932, 0.969] | 1.96 ± 0 |
| 16 | 4 | oracle | 0.954 [0.932, 0.969] | 1.96 ± 0 |
| 64 | 1 | direct | 0.960 [0.915, 0.982] | 3.92 ± 0 |
| 64 | 1 | pointwise | 0.993 [0.963, 0.999] | 1 ± 0.0098 |
| 64 | 1 | xch_known | 0.960 [0.915, 0.982] | 0.49 ± 0 |
| 64 | 1 | oracle | 0.960 [0.915, 0.982] | 0.49 ± 0 |
| 64 | 8 | direct | 0.873 [0.811, 0.917] | 3.92 ± 0 |
| 64 | 8 | pointwise | 0.920 [0.865, 0.954] | 2.57 ± 0.047 |
| 64 | 8 | xch_known | 0.927 [0.873, 0.959] | 1.39 ± 0 |
| 64 | 8 | oracle | 0.927 [0.873, 0.959] | 1.39 ± 0 |


At p=16, cap one, the P1 test amplitude is about 310,930 noise standard deviations. Such signals deliberately satisfy a conservative sufficient condition; practical signal sweeps extend from zero upward and show that this condition is far from a useful empirical cutoff. The Xu–Chen–Han comparator uses its two simultaneous iterations and exact fitted-core tangent variance. It is an asymptotic regular-signal procedure, not an honest weak-signal competitor, and often gives materially shorter intervals in the strong regime. The support oracle has unavailable structure. There is no claim of leading-constant or universal practical dominance.

The cap-valid implementation replaces empty interval intersections by {0}. At large nonzero means its **interval midpoint can have enormous MSE**: in S03_002, the observed midpoint MSE is 1.20847e+07 (MCSE 1.21e+07), despite coverage 0.982 and mean length 1.952. The large squared-loss uncertainty reflects rare sentinel events. There are 16 tested 95% pointwise cases with at least one such nonzero-target sentinel. This is retained in raw records and the audit. The P1 theorem concerns honesty and expected length; it does not promise midpoint MSE control. A useful estimation repair needs a separate analysis, rather than silently reinterpreting this midpoint as the ideal residual-fit estimator.

## Assumption failures and calibration investigation

Under equicorrelated Gaussian coordinates with rho=.8, naive iid calibration covers 0.1094, while the known-covariance interval covers 0.9512. Mean-shift contamination gives naive coverage 0.0034; a variance correction does not remove its bias. The finite-variance median scan tests the full binary net and a known covariance upper bound. Its simultaneous feasibility is conservative in these draws; the study does not implement the general robust minimax projection and does not claim dependence or Huber-contamination robustness.

Understated rank caps produce minimum pointwise coverage 0.000 in the deliberate violations. The previous rank selector can return a zero interval at weak nonzero signals, outside its separation assumption. Loading residual and approximation-allowance omissions also cause severe failures. Corrected intervals retain their explicitly supplied assumptions; general arbitrary-loading and approximate-rank sharp computation is not established by these examples.

The original S03_007 direct Gaussian interval covers 0.873 [0.811, 0.917] with B=150. This unusually low realization is displayed, including its interval excluding .95; it is not discarded because the broad family-wise screen did not flag it. Regeneration of its full Gaussian tensors checks the direct statistic independently. The separately registered S13 confirmation covers 0.949 [0.945, 0.953] with B=10,000, using a new fixed stream of exact diagonal observations. It is a diagnostic addition, not a replacement or a pooled result. See `results/gaussian_diagnostic.json` for the original one-sided test and regeneration discrepancy.

## Computation and intermediate caps

| Signal | Loading | Certified at budget 3000 | Mean finite gap | No witness |
| --- | --- | --- | --- | --- |
| zero | flat | 30/30 | 0.05858 | 0 |
| zero | arbitrary | 30/30 | 0.04044 | 0 |
| weak | flat | 30/30 | 0.09386 | 0 |
| weak | arbitrary | 0/30 | 0.1446 | 0 |
| boundary | flat | 26/30 | 0.1009 | 0 |
| boundary | arbitrary | 30/30 | 0.09998 | 0 |
| strong | flat | 0/30 | 0.1444 | 0 |
| strong | arbitrary | 0/30 | 0.2093 | 0 |


Only continuous rank-one binary tensors are optimized. All support levels in the implemented projective net are included. For every tolerance/budget the outer interval is retained, along with feasible witnesses and endpoint gaps; unmet tolerances are explicit. Float64 guard bounds are numerical evidence, not formal interval arithmetic. The ideal general-dimensional minimax residual/block optimizer remains absent. S11 reports actual diagonal access through p=1,048,576, full tensors through 64^3, and binary order-three/four costs; traced allocations exclude untraced native workspace.

| Cap at p=65536 | Executable length | Diagonal-mixture lower | Upper / lower |
| --- | --- | --- | --- |
| 1 | 2 | 0.007709 | 259 |
| 16 | 3.92 | 0.0809 | 48.5 |
| 64 | 3.92 | 0.2009 | 19.5 |
| 256 | 3.92 | 0.2993 | 13.1 |
| 1024 | 3.92 | 0.3155 | 12.4 |


The follow-up uses sparse common-target diagonal signals. Its diagonal-mixture lower bound need not be the strongest available fixed-cap bound, especially for K=3. The remaining upper/lower gap is a diagnostic of these constructions, not a new minimax theorem. Matching intermediate growing-cap factors, arbitrary loading profiles and a complete pointwise characterization remain open.

## Local power and distribution diagnostics

Intervals are inverted for the zero functional at strong signed rank-two means. Alternatives shift the target by c tau sqrt(r/p), with c in {0,1,2,4,8}. The exact direct-Gaussian power curve and empirical paired rejection probabilities are reported. Direct and oracle statistics are exact Gaussian pivots; XCH diagnostics are interpreted under regular-signal assumptions. No CLT is asserted for nonlinear interval midpoints or global-solver endpoints.

| Local shift | Method | Rejection probability [Wilson CI] |
| --- | --- | --- |
| 0.0 | direct | 0.059 [0.046, 0.075] |
| 0.0 | pointwise | 0.031 [0.022, 0.044] |
| 0.0 | xch_known | 0.048 [0.036, 0.063] |
| 0.0 | oracle | 0.048 [0.036, 0.063] |
| 1.0 | direct | 0.070 [0.056, 0.088] |
| 1.0 | pointwise | 0.049 [0.037, 0.064] |
| 1.0 | xch_known | 0.151 [0.130, 0.175] |
| 1.0 | oracle | 0.151 [0.130, 0.175] |
| 2.0 | direct | 0.108 [0.090, 0.129] |
| 2.0 | pointwise | 0.130 [0.111, 0.152] |
| 2.0 | xch_known | 0.496 [0.465, 0.527] |
| 2.0 | oracle | 0.496 [0.465, 0.527] |
| 4.0 | direct | 0.278 [0.251, 0.307] |
| 4.0 | pointwise | 0.565 [0.534, 0.595] |
| 4.0 | xch_known | 0.984 [0.974, 0.990] |
| 4.0 | oracle | 0.984 [0.974, 0.990] |
| 8.0 | direct | 0.827 [0.802, 0.849] |
| 8.0 | pointwise | 0.998 [0.993, 0.999] |
| 8.0 | xch_known | 1.000 [0.996, 1.000] |
| 8.0 | oracle | 1.000 [0.996, 1.000] |


## Real-data status and outstanding empirical requirements

No scientifically justified repeated-tensor dataset, independent target loading or known directional noise calibration was supplied. `real_data/README.md` records the missing sampling units, calibration, rank/approximation bounds, missingness and split/preprocessing requirements. R01 remains pending. Simulated observations, synthetic tensors and noise-injected images are not represented as real-data validation.

The main empirical limitations are the small solver replication count, conservative P1 signal floor, largest-p coverage uncertainty, unavailable general residual/block fits, unmatched intermediate-cap bounds, and lack of a justified application. Lower bounds and impossibility results are analytic statements, not experimentally proved. The full reviewer audit and theory/experiment comparison separate those gaps from completed simulation execution.
