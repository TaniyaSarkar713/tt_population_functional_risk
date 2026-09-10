# Coverage of the 89 requested review checks

Every item has a disposition. A check marked inapplicable explains which mathematical object is absent; it is not silently skipped.

## 1. Reconstruct the complete mathematical framework

Framework reconstructed in report Section 2 and framework.md: full Gaussian location experiment, rank-cap classes, prescribed contrast and both length criteria.

## 2. Create a complete theorem inventory

All 23 original named/technical/open items inventoried in theorem_inventory.{md,csv,json}; strengthening matrix includes all new results.

## 3. Build a dependency graph

Acyclic graph in dependency_graph.md; each direct dependency checked in dependency_audit.md.

## 4. Audit every assumption individually

26 individually separated assumptions in assumption_audit.md, with necessity, use and final version.

## 5. Avoid keeping assumptions merely because they simplify proofs

S1–S6 remove or weaken unnecessary cap constants, Gaussianity, independence, exact rank, known variance and confidence restrictions where proved.

## 6. Check identifiability before consistency

Ambient A and psi identifiable by expectations; factors not identifiable and not estimated. See framework.md and C10.

## 7. Re-derive every theorem independently

Every original proof recalculated; new results derived separately. This is not independent peer review.

## 8. Produce step-by-step proofs

Complete revised appendices provide proofs of eight theorems, seven propositions and seven lemmas.

## 9. Explicitly justify every inequality

Holder/Bessel, projection trace, likelihood integration, hypergeometric counting, net entropy and cubic mgf verified explicitly.

## 10. Verify the conditions of every external theorem

External identities and source access depth documented in external_results_audit.md; no inaccessible result is a proof dependency.

## 11. Search for hidden assumptions

Hidden-domain audit found T5's alpha omission; repeated T6's loading; retained residual information is explicit in S5.

## 12. Check whether independence is truly needed

Nonlinear union bound needs no coordinate independence; S4 uses independent clean blocks; S5 Gaussian residual independence is essential to its method.

## 13. Relax tail assumptions where possible

S3 gives sub-Gaussian and finite-moment envelopes; S4 gives Gaussian-order thresholds under finite-variance replicates.

## 14. Relax boundedness assumptions

Known M defines the structural class. C6 shows underspecification failure; unbounded diagonal image loses the structural gain. No arbitrary bounded-signal removal is claimed.

## 15. Relax Gaussian assumptions

S3 supplies non-Gaussian upper coverage; Gaussian lower likelihood proofs are not transferred without a new experiment argument.

## 16. Investigate covariance assumptions

S6 uses marginal upper variances and a covariance-floor randomization lower comparison; C8 shows why a positive universal noise lower scale can fail.

## 17. Investigate rank assumptions

Actual ranks and singular values unrestricted below supplied caps; S1 improves cap coefficient; S3 allows known approximation error.

## 18. Investigate exact sparsity assumptions

No coordinate sparsity assumption on A or L. Exact rank-one diagonal image is an ell_q ball; approximation is handled by S3, not an invented sparse model.

## 19. Investigate known structural parameters

M/caps remain supplied; S5 handles unknown Gaussian variance with residuals. Same-data cap estimation remains unproved.

## 20. Investigate tuning-parameter dependence

S3 permits all data-dependent Lambda>=lambda0 on one event. Arbitrary interval or loading selection fails by C7.

## 21. Check whether asymptotic results can become finite-sample results

Original coverage and mixture bounds already finite-sample; S7/S8 and S1–S6 are also finite-sample before rate corollaries.

## 22. Check whether consistency can be upgraded to a rate

No standalone consistency claim needs upgrading; explicit functional length rates and finite-sample envelopes are the actual conclusions.

## 23. Check whether a rate can be upgraded to asymptotic distribution

C9 prevents a generic centered normal limit for threshold centers; direct contrast is already exactly Gaussian.

## 24. Check whether asymptotic normality can be made uniform

Uniform finite-sample coverage holds; a uniform Gaussian limit for nonlinear centers does not follow and is not claimed.

## 25. Investigate Berry–Esseen-type bounds

Direct normal approximation error is exactly zero; C9 rules out the suggested generic centered-normal Berry–Esseen strengthening for threshold centers.

## 26. Investigate confidence intervals and testing

Original C_* and new C_dagger have explicit coverage. S7 test has null rejection <=gamma; acceptance plus noise event bounds target. No unproved sharp power curve.

## 27. Investigate minimax optimality

D1 sharp in restricted experiment; S7/T6 sharp L0 for K>=4; cubic and Lmax gaps explicitly retained.

## 28. Verify parameter classes in minimax arguments

Each alternative's rank, norm, target and observation likelihood checked. Enlarged unfolding classes distinguished from original tensor class.

## 29. Investigate oracle inequalities

S3 gives a pathwise infimum over approximating tensors. Its unobserved bound is not a valid adaptive radius.

## 30. Investigate misspecification

S3 proves radius plus eta on a known distance class; norm/cap violations without that allowance can give zero coverage.

## 31. Investigate contamination robustness

S4 finite variance and bounded row replacement proved; no robustness of the unchanged Gaussian method claimed.

## 32. Investigate adversarial versus stochastic contamination

Bounded adaptive row replacement separated from Bernoulli replacement; explicit binomial count conversion and failure allocation supplied.

## 33. Investigate dependence on condition numbers and eigengaps

No signal inverse or condition-number factor in original proofs; TT exact canonical factorization is not noisy subspace perturbation.

## 34. Check dimensional regimes

Finite-sample formulas track dimensions, caps and noise; fixed K/caps and M=tau sqrt(p) stated only for rate corollaries.

## 35. Check whether logarithmic factors can be removed

Diagonal log is necessary by D1; full K>=4 sqrt(log p) necessary by T6; cubic log versus log^(3/2) remains unresolved.

## 36. Check whether union bounds are unnecessarily crude

Exact Gaussian maximum threshold improves constants. S7 subset-size union bound leaves a possible cubic log cost; no unsupported removal.

## 37. Check covering-number calculations

Net size (1+4K)^s per mode proved by volume packing; binomial bound and sum over all sizes included.

## 38. Check empirical-process arguments

No empirical-process limit invoked. S7 is a finite Gaussian union bound over explicitly counted sets.

## 39. Check stochastic equicontinuity

No stochastic equicontinuity step or functional CLT used; none is assumed implicitly.

## 40. Check Taylor expansions carefully

No Taylor expansion in proofs. S3 uses an exact Lipschitz identity instead of a linearization.

## 41. Check matrix perturbation arguments

No noisy matrix perturbation theorem used; structural range uses exact projection and trace.

## 42. Check tensor perturbation arguments

Tensor proof is exact canonical factorization plus coordinate restriction; Tucker approximation tail certificate proved by commuting projections.

## 43. Check optimization-statistics interaction

Original method explicit O(m) after contractions. S7 exhaustive finite scan; no optimizer convergence or statistical-computational equivalence assumed.

## 44. Investigate computational-statistical tradeoffs

S7 exponential operation count explicit; polynomial-time achievement and any computational lower bound remain open.

## 45. Check initialization dependence

No initialization for the explicit threshold or finite scan; no iterative convergence claim.

## 46. Audit probability statements

Uniformity, randomization, conditioning, union bounds and common-target transfer checked. S7 expected rejection term retained.

## 47. Audit OO, OpO_p, oo, and opo_p notation

Rates are deterministic or explicit expected-length bounds; fixed-parameter constants identified. No unsupported O_P-to-expectation conversion.

## 48. Audit constants

Original mixture constants and new cubic constant 1/200 checked analytically and numerically; S2 improves affine constant exactly.

## 49. Check edge and boundary cases

Zero tensor, rank zero, K2, p1, caps exceeding dimensions, tied singular values, zero variance and endpoint interpolation covered.

## 50. Compare with known special cases

K2 agrees with lack of tensor-versus-one-cut separation; rank one has exact ell_q image; affine problem reduces to bounded normal mean.

## 51. Search actively for counterexamples

Twelve counterexample groups recorded in counterexamples.md, including a full-data refutation of Q2.

## 52. Distinguish sufficient from necessary assumptions

assumption_audit.md explicitly distinguishes sufficient proof conditions from necessary statistical conditions.

## 53. Search for weaker theorem formulations

T5 repaired by explicit confidence range; Q2 replaced by a proved lower bound and a partial cubic bracket.

## 54. Build a hierarchy of results

Results separated into deterministic geometry, calibrated upper inference, full-data lower bounds and rate consequences.

## 55. Investigate whether results can hold uniformly over model classes

Coverage uniform on entire cap/distance classes; robust and variance extensions use their own explicitly stated model classes.

## 56. Investigate adaptivity

Cap-uniformity is not actual-rank adaptation. Common-event tuning and independent loading selection are limited proved adaptations.

## 57. Investigate robustness–efficiency tradeoffs

Finite-variance envelope maintains order with replicates but larger constants; no oracle efficiency or contamination optimality asserted.

## 58. Check semiparametric efficiency where relevant

Regular-stratum tangent variance is a different guarantee. At singular ranks no blanket efficient influence-function argument is supplied.

## 59. Check bootstrap validity where relevant

No bootstrap procedure is defined or needed by current method. Generic bootstrap validity is not asserted; would require its own nonregular analysis.

## 60. Investigate nonregular cases

Zero and vanishing singular values are included. C9 demonstrates nonnormal threshold-center behavior at the boundary.

## 61. Check whether theorem conditions are observable

Noise/cap/norm inputs must be externally supplied or separately calibrated. Some assumptions cannot be verified from the inference tensor alone.

## 62. Compare assumptions with closest literature

External-results audit and original 20-paper matrix compare sequence theory, regular tensor inference, affine mean inference and 2026 completion result.

## 63. Explicitly search for Pareto improvements

Proved Pareto improvements: smaller D; exact max threshold; eta rather than 2eta; S7 shorter L0 with preserved worst-case upper bound.

## 64. Do not over-strengthen results

No sharp Lmax, cubic rate, actual-rank adaptation, efficient scan or robust minimax result promoted without proof.

## 65. Produce proof sketches before full proofs

Roadmaps precede each original proof and the new arguments in the reviewed appendices.

## 66. Write every lemma needed for completeness

Two new essential lemmas (finite nets/injective norm and cubic exponential moment) stated and proved explicitly.

## 67. Verify every lemma independently

All five original lemmas and both new lemmas recalculated; finite checks supplement proofs.

## 68. Verify corollaries truly follow

T5 derived only from T2–T4 on corrected domain; S7 rates use summability; D1 balances explicit support size.

## 69. Check theorem numbering and logical order

Revised theorem/proposition/lemma numbering and LaTeX cross-references checked at build.

## 70. Check proof modularity

Original proofs, full-data proofs and supporting refinements split into appendix.tex, full_data_proofs.tex and refinements.tex.

## 71. Produce a theorem-strengthening matrix

strengthening_matrix.md records each result, correctness, sharpness, final status and proposed opportunities.

## 72. Produce an assumption-relaxation matrix

assumption_audit.md and its CSV/JSON constitute the complete relaxation matrix.

## 73. Produce a counterexample appendix

counterexamples.md provides explicit model choices, failures and remedies.

## 74. Produce explicit theorem comparisons

report.md Section 4 and strengthening_matrix.md show original-to-final formulas under matched experiments.

## 75. Separate verified improvements from research opportunities

Result ledger separates PROVED, PARTIAL, REFUTED and OPEN. Potential novelty is not proof of priority.

## 76. Perform an adversarial referee attack on each theorem

Theorem-level challenges in strengthening_matrix.md and report Section 8; objections about classical sequence rates and scan cost accepted.

## 77. Determine which results are genuinely publication-level

S7/S8 strongest publication candidates; T1/T2 foundations; D1 attributed benchmark; elementary extensions kept as supporting results.

## 78. Identify the strongest theorem in the paper

S7 plus T6 yields a matched same-experiment L0 rate for K>=4; S8 adds an order-dependent obstruction.

## 79. Identify the weakest main theorem

T5 is mainly a corollary; D1 cannot carry novelty. Retain for interpretation/benchmark, not as primary new theory.

## 80. Identify the theorem most worth strengthening

Highest priorities: cubic log gap, full-data worst case, efficient scan, loading geometry/adaptation; impact/feasibility ranked.

## 81. Update the manuscript theory only after verification

Verified statements, appendices, abstract, introduction, comparisons, discussion and ledger updated only in separate reviewed revision.

## 82. Produce complete polished proofs

All numbered results have detailed proofs with assumptions, definitions and roadmaps; external inputs independently stated or verified.

## 83. Final theorem audit table

Final theorem audit in strengthening_matrix.md; input record in theorem_inventory files.

## 84. Final assumption audit

Final assumption audit in assumption_audit.md with all 26 entries.

## 85. Final proof-dependency audit

Final dependency table in dependency_audit.md, with graph.

## 86. Final theoretical contribution comparison

Existing/original/final comparison in strengthening_matrix.md and report Section 4.

## 87. Final unresolved theory list

report Section 10 and revised status appendix separate resolved, partial, open and counterexample outcomes.

## 88. Final theoretical verdict

B for reviewed theory: original intended results valid after domain repair, with complete strengthening proofs; submission remains premature.

## 89. Final deliverables

README.md links the report, reviewed PDF, full proof sources, inventory, matrices, counterexamples, source verification and reproducibility checks.

