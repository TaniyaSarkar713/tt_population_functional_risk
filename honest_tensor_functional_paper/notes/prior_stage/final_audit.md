# Final audit of the working draft

Date: September 9, 2026. Scope: manuscript main text and full appendix, theorem ledger, source matrix, scientific code, saved CSV, generated tables, PDF build and figure previews. This is an internal audit, not independent peer review or formal proof verification.

**Recommendation: Needs major theoretical development before submission to the requested strong venues.** The draft is complete as a working note and compiles cleanly. Submission-readiness score: **6/10**. Research-readiness findings: **1 CRITICAL, 3 MAJOR, 0 MINOR**. There are no remaining build/reference warnings identified by the mechanical checks.

## Macro logic and substantive findings

| ID | Exact text / object reviewed | Severity | Assessment and concrete next step |
|---|---|---|---|
| C1 | Introduction: “its elementary ingredients make a reduction to existing general theory a serious remaining novelty question.” | CRITICAL for a strong-journal submission | The central result needs a stronger novelty/importance case. Compare the exact diagonal reduction and T5 against nonconvex functional theory; obtain a full-tensor insight or retain this as a note and pivot the main contribution |
| M1 | Section 5.3: “sharp minimax length is PARTIAL” | MAJOR | The proved upper/lower scales differ by a polynomial factor. Determine a sharp rate or prove an equally substantial loading/adaptation theorem before claiming a strong statistical contribution |
| M2 | Discussion: “the restricted loading, loose growing-rank constants, known norm and noise bounds, and lack of actual-rank adaptation.” | MAJOR | Extend one scientifically important part of the inferential scope with a complete theorem; do not add several unproved extensions |
| M3 | Section 6.2: “The selected interval is substantially conservative.” | MAJOR | Improve calibration or explain a sharp tradeoff. Coverage near one is not evidence of optimal interval length |

The three contribution bullets map to delivering sections and appendix proofs. The normalized diagonal running example is consistent across introduction, method and experiments. Real-data claims are explicitly absent because a matching sampling model has not been justified. Generic skill suggestions requiring three real datasets or a method-architecture figure do not apply to this scalar theoretical note and the user's conditional application request.

## Mathematical audit

- T1: Tucker slice expansion and TT prefix squared-weight induction establish the claimed finite J envelope. TT path terms are not assumed orthogonal. The proof does not use a minimum singular value or an unbounded CP cancellation argument.
- Exact-image lemma: the signed product construction recovers any diagonal in the ell_(2/K) ball with the required Frobenius norm. This supports the classical-reduction limitation.
- T2: the threshold is lambda, the error envelope uses 2lambda, and the Gaussian tail bound has the correct 2m factor. The direct loading norm is one. The structural radius is justified by an explicit rank-projection/eigenvalue argument. Selection of the minimum radius is deterministic.
- T3: both arbitrary affine offset and use of the full tensor are allowed. The normal-shift coverage and worst-coordinate bias bounds are combined correctly. Random widths are not covered or claimed.
- T4: mixture alternatives belong to the selected unfolding class, generally not the joint class. The common target, Gaussian likelihood identity, cosh bound, chi-square/TV conversion and expected-length argument are explicit. The statement concerns a relaxed honesty class, not information loss from reshaping the observed tensor.
- T5: substituting M=tau sqrt(p) gives beta=(K-2)/(2K); fixed caps and K>=3 are required for o(tau). The growing-cap condition is retained. No computational transition or oracle optimality is inferred.
- T6: the sparse-coordinate mixture has chi-square (exp(a^2/tau^2)-1)/p. Its lower bound does not match T2 and is not described as sharp.

Every numbered theorem has a full proof. The manuscript has six theorem statements and eleven proof environments (six theorem proofs plus five lemmas). PROVED labels describe these supplied derivations; unknown rates and adaptation claims remain PARTIAL or CONJECTURED. No mathematically established result is described as independently certified.

## Numerical and reproducibility audit

The saved run contains 175 configurations, 2,000 replications each and 817 method rows. There are 172 iid Gaussian configurations and three stress configurations. Exact coverage intervals contain the reported coverage estimates. Deterministic widths have zero Monte Carlo standard error. A selected configuration was rerun with the recorded stream and all scalar metrics matched exactly. The simulation algorithm files match their original run hashes.

The numerical theory checks pass for the 101,101 scalar grid cases, 120 random tensors per format, finite-binomial mixture moments and signed exact-image constructions. Maximum observed TT squared-weight identity error is 8.89e-15; the exact-image reconstruction error is 5.56e-17 or smaller. These are floating-point sanity checks, not a probability bound or proof of a universal statement.

The theory checker was extended after the scientific run to check the exact-image lemma; the simulation algorithm did not change. This provenance is recorded in `verification.json`, while the simulation-time and figure-generation manifests retain their respective source snapshots. No repeated full simulation was needed for this proof-only addition.

## Writing, grammar and citations

The abstract names the experiment, method, proven comparison, empirical finding and unresolved gap. Statements of actual-rank adaptation and unrestricted minimax optimality are expressly excluded. A complete case-insensitive scan of `main.tex` and `appendix.tex` found no listed hyperbolic vocabulary or body em-dashes. Bibliographic titles are preserved rather than rewritten to satisfy body-style preferences.

No specific unresolved article, agreement or relative-clause error was identified in the reviewed text. This is not a claim that further editorial improvement is impossible. The bibliography has 44 unique entries; all 26 manuscript citation keys resolve. The revised closest-paper matrix contains 20 entries and now records the additional Cai–Low full-text examination. Source-inspection depth is explicit; not every bibliography entry received a complete proof audit.

## LaTeX and figures

The final PDF has 18 pages. `latexmk -pdf -interaction=nonstopmode -halt-on-error` completed successfully. The final log contains no undefined references/citations, overfull boxes or other warnings. All equation labels are referenced and all figure/table labels resolve. No target venue or page limit has been imposed on this research draft.

Both manuscript figures use vector PDFs generated from code. Font settings are nine points on a 6.6-inch canvas, keeping labels above eight points at the manuscript's near-full-width scaling. Colors are accompanied by line styles or markers. The theoretical plot explicitly separates analytic formula evaluations up to p=10^12 from simulated dimensions up to 8192. The weak-rank plot uses exact binomial intervals and labels categorical epsilon spacing. Source figure previews and rendered manuscript pages 1 and 12 were inspected for clipping and mathematical layout; no issue was identified.

## Integrity gate

Findings quote actual text and give concrete next steps. Severity distinguishes unresolved scientific readiness from document mechanics. The full body scan, build and artifact checks were run, with a machine-readable record in `verification.json`. No plagiarism certification, independent mathematical review or journal acceptance prediction is implied. The recommendation and score reflect the remaining critical novelty question and three substantive limitations.
