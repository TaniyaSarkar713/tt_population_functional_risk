# Final audit of the gap development

This is an internal mathematical audit. PROVED denotes a complete supplied derivation; finite computations corroborate selected identities and inequalities. Neither computer checks nor the literature search certify a theorem's priority.

## Current theorem ledger

| Result | Status | Decisive step | Scope boundary |
|---|---|---|---|
| G1 / Theorem 9: cubic lower bound | PROVED | A sparse harmonic profile has a common target and full likelihood overlap bounded linearly in support intersection | Equal diagonal loading; sharp specialization at M=tau sqrt(p) |
| G2 / Theorem 10: worst-case length | PROVED | Residual confidence-set projection has a deterministic diameter bound; differences obey doubled rank caps | Fixed order and supplied caps; optimization is not efficient |
| G2b / Proposition 2: minimax squared risk | PROVED | Midpoint with failure probability p^-2, bounded error off coverage, and mixture testing lower bound | Same parameter class and norm/noise regime |
| G3 / Proposition 3: truncated scan | PROVED | Leading-entry bounds plus the diagonal quasi-norm tail envelope | Fixed-level computation is polynomial; its bound is not minimax |
| G4 / Theorem 11: low-degree risk separation | PROVED | Hermite projection, hypergeometric factorial moments and a bias/variance inequality | Scalar polynomial estimators only; not arbitrary efficient algorithms |
| G5 / Proposition 4: CI-to-testing implication | PROVED conditional implication | Null coverage and Markov's inequality bound the induced test's false-positive probability | The required computational testing-hardness hypothesis is unproved |

## Checks of possible failure points

1. **No marginal-likelihood substitution.** G1 computes the inner product of the full mean tensors. It does not reuse the diagonal experiment's likelihood. Only the hypergeometric factorial-moment inequality is reused.
2. **Common target.** Placing the same harmonic values in increasing order on each support preserves the diagonal sum exactly. It need not preserve pairwise overlap weights; the decreasing-profile inequality handles those weights.
3. **Both norm and distance constraints.** The minimum defining b_m enforces the Frobenius bound and second-moment bound separately. The proof of the logarithmic specialization verifies which term is smaller, including the floor in m.
4. **Difference ranks.** Neither Tucker nor TT cap classes are assumed closed under subtraction. Every constrained unfolding of a difference has rank at most twice the supplied cap. The canonical expansion constant is evaluated at these doubled caps.
5. **TT geometry.** The earlier TT squared-component-weight lemma uses left-orthogonal cores and a prefix sum identity. It does not assert orthogonality of individual TT paths. Together with Cauchy–Schwarz, it justifies the Frobenius/injective-norm comparison used here.
6. **Extrema and measurability.** The cap class is compact. Continuous finite-net constraints give compact sections, attained extrema, a closed feasible-data domain and closed projected threshold sets. The endpoint functions, extended by zero on empty sections, are Borel measurable.
7. **Worst-case expectation.** G2 bounds the interval's diameter for every observation, including an empty feasible section. It does not infer a worst-case expected-length bound from a null acceptance probability.
8. **Squared risk off the coverage event.** A fixed confidence level alone would not yield the claimed squared-risk rate. G2b uses p^-2 and the bounded target range, making the failure contribution negligible.
9. **Small-support and high-degree factorial moments.** In G4 the factorial moment is zero when its order exceeds the support size. The proof bounds the remaining factors individually; it never assumes independence of support membership.
10. **Degree-zero term.** G4 removes the constant likelihood term and uses null variance, not an uncontrolled estimator second moment, to bound the estimator's change of mean.
11. **Testing versus estimation.** A low-degree squared-risk lower bound is not a bound on the errors of every thresholded polynomial test. It supplies no automatic hardness result for arbitrary confidence intervals. G5 is stated separately and conditionally.
12. **Adaptive computation.** Only completed support levels enter the common coverage event. Intersecting their intervals preserves coverage even with data-dependent continuation. An incomplete enumeration is never labeled a complete scan.
13. **Prototype interpretation.** The implementation covers levels one and two and checks finite-net contractions against explicit enumeration. All tested small-dimensional intervals equal the structural length; there is no empirical claim of improved precision or validation of the exact minimax projection.

## Reviewer objections and present answers

- **“Projection and mixture arguments are classical.”** Correct. The proposed contribution is the evaluated tensor minimax rate, particularly the cubic logarithmic factor, and its matching full-data worst-case bound. Generic projection or support-mixture methodology is not claimed as new.
- **“The computation theorem is just sparse tensor PCA.”** The low-degree framework and overlap expansion are established tools. The supplied coarse bound is specialized to a common scalar target and compared against the now-matched scalar minimax risk. Its independent novelty should not carry the paper by itself.
- **“The main construction cannot be implemented efficiently.”** This remains a substantive limitation. The finite-level hierarchy makes one computational tradeoff explicit but does not solve the minimax interval problem.
- **“Unknown rank is really supplied-rank-cap inference.”** Correct. Actual rank and minimum signal strength are unrestricted within the supplied cap class. Adaptive length across actual ranks is not proved.
- **“The result is narrow in loading and asymptotics.”** Correct. Matching rates are for equal diagonal loading, fixed tensor order/caps and M=tau sqrt(p). General loadings, growing caps and the full norm/noise phase diagram remain open.

## Recommended next work

The statistical core is materially stronger than the reviewed draft: the cubic and worst-case gaps are closed and an exact squared-risk benchmark is available. Before submission, seek an independent proof and priority review focused on the sparse harmonic construction and full-data projection diameter. The next computational target is an algorithm with a better certified length bound or a genuine average-case reduction for interval-specific hardness. It would be incorrect to present G4 as already supplying that reduction.

For a strong statistics submission, the current opportunity is a general theory of tensor functional geometry with the present result as a sharp case. For Annals of Statistics, the restricted loading/norm regime and unresolved broader geometric characterization remain material weaknesses. The low-degree result strengthens the comparison but does not by itself remove these limitations.
