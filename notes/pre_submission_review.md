# Pre-submission review

Date: 7 September 2026  
Artifact reviewed: complete theory-first working draft  
Current verdict: **major revision before submission**

## Executive assessment

The paper now contains a coherent statistical experiment, a population
conditional-KL target, a gauge-adjusted TT oracle inequality, a matching
modelwise lower bound, a fixed-resource approximation--estimation lower
construction, local asymptotic constants, and complete proof appendices. The
flagship claims are stated under explicit access, rank-separation,
identifiability, entropy, and likelihood assumptions. An independent
adversarial theory pass found no remaining critical or major logical defect in
the scoped theorem proofs after the final atlas and Bernstein-chaining repairs.

This is nevertheless a research draft, not a journal-ready submission. The
remaining weaknesses concern how much of the regularity structure is verified
for realistic frozen generators, whether optimization reaches the localized
estimator analyzed by the theory, and whether the functional metric predicts
compression choices in open models.

| Severity | Count | Interpretation |
|---|---:|---|
| Critical | 0 | No known contradiction or broken flagship proof remains. |
| Major | 5 | Substantial theory-to-model and empirical gaps remain before submission. |
| Minor | 7 | Presentation, format, and metadata refinements remain. |

## 1. Macro logic and statistical contribution

### Strengths

- The estimand is one common deployable student evaluated by a truth-first
  population conditional KL over a declared deployment mixture.
- The stochastic-query experiment is separated from exact-soft-label and
  white-box access. The manuscript therefore does not export a \(d/n\) lower
  bound to an experiment in which the parameter may be identified without
  response noise.
- The upper and lower results use the same gauge-adjusted local dimension.
  Fisher information appears only in the local quadratic and LAN
  specializations.
- The approximation-plus-estimation statement is limited to a fixed resource
  class with an explicitly imposed off-chart gap. The paper does not claim
  sharp adaptive union penalties.
- Same-data multi-capability certification is clearly secondary and is
  identified as an application of classical stability and bounded
  differences, not a new concentration principle.

### Major issues

1. **Atlas constants remain implicit.** The finite projector-pivot atlas is
   valid on a compact rank-separated quotient, but the dependence of
   \(H_\lambda\) and \(C_{\mathrm{atlas},\lambda}\) on TT order, ranks,
   unfolding gaps, and nonlinear-block depth is not sharp enough for a final
   rate comparison.
2. **The global separation condition is assumed.** The information-normal
   tube constructs the desired local approximation geometry, but the
   off-chart KL gap has not been verified for a broad, natural resource class.
3. **Optimization is external to the theorem.** The result permits an
   optimization tolerance but does not show that a practical nonconvex TT
   fitting algorithm enters and remains in the required chart.
4. **Sequence-level likelihoods are not covered.** The main proof uses bounded
   or truncated per-query log likelihoods; long autoregressive sequences need
   martingale or subexponential control.
5. **No open-model falsification study is included.** Current experiments
   validate quotient dimension, the local \(d/(2n)\) law, access-model
   distinctions, Gaussian adaptation, and exact Bernoulli-KL metric
   misordering, but they do not establish a practical LLM compression gain.

## 2. Writing and positioning

- The paper is correctly positioned as a **new statistical problem/setting**
  rather than as a claim that TT entropy bounds, KL distillation, Fisher-aware
  compression, or stability concentration are individually new.
- The introduction follows the required chain: deployment mismatch, limits of
  existing parameter-space theory, population estimand, geometric and
  statistical obstacles, solution, and qualified contributions.
- Novelty language is deliberately conjunctive: the residual claim is the
  combination of a black-box conditional-generator experiment, TT quotient
  geometry, a population task-functional oracle, and its matching
  gauge-dimensional lower theory.

Minor work:

1. Select a target journal and convert the generic article source to its
   current class, bibliography style, anonymization rules, and supplement
   format.
2. Recheck all 2026 preprint metadata, author names, versions, and venue status
   immediately before circulation.
3. If the target is a primarily theoretical statistics journal, reduce the
   LLM-specific empirical promises; if the title retains LLM motivation, add
   the preregistered open-model experiment.

## 3. English and style

- A mechanical scan found no em dashes and no unqualified performance
  superlatives.
- Literal uses of the “reveal” family were replaced by “provided directly”;
  the final manuscript scan has no mechanical AI-tone hit from that wording.
- Dense related-work sentences and ambiguous antecedents identified in the
  first pass were copyedited.

Minor work:

1. Perform a final journal-style copyedit after the target template is chosen.
2. Keep “conditional log-score/KL risk” in the abstract rather than the
   broader “proper-score risk,” because the proved flagship theorem is for
   log loss.

## 4. LaTeX and bibliography

- All citation keys and theorem labels resolve in the current source.
- The final clean build is 37 pages and contains no undefined-reference,
  citation, overfull-box, underfull-box, or malformed-command warnings.
- The final LaTeX source passes lacheck.
- The generic 11-point layout is for drafting only and currently produces a
  long main document; proofs will probably need a supplement under a journal
  template.

Minor work:

1. Decide whether rarely referenced numbered displays should be cross-referenced
   or made unnumbered.
2. Label naming can be normalized mechanically when the journal source is
   frozen; this does not affect correctness.

## 5. Figures and computational evidence

- All final figures are vector PDFs with marker or line-style encodings in
  addition to color.
- The simulation suite contains direct assertions for gauge-dimension
  identities and the equal-budget TT metric-misordering construction.
- The Gaussian sequence experiment is an illustration of the separate
  approximation benchmark, not evidence for nonlinear conditional-generator
  fitting.

Required empirical extension:

1. Fit an actual TT block inside at least two frozen open model families.
2. Compare population/held-out KL selection against TT-SVD or Frobenius error,
   Fisher-weighted or loss-aware baselines, and equal-storage rank choices.
3. Include a normal-direction sweep testing \(a^2+d/n\), multiple deployment
   mixtures, stochastic versus exact-soft-label queries, and confidence-band
   coverage across capabilities.
4. Publish seeds, model revisions, prompts, environment versions, and
   preregistered exclusion and stopping rules.

## Integrity gate

- **Theoretical claims:** Pass under the printed assumptions; theorem
  generality is deliberately limited.
- **Empirical claims:** Pass. All reported evidence is synthetic and is called
  synthetic; no practical LLM improvement is asserted.
- **Citation claims:** Pass against the dated primary-source novelty record,
  subject to a final pre-submission metadata refresh.
- **Reproducibility:** Pass for the current simulation suite after a clean
  direct test, quick smoke run, and full Monte Carlo rerun.
- **Submission readiness:** Fail pending the five major items above.
