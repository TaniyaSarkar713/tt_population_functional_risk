# Primary-source positioning

Checked 2026-09-11. This was a focused source check, not a systematic
literature review or a novelty certification.

- Cai and Low, *An adaptation theory for nonparametric confidence intervals*,
  Annals of Statistics 32(5), 2004, 1805–1840;
  [author preprint](https://arxiv.org/abs/math/0503662),
  [published article](https://doi.org/10.1214/009053604000000049).
  The paper develops lower bounds and adaptive intervals using between-class
  and ordered moduli. It is the conceptual reference for distinguishing
  subclass minimax length from oracle or pointwise adaptation. Our A1 is
  simply a consequence of the existing tensor upper bound and a common
  rank-one lower bound; it is not a new general adaptation theorem. The
  shifted-mixture arguments use the same established testing logic.

- Xu, Chen and Han, *Statistical Inference for Low-Rank Tensor Models*,
  [arXiv:2501.16223](https://arxiv.org/abs/2501.16223).
  The paper studies general tensor functionals using debiasing and tangent
  projection, with explicit signal/sample conditions for its guarantees.
  Our new cap-valid interval does not claim to introduce tangent projection.
  It supplies a conservative finite-sample bias bound on the full supplied-cap
  class, with weak signals handled by fallback. Its strong-signal advantage
  does not prove the original weak-signal minimax computation problem solved.

- Collier, Comminges and Tsybakov, *Minimax estimation of linear and
  quadratic functionals on sparsity classes*,
  [arXiv:1502.00665](https://arxiv.org/abs/1502.00665).
  This is the existing repository's sparse sequence-functional precursor.
  L2 uses the classical Gaussian mixture identity, with the mixing weights
  optimized analytically for orthogonal alternatives. It remains a full-data
  tensor lower bound because those alternatives are orthogonal as tensors.

L1 is a direct product-overlap specialization of canonical tensor expansion
and Gaussian two-point arguments. The optimizer uses conventional interval
bounds and branch and bound, specialized to the residual criterion already
proved in this repository. No claim of algorithmic novelty, general hardness,
or sharp geometry outside the explicitly proved regimes is made.
