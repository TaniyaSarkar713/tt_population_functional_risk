# Honest functional inference across unknown and weak Tucker/TT ranks

**Literature and novelty assessment • September 9, 2026 • Research decision document, not a manuscript**

## Decision

**Promising — sharpen the theoretical gap first.** The strongest surviving claim is **B: a meaningful partial gap**, with moderate confidence in the novelty assessment. The original wording is too broad to justify a paper. Existence of honest rank-agnostic intervals, regular Tucker functional inference, inference without estimating matrix rank, and deterministic Tucker/TT tangent-cone characterization are already established or follow from elementary procedures. Moreover, uniformly recovering the known-rank oracle interval length over an unrestricted rank union is generally impossible.

The potentially substantial project is:

> Characterize the attainable expected length of confidence intervals for prescribed tensor linear functionals, under coverage over the entire bounded-rank union, including weak and vanishing singular values. Establish when adaptation is possible, when additional rank directions prevent it, and whether the coupled tensor constraints create a statistical phenomenon beyond matrix unfolding.

Do not begin the full paper or a simulation campaign yet. First identify one concrete tensor family and loading regime where matching upper and lower bounds would improve on the direct interval, matrix relaxations, and generic confidence-set projection. The audit found no substantially equivalent **complete** theorem for that formulation, but it did find most of its proposed ingredients. Absence from this search is not proof of absence from the literature.

The strongest direct competitor is Xu–Chen–Han’s general Tucker linear-functional inference; the most serious conceptual threats are Zhu’s weak-factor adaptation impossibility, Cai–Low’s adaptation theory, Choi–Kwon–Liao’s inference without estimating rank, and Armstrong–Weidner–Zeleneev’s uniformly valid weak-factor inference. Covariance-adjusted regular-manifold inference is also covered by a Statistica Sinica accepted preprint updated September 8, 2026. [R01](https://arxiv.org/abs/2501.16223), [R02](https://arxiv.org/abs/1910.10382), [R05](https://arxiv.org/abs/math/0503662), [R03](https://arxiv.org/abs/2311.16440), [R04](https://arxiv.org/abs/2210.06639), [R06](https://www3.stat.sinica.edu.tw/statistica/fp/SS-2026-0222.html).

## What the existing project actually contains

The folder contains an existing TT population-functional-risk project, including [project status](../PROJECT_STATUS.md), [theory decisions](../theory_decisions.md), [the prior novelty audit](../novelty_audit.md), and manuscript sections on the [statistical experiment](../../paper/sections/03_experiment.tex), [functional geometry](../../paper/sections/07_functional_geometry.tex), [certification](../../paper/sections/08_certification.tex), and [lower bounds](../../paper/sections/06_lower_bounds.tex).

Those materials distinguish white-box teacher access, stochastic response access, and exact probability/soft-label access. Their regular theory uses compact, separated rank strata and studies population KL risk, model selection, and certificates. A fixed-stratum risk bound and a selected-model risk certificate do not establish uniform confidence coverage at rank boundaries. The existing indistinguishability argument for rank recovery is also different from an optimal interval-length theorem.

Three questions must remain separate:

1. **A fixed population parameter:** infer a prespecified functional of an unknown tensor or conditional law.
2. **Risk of a trained model:** infer expected loss conditional on the training data, often using independent validation.
3. **Rank or factor coordinates:** recover structural parameters that can be nonunique or statistically undetectable.

Failure of the third does not imply failure of the first. The initial mathematical formulation was saved in [formulation_before_search.md](formulation_before_search.md) before literature searching. The recommended formulation below incorporates the subsequent novelty checks. No existing manuscript sections were changed.

## 1. Precise statistical formulation

### 1.1 Primary regression experiment

Let $K\geq3$ be fixed initially, $\mathbf p=(p_1,\ldots,p_K)$, and $D=\prod_kp_k$. Observe independent pairs

$$
(X_i,Y_i)\sim P_A,\qquad
\operatorname{vec}(X_i)\sim N(0,I_D),\qquad
Y_i=\langle X_i,A\rangle+\epsilon_i,\quad
\epsilon_i\sim N(0,\sigma^2),\quad i=1,\ldots,n.
$$

The errors and designs are independent. The initial benchmark takes $\sigma>0$ and the design law as known. The identifiable parameter is $A\in\mathbb R^{p_1\times\cdots\times p_K}$. Factor matrices and cores are nonunique coordinates of $A$; there is no additional stochastic latent-factor sampling model here.

With squared loss,

$$
R_A(B)=\mathbb E_A(Y-\langle X,B\rangle)^2
=\sigma^2+\|B-A\|_F^2,\qquad
R_n(B)=\frac1n\sum_i(Y_i-\langle X_i,B\rangle)^2.
$$

For Tucker structure write $A_{(k)}$ for mode-$k$ unfolding. For TT structure write $A_{\langle k\rangle}$ for the unfolding separating modes $1{:}k$ from $k+1{:}K$. Define two distinct parameter spaces:

$$
\Theta^{\mathrm{Tu}}_{\bar{\mathbf r}}(M)
=\{A:\|A\|_F\leq M,\ \operatorname{rank}(A_{(k)})\leq\bar r_k\ \forall k\},
$$

$$
\Theta^{\mathrm{TT}}_{\bar{\mathbf r}}(M)
=\{A:\|A\|_F\leq M,\ \operatorname{rank}(A_{\langle k\rangle})\leq\bar r_k\ \forall k<K\}.
$$

Use one as $\Theta_n$, not their union by default. Both include zero and every feasible lower-rank stratum. **There is no lower bound on nonzero unfolding singular values.** The rank cap is supplied; actual ranks and singular values are unknown. Adaptation to an unknown cap is a different problem requiring an outer honesty class.

The dimensions of nonempty regular exact-rank strata are

$$
d_{\mathbf r}^{\mathrm{Tu}}=\prod_kr_k+\sum_k(p_kr_k-r_k^2),\qquad
d_{\mathbf r}^{\mathrm{TT}}=\sum_{k=1}^Kr_{k-1}p_kr_k-\sum_{k=1}^{K-1}r_k^2,
\quad r_0=r_K=1.
$$

These count identifiable local dimensions, not unrestricted core coordinates. They do not give a universal interval-length rate at singularities.

A possible pilot is a rank-penalized constrained least-squares estimator,

$$
\widehat A\in\arg\min_{B\in\Theta_n}
\{R_n(B)+\operatorname{pen}_n(\mathbf r(B))\}.
$$

Its use is a procedure choice, not an innovation. A global minimizer defines a statistical benchmark; practical alternating optimization needs a separate guarantee. Do not assume a selected rank is correct.

### 1.2 Estimand, honesty, and asymptotics

Fix a loading tensor $L=L_n$ independently of the data, normalized by $\|L\|_F=1$, and target

$$
\psi_L(A)=\langle L,A\rangle.
$$

Examples are an entry, an average with explicitly rescaled loading, or a dense contrast. A data-selected loading requires additional selection handling. Seek an interval $C_n$ satisfying

$$
\liminf_{n\to\infty}\ \inf_{A\in\Theta_n}
P_A\{\psi_L(A)\in C_n\}\geq1-\alpha.\tag{H}
$$

The infimum includes triangular sequences whose smallest nonzero unfolding singular values vanish. Begin with fixed $K$, growing mode dimensions, bounded $M$, and specified rank caps. The useful dimension/sample conditions are theorem targets, not assumptions already known to suffice for an adaptive interval. A pilot-based approach additionally needs uniform estimation control; a denoising lower bound does not automatically transfer an upper procedure to regression.

The starting experiment has no contamination, serial dependence, missingness, unknown design covariance, or model misspecification. Adding all these would obscure the central question. Weak tensor rank, factor-coordinate gauge ambiguity, and degeneracy of the observation model’s Fisher information are separate phenomena.

### 1.3 Diagnostic Gaussian experiment

Also study

$$
Z=A+\tau G,\qquad \tau=\sigma/\sqrt n,\qquad
\operatorname{vec}(G)\sim N(0,I_D).\tag{G}
$$

Here $n$ indexes noise precision; it need not count observed tensor entries. This is a separate benchmark, not an asserted asymptotic equivalence to regression. It exposes inference obstructions with minimal nuisance structure. The first substantial theorem may be developed in (G), followed by a justified regression extension.

## A. Literature taxonomy and independent search concepts

| Literature | Mathematical concepts searched independently | Why it matters |
|---|---|---|
| Structured linear inverse problems | Atomic norms; debiasing; restricted isometry; influence functions; local geometry | Generic rank-free estimation and scalar inference are established. R07–R08. |
| Tensor inference | Tucker/CP/TT regression; tensor PCA; entrywise CLTs; loading alignment; heteroskedastic perturbations | Closest positive theorems and their signal restrictions. R01, R06, R11–R12, R19–R20, R30. |
| Matrix uncertainty quantification | Trace regression; completion; rank-adaptive confidence balls; nuclear/Frobenius losses | Shows that inference and adaptation depend on the observation scheme and loss. R09–R10, R13, R21. |
| Honest adaptation and minimax theory | Expected interval length; ordered modulus; between-class modulus; testing separation; mixtures | Defines the correct benchmark and rules out false oracle promises. R05, R23. |
| Optimal recovery and aggregation | Finite unions of convex sets; nonlinear functional estimators; convex tests; discretization entropy | Nonconvex functional estimation and computational constructions have extensive prior theory. R31–R32, R35–R37. |
| Post-selection and weak identification | Pointwise versus uniform asymptotics; selected-model distributions; locally almost unidentified functionals | Consistent selection is not a uniform-inference argument; rank weakness is not automatically nonidentification. R33–R34. |
| Bayesian uncertainty | Rank priors; posterior contraction; subspace posteriors; Bernstein–von Mises; frequentist coverage of credible sets | Posterior probability and union-uniform frequentist coverage are different guarantees. R38–R39. |
| Econometrics and weak factors | Interactive fixed effects; weak identification; overestimated factor number; bias-aware intervals | Most serious prior work on unknown and weak rank. R02–R04. |
| Algebraic statistics and applied mathematics | Rank varieties; stratification; Bouligand cones; Chernoff regularity; singular likelihood | Geometry and pointwise singular likelihood limits already exist. R15–R17. |
| Random matrix theory | Weak spikes; BBP transition; critical eigenvalue laws; uniform signal inference | Critical transitions are not a new concept. R18. |
| Nonlinear functional estimation | Quadratic functional; squared norm; Schatten norm; loss estimation; vanishing derivative | A distinct possible project, requiring distinct lower bounds. R24–R25. |
| General finite-sample inference | Split likelihood; profile likelihood; e-values; model projection under misspecification | Gives coverage without rank regularity, but not automatically sharp width. R14, R22. |
| Learning and optimization | Tensor-network entropy; rank/model selection; oracle risk; nonconvex algorithms | Prevents relabeling estimation/model selection as new inference. R26, R29. |
| Prediction and AI applications | Conformal tensor completion; LoRA component testing; prompt clusters; teacher-query access | Similar applications can concern different estimands and coverage notions. R27–R29. |

The search crossed statistics, econometrics, information theory, machine learning, and applied mathematics. Venue labels are not a novelty filter: the strongest threats include JASA, Annals of Statistics, JRSS-B, Bernoulli, Statistica Sinica, JPE, IEEE TIT/ICML, and mathematical optimization journals. No claim is made that every paper at every requested venue was exhaustively enumerated.

Bayesian matrix uncertainty quantification was also screened: BayeSMG models row and column subspaces. A posterior credible probability does not by itself imply (H), and posterior contraction is not a coverage theorem. [R38](https://arxiv.org/abs/2101.01299). The classical Bayesian-coverage literature explicitly studies restrictions under which adaptation can give frequentist coverage; it should guide any later Bayesian version. [R39](https://arxiv.org/abs/1310.4489). These are supplementary comparisons, not fully audited competing tensor-union theorems.

## 2. Elementary checks that disprove broad novelty claims

The calculations in this section are audit diagnostics, not proposed new research theorems.

### 2.1 Honest intervals do not require identifiable rank

In (G),

$$
C_{\rm direct}(Z)=
\left[\langle L,Z\rangle\pm z_{1-\alpha/2}\tau\right]
$$

has exact coverage for every tensor in the ambient space. Thus “honest functional inference across all ranks” is solved if interval existence is the whole claim.

The regression benchmark has an equally revealing baseline. Set $z_i=\langle L,X_i\rangle$. Gaussian orthogonality gives

$$
Y_i=\psi_L(A)z_i+\eta_i,\qquad
\eta_i\perp z_i,\qquad
\eta_i\sim N(0,\sigma^2+\|A\|_F^2-\psi_L(A)^2).
$$

Ordinary scalar regression through the origin therefore provides an exact $t$ interval, with $n-1$ residual degrees of freedom. Its width is uniformly of root-$n$ order over bounded $\|A\|_F$. It needs no rank estimation, even when $D\gg n$. Known isotropic Gaussian design is doing substantive work here.

An independent consistent pilot can remove the extra design variation. On an inference sample of size $m$, use

$$
\widetilde\psi=\langle L,\widehat A\rangle+
\frac1m\sum_i(Y_i-\langle X_i,\widehat A\rangle)\langle X_i,L\rangle.
$$

Conditional on the pilot, put $\Delta=A-\widehat A$. Then

$$
\widetilde\psi-\psi_L(A)
=\frac1m\sum_i\epsilon_i\langle X_i,L\rangle
+\frac1m\sum_i\{\langle X_i,\Delta\rangle\langle X_i,L\rangle-\langle\Delta,L\rangle\}.
$$

The second term has conditional mean zero and variance

$$
\frac{\|\Delta\|_F^2+\langle\Delta,L\rangle^2}{m}.
$$

Uniform Frobenius consistency makes this term negligible at scale $m^{-1/2}$. Thus ambient-variance inference can be rank agnostic without a singular-value gap. This does not establish the much smaller known-rank tangent variance. Matrix geometric debiasing and hard-thresholding inference are also explicit prior precedents. [R07](https://arxiv.org/abs/1404.4408), [R08](https://arxiv.org/abs/1502.04654).

### 2.2 Known-rank oracle length is the wrong universal benchmark

On a regular exact-rank manifold $\mathcal M_{\mathbf r}$ in isotropic regression, the first-order oracle variance is

$$
V_{\mathbf r}(A,L)=\sigma^2\|\Pi_{T_A\mathcal M_{\mathbf r}}L\|_F^2.
$$

Regular projection inference exploits this geometry. If the projection vanishes, first-order normal theory alone does not determine the next-order interval length. Across a larger rank union, additional directions can change the functional even when the existing singular values are well separated.

For example, suppose $A$ is interior to the norm ball and all its ranks have one unit of slack below the cap. Let $L=u_1\otimes\cdots\otimes u_K$ with unit factors. Rank subadditivity gives

$$
A+tL\in\Theta_n
$$

for sufficiently small $|t|$, for both Tucker and TT caps. In (G), choose $B=A+c\tau L$. Then

$$
\psi_L(B)-\psi_L(A)=c\tau,\qquad
\mathrm{KL}(P_A,P_B)=c^2/2.
$$

For an interval honest at both points,

$$
\mathbb E_A|C_n|\geq c\tau
\{1-2\alpha-\mathrm{TV}(P_A,P_B)\}
\geq c\tau(1-2\alpha-c/2),\tag{1}
$$

with positive constant for sufficiently small $c$ when $\alpha<1/2$. The same joint-design KL calculation holds in regression with $\tau=\sigma/\sqrt n$.

Consequently, for rank-one loadings, including individual entries, direct intervals are already rate optimal at such points. **Strong existing factors do not remove uncertainty about an additional weak component.** A claim to recover the oracle width everywhere on strong lower-rank strata fails this elementary test. Related impossibility phenomena are central in weak-factor work, but the particular observation model and scaling must be kept explicit. [R02](https://arxiv.org/abs/1910.10382).

### 2.3 Tangent-cone formulas alone are insufficient

For a matrix $A=USV^T$ of rank $r<s$, the rank-$\leq s$ tangent cone consists, in singular-vector coordinates, of block matrices $H$ with

$$
\operatorname{rank}(H_{22})\leq s-r.
$$

Writing $T$ for the rank-$r$ tangent space, the cone’s unit-ball support in direction $L$ satisfies

$$
\sup_{H\in T_{\{\operatorname{rank}\leq s\}}(A),\ \|H\|_F\leq1}
|\langle L,H\rangle|^2
=\|\Pi_TL\|_F^2+
\sum_{j=1}^{s-r}s_j^2\big((I-UU^T)L(I-VV^T)\big).
$$

This is an elementary consequence of the matrix cone and spectral optimization. Tucker and TT cone representations are also already available. [R15](https://arxiv.org/abs/2311.18324), [R16](https://arxiv.org/abs/1705.10152).

A cone is a first-order, pointwise object. Uniform inference along $A_n$ approaching a singularity requires control of finite-radius neighborhoods, changes in geometry, and composite testing. Replacing a tangent-space projector by an estimated cone does not establish coverage or optimality.

## 3. Strongest existing theory versus proposed theory

There is no single strongest rate across denoising, random-design regression, and missing-entry completion. The following comparisons preserve the observation model and inferential target.

| Topic | Best relevant existing result | Existing assumptions | Proposed extension | Difficulty and novelty |
|---|---|---|---|---|
| Arbitrary Tucker linear functional | Tangent-based CLT, feasible variance and interval lower bound, R01; covariance-adjusted version R06 | Regular exact rank; signal and pilot/loading restrictions | Coverage over $\Theta_n$ with no positive signal floor, plus sharp length | **B**, if the length result exceeds generic baselines; existence alone **D** |
| Unknown matrix rank | Valid block-average inference using an upper projection dimension, R03 | Quantitative factor strength and projection alignment remain | General tensor loadings and arbitrarily vanishing components | **B/C**; merely overestimating rank is already solved |
| Weak-rank robust inference | Uniform bias-aware panel coefficient inference, R04 | Rank cap, noncollinearity, noise regularity | Tensor functional-specific optimal bias/variance tradeoff | **B** only with a demonstrably sharper tensor result |
| Honest adaptation | Modulus lower bounds and class-dependent upper constructions, R05; high-dimensional sparsity analogues R23 | Upper results depend on class/design structure | Coupled nonconvex rank unions and loading-dependent attainable length | **B**, the main surviving direction |
| Nonconvex functional estimation | Finite convex-union minimax bounds R35 and convex-optimization recovery R36–R37 | Finite family; approximation/number-of-sets cost must be controlled | Exact tensor union and sharp adaptive expected length | **B/C** until discretization and aggregation are ruled out as sufficient |
| Whole-object rank adaptation | Matrix Frobenius confidence sets and scheme-dependent impossibility, R09/R13/R21 | Sampling/noise/rank conditions vary | Scalar functional length without paying whole-tensor diameter | **B/C**; projecting a known ball is a baseline |
| Singular geometry | Exact Tucker/TT cones, R15–R16; singular LRT law, R17 | Deterministic geometry or fixed-point/fixed-dimensional likelihood | Uniform finite-noise functional testing/interval theorem | **B** statistically; cone formula alone **D** |
| Weak-to-strong transitions | Matrix spike-strength inference through a critical regime, R18 | Specified spike/noise configurations | Loading-dependent transitions on tensor rank unions | **B**, but no transition exponent is known from this audit |
| Quadratic functional | Sparse quadratic-functional minimax theory R24; matrix Schatten-norm theory R25 | Different parameter classes and losses | Honest squared-norm intervals over tensor rank unions | **B, provisional**; requires a separate focused audit |
| Regular TT/quantile CLT | TT quantile asymptotic normality R20; Tucker quantile theory R30 | Fixed regular model / stated high-dimensional restrictions | Unknown-rank uniformity and optimal interval length | Routine regular extension **C/D** |
| Model-selected population risk | Tree-network complexity and risk oracle theory R26; optimism analysis R29 | Specified losses/design/architectures | A new population-functional interval, if validation does not already solve it | Generic risk bound or validation certificate **C/D** |

For example, R23 gives a sparse-loading expected-length scale involving $n^{-1/2}+k\log p/n$ under its unknown-covariance high-dimensional regression assumptions; the known-design experiment can behave differently. This is a warning against copying an adaptation penalty into the tensor problem. [R23](https://arxiv.org/abs/1506.05539).

The relevant tree-network oracle has the schematic form

$$
\mathbb E\mathcal R(\widehat f)\lesssim
\inf_m\{\text{approximation}_m+\text{complexity}_m/n\ \text{with logarithmic terms}\}
$$

under bounded regression conditions. It concerns risk and model selection, not (H) or minimax interval length. [R26](https://arxiv.org/abs/2007.01165).

## C. Precise surviving research gap

For a subclass $\mathcal F_n\subseteq\Theta_n$, define the finite-sample benchmark in (G)

$$
\mathcal I_\alpha(\Theta_n)
=\{C:\inf_{A\in\Theta_n}P_A(\psi_L(A)\in C)\geq1-\alpha\},
$$

$$
\ell^*_\alpha(\mathcal F_n,\Theta_n,L)
=\inf_{C\in\mathcal I_\alpha(\Theta_n)}
\sup_{A\in\mathcal F_n}\mathbb E_A|C|.\tag{2}
$$

Predetermine subclasses by feasible rank vector, bands for unfolding singular values, and loading/subspace geometry. They are evaluation classes; the interval must retain honesty on the same outer union. Asymptotic analogues can allow uniformly vanishing coverage error. The dependence on confidence level and norm bound must remain explicit.

The unresolved target is to characterize

$$
\ell^*_\alpha(\mathcal F_n,\Theta_n,L)
\asymp r_\alpha(\tau,\mathbf p,\bar{\mathbf r},\mathcal F_n,L,M)
$$

in a nontrivial family of regimes, and determine whether **one implementable interval** achieves these bounds simultaneously across the subclasses. The rate is deliberately symbolic. Computing the infimum separately for each subclass does not establish adaptation by a common procedure.

A necessary local benchmark is

$$
\omega_L(\varepsilon;A,\Theta_n)
=\sup_{B\in\Theta_n:\|B-A\|_F\leq\varepsilon}
|\langle L,B-A\rangle|,
\qquad
\mathbb E_A|C|\gtrsim\omega_L(c\tau;A,\Theta_n).
$$

The lower inequality follows from two-point testing, subject to the usual fixed confidence constants. **Do not assert a matching upper bound from this pairwise modulus alone.** Composite alternatives or mixtures may give stronger lower bounds, especially for a continuously indexed nonconvex union. Establishing whether the pairwise benchmark is sufficient is part of the research question.

Nonconvexity itself is not the gap. Cai–Low also develop minimax functional estimation over finite convex unions, with a logarithmic family-size cost in their upper bound. [R35](https://arxiv.org/abs/math/0406427). Juditsky–Nemirovski give computable high-probability functional recovery guarantees. A global error bound immediately gives an honest interval; a bound indexed by the unknown class does not automatically give an observable adaptive radius. [R36](https://arxiv.org/abs/1804.00355). Their later aggregation work reinforces this comparison. [R37](https://arxiv.org/abs/2107.07836).

For tensors, fix factor subspaces and the allowable cores form a convex class; a net over factor subspaces therefore creates a finite convex-union approximation. The approximation error, covering entropy, and number of convex programs must all be calculated before claiming that existing theory fails. If that route already attains the proposed rate, the intended tensor upper theorem is an application. The possible gap is a sharp result beyond that reduction, or a new exact characterization of when its cost is necessary.

The exact assumption change is

$$
\{A\in\mathcal M_{\mathbf r}:s_{\min}(A)\geq c>0,\ \mathbf r\text{ known}\}
\quad\longrightarrow\quad
\Theta_n=\bigcup_{\mathbf r\leq\bar{\mathbf r}}\mathcal M_{\mathbf r}\cap\{\|A\|_F\leq M\},
$$

with moving sequences throughout that union. The desired conclusion changes from a regular-stratum Gaussian approximation to honest, optimally sized intervals under (2), including negative adaptation results.

The useful setting is likely a **dense or higher-rank loading whose relevant low-rank projections differ across modes/cuts**. This is a research hypothesis, not evidence of a new rate. A loading being dense in entries does not itself imply high tensor rank; the all-ones average is rank one and must pass the obstruction in (1). Nor does high loading rank guarantee an improvement. The project must exhibit and analyze an actual example.

## D. Proposed theorem targets and why they are nontrivial

1. **Sharp expected-length lower bound on a coupled Tucker rank union.** Derive $\ell^*_\alpha$ for specified loading/spectral subclasses, using both local perturbations and mixture alternatives where necessary. Recover direct-interval optimality in rank-slack rank-one cases. The new contribution must be the sharp tensor-specific classification, not the generic two-point inequality. Joint unfolding constraints couple directions, and first-order cones can miss finite-noise transitions.

2. **An honest upper construction matching that lower bound in at least one substantial tensor regime.** Candidate tools include functional test inversion, a bias-aware linear procedure, or profiled split likelihood with certified optimization bounds. Prove (H), a nontrivial expected-length bound, and the claimed computational conditions. Generic finite-sample validity is available; the hard part is showing that the construction pays the correct functional cost instead of ambient or whole-tensor uncertainty.

3. **A simultaneous-adaptation feasibility/impossibility theorem.** For a predeclared family $\{\mathcal F_{n,j}\}$, characterize when one interval can achieve $\ell^*_\alpha(\mathcal F_{n,j},\Theta_n,L)$ up to constants or specified logarithms. Identify cases in which weak extra components force an inflation even on strong lower-rank tensors. Unknown subspaces, loading alignment, and rank-testing complexity must enter the statement quantitatively.

4. **Uniform transition analysis, or a justified regression transfer.** Choose the one that adds substance. A transition theorem would track the length frontier when singular values cross the relevant inferential scale, without inventing a tensor analogue of the matrix $N^{-1/3}$ exponent. A regression theorem would control random-design remainder and attainable length uniformly under explicit sample-size assumptions. A pointwise normal limit or an unsupported equivalence to denoising is insufficient.

TT should become a second main theorem only if its shared cut constraints produce a result that a single unfolding cannot deliver. Otherwise choose either Tucker or TT and make the first paper deeper. A general theorem covering several stratified low-dimensional models would materially strengthen the statistical contribution.

### A separate possible pivot: quadratic functionals

If linear-functional adaptation collapses to known theory in every useful subclass, a mathematically meaningful alternative is

$$
q(A)=\|A\|_F^2\quad\text{or}\quad q_{A_0}(A)=\|A-A_0\|_F^2.
$$

At $A=A_0$, the derivative of the second functional vanishes. In (G), the baseline

$$
\widehat q=\|Z\|_F^2-D\tau^2,\qquad
\operatorname{Var}_A(\widehat q)=4\tau^2\|A\|_F^2+2D\tau^4
$$

and noncentral-$\chi^2$ inversion already provide ambient procedures. New theory would need to characterize honest interval length that exploits the rank union while accounting for the zero-derivative regime. Sparse quadratic and matrix norm estimation are serious competing literatures. Estimation of $\|A\|_F$, estimation of $\|A\|_F^2$, and honest intervals for either have different losses and cannot be interchanged. [R24](https://arxiv.org/abs/1502.00665), [R25](https://arxiv.org/abs/2111.13551).

**Verdict for this pivot: B, provisional, with lower novelty confidence than the main formulation.** Do not combine it with the primary linear-functional project before conducting a more focused loss-inference audit and checking whether tensorization changes the known rates at all.

## 4. Attempts to invalidate novelty

| Proposed claim | Adversarial comparison/search | Assessment |
|---|---|---|
| First honest intervals without known tensor rank | Direct Gaussian interval; scalar regression; universal inference; rank-free matrix debiasing | **D: substantially solved** as an existence claim. |
| First general Tucker linear-functional inference | General loading, tangent projection, covariance-weighted inference | **D** on regular strata: R01/R06. |
| Unknown rank is the new ingredient | Overestimated factor dimension; diverse projections; interactive fixed effects | **D/C** unless the new regime quantitatively exceeds R03/R04. |
| First weak-rank adaptation impossibility | Weak factors; honest adaptive intervals; matrix detection | **D** at the conceptual level: R02/R05/R13. A sharp coupled-tensor classification may be **B**. |
| Recover oracle width whenever nonzero factors are strong | Add an arbitrarily weak extra rank-one component | **False as stated**, even before searching; see (1). |
| New Tucker or TT tangent cone | Rank varieties and tangent-cone parameterizations | **D**: R15/R16. |
| Replace a Wald interval by a cone-based likelihood interval | Chernoff singular LRT; universal/profile inference | **C/D** without uniform length and computability results. |
| Sharp loading-dependent length on joint rank unions | Moduli, union-of-model inference, weak-factor tradeoffs, high-dimensional adaptivity | **B**: substantial pieces known; no equivalent full characterization found. |
| Robustness or unknown covariance rescues novelty | Weak-factor bias-aware inference; covariance projection; robust universal inference | **C** as an appended assumption change; **B** only if it changes the sharp frontier. |
| LLM compression or LoRA supplies novelty | Rank-allocation tests, tensor optimism, conformal prediction, validation | **D/C** if only motivation changes. Different targets require different comparisons. |
| Quadratic tensor rank-union intervals | Sparse quadratic functionals, Schatten norms, loss inference, testing | **B provisional**; not enough evidence yet for an independent go decision. |

No contribution receives **A — strong apparent gap** at this stage. The narrower **B** rating reflects meaningful unresolved combinations, substantial prior art, and the remaining need to demonstrate a nontrivial tensor instance.

Universal inference gives finite-sample coverage without manifold regularity. A tensor optimizer returning only a local maximum is not enough for safe null profiling: an upper bound on the null maximum likelihood is conservative, while a lower approximation can invalidate a rejection. [R14](https://arxiv.org/abs/1912.11436).

Robust universal inference also handles projection targets under misspecification; its moment-controlled coverage theorem is not a statement about the original latent tensor parameter under arbitrary contamination. Adding the word “robust” therefore does not resolve target identification. [R22](https://doi.org/10.1093/biomet/asaf070).

## 5. Application novelty versus statistical novelty

| Line of work | Classification relative to this project | Required mathematical distinction |
|---|---|---|
| Tucker/TT regression CLTs | Same structure; regular inferential theory already exists | Pointwise/fixed-stratum coverage $\to$ infimum over moving rank-union sequences, with optimal length. |
| Matrix completion and panel factor inference | Same statistical problem or obstruction in another application; serious threat | Different observation operator and coupled tensor constraints must change a bound or attainability result. |
| CP tensor completion | Same tensor application, different rank and sampling model | CP factor/entry inference $\to$ Tucker/TT general loading under union honesty. |
| Tensor-network rank/model selection | Same estimator or architecture, different statistical objective | Risk oracle $\to$ scalar confidence coverage and minimax expected length. |
| LoRA component significance | Similar AI motivation, different parameter | Optimizer-trajectory rank scores $\to$ a functional of a sampling-law parameter. |
| Conformalized tensor completion | Similar UQ terminology, different coverage target | Marginal prediction/missing-entry calibration $\to$ prescribed latent-mean functional coverage. |
| LLM compression validation | Same application, often a simpler inference problem | Conditional held-out loss $\to$ a latent functional not directly estimable by validation. |

The recent StatLoRA preprint targets rank-allocation scores derived from optimization trajectories and hypothesis tests for retaining/pruning components. This does not establish (H) for tensor population parameters. [R28](https://arxiv.org/abs/2607.20205). Tensor optimism theory targets training/test-risk discrepancies; it is a necessary comparison for the existing project’s risk claims, but not a solution to the interval-length formulation. [R29](https://arxiv.org/abs/2603.26048).

Conformalized tensor completion supplies a different uncertainty target and must not be cited as either solving or failing to solve latent-parameter inference merely because it outputs intervals. [R27](https://arxiv.org/abs/2405.00581).

## 6. Does an LLM introduce new statistical structure here?

**Not in the primary formulation.** A Tucker/TT coefficient tensor with iid Gaussian designs is a general statistical model. Calling it an LLM representation or weight block supplies application motivation, not new theory.

For a subsequent generator extension, specify a frozen network architecture, a variable tensor block $A$, prompt law $Q$, and a full conditional response distribution

$$
X_i\sim Q,\qquad Y_i\mid X_i\sim p_A(\cdot\mid X_i),\qquad
p_A(y_{1:T}\mid x)=\prod_{t=1}^T p_A(y_t\mid x,y_{<t}).
$$

An example target is $\psi(A)=\mathbb E_{X\sim Q}f(p_A(\cdot\mid X))$, for an explicitly chosen $f$. The local observation metric is governed by

$$
\rho_A(H)^2=\mathbb E_A\left[
\left\{\left.\frac{\partial}{\partial t}\log p_{A+tH}(Y\mid X)\right|_{t=0}\right\}^2\right].
$$

This can be singular for reasons unrelated to rank. Identification and differentiability of the chosen functional must be checked relative to that sampling law. A law-invariant functional cannot distinguish exactly observationally equivalent parameters; a parameter-coordinate target might be unidentified. First-order invisibility can also require higher-order analysis even without exact observational equivalence.

Potentially substantive LLM features would be repeated generations within prompt clusters, adaptive prompt selection, shared evaluator randomness, or inference under a target prompt law different from training. Each requires an explicit joint law. Tokens within a response are dependent; treating all tokens as iid replications is unjustified. Mere tensor order or parameter count does not establish a new dependence problem.

The existing project’s teacher-access distinction is decisive. With stochastic teacher responses one can observe candidate log losses and log-loss differences. Absolute teacher-to-candidate KL also contains teacher entropy and is not generically available from a single response without probabilities or additional entropy-estimation assumptions. Exact probability access defines a different experiment. Independent validation can give rank-agnostic uncertainty for observable fitted risk; that is not the proposed rank-boundary functional problem.

Recommendation: make the first paper statistically complete without LLMs. Add an AI application only after fixing the actual sampling unit, target law, access model, and functional.

## 7. Skeptical reviewer attack

| Reviewer objection | Can it be rebutted? |
|---|---|
| “This is Cai–Low with tensor notation.” | Only by deriving a sharp result for a nonconvex, continuously indexed tensor union that does not follow from the available convex-class upper theory, and displaying a new attainability boundary. Generic modulus lower bounds do not suffice. |
| “Xu–Chen–Han already gives minimax tensor functional inference.” | Yes for the changed honesty class, but only if the new theorem treats weak moving sequences and optimal union-honest length. A weaker regular theorem cannot rebut it. |
| “Choi–Kwon–Liao already removes rank estimation.” | Yes only with a precise relaxation of their remaining strength/alignment conditions and a new functional/length theorem. Overspecification alone is not a contribution. |
| “Weak-factor tradeoffs and bias-aware intervals are old.” | Correct. A new sharp coupled-tensor frontier may be a rebuttal; repeating an impossibility example or using a tensor nuclear norm is insufficient. |
| “A direct interval is already uniformly valid.” | Correct. The paper must characterize and attain a meaningful improvement where possible, and prove when improvement is impossible. |
| “Your oracle adaptation theorem is false.” | Correct for the unrestricted promise. Reformulate the oracle benchmark using the outer honesty class in (2). |
| “The cone is known, and the LRT result is standard.” | Correct. New geometry alone is unavailable; uniform statistical complexity and achievable length must carry the contribution. |
| “An unfolding reduces this to matrices.” | Potentially fatal. Show a family where simultaneous mode/cut restrictions lead to a strictly different sharp benchmark or achievable procedure. |
| “A finite net and existing convex-union recovery already solve this.” | Potentially fatal. Quantify its approximation and complexity costs. The continuous nature of the original union alone is not a rebuttal. |
| “The method is computationally inaccessible.” | A real risk. Either provide certified optimization/relaxation guarantees, or clearly separate a statistical benchmark from an implementable theorem. Local optimization success in simulations cannot replace this. |
| “The LLM framing is superficial.” | Correct for the Gaussian benchmark. General statistical importance should lead the project; an application cannot repair a weak theorem. |
| “A quadratic target makes it different but still routine.” | Possibly. Compare with existing norm/loss estimation and show a genuine union-adaptation phenomenon before pivoting. |

Fatal flaws eliminated by reformulation are the false oracle-width promise, conflation of risk and fixed-parameter inference, and the claim that unknown rank alone is novel. The remaining fatal risk is that every useful tensor example reduces to the direct interval, a matrix theorem, or a generic modulus argument.

## 8. Publication potential and feasibility

Scores are conditional assessments of research directions, not journal acceptance predictions. A 5 requires a substantial result; no theorem has yet earned that score. Higher technical-feasibility scores mean easier execution. No information about the researcher’s technical background, available collaborators, or time budget was supplied, so personal capability is not inferred.

| Criterion (1–5) | G1: sharp linear-functional length and adaptation | G2: feasible bias-aware procedure, as a standalone extension | G3: quadratic rank-union inference, provisional |
|---|---:|---:|---:|
| Statistical depth | 5 | 3 | 4 |
| Theoretical depth | 5 | 3 | 4 |
| Novelty | 3 | 2 | 3 |
| Generality beyond LLMs | 5 | 5 | 5 |
| LLM/AI relevance | 2 | 3 | 2 |
| Technical feasibility | 2 | 3 | 3 |
| Potential for substantial theorems | 4 | 3 | 4 |
| JASA/JRSS-B/Biometrika fit | 4 | 3 | 4 |
| Annals of Statistics potential | 3 | 2 | 3 |

G2 is best treated as the constructive half of G1, not an independent paper on an existing method. G3 is a fallback requiring further focused assessment. For G1, Annals of Statistics potential would rise only with a sharp general adaptation theory, matching nontrivial bounds, or a new impossibility/possibility classification of independent interest. A regular CLT plus tensor optimization is not an Annals-level case.

Under the idea-evaluator dimensions, the revised G1 aims at **Stronger: 4/5** through honest coverage and optimality, **Broader: 4/5** through rank-boundary validity, and **Higher: 2/5** because statistical accuracy improvement has not been demonstrated. **Faster: 1/5** and **Cheaper: 1/5** are not established objectives. This is a refinement of inference on stratified models, not yet a paradigm shift. A broader principle linking loading geometry, testing complexity, and honest adaptation could change that assessment.

The project is at problem-selection stage. It needs expertise in minimax testing, high-dimensional probability, and tensor geometry; a practical method also needs nonconvex optimization or certified relaxation arguments. Those requirements are substantial. A short feasibility investigation should precede a multi-month theorem program; no deadline or completion time is promised here.

## E–F. Go/no-go gates and recommended final formulation

**Current verdict: Promising — sharpen the theoretical gap first.** Proceed with a bounded feasibility stage, not full manuscript development.

1. Choose one experiment: initially Gaussian denoising with known noise, or Gaussian tensor regression with known isotropic design. Choose order-three Tucker first unless TT offers a concrete distinctive example.
2. Specify a loading family and at least two spectral/rank subclasses for evaluating (2). Include weak additional components in the outer honesty class. Exclude no difficult points merely to manufacture an oracle theorem.
3. Establish the baseline comparison: direct interval, projected whole-object confidence set, strongest applicable matrix unfolding procedure, and a generic split-likelihood construction.
   Also evaluate subspace discretization followed by finite convex-union recovery; the cost of that reduction is part of the baseline.
4. Find one mathematically explicit tensor regime where the proposed sharp frontier is not already obtained by those comparisons. Check whether mixtures invalidate a proposed local-modulus rate.
5. Require a credible route to both an upper bound and a matching lower bound. If only the elementary obstruction, known cones, or a conservative interval remains, classify the project as incremental and pivot.

The foundation should be stated as:

> For $Z=A+\tau G$ with $A\in\Theta^{\mathrm{Tu}}_{\bar{\mathbf r}}(M)$, determine the minimax expected length of intervals for $\langle L,A\rangle$ that are honest on the entire rank-cap union, uniformly over subclasses with unknown and arbitrarily weak unfolding singular values. Characterize simultaneous adaptation to rank, spectrum, and loading geometry, including impossible regimes, and construct an interval attaining the sharp benchmark in a demonstrably nontrivial tensor setting.

This formulation fixes the population target, observation law, honesty class, and decision criterion. Regression and TT are justified extensions after that core survives. Nonlinear generator risk, unknown covariance, contamination, dependence, and quadratic functionals are separate possible developments, not a list of assumptions to add for novelty.

## Evidence scope

The assessment uses primary paper texts and publisher/author records available through **September 9, 2026**. The ranked matrix records theorem-level readings, not abstract-only judgments. Most central preprints were downloaded and their relevant assumptions, methods, and theorem statements inspected; this does not mean every proof in their long appendices was independently verified. Publication and inspected-preprint versions are distinguished.

Foundational background also includes Donoho’s optimal-recovery formulation and Low’s confidence-interval adaptation work, whose bibliographic records were cross-checked against primary references. [R31](https://web.stanford.edu/dept/statistics/cgi-bin/donoho/wp-content/uploads/2018/08/SEOR.pdf), [R32](https://doi.org/10.1214/aos/1030741084). Dufour’s almost-unidentified-parameter results concern a different identification mechanism from the fully observed bounded Gaussian tensor mean. [R33](https://jeanmariedufour.github.io/Dufour_1994_ImpossibilityTheorems_W.pdf). Leeb–Pötscher provides the classical post-selection warning: pointwise consistent model selection does not settle uniform inference. [R34](https://doi.org/10.1017/S0266466605050036).

The TT quantile article’s indexed primary full text exposed Section 3, including its CLT, but some equations rendered incompletely; its detailed penalized rate is therefore not used. The newly accepted covariance-projection PDF was read online; local download failed certificate validation. These access limits do not drive the main surviving gap. Supplementary 2026 AI papers serve as target-level comparisons, not foundations for a negative theorem-level novelty conclusion.

The companion [search log](search_log.md) records independent terminology, falsification searches, citation-following routes, and access limitations. The [20-paper matrix](closest_papers.csv) has separate columns for problem, method, assumptions, asymptotics, theorem, guarantee, difference, threat, and evidence. The [verified bibliography](references.bib) distinguishes journal articles, accepted preprints, and unverified-publication-status arXiv manuscripts.

<!-- MATRIX_AND_BIBLIOGRAPHY_APPENDED_BY_BUILD -->
