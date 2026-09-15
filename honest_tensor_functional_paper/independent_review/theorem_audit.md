# Result-by-result theorem audit

Audit date: 2026-09-13. The 45 distinct numbered theorem/proposition/lemma statements in the integrated manuscript and 14 numbered supplement results are audited below. Generated TeX copies of supplement statements are not counted twice. No separately stated corollaries occur in this active inventory.

**Meaning of the judgment.** The statements and supplied proof arguments were read and reconstructed. “No defect identified” is a fallible review judgment, not a formal verification or a certificate of priority. The new finite checks can falsify selected steps but cannot prove a uniform theorem. Novelty judgments are relative to the focused closest-work review, not an exhaustive literature search.

The machine-readable table has all requested columns (statement, proof completeness, novelty, strength and issue), plus source locations and proof reasoning. Detailed entries use a vertical layout for legibility.

## T01. Orthogonal diagonal compressibility

**Result:** `thm:diagonal`. **Location:** [robust_adaptive_extension/paper/main.tex](../robust_adaptive_extension/paper/main.tex), line 207.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Canonical CP expansion, scalar Holder over modes, and concavity over squared component weights give the exponent 2/K and coefficient J^(1-1/K). The TT proof uses canonical prefix identities, not orthogonality of all paths.

**Novelty:** Useful tensor specialization; the quasi-norm exponent itself is established geometry.

**Strength and issue:** Uniform at zero and arbitrarily weak signals. Rank constants are not uniform over growing caps.

## T02. Finite-sample honest interval

**Result:** `thm:coverage`. **Location:** [robust_adaptive_extension/paper/main.tex](../robust_adaptive_extension/paper/main.tex), line 219.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** On the simultaneous Gaussian diagonal event, the scalar threshold envelope bounds each error by min(abs(a_i),2 lambda). Compressibility gives the radius; singular-value duality gives the structural option. Selection uses deterministic radii.

**Novelty:** Concrete finite-sample procedure built from classical thresholding and structural bounds.

**Strength and issue:** Efficient diagonal method; not the sharper full-data minimax optimizer. Random selection by observed widths would need a new argument.

## T03. Fixed-radius affine intervals

**Result:** `thm:affine`. **Location:** [robust_adaptive_extension/paper/main.tex](../robust_adaptive_extension/paper/main.tex), line 240.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** At zero, Gaussian variance forces a noise radius; the positive and negative coordinate atoms force maximum bias. Combining these yields the harmonic-mean lower bound.

**Novelty:** Tensor application of known affine/nonlinear distinctions.

**Strength and issue:** Only deterministic W, offset and radius. Does not exclude every interval with an affine center and a random radius.

## T04. Cost of a single unfolding honesty class

**Result:** `thm:unfolding`. **Location:** [robust_adaptive_extension/paper/main.tex](../robust_adaptive_extension/paper/main.tex), line 259.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Rank-one matrix alternatives in the enlarged unfolding class have a common target. The full matrix likelihood mixture has bounded second moment at theta <= tau sqrt(p)/4.

**Novelty:** Meaningful comparison of honesty classes.

**Strength and issue:** Does not prove that merely storing data as an unfolding loses information. The lower bound is deliberately for a larger class.

## T05. Strict length separations

**Result:** `thm:separation`. **Location:** [robust_adaptive_extension/paper/main.tex](../robust_adaptive_extension/paper/main.tex), line 270.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Combine the deterministic selected radius with the affine and enlarged-class lower bounds at fixed K and caps, M=tau sqrt(p). Powers of p separate the lengths.

**Novelty:** Useful synthesis, not a new proof ingredient.

**Strength and issue:** Correct comparison categories; later full-data sharp results supersede the initial upper bound as the headline rate.

## T06. Within-class lower bound

**Result:** `thm:jointlower`. **Location:** [robust_adaptive_extension/paper/main.tex](../robust_adaptive_extension/paper/main.tex), line 283.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Coordinate-axis Gaussian alternatives lie in every positive cap class. Their common target and likelihood second moment give a positive E_0 length bound.

**Novelty:** Classical testing applied to tensor atoms.

**Strength and issue:** Valid but not cubic-sharp. Retain as a short ingredient rather than an unresolved final gap.

## T07. Classical diagonal-information benchmark

**Result:** `prop:diagonal_minimax`. **Location:** [robust_adaptive_extension/paper/main.tex](../robust_adaptive_extension/paper/main.tex), line 310.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** The rank-one diagonal image is exactly the ell_(2/K) ball. Sparse diagonal mixtures yield the lower bound in the diagonal observation experiment; thresholding matches it.

**Novelty:** Classical sequence-functional rate after an exact tensor reduction.

**Strength and issue:** The mixture second moment here is not the full-tensor second moment. Correctly restricted to diagonal-based intervals.

## T08. A full-data interval with short expected length at zero

**Result:** `thm:scan`. **Location:** [robust_adaptive_extension/paper/full_data_section.tex](../robust_adaptive_extension/paper/full_data_section.tex), line 23.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Finite product nets control the injective norm; canonical weights turn this into an ordered-diagonal residual bound. Scan acceptance at zero yields short expected length.

**Novelty:** Nontrivial use of off-diagonal information.

**Strength and issue:** Statistical existence result with exponential search. Later uniform-diameter theorem is stronger.

## T09. A harmonic obstruction in order three

**Result:** `thm:harmonic`. **Location:** [robust_adaptive_extension/paper/full_data_section.tex](../robust_adaptive_extension/paper/full_data_section.tex), line 46.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Sign coupling fixes the diagonal target. The full likelihood exponent is a product of dependent weighted sign sums; Holder and the cubic exponential moment bound control it without independence.

**Novelty:** Nontrivial preliminary cubic construction.

**Strength and issue:** Correct but weaker than the sparse harmonic lower bound; move to historical appendix or remove from final proof chain.

## T10. Sparse harmonic lower bound

**Result:** `thm:sparse_harmonic`. **Location:** [robust_adaptive_extension/paper/gap_section.tex](../robust_adaptive_extension/paper/gap_section.tex), line 6.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Use nonnegative harmonic factors on random size-m supports. Norm and common target are explicit; the full tensor overlap is bounded by 27 b^2 times support overlap. Hypergeometric factorial moments control chi-square.

**Novelty:** Strongest candidate for a substantive new lower-bound ingredient.

**Strength and issue:** Produces the necessary cubic logarithm. Verified against exact small-support enumeration; finite checks supplement the analytic proof.

## T11. Uniform diameter and full-data minimax length

**Result:** `thm:full_minimax`. **Location:** [robust_adaptive_extension/paper/gap_section.tex](../robust_adaptive_extension/paper/gap_section.tex), line 42.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Subtract two feasible tensors, doubling caps and norm. The finite-net residual event bounds every ordered diagonal coordinate and hence deterministic functional diameter. Coordinate and sparse harmonic alternatives match the bound.

**Novelty:** Central sharp full-data tensor-functional result.

**Strength and issue:** At M=tau sqrt(p), fixed K/caps; both E_0 and worst-case expected length match. Constants may depend on fixed caps.

## T12. Squared-error consequence

**Result:** `prop:mse_sharp`. **Location:** [robust_adaptive_extension/paper/gap_section.tex](../robust_adaptive_extension/paper/gap_section.tex), line 63.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Use a confidence level decreasing as p^-2 and control failure loss by the structural range at M=tau sqrt(p). The testing lower bound transfers to squared loss.

**Novelty:** Standard consequence once the confidence-set rate is known.

**Strength and issue:** Does not justify fixed-confidence P1 interval-midpoint MSE, and does not by itself handle arbitrary huge M/tau.

## T13. Truncated scans

**Result:** `prop:truncated`. **Location:** [robust_adaptive_extension/paper/gap_section.tex](../robust_adaptive_extension/paper/gap_section.tex), line 76.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Retain only scan supports up to the supplied budget. The short-support bound and remaining deterministic envelope give the stated residual term and operation count.

**Novelty:** Useful restricted computational upper bound.

**Strength and issue:** Not an efficient minimax solution in the original diffuse weak-signal regime; budget dependence must remain explicit.

## T14. A low-degree estimation separation

**Result:** `thm:low_degree`. **Location:** [robust_adaptive_extension/paper/gap_section.tex](../robust_adaptive_extension/paper/gap_section.tex), line 115.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Expand the planted likelihood in Gaussian Hermite degrees. Sparse tensor overlap moments control the truncated norm, producing a polynomial-estimation obstruction in the stated degree range.

**Novelty:** Specialized restricted computational lower bound, related to sparse tensor PCA.

**Strength and issue:** Does not establish hardness of every polynomial-time estimator or honest interval. Fixed-order and support/degree exponent conditions matter.

## T15. What an efficient short interval would imply

**Result:** `prop:ci_detection`. **Location:** [robust_adaptive_extension/paper/gap_section.tex](../robust_adaptive_extension/paper/gap_section.tex), line 147.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** A short honest interval covering the null rarely reaches a separated common target. Markov's inequality on length and coverage create a test.

**Novelty:** Standard CI-to-testing reduction.

**Strength and issue:** An implication only; a separate computational testing lower bound is required to conclude general algorithmic hardness.

## T16. Diameter using both norm and scan constraints

**Result:** `thm:norm_diameter`. **Location:** [robust_adaptive_extension/paper/norm_loading_section.tex](../robust_adaptive_extension/paper/norm_loading_section.tex), line 12.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Intersect the scan coordinate envelope with the norm-induced ordered-coordinate envelope before summing. This prevents a spurious logarithm at small budgets.

**Novelty:** Important technical refinement of the sharp rate.

**Strength and issue:** Doubled residual ranks/norm enter constants. Separate small and large M regimes explicitly.

## T17. Full-data length for every positive norm budget

**Result:** `thm:all_norm_rates`. **Location:** [robust_adaptive_extension/paper/norm_loading_section.tex](../robust_adaptive_extension/paper/norm_loading_section.tex), line 32.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Apply the norm-sensitive sum lemma for the upper bound. A coordinate mixture and truncated sparse harmonic construction with m controlled by both p and M/tau match it.

**Novelty:** Central all-budget completion of the flat-loading theory.

**Strength and issue:** Uniform in p,M,tau for fixed positive caps and K; no extrapolation to arbitrary loading profiles or intermediate growing caps.

## T18. Squared risk uniformly over norm budgets

**Result:** `thm:all_norm_mse`. **Location:** [robust_adaptive_extension/paper/norm_loading_section.tex](../robust_adaptive_extension/paper/norm_loading_section.tex), line 58.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** A measurable approximate residual fit has controlled Gaussian excess tails on every observation. Integrating those tails gives squared risk without multiplying a fixed failure probability by M^2.

**Novelty:** Substantive risk refinement beyond a fixed-confidence midpoint argument.

**Strength and issue:** All positive budgets, but ideal residual optimization. The estimator differs from the empirical cap-valid interval midpoint.

## T19. Loading-dependent full-data bounds

**Result:** `thm:weighted_bounds`. **Location:** [robust_adaptive_extension/paper/norm_loading_section.tex](../robust_adaptive_extension/paper/norm_loading_section.tex), line 83.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Rearrange absolute weights against ordered residual coordinates for the upper bound. Equalize target weights in one factor of a nonnegative mixture; overlaps contract, so the full likelihood lower bound remains valid.

**Novelty:** Useful explicit loading envelopes.

**Strength and issue:** Upper and lower bounds need not match for arbitrary weights. Sign handling relies on the specified construction, not monotonicity of arbitrary signed inner products.

## T20. Sharp rates for a flat orthogonal loading

**Result:** `prop:flat_loading`. **Location:** [robust_adaptive_extension/paper/norm_loading_section.tex](../robust_adaptive_extension/paper/norm_loading_section.tex), line 95.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Restrict to the m-dimensional orthogonal product span, normalize by sqrt(m), and apply the all-budget theorem. The unused orthogonal observations are pure noise.

**Novelty:** Sharp corollary with useful ambient-dimension invariance.

**Strength and issue:** Flat signed orthogonal weights only. Arbitrary nonorthogonal loadings require the separate residual correction.

## T21. Full-data robustness under directional tails

**Result:** `thm:sg_full`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 14.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Replace Gaussian net tails by a joint directional moment-generating-function bound. Gaussian noise is a member of the unknown-law family for the minimax lower bound.

**Novelty:** Calibrated robustness extension.

**Strength and issue:** Joint proxy and known scale required. Minimax over a noise family does not give the lower rate for each fixed member.

## T22. Full scans with only finite-variance replicates

**Result:** `thm:mom_full`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 30.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Independent whole-tensor replicates give Chebyshev block bounds for every net direction. Median/binomial and union bounds calibrate simultaneous scans; the polynomial excess tail is integrable for squared risk.

**Novelty:** Meaningful finite-variance extension with strong replication requirements.

**Strength and issue:** Requires n at least twice the largest block count, of order p at fixed K/confidence, and a known covariance upper bound. Still exponential in scan complexity.

## T23. Two limits of a noise relaxation

**Result:** `prop:noise_limits`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 43.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Equicorrelated coordinates show why marginal variance/tail control is insufficient. A bounded scalar Rademacher-noise experiment with small signal range permits exact recovery, refuting a per-law Gaussian lower transfer.

**Novelty:** Useful explicit boundaries.

**Strength and issue:** Counterexamples are outside the sufficient assumptions or refute an overextension, not the stated robustness theorem.

## T24. Sharp length under a Frobenius approximation allowance

**Result:** `thm:approx_sharp`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 50.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Inflate scan constraints and projected endpoints by the supplied Frobenius allowance. Direct Gaussian inference caps the length; nested exact-rank and residual-ball submodels give matching lower terms.

**Novelty:** Sharp model-approximation consequence.

**Strength and issue:** Allowance must be supplied and deterministic/certified. Does not license estimating it from the same data without calibration.

## T25. A growing-rank lower bound and the unrestricted endpoint

**Result:** `prop:growing_caps`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 60.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Sparse diagonal tensors of support s have all relevant unfolding ranks s. Their full-data likelihood depends on hypergeometric overlap; the unrestricted endpoint follows from the norm-ball direction.

**Novelty:** Classical sparse lower bound identifying a tensor rank transition.

**Strength and issue:** Intermediate ranks are lower bounded, not sharply characterized here. G1 later matches only the large-cap branch.

## T26. A confidence interval for any certified loading decomposition

**Result:** `prop:loading_transfer`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 74.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** For L=L0+R, combine the interval for L0 with a Gaussian interval for the known residual contraction using allocated error probabilities.

**Novelty:** Standard and useful calibration device.

**Strength and issue:** No independence between the two intervals is needed. Same-data loading selection is not covered without simultaneous control.

## T27. Two efficiently attained minimax regimes

**Result:** `thm:efficient_regimes`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 90.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** In the small-budget or unrestricted-rank regimes, structural/direct choices meet the relevant lower bounds.

**Novelty:** Straightforward attained endpoints.

**Strength and issue:** Does not imply efficiency for diffuse fixed-cap weak signals at moderate/large budgets.

## T28. Why full convexification loses the weak-signal gain

**Result:** `prop:convex_loss`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 98.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** The convex hull of admissible signed tensor atoms contains a segment in the loading direction. A Gaussian two-point argument restores the noise-scale lower bound.

**Novelty:** Concrete convex-hull obstruction using classical nonconvex inference ideas.

**Strength and issue:** Concerns honesty over the enlarged convex class, not every algorithm using convex subroutines.

## T29. An adaptation obstruction at nonzero tensors

**Result:** `thm:shifted_adaptation`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 108.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Place the base tensor and weak rank-one mixture in orthogonal coordinate blocks. Rank subadditivity, Pythagorean norm slack and Gaussian translation preserve the lower bound.

**Novelty:** Useful nonzero refinement of an adaptation obstruction.

**Strength and issue:** Requires spare ranks and norm budget. Does not characterize every point or saturated stratum.

## T30. Finite-sample rank calibration with a computable bias correction

**Result:** `thm:adaptive_tangent`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 140.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** One simultaneous pilot operator-norm event identifies separated mode ranks. Conditional on the independent pilot, validation is Gaussian. The omitted tensor projection has at least two subspace errors, giving a second-order bias certificate.

**Novelty:** Finite-sample constructive regular-signal refinement.

**Strength and issue:** Coverage stated on the separated class only. Its product-space projector may be larger than the exact Tucker tangent space; severe signal requirements are disclosed.

## T31. Controlled squared component weights

**Result:** `lem:cp`. **Location:** [robust_adaptive_extension/paper/appendix.tex](../robust_adaptive_extension/paper/appendix.tex), line 7.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Tucker mode orthogonalization and TT canonical prefix recursions give a finite unit-product expansion with a bounded number of components and exact sum of squared weights.

**Novelty:** Standard factor geometry assembled for this problem.

**Strength and issue:** TT paths need not be mutually orthogonal. The supplied argument does not make that erroneous assumption.

## T32. Exact diagonal reduction

**Result:** `lem:image`. **Location:** [robust_adaptive_extension/paper/appendix.tex](../robust_adaptive_extension/paper/appendix.tex), line 69.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Holder gives one inclusion; product factors proportional to signed abs(a_i)^(1/K) give the reverse inclusion and correct norm.

**Novelty:** Exact useful reduction; related factor geometry is established.

**Strength and issue:** Rank-one diagonal image only. Positive caps contain this class.

## T33. Scalar threshold envelope

**Result:** `lem:soft`. **Location:** [robust_adaptive_extension/paper/appendix.tex](../robust_adaptive_extension/paper/appendix.tex), line 94.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Case analysis on thresholding with abs(noise)<=lambda yields error <=min(abs(signal),2lambda), then the q-envelope bound.

**Novelty:** Elementary scalar inequality.

**Strength and issue:** Valid for q=2/K in (0,1); the selection/event calibration is handled separately.

## T34. Matrix functional bound

**Result:** `lem:structural`. **Location:** [robust_adaptive_extension/paper/appendix.tex](../robust_adaptive_extension/paper/appendix.tex), line 108.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Von Neumann trace inequality followed by Cauchy--Schwarz over at most r singular values gives the functional range.

**Novelty:** Standard matrix inequality.

**Strength and issue:** Rank is required; replacing the rank-restricted bound by the full Frobenius norm can lose the useful factor.

## T35. Common-target alternatives

**Result:** `lem:mixture`. **Location:** [robust_adaptive_extension/paper/appendix.tex](../robust_adaptive_extension/paper/appendix.tex), line 175.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Coverage of zero and a common alternative target, followed by total variation transfer and a union bound, forces expected length at least target separation times 1-2alpha-TV.

**Novelty:** Classical testing principle.

**Strength and issue:** Common target is essential. Independent procedure randomization can be appended without changing total variation.

## T36. Finite product nets and injective norm

**Result:** `lem:net_scan`. **Location:** [robust_adaptive_extension/paper/full_data_proofs.tex](../robust_adaptive_extension/paper/full_data_proofs.tex), line 4.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** A telescoping product-net approximation bounds the injective norm by twice the finite maximum; canonical expansion then gives the rank-dependent norm comparison.

**Novelty:** Standard net argument adapted to the tensor class.

**Strength and issue:** Exponential net cardinality is explicit. Constants depend on tensor order.

## T37. Uniform cubic moment for a weighted sign sum

**Result:** `lem:cubic_moment`. **Location:** [robust_adaptive_extension/paper/full_data_proofs.tex](../robust_adaptive_extension/paper/full_data_proofs.tex), line 70.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Split the decreasing weighted sign sum into head and tail, control the tail's sub-Gaussian scale, and integrate its cubic exponential moment at the supplied small constant.

**Novelty:** Technical ingredient for the preliminary harmonic bound.

**Strength and issue:** No independence of the three coupled likelihood sums is asserted. Redundant if the preliminary lower bound is removed.

## T38. Smaller rank coefficient

**Result:** `prop:budget`. **Location:** [robust_adaptive_extension/paper/refinements.tex](../robust_adaptive_extension/paper/refinements.tex), line 7.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Combine canonical component counts, the universal m-based diagonal bound, and mode/cut rank bounds; take the minimum of valid coefficients.

**Novelty:** Useful coefficient sharpening, largely algebraic.

**Strength and issue:** May improve constants or cap dependence but does not solve intermediate-cap minimax matching.

## T39. Structural range and fixed affine optimum

**Result:** `prop:affine_exact`. **Location:** [robust_adaptive_extension/paper/refinements.tex](../robust_adaptive_extension/paper/refinements.tex), line 41.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Symmetrize coordinate biases and lower bound variance by the sum of diagonal weights. Monotonic Gaussian absolute-error quantiles reduce the optimum to one scalar t in [0,1].

**Novelty:** Exact specialization of classical bounded-normal affine inference.

**Strength and issue:** Requires alpha<1/2 and deterministic affine radii. Structural-optimum criterion is a bounded-normal calculation, not a universal estimator claim.

## T40. Envelope and approximation calibration

**Result:** `prop:envelope`. **Location:** [robust_adaptive_extension/paper/refinements.tex](../robust_adaptive_extension/paper/refinements.tex), line 81.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** A calibrated simultaneous noise envelope permits the same pathwise threshold proof. Approximation adds deterministic diagonal and target allowances.

**Novelty:** General calibration lemma.

**Strength and issue:** Its input event must actually have the claimed probability; marginal bounds alone do not imply a full directional event.

## T41. Replicate median calibration

**Result:** `prop:mom`. **Location:** [robust_adaptive_extension/paper/refinements.tex](../robust_adaptive_extension/paper/refinements.tex), line 139.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Whole-replicate corruptions spoil at most c blocks. With b>=8c, b>=32 log(m/alpha), n>=2b, Chebyshev plus a binomial tail controls the coordinate medians.

**Novelty:** Standard robust-block construction with explicit constants.

**Strength and issue:** This supporting coordinate-envelope result allows bounded row corruption; the main full-scan finite-variance theorem and S06 do not establish general contamination minimax rates.

## T42. Independent residual calibration

**Result:** `prop:variance`. **Location:** [robust_adaptive_extension/paper/refinements.tex](../robust_adaptive_extension/paper/refinements.tex), line 184.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Under iid Gaussian replicates, centered residual sums of squares are independent of sample means. A lower chi-square quantile yields a valid upper noise scale; allocate errors with the interval event.

**Novelty:** Standard Gaussian residual calibration.

**Strength and issue:** Requires retained independent replicates and the stated common variance model. XCH plug-in variance is not this finite-sample construction.

## T43. Calibrated lower bounds

**Result:** `prop:levels`. **Location:** [robust_adaptive_extension/paper/refinements.tex](../robust_adaptive_extension/paper/refinements.tex), line 214.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Choose mixture amplitude and testing constants as functions of the desired confidence level, preserving a positive common-target lower factor.

**Novelty:** Calibration refinement.

**Strength and issue:** Track the stated confidence-level range; constants are not uniform as alpha approaches its boundary.

## T44. A norm-sensitive harmonic sum

**Result:** `lem:norm_sum`. **Location:** [robust_adaptive_extension/paper/norm_loading_proofs.tex](../robust_adaptive_extension/paper/norm_loading_proofs.tex), line 19.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Split the ordered-coordinate sum near s=x^2 and integrate the harmonic tail. Order three accumulates a logarithm; higher orders have a summable tail.

**Novelty:** Key analytic step behind all-budget sharpness.

**Strength and issue:** The minimum of envelopes must precede summation. It correctly retains the small-budget linear branch.

## T45. Residual fit and its noise tail

**Result:** `lem:residual_fit`. **Location:** [robust_adaptive_extension/paper/norm_loading_proofs.tex](../robust_adaptive_extension/paper/norm_loading_proofs.tex), line 103.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Compactness/continuity permit a countable dense approximate minimizer, avoiding uniqueness assumptions. Gaussian net excess tails control the fitted residual at every observation.

**Novelty:** Important existence and risk-control lemma.

**Strength and issue:** An arbitrarily selected local numerical solution does not satisfy this contract; C1 specifies the needed certified gap.

## T46. A quantitative contract for approximate minimax optimization

**Result:** `C1`. **Location:** [certified_weak_signal/theory/results.md](../certified_weak_signal/theory/results.md), line 29.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Certified lower/upper objective bounds and an O(tau) objective gap control the ideal residual-fit error. Feasible witnesses and global endpoint outer bounds distinguish inner approximation from honest projection.

**Novelty:** Useful numerical/statistical error contract.

**Strength and issue:** For squared risk the contract must hold on every observation or have its own integrated failure control. No general-dimensional implementation or polynomial complexity is supplied.

## T47. An implemented global solver on the binary rank-one class

**Result:** `C2`. **Location:** [certified_weak_signal/theory/results.md](../certified_weak_signal/theory/results.md), line 85.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Parameterize the continuous binary rank-one ball by amplitude in [-M,M] and projective angles. Global trigonometric box bounds prune only infeasible/uncompetitive cells; retained cells enclose endpoint extrema.

**Novelty:** Executable global benchmark in a very small class.

**Strength and issue:** Valid in exact real arithmetic; float64 safety guards are not directed interval arithmetic. Finite node budgets may leave large unresolved gaps; neither general ranks nor p>2 is implemented.

## T48. Sharp small-budget rates for every loading tensor

**Result:** `L1`. **Location:** [certified_weak_signal/theory/results.md](../certified_weak_signal/theory/results.md), line 140.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** A maximizing unit product contraction supplies a two-point lower bound at M<=tau. Canonical expansion bounds the structural range by sqrt(J) M rho(L), giving the upper bound.

**Novelty:** General small-ball geometry rather than a new testing principle.

**Strength and issue:** Every fixed loading tensor, fixed caps; evaluating the injective norm rho(L) can itself be hard. Does not extend beyond the small-budget regime for arbitrary L.

## T49. An optimized common-target lower bound for unequal weights

**Result:** `L2`. **Location:** [certified_weak_signal/theory/results.md](../certified_weak_signal/theory/results.md), line 190.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Choose common-target axis amplitudes Delta/w_i. Minimize the diagonal-mixture second moment over prior weights by Cauchy--Schwarz, yielding the inverse sum of inverse exponential costs.

**Novelty:** Useful optimized axis-family certificate.

**Strength and issue:** Optimized within this family only; cannot replace the cubic harmonic prior or claim arbitrary-loading minimax sharpness.

## T50. Unseparated rate adaptation across positive fixed caps

**Result:** `A1`. **Location:** [certified_weak_signal/theory/results.md](../certified_weak_signal/theory/results.md), line 228.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** The ideal outer-class procedure has the fixed-cap upper rate; every smaller positive-cap class contains the rank-one least favorable submodel with the same rate.

**Novelty:** Immediate but clarifying corollary.

**Strength and issue:** No actual-rank estimation; excludes the known-zero class; constants depend on the fixed outer caps and cannot be used for growing caps.

## T51. A computable projection certificate without separation

**Result:** `A2`. **Location:** [certified_weak_signal/theory/results.md](../certified_weak_signal/theory/results.md), line 256.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Conditional pilot/validation Gaussian inference plus norm-ball or mode nuclear-norm residual certificates gives honest projected intervals. Triangle inequalities show the elementary certificate cannot improve the direct bound under the stated conservative calibration.

**Novelty:** Useful certificate and explicit limitation.

**Strength and issue:** No separation needed, but the basic certificate can be vacuous for shortening. The later supplied-cap second-order construction is different.

## T52. The adaptation obstruction at an arbitrary orientation

**Result:** `A3`. **Location:** [certified_weak_signal/theory/results.md](../certified_weak_signal/theory/results.md), line 324.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Rotate the spare orthogonal product block and use the induced residual loading in the shifted-mixture argument. Norm and rank feasibility remain unchanged under modewise orthogonal transformations.

**Novelty:** Geometric extension of the nonzero obstruction.

**Strength and issue:** Requires an unused block, rank slack and norm slack. Not an all-point local modulus characterization.

## T53. A cap-valid tangent interval on the original unseparated class

**Result:** `A4`. **Location:** [certified_weak_signal/theory/results.md](../certified_weak_signal/theory/results.md), line 357.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Retain supplied cap dimensions. On a simultaneous operator-noise event, resolved subspace errors follow Weyl/Wedin; unresolved errors are bounded by one. The product projector omits at least two bad modes, yielding the pairwise error certificate.

**Novelty:** Useful honest weak-signal extension of the split projection method.

**Strength and issue:** Covers zero and unsaturated caps. No weak-signal minimax rate asserted. TT use is via induced Tucker mode caps, not an exact TT tangent theory.

## T54. Sharp growing-cap rates with a polynomial algorithm

**Result:** `G1`. **Location:** [high_dimensional_extension/theory/results.md](../high_dimensional_extension/theory/results.md), line 16.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Structural/direct selection meets the sparse-diagonal full-data lower bound when r>=c sqrt(p). Hypergeometric factorial moments make chi-square <=exp(1/4)-1 uniformly.

**Novelty:** Matched large-cap consequence of a classical mixture.

**Strength and issue:** Sharp min(M sqrt(r/p),tau), with constants depending on alpha,c but not growing caps/order. O(p) accesses only for coordinate loading; no intermediate-cap conclusion.

## T55. General adaptation across positive growing caps is impossible

**Result:** `G2`. **Location:** [high_dimensional_extension/theory/results.md](../high_dimensional_extension/theory/results.md), line 79.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Apply G1 at zero in the growing outer class and compare with the vanishing fixed-cap oracle rate. Orthogonal-block translation provides the stated nonzero variant.

**Novelty:** Direct, valuable consequence identifying a real adaptation barrier.

**Strength and issue:** Rules out simultaneous oracle-rate adaptation across these classes even with unlimited computation. Does not contradict A1 for fixed outer caps.

## T56. A dyadic loading bound using the full weight profile

**Result:** `W1`. **Location:** [high_dimensional_extension/theory/results.md](../high_dimensional_extension/theory/results.md), line 116.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Decompose ordered weights into dyadic blocks. Apply ideal block residual fits and an allocated confidence budget; sum widths and use Minkowski for root risk. Geometric budgets control the accumulating logarithms.

**Novelty:** Useful profile-sensitive upper envelope.

**Strength and issue:** The dyadic lower/upper envelope calculation in code is not an implemented residual fit. Arbitrary profiles need not have matching lower bounds.

## T57. Sharp rates at every budget for polynomially decreasing loadings

**Result:** `W2`. **Location:** [high_dimensional_extension/theory/results.md](../high_dimensional_extension/theory/results.md), line 171.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Fixed positive power decay makes the W1 dyadic sum bounded by a beta-dependent multiple of the first weight. A single largest-weight atom yields the matching two-point lower bound at all budgets.

**Novelty:** A meaningful special-family corollary, not a general-loading solution.

**Strength and issue:** Sharp abs(w_1)min(M,tau); constants deteriorate as beta approaches zero. Small residual perturbations require the stated norm bound and fixed epsilon<1.

## T58. A restricted computational separation for these newly matched loadings

**Result:** `W3`. **Location:** [high_dimensional_extension/theory/results.md](../high_dimensional_extension/theory/results.md), line 224.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Reweight one nonnegative planted factor to equalize the target. Overlap contractions and Hermite-degree bounds reproduce a sparse-tensor low-degree separation in the displayed beta/support/degree ranges.

**Novelty:** Specialized restricted computational extension.

**Strength and issue:** Requires 0<beta<1/K and admissible exponents; does not imply hardness for every efficient interval or the fast G1 regime.

## T59. Efficient pointwise optimality at strong saturated Tucker means

**Result:** `P1`. **Location:** [high_dimensional_extension/theory/results.md](../high_dimensional_extension/theory/results.md), line 292.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Use A4 with pilot error budget proportional to alpha r/p. Strong saturated singular values control subspace errors; the pairwise bias is O(tau sqrt(r/p)), as is the projected noise. Direct intersection controls expected length on pilot failure. A supported local Gaussian submodel supplies the matching lower bound.

**Novelty:** Useful constructive pointwise rate at a restricted geometry.

**Strength and issue:** Honest on the full supplied-cap class, but the short-length conclusion needs strongly separated saturated diagonal Tucker means, norm slack and M comparable to signal norm. Sufficient amplitude grows roughly as tau p^(K-1/2); no optimal threshold, complete TT theory or midpoint MSE claim.
