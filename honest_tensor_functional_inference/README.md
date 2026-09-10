# Honest tensor functional inference

**Working title:** Joint Tensor Rank Constraints Can Shorten Honest Functional Confidence Intervals.

**Decision:** Promising — theory requires further work. This project provides a complete working research note and reproducible experiments. It does not solve the broad original problem of optimal, rank-adaptive functional inference for arbitrary Tucker/TT loadings, and is not ready for submission as that stronger paper.

## Start here

- [Compiled manuscript](paper/main.pdf), [LaTeX source](paper/main.tex), and [complete proof appendix](paper/appendix.tex).
- [Research and publication decision](notes/decision_checkpoint.md): what is new, which comparisons are proved, venue assessments, reviewer objections and the next theorem targets.
- [Literature review](literature/literature_review.md), [20-paper novelty matrix](literature/novelty_matrix.md), and [44-reference verified bibliography](literature/bibliography.md).
- [Theorem ledger](theory/theorem_statements.md), [assumptions](theory/assumptions.md), [derivations](theory/proofs.md), and [open questions](theory/open_questions.md).
- [Simulation protocol](simulations/simulation_design.md), [findings](simulations/results/findings.md), [configuration-level results](simulations/results/summary.csv), and [run manifest](simulations/results/run_manifest.json).
- [Final audit](notes/final_audit.md) and [application status](real_data/README.md).

## What was established

For Z=A+tau G with known Gaussian noise, a known norm bound M, supplied Tucker/TT rank caps and a prescribed orthogonal loading, T1–T2 give a finite-sample honest interval without a minimum nonzero singular value. For the normalized diagonal contrast, fixed K>=3 and M=tau sqrt(p), its length is at most

$$2\tau J^{1-1/K}\left\{8\log(2p/\alpha)/p\right\}^{(K-2)/(2K)}=o(\tau).$$

T3–T5 compare this with every fixed-radius affine interval on the same class and every interval honest on an enlarged one-unfolding class, both requiring an order-tau length in the specified sense. T6 gives a smaller within-class lower bound; the resulting polynomial minimax gap remains unresolved. The rank-one diagonal image is exactly an ell_(2/K) ball, so the method is a classical sequence-space construction. The explicit joint-constraint comparison is the potential novelty, subject to further literature scrutiny.

PROVED means a complete derivation is supplied and checked algebraically, with numerical sanity checks. It does not mean independent peer review or machine-verified mathematics. PARTIAL and CONJECTURED items are explicitly separated in the ledger and manuscript.

## Reproduction

Run commands from this project directory, using Python 3.13 (the recorded environment used 3.13.9). A separate virtual environment is optional. Install dependencies with `python -m pip install -r requirements.txt` if needed; no packages were installed into the user's environment for this run.

```sh
python simulations/code/check_theory.py
python simulations/code/run_simulations.py --repetitions 2000
MPLCONFIGDIR="$PWD/simulations/.mplconfig" python simulations/code/summarize_and_plot.py
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error paper/main.tex
```

The reference run has 175 configurations, 2,000 independent replications each, 817 method/configuration rows and seed 20260909. Random streams are derived from stable configuration hashes. The code generates exact required marginals of the Gaussian tensor experiment instead of allocating p^K arrays. The full scientific simulation finished in about 16 seconds on the recorded machine; this is not a comparative runtime claim. Results contain exact binomial intervals even when empirical coverage is one. Figure 1 evaluates analytic formulas beyond the simulated dimension range and labels them accordingly.

`run_manifest.json` records the simulation-time versions and source hashes. `analysis_manifest.json` records figure/table generation. Numerical verification is separate from simulation. The environment snapshot is descriptive; bitwise identity of floating-point linear algebra across platforms is not guaranteed.

## Organization and provenance

All new work is in this folder. The earlier broad survey is preserved under `literature/prior_*`, and 17 previously downloaded primary PDFs and extracted text are retained under `literature/references/prior_sources/`. Additional references are linked and their local download status is recorded separately; not every bibliography entry has a local PDF. The current survey cutoff is September 9, 2026, with accepted papers and preprints identified as such.

The original broader project has not been modified by this new research folder. No external publication, submission, data collection, communication or real-data experiment was performed.
