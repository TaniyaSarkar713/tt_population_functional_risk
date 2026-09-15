# Writing, notation, figures and tables

The pre-submission-reviewer skill informed this audit. The user's scientific severity definitions take precedence over automatic stylistic severity: an obsolete figure or long paragraph is not called a CRITICAL mathematical defect. A theory paper is not required to manufacture an architecture diagram, three datasets or an LLM application. Proposed edits are review recommendations; the original documents are preserved.

## Five-dimensional presentation assessment

| Dimension | Judgment and evidence | Severity / action |
|---|---|---|
| Macro logic | The integrated paper explains the Gaussian experiment and honesty-class comparison, but its 55 pages predate the two supplements and the new empirical study. Six contribution bullets mix central sharpness with routine and historical refinements | MAJOR, F03: one final narrative and proof chain, focused on sharp full-data rates; concise method-status table |
| Writing details | Paragraph topics are generally explicit; the running flat-diagonal example is consistent. Repeated gap/open-question paragraphs and sequential stages dilute the final result. Abstract is dense and historically scoped | F03/F10: replace obsolete gap narrative; proposed abstract supplied; move superseded material rather than adding another layer |
| English grammar | No repeated article, agreement, tense, relative-clause or nonidiomatic construction was identified as a material defect in the active text | No invented grammar-rule violation. Mathematical precision and organization deserve attention before cosmetic rewriting |
| LaTeX / references | 132 integrated labels; no duplicate or unresolved reference labels; all 34 cited keys exist in the integrated bibliography. Five active PDFs parse with no text spans outside page bounds and no replacement characters | Mechanical source/PDF checks newly run; full citation accuracy and exhaustive priority are outside this stage's scope. Global symbol consistency still needs F10 |
| Figure/table quality | Four integrated manuscript figures and ten current empirical figures freshly inspected; all 14 are vector PDFs with no embedded raster images. Labels, legends and uncertainty generally readable | Replace the obsolete leading gap figure; keep scope/uncertainty conventions in captions. Details below |

The active-source scan covered 22 files, including the integrated TeX inputs, both supplement theory files and their generated TeX, the new empirical report and manuscript insert. It found **zero hits** for the skill's listed banned vocabulary patterns and em-dash patterns; [style_scan.json](tables/style_scan.json) records the result and `code/inventory.py` records the exact search patterns. Bibliographic author/title punctuation is not treated as prose to rewrite. This is a reproducible lexical scan, not a universal detector of writing quality.

Visual inspection included all 14 individual figures and integrated manuscript pages 1, 9, 16, 26, 36 and 55. All five active PDFs were also scanned programmatically across every page. The integrated paper was compiled in an isolated copy; the build log and result are in [presentation_checks.json](results/presentation_checks.json). Visual sampling cannot exclude every local typesetting issue on unrendered pages, and a syntactically resolvable citation does not establish its scientific accuracy.

## Figure audit

| Figure | What it communicates / visual checks | Scientific or presentation action |
|---|---|---|
| Main: `theoretical_comparison` | Readable log-scale rate comparison with labeled classes and an intermediate full-data gap | Move to a historical appendix or replace by the final all-budget cubic/higher-order rate diagram. Caption acknowledges its early-stage status, but this should not be the lead visual of the final theorem |
| Main: `weak_rank_coverage` | Clear coverage/length panels near a vanishing second singular value; categorical spacing is identified | Retain only if it adds to the new signal sweep. “No actual-rank adaptation” should mean no rank tracking/width change here, not failure of A1's fixed-cap rate statement |
| Main: `adaptive_intervals` | Readable length ratio and coverage against singular value/pilot bound; shaded region marks separation violation | The separated selector is not A4/P1. Keep the distinction explicit when integrating the newer honest-cap method |
| Main: `robustness_and_loadings` | Full binary-net feasibility versus noise laws, and calibrated loading-residual length; appropriate bars/units | Explain that feasibility is a component event. Could move to supplement when current figures 05/07 cover the same concepts |
| Empirical 01: growing rates | Log axes and deterministic length curves; clear $p$ and $n$ sweeps | Retain as a computable matched regime; zero bars reflect deterministic lengths, not extraordinary empirical precision |
| Empirical 02: weak threshold | Separate orders three/four; readable log scale and selected/raw method legend | Good executable weak-signal example; caption correctly denies full-data ideal attainment |
| Empirical 03: pointwise rates | Cap-one and growing-cap panels; 1.96-SE length bars; XCH/oracle overlap visible | Retain strong-signal and cap-rounding qualifications. Overlap is substantive, not missing curves. Prefer explicit rate-normalized inset if main space allows |
| Empirical 04: signal sweep | Symlog axes preserve zero; Wilson coverage and mean-length bars; regular/separated failures visible | Add that $M$ changes along the sweep; a fixed-$M$ panel would isolate the signal effect (F05) |
| Empirical 05: noise | Correlation and noise-law panels clearly distinguish naive and calibrated methods | Valid illustration of calibration and mean-shift limits. Category labels and captions explain standardization/proxy types |
| Empirical 06: solver | Log mean endpoint gaps and Wilson certification fractions; bootstrap gap bars | Nonmonotone certification can reflect the changed tolerance at the first budget. Different signal cases also use different fixed loadings. Keep current caveats; add a fixed-tolerance/loading experiment before a causal budget interpretation |
| Empirical 07: corrections | Two distinct loading/approximation bias mechanisms with visible catastrophic misses | Keep: materially informative adversarial construction. These corrections are conservative implemented bounds, not the general sharp fit |
| Empirical 08: power and pivots | Exact direct power reference and regular-signal/oracle comparisons; QQ axes readable | No normality result for the nonlinear midpoint is tested. Prefer mathematical $\tau\sqrt{r/p}$ in final label instead of code-like text |
| Empirical 09: runtime | Log time and traced-allocation scaling with explicit uncertainty conventions | Current caption properly says one SE and excludes native/input memory. Add tensor entry count for readers comparing mode dimensions |
| Empirical 10: intermediate caps | Shows the upper interval and ratio to an analytic lower bound across caps | Useful visualization of a remaining gap. The lower reference is a testing bound with constants, not an attained competitor; cap grid does not establish a sharp transition |

No new AI-generated figure was appropriate: these are scientific vector plots and PDF review artifacts. A final paper could use three main figures: the final theoretical rate comparison, representative weak/strong coverage and length, and computational gaps or correction failures. Additional suites belong in the supplement. An architecture diagram would add little to a Gaussian inference paper.

## Table audit

The integrated analytic assumption/comparison tables use explicit procedure and honesty classes, which prevents a common misreading of lower bounds. The selected-interval rate in the historical comparison is an attainable diagonal upper bound, not the final full-data optimum; the final row correctly points to the stronger theorem. When integrating, replace historical cross-references with the final rate notation and avoid making the reader jump through superseded bounds.

The empirical report's count, coverage, slope, finite-geometry, precision, failure and power tables have appropriate units and uncertainty. Coverage rounded to three decimals and short significant-digit length/SE displays are reasonable. Full machine-readable precision in CSV/JSON is appropriate for reproducibility and should not be copied verbatim into publication tables. Length/risk ratios must identify the analytic scale, not imply exact minimax constants. Highlighting does not appear to conceal inferior results; the regular comparator is often shorter than the cap-valid method in its favorable regime.

F01 requires correction in the underlying coverage rows and any derived paired-coverage/diagnostic tables. F09 requires an estimator-level identifier for losses repeated across confidence levels. All stored risk and paired-difference summaries were recomputed during review; no rounding of table displays was used to assess their numerical agreement. Original and follow-up calibration tables must remain separate, and solver counts must remain solves versus independent observations.

## Global notation audit

| Current collision / ambiguity | Where it matters | Suggested convention |
|---|---|---|
| $D$ as ambient dimension, degree or envelope coefficient | Integrated setup, low-degree theory, refinements | $D_{\rm amb}$, $d_{\rm poly}$ and $C_{\rm diag}$ |
| $q$ as $2/K$ and Gaussian critical value | Threshold geometry versus split projection | $q_K$ and $z_u$ |
| $\eta$ as approximation budget, pilot bound or total-variation constant | Robust section and both supplements | $\varepsilon_A$, $\eta_{\rm op}$ and $\varepsilon_{\rm TV}$ |
| $J$ as component count or overlap | CP/TT geometry and mixture proofs | $J_{\rm cap}$ and $H$ |
| Loading tensor and loading-dependent bound both indexed by $w$ | Weighted-rate envelopes | $L_w$ for the tensor; $\underline R(w)$ and $\overline R(w)$ for bounds |
| Supplied rank versus actual rank and effective minimum cap | Main theory, G1 and P1 | $\bar r_k$, $r_k(A)$ and $r_{\min}$; state when all supplied mode caps equal $r$ |
| “Tangent” for a larger product-subspace projector | A4/P1 versus XCH exact manifold tangent variance | Name the cap projection $\mathcal T_Q$ and separately define $P_{T_A}$ for the exact manifold tangent space |
| “Minimax optimizer” for existence fit versus executable search | C1/C2 and empirical comparisons | “Ideal residual fit,” “binary global search,” and “cap-valid split interval,” each with its own error/output contract |

No dimensionally invalid tensor operation was identified in the reviewed statements. Fixed-order constants and Kronecker projection dimensions are explicitly used in the proof audit. The task is consolidation of local notation, not correction of an established dimension mismatch.

## Integrity gate

The review preserves pre-existing research files, stores its own evidence and reproduction logs, and does not claim new experiments where it only recomputes saved data. Its simulated reviewers are explicitly labeled. Source-key and rendering checks do not certify citation accuracy or prove theorems. No fabricated real-data section or general efficient optimizer is introduced. Scientific submission remains blocked by the P0 revisions, rather than by a stylistic checkbox or an unsolicited approval rule.
