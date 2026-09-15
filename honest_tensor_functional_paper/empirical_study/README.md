# Theory-led simulation study

**Simulation execution completed 2026-09-13.** This stage evaluates the existing theory and algorithms before further open-problem development. It does not resolve the general optimizer, arbitrary-loading, intermediate-cap or complete pointwise theory requirements.

Start with the [observed report](report.md), [report PDF with figures](report.pdf), [theory–experiment comparison](theory_comparison.md), and [reviewer audit](reviewer_audit.md). The [manuscript sections](manuscript/empirical_sections.md) and [PDF](manuscript/empirical_sections.pdf) are standalone drafts based on the completed runs; earlier manuscripts are preserved.

## What was run

- **1,084,640 Monte Carlo data sets** across 318 stochastic configurations, plus 84 analytic-only configurations: **402 statistical/envelope configurations** in total. The primary registry had 351 configurations and 824,640 data sets. The separately registered S12/S13 follow-up added 51 configurations and 260,000 data sets. A separate 18-setting runtime study does not contribute independent coverage replications.
- Gaussian coverage at 90%, 95%, 99%; large-cap p/n/budget branches; fixed-cap threshold rates; strong and weak pointwise signals; under/exact/over-supplied caps; rotated and weak-extra-component means; heavy tails, correlation and contamination; full binary directional median scans; signed loading profiles; approximation/residual corrections; local power and relevant Gaussian diagnostics.
- A paired local reimplementation of Xu–Chen–Han's tensor PCA procedure, with known and plug-in noise scales, alongside direct, structural, threshold, previous separated-selector and oracle comparisons. Methods see the same observations; split ablations share auxiliary noise.
- **2,160 finite-budget binary optimizer solves on 240 independent observations.** At 95% confidence and the 3,000-node budget, 146/240 met the endpoint tolerance and 94 remained unresolved. Outer endpoints, feasible witnesses, gaps and statuses are retained. This is an exponential float64 benchmark, not a general high-dimensional minimax algorithm or formal interval arithmetic.
- 336 loading-envelope calculations, eight post-hoc frozen-subspace length diagnostics, and separate actual-access/runtime/memory measurements. These calculations are not simulated attainment of the ideal block optimizer.

## Main findings and limits

The large-cap noise-branch RMSE slope is -0.498 (Monte Carlo slope SE .0023), consistent with the -1/2 reference. Pointwise p slopes are -0.474 for cap one and -0.179 for cap ceil(sqrt(p)), versus limiting references -1/2 and -1/4. Those finite-grid departures exceed Monte Carlo slope errors; a separately labeled true-subspace intersection calculation accounts for the trend. No exact pointwise exponent confirmation is claimed.

Strong-signal regular inference can be substantially shorter than the conservative cap-valid interval. At p=16 and cap one, their 95% mean lengths are approximately .98 and 1.95. Wrong covariance, understated caps and omitted loading/approximation corrections can fail severely. With coordinate correlation .8, naive/calibrated coverage is .1094/.9512.

The `{0}` replacement for an empty cap-valid interval intersection can produce enormous midpoint MSE at nonzero means. This is an observed estimator failure, not a contradiction of P1's coverage/expected-length statement. An unusual p=64 direct-Gaussian realization (131/150 coverage) remains visible; regenerating its full tensors reproduced the statistic. Separately registered confirmation gives 9492/10000 coverage, without replacing or pooling away the original result.

The primary finite-sample coverage screen flags no in-scope row at its Bonferroni threshold across 2,526 rows. This is not proof of uniform honesty. Solver B=30 and largest-tensor B=150 have wide coverage uncertainty. No general robust/block minimax optimizer, unknown-noise-scale guarantee or real-data inference result is claimed. **R01 remains pending a dataset and defensible sampling/target/noise model**; see the [application audit](real_data/README.md).

## Organization

| Path | Contents |
|---|---|
| `simulation_design.md`, `theorem_experiment_map.md`, `experiment_registry.md` | Frozen primary protocol written before execution |
| `registry_amendment_20260913.md` | Explicitly registered intermediate-cap and Gaussian-calibration follow-ups |
| `configs/` | Every case, runtime settings, fixed seed rules and archived user guidelines |
| `code/` | Generation, checked methods, tests, analysis, vector plotting, report build and validation |
| `results/` | Raw per-trial NPZ arrays, case metadata, numerical statuses and validation audits |
| `tables/` | All 3,444 summary rows; paired differences; loading bounds; individual solver records; slopes; normal and geometry diagnostics, in CSV/JSON |
| `figures/` | Ten vector PDF/SVG figures, inspection PNGs, captions and design/visual audits |
| `manuscript/` | Observed simulation section and explicit real-data limitation, in Markdown/PDF |
| `real_data/` | Applicability and missing-input audit; no manufactured application results |
| `logs/` | Run/source hashes, checks, original warning log, deviations, host-timing qualification and artifact manifest |

Raw execution metadata initially records `NEEDS CHECK`; validated conclusions and recomputed summaries are in `tables/` and `results/analysis_audit.json`. `VALIDATED` describes checked implementation/results, not a proof of a statistical theorem. Failed tolerance targets remain visible even when the outer-interval calculation is validated.

## Reproduction

From the repository root, `bash honest_tensor_functional_paper/empirical_study/reproduce.sh` runs the full primary study, follow-ups, analysis, plots, PDF reports and validation. The exponential solver is the slow stage. The supplied configurations are fixed; `code/build_configs.py` is their original materializer and is not needed for an ordinary reproduction. The post-hoc follow-up stays separately identified even on later reproductions.

To rebuild reports from saved observations without rerunning Monte Carlo:

```bash
cd honest_tensor_functional_paper/empirical_study
python3 code/analyze_results.py
python3 code/plot_results.py
python3 code/build_report.py
python3 code/validate_artifacts.py
```

The actual environment used Python 3.9.6, NumPy 2.0.2, SciPy 1.13.1, Matplotlib 3.9.4, threadpoolctl 3.6.0 and PyMuPDF 1.26.5; Python dependencies are pinned in `requirements.txt`. PDF builds also require Pandoc and XeLaTeX. Computational runs set BLAS/OpenMP thread counts to one. Traced allocation figures exclude preallocated input and untraced native workspace. Host scheduling/inactive time limits interpretation of primary wall-clock totals; use the separate repeated-call benchmark.

The 329 implementation checks, 8,159 result checks and 87 artifact checks are newly run. All 48 local Markdown links resolve, and rendered report text stays within its pages. The 330 protected earlier files, including the two preceding uncommitted supplements, are verified unchanged. Earlier saved Monte Carlo outputs are not pooled into this study or counted as new evidence. [Root requirements](../../requirements.md) retains the unresolved theory and application work.
