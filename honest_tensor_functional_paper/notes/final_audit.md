# Final audit of the complete manuscript draft

Date: September 9, 2026. Scope: the revised manuscript and appendix, theorem and novelty ledgers, reused scientific code/results, new diagonal benchmark, generated figures/tables and compiled PDF. This is an internal audit, not independent peer review or formal proof verification.

**Document decision:** Complete draft with a clean build. **Research decision:** Promising — theory requires further work. **Strong-venue submission readiness: 5/10.** Substantive findings: **1 CRITICAL, 3 MAJOR**; no remaining mechanical defect was found in the checks below. The readiness score concerns the scientific contribution, not the completeness of the delivered files.

## Macro logic and substantive findings

| ID | Reviewed text or object | Severity for submission | Assessment and next step |
|---|---|---|---|
| C1 | Section 5.4: “It is a benchmark for the proposed use of diagonal information, not a new Gaussian-sequence minimax principle.” | CRITICAL | The diagonal rate is classical. The joint-constraint separation needs an independent novelty/importance assessment against general nonconvex functional theory. A stronger paper should establish the value of full-tensor observations or a comparably substantial geometric/adaptation result. |
| M1 | Section 5.3: “sharp full-data minimax length is PARTIAL” | MAJOR | Upper and lower scales differ by a polynomial factor. Proposition 1 closes only the diagonal-information problem; obtain a full-data result before making a sharp minimax claim. |
| M2 | Discussion: “The loading must have the orthogonal product form, the Frobenius and rank caps are supplied, and the noise standard deviation is known.” | MAJOR | These restrictions delimit the theorem. Extend one statistically important part with proof; routine plug-ins are insufficient. Actual-rank adaptation remains open. |
| M3 | Section 6.2: “The selected interval is substantially conservative.” | MAJOR | High coverage is accompanied by shrinkage bias and loose calibration. The new center-accuracy table makes this visible. The proved comparison is useful, but it is not efficiency or unrestricted dominance. |

The three contribution bullets map to the delivered results and proofs. The running third-order example is consistent with the asymptotic regime. The title refers to rank bounds, and the manuscript distinguishes honesty under supplied caps from adaptation to the actual rank. No real-data or LLM result has been fabricated.

## Mathematical review

- T1 uses exact orthonormal Tucker slicing and a left-canonical TT prefix-weight identity. TT path terms are not assumed orthogonal; the number of terms and squared-weight identity are explicit.
- The exact-image lemma includes both directions and handles signs. It proves equivalence only for the observed diagonal marginal, not the full experiment.
- T2 uses the threshold lambda and the correct 2lambda error envelope; Gaussian tails have the 2m factor. The structural bound and deterministic choice of the smallest radius are proved.
- T3 allows arbitrary deterministic affine offset and full-data coefficients. It compares fixed radii only; no random-width lower bound is claimed.
- T4's alternatives lie in a single-unfolding class and generally outside the joint tensor class. The common target, likelihood second moment, cosh bound and total-variation conversion are explicit. Matricization preserves the observations.
- T5 substitutes M=tau sqrt(p) correctly, requires K>=3 for a positive exponent, and retains the growing-cap condition. It makes two separate comparisons with different procedure or honesty classes.
- T6 is the coordinate-mixture full-data lower bound; it is not sharp on present evidence.
- D1 is explicitly attributed as a classical benchmark. The support alternatives satisfy the rank/norm constraints, and all share a target. The exact hypergeometric factorial-moment bound establishes the finite-length lower bound. The floor choice of support gives matching diagonal rates. The proof explicitly identifies the full-data overlap power K, where an invalid transfer would fail.

The paper contains **six theorems, one proposition, five lemmas and twelve complete proof environments**. Numbering these statements does not create seven independent novelty claims. PROVED describes the supplied derivations; the full-data minimax and adaptation questions remain PARTIAL, and the proposed zero-point improvement remains CONJECTURED.

## Numerical evidence and provenance

The original scientific simulation is reused: 175 configurations, 2,000 replications each and 817 method/configuration rows. There are 172 iid Gaussian configurations and three out-of-model stress configurations. The interval and simulation-driver files, saved CSV and configurations are byte-identical to the prior project. Their original run-time hashes are preserved.

This revision adds the diagonal benchmark proof and its numerical checks: 24 hypergeometric cases and enumeration of 3,136 pairs of supports. The exact checks pass; the largest checked log second moment is below 1/4. The earlier scalar, random-tensor, TT weight and exact-image checks are retained with their provenance rather than advertised as newly rerun.

The new accuracy table is generated from the saved CSV. Its support choices represent all three prespecified support types at one disclosed configuration; it is descriptive. Bias standard errors, RMSE and lengths use the same normalization. The analytic figure now includes the diagonal-only lower curve and gives its support choice. No new stochastic simulation or algorithm comparison is invented.

## Writing and references

The abstract names the statistical problem, method, comparison theorem, empirical coverage and unresolved full-data gap. The related-work section explicitly credits classical sparse-sequence rates and states mathematical differences from regular tensor and weak-factor inference. The closest-paper matrix has 20 entries, with Collier–Comminges–Tsybakov promoted after deeper inspection. The bibliography file contains 44 unique references; the manuscript cites 29 of them.

A case-insensitive body scan found no listed hyperbolic vocabulary, placeholder markers or em dashes. Bibliographic titles are preserved. No specific remaining grammar error was identified, although further editorial review may improve the draft. Every citation key resolves, every numbered equation is referenced, and all local manuscript inputs exist.

## LaTeX and visual review

The final PDF has 22 pages, including proofs and references, with two vector figures and six tables. The final LaTeX log has no warnings, unresolved references/citations, overfull boxes or underfull boxes. No target-venue page limit was imposed.

The generated analytic figure and rendered manuscript pages containing the title/abstract, theory comparison, center-accuracy table and proposition proof/status table were visually inspected. Tables fit the text width and equations are legible. Both figures use color plus line/marker distinctions; the weak-rank figure includes exact binomial Monte Carlo intervals and labels categorical spacing. Figure 1 distinguishes analytic evaluation through p=10^12 from simulations through p=8192. The gray full-data bracket is not an empirical confidence band.

## Integrity conclusion

The completed draft records what was derived and what remains open. It does not claim independent mathematical certification, a new diagonal minimax rate, unrestricted optimality, actual-rank adaptation, or LLM-specific statistical novelty. The final publication checkpoint recommends further focused theory before submission to the requested strong venues.
