# Revised manuscript plan

The user's pasted guidelines are preserved in `guidelines.txt`. The existing survey and derivations are the source material. A separate project copy preserves the earlier research note.

## Position and running example

Type: theoretical setting/comparison paper. The central question is whether joint tensor rank restrictions can improve honest functional interval length beyond a single-unfolding honesty class. The running example is a p-by-p-by-p Gaussian mean tensor, n=p replicates, norm bound one and normalized diagonal sum. The paper studies prescribed orthogonal contrasts and supplied rank caps; it does not claim arbitrary-loading inference or actual-rank adaptation.

## Introduction logic

1. Explain why weak or disappearing components make a uniform coverage requirement relevant; introduce the concrete diagonal contrast.
2. State the three relevant precedents: regular tensor functional inference, weak/unknown matrix rank inference, and classical nonconvex Gaussian functionals.
3. Define the precise joint-versus-relaxed honesty comparison and its order-tau benchmark.
4. Identify three proof tasks: control the diagonal without a signal floor; prove an all-procedures lower bound on the relaxed class; distinguish diagonal-only and full-data optimality.
5. Map those tasks to canonical expansions, a threshold envelope and common-target mixtures. State the exact diagonal reduction and credit the classical benchmark.
6. End with three section-linked results: cap-uniform interval; joint/affine separations; the diagonal benchmark and unresolved full-data bracket.

The target is a substantive statement about parameter constraints. There is no new thresholding algorithm or tensor Schatten exponent claim. Collier–Comminges–Tsybakov moves into the closest-paper matrix after the deeper theorem inspection.

## Main paper structure

Abstract; Introduction; Related Work with precise mathematical comparisons; Statistical Experiment and Assumptions; Interval Construction; Statistical Theory and a summary comparison table; Simulations; Discussion. A short discussion paragraph explains why a real-data/LLM experiment is not scientifically justified by this model. The appendix contains every proof, including an explicit classical confidence-interval specialization for the diagonal-only experiment, a status table and supplementary experimental details.

## Figure plan

Keep the two scientific figures. Extend the second panel of the analytic comparison with the diagonal-only lower bound. Label full-data and diagonal-only bounds distinctly; do not transfer the marginal lower bound to the full experiment. Keep the weak-rank coverage figure with exact binomial intervals. Use vector PDF, nine-point labels and dual color/style encoding. Existing simulation results remain valid because the interval algorithm is unchanged; this revision adds proof checks and analytic curves.

## Integrity checks

Contribution-to-proof links, all assumptions and known constants, comparison classes, no first-in-literature assertion, exact simulation provenance, classical attribution and the remaining polynomial full-data gap must survive the revision. Publication evaluation belongs in a companion checkpoint, with scientific limitations retained in the paper. A completed manuscript is distinct from a journal-ready contribution.
