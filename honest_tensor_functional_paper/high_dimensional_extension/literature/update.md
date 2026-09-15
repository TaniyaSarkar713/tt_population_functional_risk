# Focused primary-source check

Checked 2026-09-12. This is a positioning check, not a systematic literature
review, priority claim, or independent mathematical audit.

- Collier, Comminges and Tsybakov, *Minimax estimation of linear and quadratic
  functionals on sparsity classes*, [arXiv:1502.00665](https://arxiv.org/abs/1502.00665).
  The sparse Gaussian linear-functional calculation underlying the repository's
  diagonal lower bounds is classical. G1 reuses that lower-bound mechanism
  and matches it by a structural/direct upper bound on the full tensor class
  in the regime $r\gtrsim\sqrt p$. It is not a new sparsity lower-bound method.

- Collier, Comminges, Tsybakov and Verzélen, *Optimal adaptive estimation of
  linear functionals under sparsity*,
  [arXiv:1611.09744v2](https://arxiv.org/abs/1611.09744v2).
  This paper gives estimation rates and adaptation costs when sparsity is
  unknown. G2 concerns honest confidence intervals on a growing outer tensor
  class. Its obstruction follows directly from the common zero-point lower
  bound; the estimation adaptation guarantee in this reference is not
  transferred to honest intervals.

- Choo and d'Orsi, *The Complexity of Sparse Tensor PCA*,
  [arXiv:2106.06308v2](https://arxiv.org/abs/2106.06308v2).
  The paper supplies recovery algorithms and a low-degree likelihood-ratio
  analysis showing a computation/signal tradeoff. This supports retaining a
  precise restricted-model distinction. It does not prove that all efficient
  confidence interval algorithms fail on the original weak-signal class.

- Xu, Chen and Han, *Statistical Inference for Low-Rank Tensor Models*,
  [arXiv:2501.16223](https://arxiv.org/abs/2501.16223).
  This paper uses debiasing and tangent projection for general tensor
  functionals under explicit signal/sample conditions. P1 does not introduce
  tangent projection. It proves a pointwise expected-length rate for the
  repository's conservative cap-valid interval under the same outer-class
  honesty requirement, including the contribution from pilot failure.
  Its sufficient signal threshold is not asserted optimal.

W1/W2 follow from deterministic dyadic decomposition, the previously proved
weighted block diameter, and two-point testing. The result is stronger than
the earlier small-budget statement for these loading families, but a broader
novelty assessment would require a dedicated literature comparison. No claim
of sharp rates for all slowly varying weight profiles is made.
