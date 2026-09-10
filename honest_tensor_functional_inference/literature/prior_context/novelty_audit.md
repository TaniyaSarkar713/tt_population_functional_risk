# Primary-source novelty audit

Search cutoff: **7 September 2026**  
Scope: TT/tree-tensor statistical learning, tensor and low-rank minimax theory, post-training LLM compression, Fisher/KL/output-aware objectives, and post-selection multi-risk certification.  
Evidence rule: arXiv originals, official proceedings, and journal pages were prioritized. A search can support “we did not find,” never prove universal absence.

## Verdict

The *conjunction* below appears unoccupied among the primary sources located through the search cutoff:

1. one common TT-compressed parameter inside a frozen nonlinear conditional generator;
2. population teacher-relative conditional KL across deployment environments;
3. tensorization/rank selection from finitely many stochastic teacher queries; and
4. modelwise upper and lower risk bounds expressed in horizontal coordinates of a TT gauge quotient.

That is not yet the same as establishing a top-journal theoretical contribution. The current draft obtains the regular \(d_\lambda/n\) law using a concrete finite pivot atlas on compact rank-separated strata, a quadratic likelihood margin, and a local information-normal tube with an off-chart separation condition. It does not derive uniform geometry on the singular rank union or verify every regularity condition for a full transformer. Smooth-parametric fast rates, local asymptotic minimax constants, stability concentration, and the TT dimension formula are classical ingredients.

Estimated confidence that the **exact problem conjunction** is novel: **0.65–0.80**. Estimated confidence that the **current conditional theorem package is already substantively novel enough for JASA/JRSS-B**: **0.30–0.45**. Estimated methodological novelty of the same-data certificate: **0.05–0.15**.

The core theory becomes materially stronger to the extent that it makes the rank-separation dependence of the quotient atlas/entropy constants explicit, verifies nonlinear functional identifiability beyond the deliberately restricted frozen block, and discharges the normal-tube off-chart separation condition in a nontrivial resource class. A theory in which the restricted information is singular or weak would be a further contribution; the present proof does not establish a universal \(d_{\mathrm{fun}}/n\) law in that regime.

## Closest-collision matrix

| Collision | What the primary source already establishes | Surviving distinction |
|---|---|---|
| [Michel & Nouy, *Learning with tree tensor networks: complexity estimates and model selection*, Bernoulli 2022](https://projecteuclid.org/journals/bernoulli/volume-28/issue-2/Learning-with-tree-tensor-networks-Complexity-estimates-and-model/10.3150/21-BEJ1371.full) | Metric entropy and penalized empirical-risk model selection for tree-tensor function classes under general contrasts; fast rates and near-minimax adaptation are developed under bounded least squares. Their complexity \(C_m\) counts representation parameters and is not the present gauge-quotient dimension. This is the strongest oracle collision. | Their object is a tree-tensor predictor, not TT-compressed weights propagated through a fixed nonlinear conditional generator. The observation model, teacher-relative KL projection, quotient-functional identifiability, and access comparison remain different. |
| [Novikov et al., *Tensorizing Neural Networks*, NeurIPS 2015](https://papers.nips.cc/paper_files/paper/2015/hash/6855456e2fe46a9d49d3d3af4f57443d-Abstract.html), [Qi et al., *Performance Analysis for Tensor-Train Decomposition to DNN Based Vector-to-Vector Regression*, CISS 2020](https://doi.org/10.1109/CISS48834.2020.1570617364), and [Xu, Xu & Mandic, *TensorGPT*](https://arxiv.org/abs/2307.00526) | Direct TT neural layers, approximation/estimation/optimization performance decompositions for TT neural regression, and TT compression of GPT-family embeddings. | No teacher-relative conditional KL, coded rank oracle, gauge-sharp lower bound, or access comparison. These sources block “first TT neural/LLM compression” and “first population risk bound for TT neural networks.” |
| [Imaizumi, Maehara & Hayashi, *On Tensor Train Rank Minimization: Statistical Efficiency and Scalable Algorithm*, NeurIPS 2017](https://proceedings.neurips.cc/paper_files/paper/2017/hash/1b5230e3ea6d7123847ad55a1e06fffd-Abstract.html), [Zhou et al., *Optimal High-Order Tensor SVD via Tensor-Train Orthogonal Iteration*, IEEE TIT 2022](https://doi.org/10.1109/TIT.2022.3152733), [Qin, Wakin & Zhu, *Guaranteed Nonconvex Factorization Approach for Tensor Train Recovery*, JMLR 2024](https://www.jmlr.org/papers/v25/24-0029.html), [Qin & Zhu, *Computational and Statistical Guarantees for Tensor-on-Tensor Regression with Tensor Train Decomposition*](https://arxiv.org/abs/2406.06002), [Liu, Lee & Zhang, *Tensor Quantile Regression with Low-Rank Tensor Train Estimation*, AOAS 2024](https://doi.org/10.1214/23-AOAS1835), and [Peng, Lin & Lian, *Tensor Train Regression with Convex Regularization*, Statistics 2025](https://doi.org/10.1080/02331888.2025.2482070) | TT-rank estimation/recovery, optimization, upper rates, information-theoretic or minimax lower bounds, inference, and regression have already been developed in explicit tensor observation models. | None of these sources studies the present teacher-query conditional-density experiment after a frozen nonlinear map. They categorically block “first TT statistical theory,” “first TT minimax result,” and broad TT-inference claims. |
| [Holtz, Rohwedder & Schneider, *On manifolds of tensors of fixed TT-rank*, Numerische Mathematik 2012](https://link.springer.com/article/10.1007/s00211-011-0419-7) | Fixed-full-rank TT manifold, gauge action, tangent representation, dimension formula. | Novelty can only lie in connecting the quotient to visible nonlinear conditional-law information. The dimension formula itself is classical. |
| [Jovcheva, Seynnaeve & Vannieuwenhoven, *Minimality of Tree Tensor Network Ranks*, LAA, online 2 Sep 2026](https://www.sciencedirect.com/science/article/pii/S0024379526003538) | Admissible/minimal tree-tensor bond ranks and genericity. | Rank tuples in this paper must be explicitly admissible/minimal. |
| [Zhang & Saab, *Theoretical Guarantees for Low-Rank Compression of Deep Neural Networks*](https://arxiv.org/abs/2502.02766) and [El Cheairi, Gamarnik & Mazumder, *Theoretical Compression Bounds for Wide MLPs*, COLT 2026](https://proceedings.mlr.press/v336/el-cheairi26a.html) | Rigorous matrix low-rank or pruning/quantization approximation results for neural networks. | Not TT population model selection from teacher queries. |
| [Arunan J, *Tight Sample Complexity for Low-Rank Adaptation: Matching Bounds and Rank Selection*](https://arxiv.org/abs/2607.27680) | Local-Rademacher upper \(\widetilde O(rd/n)\), matching Fano lower bounds, and rank selection for low-rank adaptation; the framework includes a frozen nonlinear pretrained map and locally quadratic losses, with cross-entropy examples/extensions. | TT gauge geometry, approximation to a dense teacher, and the stochastic-teacher access comparison remain different. “Frozen nonlinear networks” and “matching low-rank neural rates” are not surviving novelty claims. |
| [Haverbeck et al., *The risk of KV cache compression*](https://arxiv.org/abs/2607.01520) | Query-distribution population MSE for fixed-budget KV-cache summaries, with spectral-tail upper bounds and matching minimax lower bounds. | The compressed object, loss, and experiment differ, but this blocks “first population/minimax functional compression theory.” |
| [Phuong & Lampert, *Towards Understanding Knowledge Distillation*, ICML 2019](https://proceedings.mlr.press/v97/phuong19a.html), [Menon et al., *A Statistical Perspective on Distillation*, ICML 2021](https://proceedings.mlr.press/v139/menon21a.html), and [Xie, Schmidt & Duchi, *Two Mathematical Models of Knowledge Distillation*, AISTATS 2026](https://proceedings.mlr.press/v300/xie26b.html) | Identifiability/optimization in structured student models, variance and label-noise effects of soft teachers, and statistical analyses of distillation. | The present TT quotient and model-selection geometry remain different. The access claim is limited to counterexamples: a feasible teacher parameter supplied directly gives immediate zero error, while sampled exact probability vectors identify the parameter in the stated full-rank logistic design but not in every soft-label model. |
| [Isik, Weissman & No, *An Information-Theoretic Justification for Model Pruning*, AISTATS 2022](https://proceedings.mlr.press/v151/isik22a.html), [Kong et al., *A KL Lens on Quantization*](https://arxiv.org/abs/2604.13440), [Helcig et al., *Statistically-Lossless Quantization of LLMs*](https://arxiv.org/abs/2605.02404) | Output distortion, KL sensitivity, and statistically lossless compression objectives. | Conditional KL is appropriate but not itself novel. |
| [Hsu et al., *Language model compression with weighted low-rank factorization*, ICLR 2022](https://openreview.net/forum?id=uPv9Y3gmAI5), [Chekalina et al., *GFWSVD*](https://arxiv.org/abs/2505.17974), [Abbasi et al., *IO-SVD*](https://arxiv.org/abs/2605.15626), and [Wang et al., *LASER*](https://arxiv.org/abs/2606.00573) | Activation-, output-, Fisher-, or Hessian-aware low-rank objectives and layer/rank allocation already make compression loss-sensitive. | Within the present framework, Fisher is the local second-order pullback of correctly specified conditional KL. Under misspecification the contrast Hessian and score covariance need not agree. This is an organizing distinction, not a claim that Fisher-aware compression is new. |
| [Zagitov et al., *Rethinking the Role of Tensor Decompositions in Post-Training LLM Compression*](https://arxiv.org/abs/2606.03465) | Large empirical/theoretical diagnosis of the tensor weight-reconstruction versus model-behavior mismatch. | Motivates the problem but does not give the population TT oracle/minimax experiment. |
| [Swift-SVD, 2026](https://arxiv.org/abs/2604.01609) | Activation-aware layerwise optimum and dynamic global allocation using reconstruction, effective rank, and importance. | Calibration optimum is not a global population conditional-risk oracle. |
| [StatLoRA, 2026](https://arxiv.org/abs/2607.20205), [RAFFT, AISTATS 2026](https://proceedings.mlr.press/v300/zhou26a.html), [MetaTT, 2025](https://arxiv.org/abs/2506.09105) | Statistical component tests, dynamic rank algorithms, or meta-learned TT ranks. | Rank allocation in isolation is occupied; none gives the target oracle/lower pair. |
| [Shi, Chi & Luo, *Asymptotic Optimism for Tensor Regression Models with Applications to Neural Network Compression*](https://arxiv.org/abs/2603.26048) | Population training--test optimism for Gaussian random-design CP/Tucker regression and prediction-oriented rank selection applied to neural-network compression. The paper explicitly leaves TT extensions to future work. | The present experiment is nonlinear conditional-density estimation on TT weight quotients. “Prediction-aware rank selection” is occupied; the TT/conditional-density instantiation is the narrower distinction. |
| [Xu, Chen & Han, *Statistical Inference for Low-Rank Tensor Models*](https://arxiv.org/abs/2501.16223) and [Silva et al., *Identifiability of Tensor Ranks via Prior Predictive Matching*, AISTATS 2026](https://proceedings.mlr.press/v300/silva26a.html) | Tangent-space debiasing, minimax confidence intervals, and rank identification in probabilistic tensor models. | Do not study pretrained-network functional approximation, but block broad inference/identifiability claims. |
| [Learn then Test](https://arxiv.org/abs/2110.01052), [Pareto Testing](https://openreview.net/forum?id=cyg2YXn_BqF), [Adaptive Learn-then-Test](https://proceedings.mlr.press/v267/zecchin25a.html), and [Adams, Shawe-Taylor & Guedj, *Controlling Multiple Errors Simultaneously with a PAC-Bayes Bound*, NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/09887fac6cb071922e870090ce32aeff-Abstract-Conference.html) | Simultaneous/adaptive multi-risk control and multiple-error PAC-Bayes bounds already address finite families and several risks. | The draft's result is an application-level band for a coded TT path fit and evaluated on the same independent clusters, not a new general multiple-risk concentration method. |
| [Bousquet & Elisseeff, *Stability and Generalization*, JMLR 2002](https://www.jmlr.org/papers/v2/bousquet02a.html), [Feldman & Vondrák, *High Probability Generalization Bounds for Uniformly Stable Algorithms with Nearly Optimal Rate*, COLT 2019](https://proceedings.mlr.press/v99/feldman19a.html), [Bousquet, Klochkov & Zhivotovskiy, *Sharper Bounds for Uniformly Stable Algorithms*, COLT 2020](https://proceedings.mlr.press/v125/bousquet20b.html), [Pérez-Ortiz et al., *Tighter Risk Certificates for Neural Networks*, JMLR 2021](https://www.jmlr.org/papers/v22/20-879.html), [Cross-Validation Conformal Risk Control](https://arxiv.org/abs/2401.11974), and [Feng et al., *Sequential algorithmic modification with test data reuse*, UAI 2022](https://proceedings.mlr.press/v180/feng22a.html) | Stability concentration, PAC-Bayes self-certification, cross-validation risk control, and controlled test reuse already cover the proof technology and neighboring reuse settings. | No exact same-cluster TT-path formulation was located, but specialization of bounded differences plus a coded union bound is not a flagship theoretical novelty. |
| [Carpentier & Nickl, *Signal detection and confidence sets for low rank inference*](https://arxiv.org/abs/1507.03829), [Carpentier et al., *Adaptive confidence sets for matrix completion*](https://arxiv.org/abs/1608.04861) | Detection/adaptation limitations near low-rank matrix boundaries. | Matrix analogues strongly constrain any honest TT-rank adaptation claim; separation is required. |

## Exact mathematical gap

Let \(\mathcal M_\lambda(\eta,R)\) be a compact, rank-separated product of exact-minimal TT-rank core strata, \(\mathcal G_\lambda\) its internal gauge group, and

\[
\Phi_\lambda:\mathcal Q_\lambda=\mathcal M_\lambda/\mathcal G_\lambda
\longrightarrow\{p_W(\cdot\mid x,e)\}
\]

the conditional-law map through the frozen nonlinear network. For a stochastic teacher-query experiment

\[
E_i\sim w,\qquad X_i\mid E_i=e\sim P_e,\qquad
Y_i\mid X_i,E_i\sim q_0(\cdot\mid X_i,E_i),
\]

define

\[
D_w(W;q_0)=\sum_e w_eE_{P_e}
\operatorname{KL}\{q_0(\cdot\mid X,e)\|p_W(\cdot\mid X,e)\},
\]

and \(A_w^2(\lambda)=\inf_{W\in\Theta_\lambda}D_w(W;q_0)\). On an untied regular TT stratum, the algebraic quotient dimension is

\[
d_{\lambda}^{\mathrm{TT}}=
\sum_\ell\left\{
\sum_{j=1}^{q_\ell}r_{\ell,j-1}m_{\ell j}r_{\ell j}
-\sum_{j=1}^{q_\ell-1}r_{\ell j}^2
\right\}+d_{\lambda,\mathrm{free}}.
\]

If \(G_w(W)\) denotes the conditional-KL pullback on the horizontal tangent, then

\[
d_{\mathrm{fun}}(W)=
\operatorname{rank}\!\left\{
G_w(W)\big|_{T_W^H\mathcal Q_\lambda}
\right\}\le d_{\lambda}^{\mathrm{TT}}.
\]

The *current regular result* assumes uniform restricted information,

\[
0<\underline\kappa I_{d_\lambda}
\preceq G_w(W)\big|_{T_W^H\mathcal Q_\lambda}
\preceq \overline\kappa I_{d_\lambda},
\]

so that \(d_{\mathrm{fun}}=d_\lambda^{\mathrm{TT}}\). With a finite horizontal atlas of size \(H_\lambda\), bounded likelihood ratios, a quadratic margin, chartwise Lipschitz likelihoods, and explicit optimization error, the defensible oracle target is

\[
\mathbb E D_w(\widehat W_{\widehat\lambda};q_0)
\le C\inf_\lambda\left[
A_w^2(\lambda)+C_{\mathrm{reg},\lambda}
\frac{d_\lambda^{\mathrm{TT}}+\log H_\lambda+\log(1/\pi_\lambda)}{n}
+\varepsilon_{\lambda,\mathrm{opt}}
\right]+r_n.
\]

On a regular horizontal chart with two-sided local experimental-metric equivalence, the modelwise target is

\[
\inf_{\widetilde p}\sup_{u\in B_{d_\lambda}(0,\rho)}
\mathbb E_uD_w\{p_{\psi(u)},\widetilde p\}
\ge c\left\{\rho^2\wedge\frac{d_\lambda^{\mathrm{TT}}}{n}\right\}.
\]

The draft's stronger approximation-plus-estimation result is correctly restricted to a fixed resource class and an explicitly constructed local normal teacher family. It requires positive functional codimension, a smooth information-normal field, a separated off-chart complement, and two-sided tube control. These conditions yield

\[
\inf_{\widetilde W\in\Theta_\lambda}\sup_u
\mathbb E_{u,a}D_w(P_{u,a},p_{\widetilde W})
\gtrsim a^2+\left(\rho^2\wedge\frac{d_\lambda^{\mathrm{TT}}}{n}\right),
\qquad A_w^2(\lambda;P_{u,a})\asymp a^2.
\]

This is not an oracle lower bound for an arbitrary union of ranks. A universal pointwise lower bound equal to \(\inf_\lambda\{A_\lambda^2+d_\lambda/n\}\) is false without a least-favorable family and a resource restriction.

The main unresolved mathematical gap is the *singular or weakly identified* case. When \(G_w|_{T^H}\) is rank deficient or has eigenvalues tending to zero with \(n\), replacing \(d_\lambda\) by \(d_{\mathrm{fun}}\) is not justified in general: higher-order identification and the spectrum of weak directions can change both rate and local experiment. A genuine extension would characterize a localized effective complexity such as

\[
\mathfrak d_\lambda(t)
=\operatorname{tr}\!\left[
G_{w,\lambda}\{G_{w,\lambda}+tI\}^{-1}
\right]
\]

or an appropriate higher-order analogue, prove an oracle rate solving a fixed-point equation in \(\mathfrak d_\lambda(t)\), and match it by a lower experiment on the stratified TT quotient. The displayed \(\mathfrak d_\lambda\) is a research target, not a theorem of the current paper.

If query and deployment mixtures differ, the sharp regular local constant is

\[
\frac{1}{2n}\operatorname{tr}(G_wI_\pi^{-1}),
\]

not \(d/(2n)\). At correct conditional specification \(G_w=I_w\); it reduces to \(d/(2n)\) only if \(w=\pi\). Under misspecification, the contrast Hessian and score covariance form a sandwich and should not both be called Fisher information.

## Safe novelty wording

> Among the primary sources identified through 7 September 2026, we did not find a result that simultaneously treats a common TT-compressed parameter inside a frozen nonlinear conditional generator, measures population teacher-relative conditional KL across deployment environments, selects tensorizations and ranks from stochastic teacher queries with a nonasymptotic approximation--estimation oracle inequality, and obtains a matching modelwise local lower bound in horizontal coordinates of a rank-separated TT quotient. The rate is indexed by the classical gauge-adjusted TT dimension only under the paper's explicit atlas, functional-identifiability, likelihood-margin, and local experimental-metric conditions.

Secondary claim:

> As an application of classical stability and bounded-difference concentration, the paper gives simultaneous multi-capability upper bands for a fixed coded family of TT procedures whose ranks and cores are fitted and evaluated on the same independent prompt clusters, followed by least-cost feasible selection. We do not claim a new general concentration method; the result is narrower than Learn-then-Test, Pareto Testing, multiple-error PAC-Bayes bounds, cross-validation risk control, and adaptive test-data reuse.

## Search conclusion

The direction survives, but narrowly. It should be presented as a statistics paper about a specific stochastic teacher-query experiment and its TT quotient-functional geometry, not as the first tensor oracle, first TT statistical theory, first loss-aware compression method, first distillation theory, or first low-rank minimax result.

For JASA or JRSS-B, the decisive technical material is the explicit rank-separated pivot atlas, a genuinely checkable nonlinear-block information bound, and the fixed-resource normal-tube construction, with every dependence on rank separation, atlas size, off-chart separation, and likelihood curvature carried into the oracle constants. The current theorem should remain advertised as regular-stratum and modelwise. Annals of Statistics or Biometrika would likely require a broader advance: singular/weak-information rates, a stratified union result, or a genuinely adaptive lower/upper theory across TT-rank boundaries. The certification result is useful operationally but should remain secondary.
