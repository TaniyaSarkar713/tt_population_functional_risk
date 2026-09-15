# Simulation study

We evaluated honest confidence intervals for fixed scalar loadings in the additive tensor model Z=A+tau G, with known noise and supplied Frobenius and rank bounds. The primary design was fixed before execution and separates implementable theory validation from paired comparisons and assumption violations. Exact sufficient observations are used for diagonal procedures; full tensors are generated for projection and the binary global benchmark. All methods share observations, with correctly scaled independent artificial splitting when needed.

The direct Gaussian and structural intervals are compared with calibrated sequence-style thresholding, the cap-valid pointwise method, the Xu–Chen–Han tensor PCA procedure, and explicitly labeled known-support/direction oracles. The PCA comparator is reimplemented from Section 4.2 and Algorithm 3 of the primary preprint (https://arxiv.org/abs/2501.16223v1), including its exact tangent variance. Its regular-signal guarantee is kept distinct from finite-sample cap-uniform honesty. The diagonal comparison is connected to the Gaussian functional literature of Collier, Comminges and Tsybakov (https://arxiv.org/abs/1502.00665).

The completed study contains 1,084,640 data sets and 402 configurations, including 51 explicitly registered follow-ups and 84 analytic-only envelope configurations. Confidence levels 90%, 95% and 99% are evaluated with Wilson intervals, mean-length standard errors, scalar losses and paired differences. Expensive full tensors and solver cases have fewer replications; their uncertainty is retained.

The large-cap interval follows its structural and noise rate branches. Strong saturated pointwise signals permit shortening, while regular-signal and oracle intervals can be substantially shorter. The observed pointwise p slopes are about -0.474 and -0.179, compared with limiting references -0.5 and -0.25; these finite-grid discrepancies exceed Monte Carlo slope errors. An explicitly post-hoc frozen-subspace calculation predicts the effect of intersection with the direct interval and matches all eight mean lengths within two Monte Carlo standard errors. It is an explanatory approximation, not exact exponent validation or a new estimated-subspace theorem. At moderate signals, the cap-valid method may remain near or above the direct interval's width. The ideal general-dimensional residual optimizer is not replaced by diagonal thresholding or analytic loading envelopes.

| Curve | Observed slope | MC slope SE | Reference |
| --- | --- | --- | --- |
| G1 fixed-M structural length vs p | -0.2500 | deterministic | -0.25 |
| G1 noise-branch length vs n | -0.5000 | deterministic | -0.5 |
| G1 noise-branch RMSE vs n | -0.4980 | 0.0023 | -0.5 |
| P1 length vs p: cap 1 | -0.4745 | 0.0053 | -0.5 |
| P1 length vs p: cap ceil(sqrt(p)) | -0.1791 | 0.0071 | -0.25 |
| Threshold raw length vs p, K=3 (log factor retained) | -0.1526 | deterministic | -0.1667 |
| Threshold raw length vs p, K=4 (log factor retained) | -0.2289 | deterministic | -0.25 |


At 95% confidence, correlated Gaussian noise with rho=.8 yields coverage 0.1094 under naive iid calibration and 0.9512 under known covariance calibration. Understated rank bounds, omitted loading/approximation contributions and rank selection outside separation produce failures in the deliberately misspecified settings. The finite-variance full-net event is conservative in the tested laws; this does not establish contamination or dependent-replicate robustness.

An unusual direct-Gaussian realization in the largest-dimensional primary case is retained: coverage 0.873 [0.811, 0.917], B=150. Independent, separately registered confirmation gives 0.949 [0.945, 0.953], B=10,000; the confirmation is not substituted for the original result. A further negative finding concerns the {0} fallback for empty cap-valid interval intersections: its midpoint can have large squared error at strong nonzero signals, even when the interval's coverage and expected length behave as predicted. The pointwise theorem does not provide a midpoint risk bound.

The binary rank-one optimizer performs 2,160 finite-budget solves on 240 independent observations, with all gaps and unresolved certificates retained. This is an exponential numerical benchmark. Intermediate-cap upper/lower comparisons and general loading envelopes remain diagnostic rather than claims of sharp computational attainment. Complete configuration-level results, uncertainty, numerical statuses, source hashes and code accompany the study.

# Real-data analysis: current limitation

No real-data inference result is asserted. The available workspace does not supply a defensible repeated-tensor sampling model with calibrated directional noise, an independently fixed scientific loading, and justified norm/rank or approximation bounds. An application would require those choices before preprocessing, split construction or interval evaluation. The accompanying application audit records the missing inputs; simulated data are not presented as observational validation.
