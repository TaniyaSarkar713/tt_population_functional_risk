# Honest inference for tensor contrasts

**Manuscript:** *Honest Inference for Tensor Contrasts under Tucker and Tensor-Train Rank Bounds.*

**Decision:** Promising — theory requires further work. The complete draft treats a restricted, mathematically specified problem. It does not claim that optimal full-tensor inference or adaptation to actual unknown rank has been solved.

## Start here

- [Compiled paper](paper/main.pdf), [LaTeX source](paper/main.tex), and [complete proof appendix](paper/appendix.tex).
- [Research and publication checkpoint](notes/decision_checkpoint.md): novelty, mathematical improvements, reviewer objections, venue assessments and next theorem targets.
- [Literature review](literature/literature_review.md), [20-paper comparison matrix](literature/novelty_matrix.md), and [44-reference bibliography](literature/bibliography.md).
- [Result ledger](theory/theorem_statements.md), [assumptions](theory/assumptions.md), [proofs](theory/proofs.md), [classical diagonal benchmark](theory/diagonal_minimax.md), and [open questions](theory/open_questions.md).
- [Simulation protocol](simulations/simulation_design.md), [findings](simulations/results/findings.md), [817 configuration/method rows](simulations/results/summary.csv), and [original run manifest](simulations/results/run_manifest.json).
- [Guideline completion map](notes/guideline_compliance.md), [final audit](notes/final_audit.md), [revision provenance](notes/revision_manifest.json), and [application status](real_data/README.md).

## Main mathematical result

Observe Z=A+tau G with independent standard Gaussian entries, a known Frobenius bound M, supplied Tucker or TT upper rank bounds, and a prescribed orthogonal loading. Actual ranks may be smaller and nonzero singular values arbitrarily weak. T1–T2 give a finite-sample honest interval without rank recovery.

For the normalized diagonal contrast, fixed K>=3, fixed rank caps and M=tau sqrt(p), its length satisfies

$$|C_*|\le2\tau J^{1-1/K}\{8\log(2p/\alpha)/p\}^{(K-2)/(2K)}=o(\tau).$$

T3–T5 compare this with every fixed-radius affine interval on the same class and with every interval honest over a larger class retaining one unfolding constraint. Those two classes require order-tau length in the stated senses. Matricization does not discard observations; the second comparison changes the required honesty class.

At rank one, the diagonal image is exactly an ell_(2/K) ball. Proposition 1 (D1) identifies the matching length rate **among diagonal-only procedures**, as a specialization of classical Gaussian sequence theory. This is not a new minimax-rate claim. T6 gives a smaller lower bound for the **full tensor experiment**; its sharp rate remains unresolved.

There are six theorem statements, one attributed proposition and complete supporting proofs. PROVED describes complete checked derivations, not independent peer review or machine-verified mathematics. PARTIAL and CONJECTURED items remain visibly separate.

## Revision and provenance

This folder is a separate complete-paper version of the earlier project in ../honest_tensor_functional_inference. The earlier project is preserved. The original user guidelines are in [notes/guidelines.txt](notes/guidelines.txt).

The revision reorganizes the manuscript, deepens the classical novelty comparison, proves the explicit diagonal confidence-interval benchmark, adds a center-accuracy table, updates the analytic figure and synchronizes the theorem and novelty ledgers. The interval algorithm and original simulation results are unchanged. The previously recorded simulation run has 175 configurations, 2,000 replications each, 172 Gaussian configurations and three out-of-model stress configurations. Additional proof checks are recorded separately.

Primary literature inspection extends through September 9, 2026. The library retains 17 previously downloaded primary PDFs and extracted text under literature/references/prior_sources. Other sources are linked; not all 44 references have local PDFs. Older assessments are preserved as historical records under notes/prior_stage and literature/prior_*. They are not the current decision checkpoint.

## Reproduction

Use Python 3.13 with the recorded dependencies in requirements.txt. No packages were installed during this revision. From this project directory, run the following commands (replace python with python3 if needed):

```sh
python simulations/code/check_theory.py
python simulations/code/check_diagonal_benchmark.py
python simulations/code/run_simulations.py --repetitions 2000
MPLCONFIGDIR="$PWD/simulations/.mplconfig" python simulations/code/summarize_and_plot.py
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error paper/main.tex
```

The simulation uses seed 20260909 and stable configuration-based streams. It generates exact Gaussian marginals needed by the procedures without allocating p^K arrays. Configuration-level output includes coverage, exact binomial confidence intervals, center bias and its Monte Carlo standard error, RMSE and length. Figure 1 evaluates analytic bounds beyond simulated dimensions and labels this explicitly.

The original run manifest records source/result hashes and the software environment. The analysis manifest records figure/table generation; the revision manifest identifies reused versus revised files. Bitwise floating-point agreement across platforms is not guaranteed.

No real-data or LLM experiment is included because a suitable sampling model has not been justified. No paper was submitted or published.
