# Theory decisions and claim locks

## 1. Main experiment

The flagship lower and upper bounds use black-box stochastic distillation:

\[
E_i\sim w,\quad X_i\mid E_i=e\sim P_e,\quad
Y_i\mid X_i,E_i\sim p_{W^0}(\cdot\mid X_i,E_i).
\]

One continuation is one independent response unit. Tokens are not multiplied into the sample size without a separate martingale argument.

Why: this experiment contains conditional-response information and supports a genuine \(d/n\) minimax lower bound. It represents API-limited compression or finite teacher sampling.

## 2. Soft-label and white-box regimes

Known weights and exact soft labels define two different experiments. White-box access permits returning a feasible teacher and gives zero error. Soft labels make the pointwise score vanish under correct specification but require empirical identifiability for exact recovery; binary logistic regression with a full-column-rank prompt design supplies an explicit finite-sample zero-risk counterexample. Under misspecification, the leading random-design quadrature term is

\[
\frac{1}{2n}\operatorname{tr}(V_XH^{-1}),
\]

which may be much smaller than \(d/n\) and vanishes when promptwise scores vanish. This regime is never used to justify the flagship lower bound.

## 3. Model and dimension

- Statistical models are indexed by tensorization and rank, not by an optimizer label.
- Exact TT ranks are assumed admissible and minimal.
- The main uniform theory uses compact, rank-separated quotient strata.
- For independent layers,

  \[
  d_\lambda=\sum_{\ell,j}r_{\ell,j-1}m_{\ell j}r_{\ell j}
  -\sum_{\ell,j<q_\ell}r_{\ell j}^2+d_{\lambda,free}.
  \]

- Tied/shared cores require the rank of the constrained quotient map.
- The functional rank \(d_{fun}=\operatorname{rank}(G_w|_{T^H})\) diagnoses invisible directions. The paper proves the \(d_{TT}/n\) law only under a uniform restricted-information bound, where \(d_{fun}=d_{TT}\); it does not prove a singular \(d_{fun}/n\) theorem.

## 4. Upper theorem

Primary statement: split-sample approximate MLE within each model plus coded validation selection. Assumptions:

1. bounded likelihood ratios or an explicit replacement tail condition;
2. unique interior KL projection and quadratic margin;
3. chartwise Lipschitz log likelihood;
4. finite well-conditioned quotient atlas;
5. fixed Kraft-coded candidate family;
6. explicit optimization errors.

Conclusion:

\[
E D_w(\widehat W,W^0)
\lesssim
\inf_\lambda\left\{A_w^2(\lambda)+
\frac{d_\lambda+\log H_\lambda+\log(1/\pi_\lambda)}{n}
+\varepsilon_{\lambda,opt}\right\}.
\]

A same-sample structural-risk result is a corollary only under a uniform isomorphic likelihood inequality over the predeclared union.

## 5. Lower theorems

1. Horizontal local Assouad cube: \(\rho^2\wedge d_\lambda/n\).
2. Smooth information-normal dense-teacher tube under a fixed budget and off-chart separation: \(A_w^2(\lambda)+\rho^2\wedge d_\lambda/n\).
3. A separate exact Gaussian-sequence benchmark matches \(\inf_D\{L^2D^{-2s}+D/n\}\); no automatic transfer to a growing conditional-generator experiment is claimed.
4. LAN constant: \(\tfrac12\operatorname{tr}(G_wI_\pi^{-1})\); it is \(d/2\) only when target and query conditional-KL information agree.

A fixed-stratum lower bound is not advertised as a universal pointwise lower bound for an arbitrary union.

## 6. Rank adaptation

- Prediction-risk adaptation and exact minimal-rank recovery are different.
- Le Cam gives no uniform rank recovery inside an \(o(n^{-1/2})\) functional neighborhood of a lower-rank stratum.
- A \(\sqrt{d/n}\) universal detection boundary is not claimed.
- Selection consistency is conditional on both an underfit likelihood gap and an overfit empirical-gain bound dominated by the penalty. BIC supplies the familiar template in regular nested models, but singular TT unions require a separate proof.

## 7. Fisher terminology

- Global target: exact teacher-relative conditional KL.
- Local correct-specification Hessian: Fisher information.
- Misspecified likelihood: separate Hessian \(H\) and score variance \(V\).
- Generic task metric: Jacobian pullback, Gauss–Newton metric, or task Hessian as appropriate.
- Generic downstream task loss can have a nonzero first-order term.

## 8. Same-data certification

The result is conditional on replace-one-cluster stability of each complete fitting algorithm. It is uniform over a fixed coded algorithm family and therefore survives data-dependent selection from that family. It does not validate a newly invented data-dependent path or an unstable full-data refit.

## Claims prohibited in the manuscript

- “First tensor-network oracle inequality.”
- “First population/minimax compression theory.”
- “First matching low-rank neural sample complexity.”
- “Gauge dimension automatically equals statistical dimension.”
- “Every white-box compressor pays \(d/n\).”
- “Fisher is the global task metric.”
- “A fixed-stratum packing proves the arbitrary oracle-infimum lower bound.”
- “Rank recovery is uniform without separation.”
- “Tokens in one continuation are independent queries.”
- “TT-SVD/SGD automatically attains the statistical oracle.”
- “Same-data certification is distribution-free for arbitrary adaptive paths.”
