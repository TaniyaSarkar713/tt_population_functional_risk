# Complete scientific review

**September 13, 2026. Verdict: C — Major revision required.** This is a fresh tool-assisted internal review with three simulated referee perspectives, not independent external peer review. The central theory appears viable; no fatal mathematical counterexample was found.

- [Complete review with all audits (PDF)](complete_review.pdf) and [Markdown](complete_review.md).
- [Main referee report (PDF)](report.pdf) and [Markdown](report.md).
- [59-result theorem/proof audit](theorem_audit.md), with [CSV](tables/theorem_audit.csv) and [JSON](tables/theorem_audit.json).
- [Assumptions and tuning](assumption_audit.md), [simulation and claims audit](simulation_and_claims.md), [figures/tables/notation](presentation_audit.md).
- [P0–P3 revision plan](revision_plan.md), [proposed abstract](proposed_abstract.md), and [all 50 guideline items](guideline_coverage.md).

The three MAJOR findings are a coverage tolerance that counts a genuine miss, a multicomponent “no-bias” ablation, and the absence of a synchronized final manuscript. Five MODERATE and two MINOR findings address midpoint risk, norm-budget coupling, comparator applicability, computational scope, calibration experiments, exported-estimator identity and notation. Already disclosed limitations remain distinguished from newly discovered errors.

## New review evidence

The review ran 60,496 raw-result recomputations and 1,377 finite mathematical probes. An exact regeneration of a Gaussian oracle error proves that one 90% miss in S03_007 was counted as covered in two paired rows: 134/150 becomes 133/150. The other 24 strict/tolerant row discrepancies arise from harmless one-ULP structural boundaries. Nine additional binary grid containment checks found no outer violation; these do not prove global numerical validity.

Saved empirical analysis, plots, reports and validation were rebuilt in an isolated copy. Compared numerical tables and report text were byte-identical. The integrated 55-page manuscript was also freshly compiled in a copy. All 14 active figures were visually reviewed, all five active PDFs scanned, and integrated label/bibliography-key resolution checked. The original million-dataset study and full exponential benchmark were not rerun.

The entire preceding research state was hashed before review. Only root `README.md` and `requirements.md` receive intentional review-status edits outside this directory. Proofs, methods, raw observations and saved reports remain unchanged; F01 is documented, not silently patched. `results/review_validation.json` records final preservation and artifact checks. No commit or push was performed.

## Files and reproduction

`code/` contains the review checks, manually reasoned theorem-audit source, crosswalk/PDF builder and artifact validator. `results/` contains new mathematical, numerical, implementation, presentation, reproduction and preservation evidence. `tables/` contains the active theorem inventory, detailed audits, guideline map and lexical scan. `logs/` preserves the initial hashes, environment and isolated rebuild logs. `review_guidelines.txt` archives the user's complete attachment. Markdown files are the editable review text; the complete PDF combines the substantive documents.

From the repository root, with the package versions in `../empirical_study/requirements.txt` and Pandoc/LaTeX available:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 honest_tensor_functional_paper/independent_review/code/check_results.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 honest_tensor_functional_paper/independent_review/code/check_proofs.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 honest_tensor_functional_paper/independent_review/code/check_implementations.py
python3 honest_tensor_functional_paper/independent_review/code/reproduce_saved.py
python3 honest_tensor_functional_paper/independent_review/code/check_presentation.py
python3 honest_tensor_functional_paper/independent_review/code/write_theorem_audit.py
python3 honest_tensor_functional_paper/independent_review/code/build_review.py
python3 honest_tensor_functional_paper/independent_review/code/validate_review.py
```

These commands write only review outputs and temporary isolated copies. The original `inventory.py` captured the initial baseline and intentionally refuses to overwrite it after root status documentation changes. Re-running a check is not a new independent referee assessment. The implementation probe is designed to reproduce the currently preserved coverage-policy finding; after a future authorized fix, its regression expectation must be updated deliberately.
