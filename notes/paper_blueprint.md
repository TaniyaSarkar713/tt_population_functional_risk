# Paper blueprint

## Positioning

Paper type: **New Problem / Setting**, with a companion selection method.

The new setting is finite-query population compression of a frozen nonlinear conditional generator. TT is the structured model class. Penalized likelihood is deliberately conventional; the research burden is to identify the correct quotient-functional complexity and prove its sharpness under the right observation model.

## Thinking template

| Element | Decision |
|---|---|
| Research background | Tensor compression saves parameters and compute, but algebraic weight error can be disconnected from deployment behavior. |
| Existing limitation | Output-aware objectives, Fisher weighting, tensor risk oracles, and tensor minimax theory exist separately; none resolves the nonlinear teacher-relative TT quotient experiment. |
| Problem essence | Learn one deployable TT student from finite teacher queries to minimize weighted population conditional KL. |
| Goal | Establish a sharp approximation–estimation oracle and matching lower benchmark indexed by visible gauge-adjusted dimension. |
| Challenge 1 | TT cores are gauge-nonidentifiable. |
| Challenge 2 | Tensor identifiability does not imply conditional-law identifiability. |
| Challenge 3 | The rate changes with teacher access; exact soft labels remove response noise and can enable exact recovery under empirical identifiability. |
| Challenge 4 | Approximation shells and rank singularities complicate lower bounds/adaptation. |
| Challenge 5 | Capabilities are certified after reusing clusters for rank/core fitting. |
| Module 1 | Horizontal quotient atlas and gauge-adjusted entropy. |
| Module 2 | Nonlinear frozen-block restricted-curvature verification. |
| Module 3 | Split likelihood fitting/selection and localized fast-rate proof. |
| Module 4 | Horizontal Assouad cube, smooth information-normal tube, LAN constant, and rank-boundary Le Cam argument. |
| Module 5 | Metric-reversal theorem and stability-based multi-capability band. |
| Main contributions | Oracle; matching modelwise/tube lower; access counterexamples; rank boundary; strict metric improvement; secondary certificate. |

## Six-paragraph Introduction logic

1. Running example: equal-cost allocations, smaller Frobenius error but worse safety behavior.
2. Closest-work boundary: TT geometry/oracles, loss-aware compression, tensor inference/minimax, and certification already exist.
3. Exact new problem: finite-query teacher experiment and one common population KL projection.
4. Challenges: gauge, functional null directions, access phase, singular ranks, same-data reuse.
5. Solution overview: pivot-gauge entropy, penalized likelihood, Assouad/information-normal tube, access counterexamples, stability.
6. Contributions: one item per challenge, with Fisher explicitly local and conditional.

## Section skeleton

1. Introduction.
2. Related work and claim boundary.
3. Statistical experiment, functional risk, task transfer, and soft-label/white-box counterexamples.
4. TT quotient geometry, functional visibility, and a verifiable nonlinear block.
5. Split-sample and same-sample population oracle inequalities.
6. Matching lower bounds, LAN constant, a separate Gaussian-sequence benchmark, and rank boundary.
7. Functional-versus-Frobenius improvement; Fisher scope.
8. Same-data multi-capability certification.
9. Synthetic experiments and preregistered LLM falsification gate.
10. Discussion, limitations, and narrow novelty statement.
11. Appendices with complete proofs and reproducibility details.

## Challenge-to-contribution consistency

| Challenge | Method | Theorem/evidence | Contribution claim |
|---|---|---|---|
| Gauge redundancy | Horizontal TT charts | Dimension lemma and Jacobian ranks | Correct \(d_{TT}\), not raw cores |
| Functional null directions | Restricted information + nonlinear block | Curvature proposition | States when \(d_{fun}=d_{TT}\) |
| Population selection | Local entropy + coded validation | Oracle theorem | \(A^2+(d+x)/n\) |
| Sharpness | Assouad + normal tube + LAN | Three lower/sharp results | Modelwise matching and exact constant |
| Access ambiguity | Soft-label and white-box experiments | Exact-recovery counterexamples/sandwich trace | No access-free \(d/n\) claim |
| Rank singularity | Functional separation + Le Cam | Boundary impossibility | Separates risk adaptation/rank recovery |
| Surrogate mismatch | Generalized eigenvectors | Misordering theorem/simulation | Strict improvement on constructed class |
| Data reuse | Cluster stability + McDiarmid | Uniform band | Valid post-selection capabilities under stability |

## Self-consistency check

- **Problem–method:** Each theorem targets the finite-query conditional-law experiment; the white-box regime is explicitly separate.
- **Challenge–module:** Every listed challenge has a method and a theorem or an explicit limitation.
- **Method–contribution:** No contribution claims a generic tensor-network oracle, Fisher objective, or simultaneous risk control as new.
- **Theory–experiment:** Simulations test quotient rank, \(d/(2n)\), the access counterexample, metric reversal, and oracle adaptation. They do not impersonate LLM evidence.
