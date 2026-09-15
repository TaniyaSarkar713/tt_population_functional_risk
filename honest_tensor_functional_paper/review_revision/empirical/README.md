# Corrected copy of the saved empirical study

This directory contains the reevaluated saved observations and regenerated tables/figures used by the current review revision. It is not another current manuscript. Read the [current empirical report](../empirical_report.pdf) and [revision guide](../README.md).

All original study files remain unchanged at `../../empirical_study/`. The 1,084,640 observations here are saved evidence, not newly generated draws. All 303 interval cases use corrected coverage comparisons and the separate R1 scalar estimator where applicable; original endpoints and old estimates are retained. The 15 event-only cases and 84 analytic-only configurations are unaffected. Event-only calibration records have no scalar estimator.

The original design, literature and theory-mapping notes are preserved here as provenance and should be read with the current corrections in the parent report. The old combined ablation is named `split_unprotected`. The original signal sweep changes the supplied M with signal amplitude. The old solver sweep uses different loadings by case and a looser tolerance at budget 100; the parent V02 experiment fixes both confounders.

The `code/` folder retains the original generation/analysis machinery with the documented numerical and scalar patches. For a complete current rebuild use `bash ../reproduce.sh` from this directory; use the original preserved study pipeline to recreate its original observations before reevaluation. Historical copied report/manuscript files were removed to avoid competing current narratives; they remain available in the untouched original study.
