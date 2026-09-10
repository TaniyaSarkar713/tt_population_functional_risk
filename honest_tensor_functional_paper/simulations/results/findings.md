# Simulation findings

Fixed seed 20260909; 2,000 replications in each of 175 configurations. There are 172 configurations within the stated iid Gaussian model and three out-of-model stress configurations. Intervals share noise within a configuration; streams are independent across configurations.

## In-model coverage

| Method | Configurations | Minimum | Maximum |
|---|---:|---:|---:|
| Direct Gaussian | 172 | 0.9365 | 0.9625 |
| Structural | 172 | 1.0000 | 1.0000 |
| Threshold | 172 | 0.9975 | 1.0000 |
| Selected | 172 | 0.9975 | 1.0000 |
| Known-direction oracle | 117 | 0.9370 | 0.9615 |

The selected interval is conservative on this grid. Coverage ranges are descriptive extrema, not confidence bounds for uniform coverage. With 2,000 replications, the Monte Carlo standard error at coverage 0.95 is 0.00487. If all replications cover, the exact 95% binomial interval is approximately [0.99816,1], despite the plug-in Monte Carlo standard error being zero. Full configuration-level exact intervals, bias, bias standard errors and RMSE are in summary.csv.

## Deterministic lengths at p=n=8192, cap one

| Order K | Selected length / tau | Direct length / tau | Ratio to direct |
|---|---:|---:|---:|
| 2 | 2.000000 | 3.919928 | 0.5102 |
| 3 | 0.962231 | 3.919928 | 0.2455 |
| 4 | 0.667428 | 3.919928 | 0.1703 |
| 6 | 0.462944 | 3.919928 | 0.1181 |

These are exact evaluated formulas, not fitted empirical rates. At K=2 the selected length is 2 tau and no polynomial separation is obtained. The known-direction oracle may be far shorter for diffuse signals because it is given unavailable factor information; the proposed interval does not dominate that different experiment.

## Assumption stress tests

| Noise | Direct coverage | Threshold / selected coverage | Interpretation |
|---|---:|---:|---|
| gaussian | 0.9540 | 1.0000 | In model |
| student_t3 | 0.9585 | 0.9670 | Variance one, heavier tails; outside Gaussian proof |
| variance_contamination | 0.5740 | 0.3830 | 5% noise SD multiplied by 10; stated variance calibration is false |
| correlated | 0.1430 | 1.0000 | Gaussian margins; direct variance wrong, nonlinear union bound still applies |

Stress-test results are not evidence of robustness. The heavy-tail result at zero does not establish coverage for other means. No data tuning or post hoc configuration removal was performed. The weak-rank radii remain constant as the second singular value vanishes, explicitly demonstrating the lack of actual-rank adaptation.

## Figures and checks

theoretical_comparison.pdf evaluates exact analytic bounds up to p=10^12; simulated dimensions stop at 8192. The shaded full-data bracket is unresolved, not a confidence band. The added diagonal-only lower curve is a classical benchmark; it matches the upper order only for procedures restricted to diagonal observations. Exact hypergeometric checks and 3,136 enumerated support pairs are in diagonal_benchmark_checks.json. weak_rank_coverage.pdf uses exact binomial Monte Carlo intervals, with categorical spacing in epsilon. check_theory.py checks 101,101 scalar cases, 120 random tensors of each format, and exact finite-binomial mixture second moments. Numerical checks supplement the written proofs and cannot verify them logically.
