# Scientific revision after the complete review

This is the **current submission stage**, dated September 13, 2026. The focused theory paper is assessed **B: near ready** after the scientific revision. Thirteen review concerns are resolved, one is partially resolved and five remain unresolved. The original research drafts and independent review are preserved outside this directory.

## Reading order

1. [Revised main paper](paper/main.pdf): the central all-budget result, mechanism, computational/loading/adaptation scope and current evidence.
2. [Complete technical supplement](paper/technical_supplement.pdf): full supplied proofs for 59 retained results plus the new R1 scalar proposition.
3. [Empirical supplement](empirical_report.pdf): corrected saved evidence and 87,200 new independent datasets, with all configurations and failures.
4. [Scientific revision summary](revision_summary.md), [individual responses](response_to_review.md), [19-issue matrix](tables/issue_registry.csv), [40-instruction crosswalk](guideline_coverage.md), and [second adversarial review](second_review.md).

## What changed scientifically

- A bounded four-ULP endpoint policy corrects two 90% coverage rows for one real miss; strict counts are retained. All 303 saved interval cases were reevaluated on their original observations.
- R1 adds a separate scalar estimator with unconditional noise-scale risk. It removes the catastrophic zero-sentinel midpoint loss without changing the confidence intervals. P1 still claims expected length, not pointwise minimax squared risk.
- Fifty-five registered new configurations generate 87,200 independent datasets. They isolate bias/fallback/quantile effects, hold M fixed across signals, test row-corruption and independent variance refinements, increase large-p precision, and hold loading/tolerance fixed across solver budgets.
- The binary benchmark achieves 7 of 600 endpoint tolerances. All 593 unresolved solves remain in the reported results; float64 guards are not formal interval arithmetic.
- The main manuscript and complete supplement now state the same final rates and limitations. Numerical main-text claims are generated from checked tables.

The general efficient fixed-cap weak-signal optimizer, arbitrary loading profiles, intermediate growing-cap rates and complete pointwise/TT adaptation remain open. No real-data application is claimed; no defensible repeated-tensor dataset and prescribed contrast were established.

## File organization

| Location | Contents |
|---|---|
| `paper/` | Current main LaTeX/PDF, abstract and generated numerical section; full technical supplement and proof inputs; introduction outline and notation dictionary |
| `theory/` | New R1 proof, copied/reorganized later results, 60-result status ledger and scientific dependency/assumption audit |
| `code/` | Public revised API, registered experiment runner, all-observation correction, independent analysis, plotting, report assembly and validators |
| `configs/` | Complete pre-execution registry and seeds for the 55 new cases |
| `results/V*.npz,json` | Immutable raw new outputs and per-case generation records |
| `results/evaluated_V*.npz` | Derived pure-fallback ablation, strict and rounded coverage; no additional noise draws |
| `tables/` | All 612 new method/level summaries, paired uncertainties, 600 solver trials/gaps, calibration, old/new scalar losses, runtime and issue registry |
| `figures/` | Six new PDF/SVG/inspection PNG figures and captions; analytic rates are explicitly distinguished from experiments |
| `empirical/` | Isolated reevaluation of the original 1,084,640-dataset study: corrected raw scalar outputs, unchanged endpoints, all saved-study tables and ten regenerated figures |
| `logs/` | Original baseline hashes, full-review read manifest, five new run manifests, source hashes, new checks/builds and final preservation/artifact validation |

The original study's reports remain at `../empirical_study/`. Obsolete copied report builds are not a second current submission. Original study and review files are untouched. The root README and requirements ledger record the current status.

## Reproduce

The executed environment uses Python 3.9.6, NumPy 2.0.2 and SciPy 1.13.1; exact platform and BLAS details are in `logs/method_checks.json`. Matplotlib and PyMuPDF are needed for figures and PDF checks. Pandoc, XeLaTeX and latexmk build the documents. Install requirements in an appropriate environment using the preserved `empirical/requirements.txt`; no packages were installed globally by this revision.

```bash
# From this directory: rebuild from saved raw observations and current new runs.
bash reproduce.sh

# Re-execute all 55 registered new cases, then rebuild.
bash reproduce.sh --rerun-new

# Standalone public-method scientific checks and fresh API timings.
python3 code/check_methods.py
```

The default command reevaluates every affected original observation and rebuilds analysis, figures and PDFs. It does not count saved data as newly simulated. The optional new-run command recreates 87,200 datasets with case-local deterministic seeds; timing varies across runs. The original 1,084,640 observations can be regenerated through their preserved original study pipeline, followed by this stage's deterministic reevaluation. Paired confidence levels and methods do not count as independent datasets.

`code/methods.py::interval_and_estimate` returns `lo`, `hi`, `estimate`, `estimator_id`, `estimator_alpha`, `midpoint_diagnostic`, and the scoped R1 risk upper bound. Supply a valid M, common Tucker mode cap, Gaussian noise scale and independent random generator. Its pointwise length guarantee additionally requires the explicit P1 conditions. It is not the ideal weak-signal minimax optimizer.

## Verification scope

New method checks include 120,026 assertions/pathwise cases and 40 timed API calls. New-data summaries independently pass 3,125 checks; every affected saved interval case has two scaling checks. Final artifact, source-dependency and baseline-preservation results are in `logs/final_validation.json`. Prior review checks and saved study checks are labeled as prior evidence, not rerun Monte Carlo data. Numerical tests supplement mathematical proof review and do not constitute formal verification.
