# Claim and proof audit

This is an internal derivation audit. No independent mathematical review or
formal verification has been performed.

| Result | Dependency and check | Exact scope |
|---|---|---|
| C1: optimization tolerance | Existing ordered-diagonal/net proof and residual excess-tail proof; direct triangle/Lipschitz argument | General fixed caps; statistical guarantee conditional on an actual global objective certificate |
| C2: global implementation | Projective circle covering, real-arithmetic box inclusions, complete supports; independent sampled containment and analytic cases | Binary mode sizes, rank one, arbitrary loading; floating point guards; exponential cost |
| L1: every-loading small-budget rate | Canonical squared-coefficient expansion and Gaussian two-point lower bound | Every known loading and every dimension, fixed caps, $M\le\tau$; product overlap may be hard to compute |
| L2: unequal-weight mixture | Exact full-tensor likelihood Gram matrix and Cauchy–Schwarz optimization of prior weights | Lower bound from orthogonal one-atom alternatives; not a full minimax characterization |
| A1: positive-cap rate adaptation | Restrict the old outer upper bound; reuse the common rank-one lower bound | Equal/flat loadings, fixed positive nested caps, rate up to outer-cap constants; statistical, not computational |
| A2: first-order bias repair | Simultaneous operator envelopes, nuclear norm duality, conditional Gaussian validation | Full norm-ball honesty; proved unable to improve the direct/structural radius when pilot envelopes exceed validation quantile |
| A3: rotated local obstruction | Rank subadditivity, orthogonal norm addition, translated Gaussian mixtures | Bases with unused caps and a product subspace orthogonal to the base; lower bounds only |
| A4: cap-valid tangent interval | Weyl/residual SVD inequality with a conservative unresolved case; orthogonal two-complement decomposition | All tensors under supplied mode caps, no separation; efficient but not weak-signal minimax or actual-rank adaptive |

The eight labels include propositions and algorithmic contracts of different
strength; they are not eight independently novel theorems. A1 is an immediate
but useful consequence of previous results. L1 and L2 specialize standard
lower-bound methods. A4 extends the previous tangent certificate's domain
of honesty by using caps and keeping the unresolved case conservative.

Numerical checks verify implementations and finite inequalities, not the
universal mathematical claims. Monte Carlo coverage is reported with Wilson
95% intervals. Strong-signal projection budget failures and conservative
rank-cap behavior are retained in the results.

## Still open

- A polynomial-time minimax interval for the general diffuse-loading
  weak-signal tensor class, or an interval-specific computational impossibility
  result under an explicit justified hypothesis.
- Sharp larger-budget rates for every loading or every unequal orthogonal
  weight sequence, beyond the special regimes already established.
- Optimal growing-cap dependence and pointwise rank adaptation where it is
  possible. Rank-zero oracle adaptation and some nonzero-base oracle demands
  are impossible under the stated outer honesty requirements.
- General-dimensional/cap global optimization and formally validated numerical
  interval arithmetic. The binary rank-one benchmark is implemented; it does
  not establish scalability.

The full-data statistical optimizer is therefore no longer entirely
unimplemented, but its general and efficient versions remain unfinished.
