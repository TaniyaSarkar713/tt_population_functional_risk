---
title: "Theory review: Honest inference for tensor contrasts"
subtitle: "Audit of the preserved main.pdf and a separately reviewed revision"
date: "September 9, 2026"
---

The original finite-sample theory is sound under its intended confidence-level restrictions. The review found one omitted theorem-domain condition and refuted an explicitly labeled conjecture. It also produced complete derivations that materially strengthen the full-data analysis.

**Final verdict for the reviewed version: B — RIGOROUS BUT CAN BE STRENGTHENED.** The supplied arguments establish the stated results; further strengthening is optional for their correctness, but important for publication positioning. This is an internal mathematical audit, not independent peer review, proof-assistant verification, or certification of novelty.

## 1. Scope and most consequential findings

The audited input is the 22-page PDF in [input_snapshot/main.pdf](input_snapshot/main.pdf). Its PDF and source hashes are preserved in [input_manifest.json](input_manifest.json). The original project manuscript remains unchanged. The separate [reviewed manuscript](revised_paper/main.pdf) incorporates verified corrections, strengthened statements, complete proofs, updated interpretations and a revised result ledger.

The main findings are:

1. **Theorem 5 needs an explicit \(0<\alpha<1/4\) condition.** Its intended 95% comparison is valid. Read without that restriction, its affine lower bound is false.
2. **Original conjecture Q2 is false for \(K=3\).** A full-tensor harmonic sign mixture gives a larger lower bound. Q2 was explicitly a conjecture, so this does not invalidate an original proved theorem.
3. **For fixed \(K\ge4\), the optimal full-data expected length at zero is now matched.** A finite subtensor scan attains the coordinate-mixture lower rate under the same observation model and honesty class.
4. **For \(K=3\), the original polynomial gap reduces to a factor \(\sqrt{\log p}\).** The full-data worst-case criterion remains unmatched.
5. **Several assumptions and constants can be improved.** The review supplies a smaller cap coefficient, an exact affine benchmark, an envelope formulation, an additive approximate-rank radius, and separately calibrated replicate-noise extensions.

The new scan is exponential. The original simulations evaluate the threshold procedure and do not evaluate this scan. The finite audit checks corroborate algebra and constants; they are not evidence of uniform coverage or computational practicality.

## 2. Reconstructed statistical problem

On the finite-dimensional Borel space \(\mathbb R^D\), \(D=\prod_{k=1}^Kp_k\), observe
\[
 Z=A+\tau G,\qquad \operatorname{vec}(G)\sim N(0,I_D),\quad\tau>0.
\]
The parameter is the ambient real tensor \(A\). Equivalently, retain independent full tensor replicates \(W_j=A+\sigma G_j\), with \(\tau=\sigma/\sqrt n\). This is not scalar-response tensor regression or tensor completion. For known \(\sigma\), the sample mean is sufficient; when estimating \(\sigma\), residuals contain information and must be retained for the proposed extension.

The two honesty classes are
\[
 \Theta_{\rm Tu}=\{A:\|A\|_F\le M,\ 
                 \operatorname{rank}(A_{(k)})\le\bar r_k,\ k\le K\},
\]
\[
 \Theta_{\rm TT}=\{A:\|A\|_F\le M,\
                 \operatorname{rank}(A_{\langle k\rangle})\le\bar r_k,\ k<K\}.
\]
TT cuts use the fixed mode order. Positive upper caps and \(M>0\) are supplied; actual rank may be zero and nonzero singular values may be arbitrarily small. These are closed bounded subsets of a finite-dimensional space. Rank constraints are closed because they set appropriate minors to zero.

The prescribed loading is
\[
 L=\sum_{i=1}^m w_iV_i,\qquad
 V_i=\bigotimes_{k=1}^K v_{ki},\qquad
 v_{ki}^{\mathsf T}v_{kj}=\mathbf1_{\{i=j\}},\qquad \|w\|_2=1.
\]
Thus \(\|L\|_F=1\), \(m\le\min_k p_k\), and
\[
 \psi(A)=\langle L,A\rangle,\qquad
 d_i=\langle Z,V_i\rangle=a_i+\tau g_i
\]
has independent standard normal \(g_i\). The loading must be fixed or independent of the inference observations.

The required coverage is finite-sample and uniform:
\[
 \inf_{A\in\Theta}P_A\{\psi(A)\in C(Z)\}\ge1-\alpha.
\]
The two full-data length criteria are distinct:
\[
 \mathcal L_0=\inf_{C\ {\rm honest}}E_0|C|,\qquad
 \mathcal L_{\max}=\inf_{C\ {\rm honest}}\sup_{A\in\Theta}E_A|C|.
\]
Intervals may use the entire tensor and independent randomization. The diagonal versions restrict them to \(d\). A marginal diagonal lower bound is not a full-data lower bound.

**Identifiability:** equality of Gaussian location laws implies equality of their expectations, hence \(A=B\) and equal targets. Factors and cores are nonunique under scaling, signs and TT gauge transformations, but no theorem estimates those coordinates. At zero the tensor remains identified although factor directions do not. No latent random-factor or gauge-identification assumption is missing.

The principal rate regime is equal dimensions \(p_k=m=p\), equal weights \(w_i=p^{-1/2}\), fixed \(K\ge3\), fixed positive caps, and \(M=\tau\sqrt p\). Taking \(M=\sigma=1\) and \(n=p\) gives \(D=n^K\). These rate comparisons are derived from finite-sample inequalities.

## 3. Findings requiring corrections or changed interpretation

### F1. Missing confidence-level domain in Theorem 5

**Severity: MAJOR, statement precision; corrected.** Input PDF p. 7 begins the theorem with “Let \(K\ge3\) and the rank caps be fixed.” The theorem does not repeat the confidence range needed by its lower-bound dependencies. A surrounding sentence about simplifying constants does not make the domain as explicit as it should be.

For every \(p\), take cap one, \(M=\tau\sqrt p\), and \(\alpha=0.9\). The target range is \([-\tau,\tau]\). The affine interval
\[
 C(Z)=[\,0.6\langle L,Z\rangle-0.1\tau,\
          0.6\langle L,Z\rangle+0.1\tau\,]
\]
has worst-case coverage
\[
 \Phi(-1/2)-\Phi(-5/6)=0.106209\ldots>0.1.
\]
Its radius \(0.1\tau\) is below the theorem's unqualified claimed lower radius
\[
 \frac{z_{0.55}}{1+z_{0.55}}\tau=0.111633\ldots\tau.
\]
The repair is to state \(0<\alpha<1/4\). No change to the original 95% simulations or intended proof is necessary. A further proposition extends the fixed-confidence rates to every \(\alpha<1/2\) with recalibrated constants.

### F2. Cubic counterexample to Q2

**Severity: MAJOR for research direction; conjecture refuted.** The input ledger, p. 19, describes Q2 as “Attainment of the coordinate-mixture lower scale at zero.” Its proposed rate is \(\tau\sqrt{\log p/p}\) in the principal norm regime.

For independent uniform sign vectors \(u,v\), define
\[
 (x_u)_i=u_i i^{-1/3},\qquad
 A_{u,v}=\frac{\tau}{200}\,x_u\otimes x_v\otimes x_{uv}.
\]
These tensors have rank one, Frobenius norm at most
\(3^{3/2}\tau\sqrt p/200\), and common target
\[
 \delta=\frac{\tau H_p}{200\sqrt p},\qquad H_p=\sum_{i=1}^p i^{-1}.
\]
The full Gaussian likelihood mixture has second moment below \(5/4\).
The proof uses a uniform cubic exponential moment of
\(\sum_i i^{-2/3}\epsilon_i\). Its three coupled copies are dependent; Hölder, not an independence assertion, controls their product.

The common-target interval lemma yields
\[
 E_0|C|\ge(3/4-2\alpha)\frac{\tau H_p}{200\sqrt p}.
\]
Because \(H_p\asymp\log p\), this disproves the proposed cubic rate by a factor growing as \(\sqrt{\log p}\). Complete constants, tail integrals and likelihood calculations appear in revised Theorem 8 and its appendix. No diagonal-only experiment is substituted.

### F3. Previously unresolved full-data upper bound

**Severity: MAJOR opportunity, not an input proof error; resolved for one criterion.**

For every coordinate subset \(S\) of size \(s\), scan predetermined product nets of its mode spheres at resolution \(1/(2K)\). Each mode net has cardinality at most \((1+4K)^s\). Let \(N_S(Z)\) be the largest absolute net contraction and set
\[
 \lambda_s=\tau\sqrt{2\{s\log(ep/s)+Ks\log(1+4K)+\log(2p/\gamma)\}}.
\]
Accept zero if all \(N_S(Z)\le\lambda_s\). A finite Gaussian union bound controls all noise contractions with probability at least \(1-\gamma\).

The canonical expansion implies
\(\|B\|_F\le\sqrt J\,\rho(B)\), where \(\rho\) is the injective norm.
Coordinate restriction preserves each constrained unfolding rank.
On test acceptance and the noise event, the \(s\)th largest diagonal magnitude satisfies
\[
 |a|_{(s)}\le4J^{K/2}\lambda_s s^{-K/2}.
\]
Consequently a scan interval centered at zero can use radius
\[
 R_\gamma=\frac{4J^{K/2}}{\sqrt p}
             \sum_{s=1}^p\lambda_s s^{-K/2}
\]
on acceptance and the certain structural interval on rejection.

Intersect it with the original honest interval at error level \(\alpha_0\), taking \(\alpha_0+\gamma\le\alpha\). Replace an empty intersection by the point interval \(\{0\}\). If \(\ell_*\) is the deterministic original length, the resulting \(C_\dagger\) satisfies
\[
 \sup_A E_A|C_\dagger|\le\ell_*,
 \qquad
 E_0|C_\dagger|\le\min\{\ell_*,\,2R_\gamma+\ell_*\gamma\}.
\]
For \(\alpha_0=\alpha/2,\gamma=\alpha/(2p)\),
\[
 E_0|C_\dagger|
 \lesssim \frac{\tau\sqrt{\log p}}{\sqrt p}
              \sum_{s=1}^p s^{-(K-1)/2}.
\]
The sum is bounded for \(K\ge4\) and harmonic for \(K=3\). The shrinking rejection budget is essential for this expected-length calculation. Neither independence of scans nor independence of intersected intervals is assumed.

### F4. Assumptions stronger than needed

**Severity: MINOR for validity, substantial opportunity for generality; repaired in supporting propositions.**

Gaussian independence is unnecessary for the threshold bound when a valid uniform coordinate-noise envelope is supplied. Orthonormality can be weakened to frame bounds for the diagonal budget, with a geometry penalty. Exact rank can be replaced by a supplied Frobenius distance \(\eta\) from the rank-cap class, increasing radius by only \(\eta\). Unknown Gaussian variance can be calibrated from retained independent residuals. Finite-variance and bounded adversarial row corruption require a robust replicate summary and explicit block conditions.

These are separately stated experiments and procedures. They are not reasons to claim that the original unchanged Gaussian procedure is robust. Counterexamples to that claim are provided.

### F5. Scope and attribution

**Severity: MINOR clarity improvement; corrected.** The equal-loading assumption is repeated in Theorems 6 and 8. The abstract, introduction, discussion, comparison table, figure caption and ledger now distinguish diagonal optimality, full-data optimality at zero, and unresolved full-data worst-case optimality. The original figure's full-data curves are explicitly labeled as initial bounds. The diagonal minimax rate is credited to classical sequence theory, not claimed as a new rate.

## 4. Final mathematical contribution

For fixed positive caps, fixed confidence, equal diagonal loading and \(M=\tau\sqrt p\), the final verified full-data statements are
\[
 \boxed{\mathcal L_0(\Theta)\asymp\tau\sqrt{\log p/p},\qquad K\ge4,}
\]
and
\[
 \boxed{c_\alpha\tau\log p/\sqrt p
       \le\mathcal L_0(\Theta)
       \le C_{J,\alpha}\tau(\log p)^{3/2}/\sqrt p,\qquad K=3.}
\]
The same statements apply to fixed Tucker and TT cap classes, since the upper construction respects their geometry and the lower alternatives are rank one.

For diagonal-only procedures, the already classical optimal rate remains
\[
 \mathcal L_{0,d}\asymp\mathcal L_{\max,d}
 \asymp\tau(\log p/p)^{(K-2)/(2K)}.
\]
For full-data worst-case length, only
\[
 \mathcal L_0\le\mathcal L_{\max}
 \lesssim\tau(\log p/p)^{(K-2)/(2K)}
\]
is established. The zero-point and worst-case criteria must not be merged.

The exact fixed affine benchmark is also sharpened. Put
\(a_0=M\sqrt{s_{\rm cap}/p}\) and let \(Q_\alpha(\mu,v)\) be the \(1-\alpha\) quantile of \(|N(\mu,v^2)|\). Then
\[
 h_{\rm aff}^*=\min_{0\le t\le1}Q_\alpha(a_0(1-t),\tau t).
\]
At cap one, \(M=\tau\sqrt p\) and 95% confidence, the exact best affine length is \(2\tau\). This is a tensor reduction to a classical bounded-normal-mean problem, not a new scalar decision-theory principle. [Stark (1992)](https://www.sciencedirect.com/science/article/abs/pii/016771529290234V).

## 5. Proof and assumption audit

The audit inventory contains all six original theorems, one proposition, five lemmas, three open/conjectured items and eight additional technical claims. The new derivations add two theorems, two essential lemmas and six supporting propositions. Each numbered result has a complete proof; the revised appendices include proof roadmaps.

The proof graph has no cycles and no dependence on an unresolved claim. The most important checks were:

- TT path terms are generally not orthogonal. The squared-weight identity follows from the left-orthogonal core prefix recursion.
- The rank-one diagonal image identity is a statement about a parameter image, not equivalence of statistical experiments.
- Gaussian mixture inner products use the entire tensor. The diagonal support construction has overlap \(H\), whereas its full tensor version has overlap \(H^K\).
- The affine quantile proof uses variance monotonicity only when the radius exceeds the absolute mean, justified by confidence greater than one half.
- Net cardinalities include every subset size and every product direction. Finite sets make all tests measurable.
- The harmonic mixture uses dependent weighted sign sums and handles this dependence explicitly.
- Expected-length conclusions use deterministic bounds plus a bounded rejection contribution. No \(O_P\) statement is converted to expectation without justification.
- Approximation uses a one-Lipschitz residual map, avoiding an unnecessary \(2\eta\) loss.
- Robust block calibration tolerates adaptive row replacement because at most \(c\) predetermined blocks are changed.
- Residual-based interval selection is valid by conditional independence, not because selecting any individually valid interval would be safe.

The full [assumption audit](assumption_audit.md) splits the assumptions into 26 entries, each with necessity, use, relaxation and counterexample. The [dependency audit](dependency_audit.md) and [graph](dependency_graph.md) identify every essential lemma and external identity. The [counterexample appendix](counterexamples.md) includes invalid covariance, underestimated caps, nonorthogonal loadings, data-selected functionals, heavy tails and nonregular Gaussian-limit proposals.

No optimization initialization, restricted strong convexity, tensor perturbation inverse, Taylor remainder, stochastic equicontinuity or empirical-process limit is hidden in the proofs: none is used. The finite scan uses an explicitly proved covering argument. The absence of these tools is a feature of this formulation, not evidence that a scalar-response regression analogue follows.

## 6. Inference, adaptation and remaining mathematical limits

**Uniformity.** The original and revised coverage bounds are finite-sample infima over the entire stated cap class. They include zero and sequences approaching lower-rank strata. The new zero-point expected-length guarantee remains subject to honesty on that whole outer class.

**Distributional strengthening.** The threshold center should not receive an unqualified normal limit. In the scalar submodel \(A=0,\lambda=c\tau\), its standardized distribution is \(\operatorname{soft}_c(g)\), with an atom at zero. For fixed positive mean and vanishing \(\tau\), the standardized error converges to \(g-c\), rather than a centered efficient normal law. The direct Gaussian contrast is already exactly normal, with zero normal-approximation error. No bootstrap or uniform Berry–Esseen theorem for the threshold center is established.

**Adaptation.** Unknown actual rank is allowed in the coverage class; this does not mean interval length adapts to actual rank. The cap-based radius does not shrink when a singular value vanishes. A pathwise oracle inequality with an unobserved approximation term is not a computable adaptive confidence interval. Independent training can justify a selected loading, but generic same-data loading/rank selection needs separate theory.

**Sharpness.** The diagonal rate is matched for fixed caps. The full-data zero-point rate is matched for \(K\ge4\); the cubic logarithmic gap is unresolved. Cap dependence, arbitrary loadings, confidence-level dependence and general \(M/\tau\) regimes are not sharply characterized. Constants such as \(1/200\) are conservative. The constant in the additive approximation term is sharp in a scalar boundary example.

**Computation.** The scan uses at most
\((1+(1+4K)^K)^p-1\) product directions. It is finite and defines a valid measurable procedure, but this does not supply an efficient algorithm. No complexity lower bound is proved.

**Robustness.** The finite-variance extension needs independent replicate vectors, a known contraction-variance upper bound and explicit block-size conditions. The contamination model is bounded replacement of entire replicates; a separate binomial-count argument handles independent Huber-style replacements. No minimax contamination rate, optimal breakdown point, or unrestricted dependent-data theorem is asserted.

## 7. Literature comparison and novelty judgment

The strongest threat to a new diagonal-rate claim is classical Gaussian-sequence theory. Its \(\ell_q\) functional rate specializes exactly to \(q=2/K\) here. The manuscript now treats that rate as a benchmark. [Collier, Comminges and Tsybakov (2017)](https://arxiv.org/pdf/1502.00665).

Canonical TT geometry is established prior work, and robust block means are also classical. The new proof burden is the particular tensor geometry and full-data lower/upper constructions, not inventing those components. [Oseledets (2011)](https://users.math.msu.edu/users/iwenmark/Teaching/CMSE890/TENSOR_oseledets2011.pdf), [Devroye et al. (2016)](https://arxiv.org/pdf/1509.05845).

A recent competing result hidden in a matrix-titled paper is the tensor-completion CI lower bound in Appendix E, Theorem 10, of Ma, Du, Xia and Yuan's 2026 version. Its sampled-entry model and class with a positive minimum signal, incoherence, condition-number and tangent-alignment restrictions differ from the present zero-inclusive Gaussian location model. [Primary full text](https://arxiv.org/pdf/2312.00305).

The inspected literature does not establish an equivalent S7/S8 pair. That supports **apparent novelty**, not a first-result claim. A specialist should check whether a broader nonconvex functional-testing theorem subsumes the evaluated tensor rates. The [external-results audit](external_results_audit.md) distinguishes full-text inspection, inherited project notes and metadata-only verification. In particular, Stark's PDF was inaccessible; its result is not a missing dependency because the scalar reduction is proved directly.

## 8. Skeptical-referee attack

| Objection | Assessment and response |
|---|---|
| “Thresholding an \(\ell_q\) sequence is already solved.” | Correct. D1 is explicitly attributed. It cannot carry the main novelty claim. |
| “This is generic nonconvex inference with tensor notation.” | Serious positioning risk. The defense is the evaluated full-data rate for \(K\ge4\), the cubic obstruction and their matched honesty class. Generic nonlinearity is not a contribution. |
| “The matrix comparison throws away data.” | Incorrect for T4. It changes the honesty class while retaining full observations. The revised text makes this distinction explicit. |
| “You claim rank adaptation without proving it.” | The revised text does not. Cap-uniform coverage is proved; actual-rank length adaptation remains open. |
| “Your lower bound ignores off-diagonal information.” | D1 intentionally concerns a restricted experiment. T4/T6/T8 all use full likelihoods. |
| “The scan is infeasible.” | Correct. It establishes an attainable statistical rate, not a practical algorithm. This limits methodological publication claims. |
| “Matching at zero is not minimax worst-case optimality.” | Correct. The two criteria are explicitly separated throughout. |
| “Why not an oracle tangent interval?” | It relies on unavailable subspace information or regularity conditions; no pointwise dominance over that regime is claimed. |
| “The LLM framing adds no mathematics.” | Correct for this draft. No LLM experiment is forced into the paper. |
| “New proofs are not independently verified.” | Correct. The review supplies detailed arguments and finite checks, not an external referee's certification. Independent mathematical review remains valuable. |

## 9. Publication potential and priorities

The strongest current contribution is the full-data zero-point analysis in revised Theorems 7–8. T1–T2 are necessary methodological foundations; T5 is a useful corollary. D1 should remain an attributed benchmark, and the elementary noise extensions should not dilute the main story.

| Venue | Current assessment | What is most needed |
|---|---|---|
| Annals of Statistics | Substantial potential not yet established | Confirm priority; sharpen the cubic or worst-case theory, broaden loading geometry, or derive a general statistical principle beyond this contrast. |
| JASA, Theory and Methods | Promising, not submission-ready | A usable algorithm or stronger methodological implications, with experiments evaluating that procedure. |
| JRSS-B | Promising but incomplete positioning | Practical inference benefit beyond conservative diagonal calibration; broader loading/sampling justification. |
| Biometrika | Possible after a focused rewrite | Center the paper on one sharp insight; reduce ancillary extensions; settle the most consequential remaining gap if feasible. |
| Bernoulli | Plausible theory direction | Independent proof/novelty scrutiny and a clearly substantial inferential geometry contribution. |
| Statistica Sinica | Plausible with development | Clear comparison, practical calibration and coherent theorem-to-experiment validation. |
| COLT / ML theory | Possible but presently narrow | Stronger statistical-computational insight or general theorem; no efficient scan claim is available. |

A strict 1–5 assessment is: statistical depth 4, theoretical depth 4, apparent novelty 3, generality beyond AI 5, present AI-specific relevance 1, feasibility of remaining sharp theory 3, substantial-theorem potential 4, JASA/JRSS-B/Biometrika readiness 3, AoS readiness 2. These are editorial judgments, not probabilities of acceptance.

Priority order: (1) resolve the cubic logarithmic factor, (2) distinguish and characterize worst-case length, (3) find a computable scan substitute, (4) characterize general loading geometry or actual-rank adaptation. Adding unrelated assumptions solely to make another theorem is not recommended.

## 10. Verification, unresolved items and final verdict

The audit reran deterministic and finite numerical checks with seed 20260910. They include exact sign-mixture second moments through \(p=10\), 120 rank-one profile checks, 200 random Tucker/TT refined-budget checks, 10,000 residual-approximation cases, exact Gaussian maximum calibration and explicit coverage counterexamples. Saved outputs are in [results/audit_checks.json](results/audit_checks.json). These supplement the analytic proofs; they do not replace them.

**RESOLVED:** original proof audit; confidence-domain correction; smaller budget; affine optimum; calibrated noise and approximation extensions; full-data zero-point optimality for \(K\ge4\); cubic harmonic lower bound.

**COUNTEREXAMPLE FOUND:** original Q2 for \(K=3\); unrestricted-confidence reading of T5; unchanged Gaussian calibration under general finite variance; unadjusted correlated-noise direct interval; underreported norm/rank caps; naive loading or interval selection; a generic centered Gaussian limit for the threshold center.

**PARTIAL:** full-data cubic zero-point rate and full-data worst-case minimax length.

**OPEN PROBLEM:** efficient optimal scanning, actual-rank adaptation, sharp general-loading geometry, broader sampling models and an empirically justified AI application.

The final reviewed mathematical verdict is **B — RIGOROUS BUT CAN BE STRENGTHENED**. The original main results survive the audit after an explicit domain repair; an open conjecture is replaced by a counterexample and stronger proved results. The publication recommendation is **Promising — sharpen the theoretical contribution and obtain independent scrutiny before submission**.
