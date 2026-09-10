# Population Functional Risk for Tensor-Train Compression

This folder contains a theory-first working paper on population functional risk for tensor-train (TT) compression of conditional generators. The main statistical experiment uses finitely many stochastic teacher queries. That access model is stated explicitly because a universal \(d_{\mathrm{TT}}/n\) lower bound is false after moving to white-box access, and can also fail under exact soft-label queries when the sampled teacher probability vectors identify the teacher.

## Main claim

For a finite, coded collection of rank-separated TT models, penalized likelihood achieves

\[
\mathbb E\,\mathcal D_w(\widehat W,W^0)
\lesssim
\inf_{\lambda}
\left\{
A_w^2(\lambda)
+\frac{d_\lambda+\log H_\lambda+\log(1/\pi_\lambda)}{n}
\right\},
\]

where \(d_\lambda\) is the gauge-adjusted dimension of the active TT quotient and \(H_\lambda\) is the size of a finite atlas subordinate to a thresholded projector-pivot cover. A local Assouad construction gives a matching \(d_\lambda/n\) lower bound, and an information-normal teacher family gives \(A_w^2(\lambda)+d_\lambda/n\) under a fixed compression budget and off-chart separation. The exact local asymptotic constant is \(\tfrac12\operatorname{tr}(G_w I_\pi^{-1})\); it equals \(d_\lambda/2\) only for matched conditional-KL sampling with a functionally identifiable quotient.

## Contents

- `paper/main.tex`: complete manuscript, including theorem statements and proofs.
- `paper/references.bib`: primary-source bibliography.
- `notes/idea_evaluation.md`: reviewer-style feasibility and fatal-flaw audit.
- `notes/paper_blueprint.md`: paper logic, contribution-to-challenge mapping, and scope decisions.
- `notes/novelty_audit.md`: dated closest-work audit and collision matrix.
- `notes/theory_decisions.md`: access-model and theorem-qualification record.
- `notes/pre_submission_review.md`: post-revision integrity and readiness audit.
- `code/run_simulations.py`: reproducible synthetic experiments.
- `code/test_simulations.py`: smoke tests for geometry and numerical routines.
- `results/`: generated tables and summaries.
- `figures/`: generated publication figures.

## Reproduce

From this directory:

```bash
python3 code/test_simulations.py
python3 code/run_simulations.py --quick
latexmk -pdf -interaction=nonstopmode -halt-on-error -cd paper/main.tex
```

Remove `--quick` for the larger Monte Carlo run used for a submission draft.

## Scope warning

The manuscript proves a regular-stratum theorem under explicit likelihood, local-entropy, and functional-identifiability conditions. It does **not** claim that gauge dimension alone implies functional dimension, that compression from exact teacher probability vectors always pays \(d/n\), or that rank recovery is uniform near lower-rank strata.
