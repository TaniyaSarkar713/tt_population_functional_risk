# Derivation and scope audit

These are supplied mathematical proofs, not independent review or formal
verification. Finite checks corroborate formulas and implementations; they
do not establish universal mathematical claims.

| Result | What is resolved | Dependency / limitation |
|---|---|---|
| G1 | Sharp all-budget length and MSE when the smallest cap is at least a fixed multiple of $\sqrt p$; polynomial attainment | Reuses the sparse diagonal lower mixture and matches it to a structural/direct upper bound; intermediate caps are not covered |
| G2 | Impossibility of simultaneous rate adaptation between growing outer caps and positive fixed inner caps; nonzero extension | A consequence of G1 at zero and existing fixed-cap oracle rates; it does not exclude all forms of pointwise shortening |
| W1 | Finite dyadic weight-sensitive upper envelope and MSE bound | Error allocations are simultaneous; block confidence extrema and residual fits remain ideal optimizations |
| W2 | All-budget sharp rates for fixed polynomial decay and small nonorthogonal residuals | Constants depend on fixed decay exponent and fixed caps; not uniform as exponent tends to zero |
| W3 | Low-degree estimation separation for $0<\beta<1/K$ | Full-data Hermite argument with a loading-compatible prior; not a lower bound for all polynomial-time intervals |
| P1 | Efficient pointwise optimal expected-length rate at strong saturated diagonal Tucker means | Same unseparated outer honesty class for upper and lower bounds; requires sufficient amplitude, norm slack, and shrinking pilot failure probability |

G1/G2 are useful consequences of previously supplied lower bounds, not new
testing techniques. W1/W2 use block decomposition and ordinary two-point
testing. W3 transfers the existing restricted computational argument to a
new loading family. P1 uses the previous cap-valid tangent construction
with the failure budget needed to control expected length at growing
dimensions. No broad novelty claim follows from this internal audit.

## Delicate points checked

- G1 uses full tensor likelihoods. Its alternatives have rank exactly the
  selected support size under every constrained unfolding.
- G2 excludes adaptation even between positive classes because they share
  zero. Fixed-outer-cap adaptation was only uniform in dimension/budget,
  with constants depending on the outer cap, and is not contradicted.
- W1 retains the error allocation at each block, including tiny final
  blocks at a large dyadic index. Minkowski handles potentially dependent
  block estimation errors.
- W2 permits diffuse loadings for $0<\beta<1/2$. Its upper constant is not
  uniform as $\beta\to0$; flat loading rates cannot be inferred by that limit.
- W3 equalizes the weighted target by contracting one nonnegative factor;
  it does not increase full likelihood overlaps or tensor norms.
- P1's lower bound uses the same supplied-cap class as its upper interval,
  not a known-support honesty class. The support is unknown to the algorithm.
- The pilot failure probability shrinks as $r/p$ so its expected-length
  contribution is negligible at the claimed scale. Fixed failure probability
  would not justify that proof.
- P1 concerns Tucker mode caps. TT bond caps do not generally imply the
  same mode caps and are not silently substituted.
- Runtime experiments record actual economy-SVD output sizes. The larger
  full-SVD size is a comparison calculation, not an allocation performed in
  the new experiments. Counts are array entries, not measured peak RSS.

## Remaining work

1. Efficient minimax inference for original fixed-cap diffuse weak signals,
   or an interval-specific lower bound under a justified computational
   hypothesis.
2. Sharp geometry for every loading, especially slowly varying unequal
   weights and general tensors beyond the certified residual family.
3. Sharp rates for intermediate growing caps $1\ll r\ll\sqrt p$ and the
   full range of optimal pointwise lengths where adaptation is possible.
4. Less conservative sufficient signal strengths for P1, optimal leading
   constants, TT pointwise adaptation, and broader loading-dependent
   pointwise results.

The original binary optimizer remains an exponential benchmark. This stage
adds different polynomial procedures and matching results in the regimes
listed above; it does not relabel that optimizer as scalable.
