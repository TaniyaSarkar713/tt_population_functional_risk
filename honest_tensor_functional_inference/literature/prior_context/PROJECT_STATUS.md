# Project status

Date: 7 September 2026

## Completed in this working draft

- A complete LaTeX manuscript with abstract, introduction, related work, experiment, geometry, oracle theorem, matching lower results, rank boundary, functional misordering, same-data certification, experiments, discussion, and proof appendices.
- An explicit split among finite stochastic teacher queries, exact-soft-label queries, and white-box access.
- Gauge-adjusted TT dimension and functional-identifiability caveat.
- A thresholded projector-pivot cover, a finite local TT atlas, and a
  uniform-entropy repair.
- Modelwise and smooth information-normal approximation-plus-estimation lower bounds with off-chart separation.
- An independent line-by-line theory audit and repairs to KL orientation, global localization, LAN, rank recovery, and the adaptive benchmark.
- A dated primary-source novelty audit, including the Michel–Nouy tree-tensor oracle collision and the 2026 LoRA matching-bound collision.
- Reproducible simulation code and smoke tests.
- Full synthetic Monte Carlo outputs and four publication figures.
- A synchronized 37-page PDF from a clean build with no final LaTeX warnings;
  the source also passes lacheck.

## Current numerical checks

- Generic TT contraction Jacobian ranks: 13, 36, and 69, exactly matching raw cores minus gauge dimensions.
- At \(n/d=64\), normalized black-box conditional-KL risks: 0.497, 0.502, and 0.510; sharp asymptotic target: 0.5.
- Exact soft labels under correct specification: zero numerical estimation risk.
- Exact rank-one TT misordering: all five information ratios reverse the Frobenius choice; exact KL improvement ranges from 1.294 to 20.707.
- Gaussian approximation–estimation selector: mean selected/oracle risk ratio 1.062 over the five sample sizes.
- All smoke tests pass.

## Required before journal submission

1. Sharpen the atlas constant into transparent rank, order, separation, depth, and activation dependence for the nonlinear frozen block.
2. Discharge the off-chart KL-separation assumption for a nontrivial full resource class.
3. Prove or certify an optimization-localization result for the proposed TT fitting routine.
4. Extend bounded/truncated response theory to sequence-level martingale or subexponential log likelihood.
5. Run the preregistered open-model falsification study on at least two model families and compare all current loss-aware baselines.
6. Decide whether to retain the secondary same-data certificate after seeing its empirical width; remove it if it distracts from the sharp core theorem.

## Honest readiness assessment

This is a complete **research draft**, not a submission-ready proof artifact. The mathematical claims are explicit and accompanied by proofs under stated assumptions, but journal-level acceptance will depend on making the TT/nonlinear verification less assumption-driven and demonstrating that the functional ordering predicts real held-out behavior.
