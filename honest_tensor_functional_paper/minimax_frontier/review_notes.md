# Scientific audit and continuation

This is an internal adversarial check of the new results, not independent peer
review. The prior 19-issue registry is continued without deleting any concern.
The expanded program remains **C: additional scientific work required**.

| Concern | Before this stage | New scientific result | Remaining issue |
|---|---|---|---|
| General computation, T01 | General ideal fits absent; binary exponential benchmark | M1 polynomial minimax on the full one-unfolding class; M2 affine obstruction | Nonlinear efficient minimax under simultaneous restrictive caps |
| Intermediate caps, T02 | Large-cap regime and exact-diagonal sparse submodel | M1 all caps, all budgets, every loading in a full one-cap tensor model | Arbitrary simultaneous cap vectors |
| General loadings, T03 | Abel upper/largest-prefix lower bracket | L3 exact Abel rate for every orthogonal profile, K >= 4; M1 all one-cap loadings | Cubic and nonorthogonal profiles under several caps; efficient prefix fits |
| Pointwise adaptation, T04 | Strong/aligned families and a known rank-one minor | P5 unknown-axis coordinate hierarchy, every Hamming distance, global rank-one honesty | Arbitrary points/loadings and higher/growing ranks; sharp localization threshold |
| Real data, D01 | Executed subject-level EEG with broad finite uncertainty | Preserved; no new application run | Subject/family dependence; no demonstrated tensor efficiency gain |

The core proof audit addressed the following potential failures.

1. **Full model versus a reduced experiment.** M1's sign prior contains full
   off-diagonal block means. Its likelihood calculation uses the full matrix
   inner product, which equals the full tensor inner product after reshaping.
   L3 bounds the entire rank-one tensor likelihood, not only its diagonal.
2. **Rank intersections.** A rank-r matrix mixture may violate other tensor
   unfolding caps. M1 explicitly sets those caps to ambient maxima. Its lower
   bound is not transferred to their intersection. L3's rank-one prior satisfies
   all positive caps simultaneously.
3. **Norm budgets.** M1's deterministic balanced partition yields a squared
   norm bound before randomization. L3's geometric factor mass gives norm at
   most M/16. P5's lower alternatives rotate unit factors at fixed norm, so its
   lower bound remains valid when |a| = M.
4. **Common targets in mixtures.** M1 uses matched left/right random signs, so
   diagonal loading contributions are deterministic. L3 contracts its first
   factor by the endpoint-weight ratio to make each scale's target constant.
   Zero weights are handled without division by zero.
5. **Many entropy scales.** L3 groups by the largest collision and sums an
   exponentially decreasing series. The bound is uniform in the number of
   groups. A disjoint interval partition proves the entire Abel sum is bounded
   by a fixed multiple of that same prior's target.
6. **Selection and validation.** P5's auxiliary split makes validation
   independent of anchor selection. The original direct interval need not be
   independent of validation because only a union bound is used.
7. **Denominators, signs, and empty intersections.** Ratio constraints are
   applied only if the validation anchor interval excludes zero. Signed powers
   are retained. An empty replacement is included in coverage accounting, and
   no scalar-risk theorem is inferred from its midpoint.
8. **Pointwise optimality.** The lower criterion is expected length at a fixed
   mean under honesty on the whole rank-one ball. It is not minimax risk on a
   singleton. The sufficient anchor threshold is not called necessary.
9. **Computational statements.** M2 concerns deterministic affine centers and
   constant radii before intersection. It does not exclude adaptive-length or
   nonlinear algorithms. Timing M1 is not timing the unresolved general fit.
10. **Numerical boundaries.** All retained endpoints are reanalyzed with strict
    and four-ULP counts. F037's one-step mismatch is disclosed. The independent
    convex solve, scale/tie checks, exact mixture enumeration, and public-API
    comparisons pass. These checks support, but do not certify, real-arithmetic
    results in floating point.

The simulated pointwise slopes approach the predicted exponents but differ from
them by more than their small Monte Carlo standard errors in several cases.
That is finite-amplitude bias: the denominator confidence radius remains in
the finite procedure. The report labels the slopes as finite-range contrasts
and does not claim exact exponent equality. Spectral length gains are modest
on the executed grid. The rank-two violation has zero coverage and is retained.

The full proof supplement depends on the preserved AB1/flat-prefix upper theorem
for L3; this dependency is explicit. Its new contribution is the matching
multiscale lower bound. M1, M2 and P5 have self-contained arguments apart from
standard Gaussian, spectral, and convex-duality identities.

For a focused submission, the one-cap result requires a targeted external
priority check against low-rank matrix functional estimation and convex
regularization. The higher-order arbitrary-profile result requires a careful
assessment of how much is inherited from the project's flat-prefix theorem.
No external novelty or journal acceptance claim is made. The major unresolved
generalizations are submission risks for a paper claiming the whole original
program, and future work for a paper confined to these explicit new theorems.
