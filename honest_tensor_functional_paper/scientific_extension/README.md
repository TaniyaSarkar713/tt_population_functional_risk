# Scientific extension, 14 September 2026

This is the latest research stage. It preserves the preceding `review_revision/` manuscript and every earlier study. Read the [research and empirical report](paper/report.pdf), its [Markdown source](paper/report.md), and the [complete new derivations](paper/technical_supplement.pdf) ([source](theory/results.md)).

The work provides an all-budget orthogonal-loading bracket within a doubly logarithmic factor, sharp noncritical logarithmic-decay rates, a scalar safeguard with uniform and strong-pointwise risk, arbitrary-core Tucker and TT pointwise families, and a sharp four-entry off-tangent rank-one interval. It implements the exact diagonal sparse submodel across all caps and a bounded subject-data projection-bias correction. The [theorem ledger](theory/theorem_status.json) contains seven supplied results and a fixed-stratum corollary. PROVED means internally checked supplied derivation, not external review or formal verification.

**Still open:** the general efficient fixed-cap weak-signal minimax optimizer; exact arbitrary/nonorthogonal-loading and full-model intermediate-cap rates; critical loading exponents; and the complete weak, undersaturated and higher-order pointwise theory. The old exponential binary optimizer remains a benchmark. Proxy evaluation is not implementation of the ideal loading optimizer. The diagonal sparse rate is classical and requires an additional exact diagonal-mean assumption.

Newly executed evidence: **109,000 independent Monte Carlo data sets in 92 configurations**, 504 analytic loading calculations, and **40,553 finite checks**. All per-replicate outputs are retained. The deliberate dense-rank-one misuse of the sparse-diagonal procedure has zero coverage; the bounded-data uncorrected projection also fails for the original target at larger sample size. These failures are included in the report. A separate 36-call public-API timing study reaches 2,097,152 input entries; its timing calls are not counted as statistical MC replications. The new counts exclude the 87,200 saved revision data sets and 1,084,640 saved pre-review data sets.

The real-data analysis downloaded and processed the full UCI EEG archive: **122 subjects, 11,074 trial files, 10,962 retained trials**. Its prespecified clipped S2 contrast has cohort mean **2.222 microvolts** at the 100-microvolt threshold. The primary stratified finite-sample 95% interval is **[-77.920, 82.364]**, and the approximate t interval is **[1.739, 2.706]**. The bias-calibrated tensor interval is **[-200, 200]**. This is a transparent bounded-data application under independent-subject assumptions, with no demonstrated tensor precision gain or validation of the original Gaussian minimax model. Family dependence and general-population selection cannot be verified. See the [locked protocol](real_data/protocol.md), [pre-outcome sampling amendment](real_data/sampling_amendment.md), and [provenance](real_data/provenance.json).

## Files

- `theory/`: full proofs and status ledger; no old result is silently replaced.
- `code/methods.py`: loading proxies, general Tucker/TT cap interval and protected scalar, sparse-diagonal interval, rank-one minor interval, bounded mean/bias calibration.
- `code/check_theory.py`: independent finite algebra, numerical integration, geometry, inequalities and input checks.
- `code/run_experiments.py`, `run_followups.py`, `run_minor.py`: registered grids, MC runs and per-replicate archives.
- `results/`: configuration locks, analytic proxies, aggregate results and all independent replicate summaries.
- `real_data/`: immutable protocol and amendment records, source metadata, subject tensors, explicit loading, subject/trial provenance, splits, contrasts and inference results. The 762 MiB raw zip is cached outside the repository at the path recorded in provenance; reproduction can redownload it.
- `code/prepare_eeg.py`, `analyze_eeg.py`: schema-checked streaming parser and full analysis with stratified subject splitting.
- `figures/`: five reproducible PDF/SVG figures; PNG files are inspection previews only.
- `paper/`: new report and proof supplement, separate from the preserved submission paper.
- `audit/`: initial 2,733-file baseline hash manifest, complete inherited review registry with continuation fields, correction log, checks, figure audit, adversarial review and final validation.

## Reproduce

Python 3.9.6, NumPy 2.0.2, SciPy 1.13.1, Matplotlib 3.9.4 and threadpoolctl 3.6.0 were used. Pandoc and XeLaTeX build PDFs. The baseline manifest records preexisting files; it is not recreated by the reproduction script. The original protocol hash is checked during validation. The final deliverable manifest excludes its own file, validation.json, and the two logs that are still being written during validation (validation.log and reproduction.log).

Run from this directory:

```bash
bash reproduce.sh
```

This reruns the new finite checks and **all** new simulations, reanalyzes the saved subject tensors, rebuilds the plots/reports/PDFs, and validates outputs. It does not download or reparse raw data, alter previous stages, commit or push.

For raw-data reproduction, download the public archive (network access is needed) and run:

```bash
curl -L --fail -o /private/tmp/tensor_eeg_database_121.zip 'https://archive.ics.uci.edu/static/public/121/eeg+database.zip'
python3 code/prepare_eeg.py /private/tmp/tensor_eeg_database_121.zip
python3 code/analyze_eeg.py
```

The provenance JSON records the expected SHA-256; compare it before treating a different download as the same data version. The parser streams zip/tar/gzip data without extracting archive paths. Both the trial manifest and derived tensors are included, so analysis reproduction does not depend on continued availability of the temporary raw cache.

The [scientific review continuation](audit/adversarial_review.md) retains verdict C for the expanded goals; the preceding focused manuscript's earlier B assessment remains a historical result. No commit, push, external message or submission was performed.
