# Scientific review of the honest tensor-functional inference project

Review date: September 13, 2026. Recommendation: **Major revision. Readiness: C — Major revision required.**

This is a fresh, tool-assisted internal review, not an external referee decision. The three referee perspectives below are simulated perspectives from this review. No central theorem counterexample or fatal identifiability defect was found. The core statistical contribution appears viable. A reproducible coverage-count error, a confounded ablation, and an out-of-date integrated submission require correction before submission.

## 1. Scope and independent reconstruction

The active package consists of the 55-page manuscript in `robust_adaptive_extension/paper/`, its included proofs, the 7-page `certified_weak_signal/` supplement, the 6-page `high_dimensional_extension/` supplement, and the 14-page empirical report and 2-page manuscript insert in `empirical_study/`. These documents represent successive stages, not one synchronized final paper. The root README and current requirements correctly acknowledge that distinction. Earlier inference drafts, theory ledgers, novelty matrices, reference PDFs, and implementation records were used to trace provenance and dependencies. The original TT compression/conditional-generator project is a separate statistical problem; this review does not certify all of its historical theorems or experiments.

All 45 distinct numbered theorem, proposition and lemma statements in the integrated inference manuscript and all 14 numbered supplement results receive individual entries in [theorem_audit.md](theorem_audit.md), with a [machine-readable table](tables/theorem_audit.csv). The audit covers the supplied proof arguments, not just the authors' status labels. Generated copies of supplement statements are counted once. The [assumption audit](assumption_audit.md), [simulation and claims audit](simulation_and_claims.md), [presentation audit](presentation_audit.md), and [revision plan](revision_plan.md) are part of this report. A [50-item crosswalk](guideline_coverage.md) maps the user's complete review protocol, including its final deliverables.

### Statistical experiment

For an order-$K$ tensor with ambient dimension $D=\prod_{k=1}^K p_k$, observe

$$Z=A+\tau G,\qquad \operatorname{vec}(G)\sim N_D(0,I_D),\qquad \tau>0.$$

The scale $\tau$ is known in the principal experiment. Equivalently, $Z$ is the mean of $n$ independent fully observed tensors with Gaussian noise scale $\sigma$, and $\tau=\sigma/\sqrt n$. The principal theory does not require $n>D$: it is a Gaussian location experiment with structural constraints, not recovery from incomplete entries. Generating the exact scalar or diagonal marginal is sufficient when the evaluated method accesses only those contractions; it is not evidence that the full tensor was unavailable.

The parameter is the mean tensor itself. The Tucker class imposes $\|A\|_F\le M$ and $\operatorname{rank}(A_{(k)})\le\bar r_k$ on each mode unfolding. The TT class instead bounds ranks of the consecutive-cut unfoldings. Caps and $M$ are supplied. These are closed bounded unions of strata, containing zero and arbitrarily weak nonzero components. Factors, support sets and subspaces are unknown representations of the parameter, not observed covariates. The main loading is prescribed independently of the data:

$$L=\sum_{i=1}^m w_i\bigotimes_{k=1}^K v_{ki},\qquad
\langle v_{ki},v_{kj}\rangle=\mathbf 1\{i=j\},\qquad \|w\|_2=1,$$

with scalar target $\psi_L(A)=\langle L,A\rangle$. The sharp central case has $p_k=p$, $m=p$ and $w_i=p^{-1/2}$. More general fixed loadings are covered only by the explicit later regimes or conservative bounds.

For a stated class $\Theta$, honest intervals satisfy

$$\inf_{A\in\Theta}P_A\{\psi_L(A)\in C(Z)\}\ge1-\alpha.$$

The paper studies the infimum of $E_0|C|$ and of $\sup_{A\in\Theta}E_A|C|$ over this same honesty class, and separately the minimax squared error $\inf_{\widehat\psi}\sup_{A\in\Theta}E_A(\widehat\psi-\psi_L(A))^2$. A short interval does not automatically supply a good midpoint estimator. Known $K$, fixed positive caps, and fixed $0<\alpha<1/4$ underlie the central uniform comparisons. Growing caps and non-Gaussian laws have separate assumptions; they cannot be absorbed into unspecified constants.

The target is identifiable: equal Gaussian laws with the same known covariance imply equal means $A$, hence equal $\psi_L(A)$. Factor sign, rotation, scale and permutation ambiguities do not affect this tensor functional. The manuscript does not need globally identifiable tensor factors, a unique optimizer, or rank recovery at zero for its central assertions. It appropriately restricts rank-selection conclusions to a separated class.

### What is established

The methodological construction has two levels. An efficient diagonal threshold interval uses rank-induced diagonal compressibility, with deterministic selection against structural and direct-Gaussian radii. A stronger statistical procedure projects a simultaneous full-data residual confidence set onto the target; a related residual fit controls squared risk. The latter constructions are global, generally exponential benchmarks. The executable binary continuous rank-one optimizer is a small-instance realization with unresolved numerical gaps, not an implemented high-dimensional minimax algorithm.

The main theoretical advance is a sharp functional comparison between simultaneous tensor constraints, diagonal-only information, affine fixed-radius inference, and enlarged single-unfolding honesty classes. The sparse harmonic mixture is particularly consequential for order three. The later stages sharpen norm dependence, delimit loading regimes, identify a large-cap endpoint, and construct an honest interval with pointwise shortening at very strong saturated Tucker means. They do not settle the four remaining general problems in `requirements.md`.

The new empirical contribution is a broad, reproducible stress study of available procedures and benchmarks, including a faithful local regular-signal comparator, paired uncertainty, assumption violations and visible failures. It supports calibrated coverage at the tested points, selected rate branches, and important computational limitations. It does not empirically attain the main ideal high-dimensional full-data rate, establish uniform honesty, or provide real-data evidence.

### One-paragraph referee summary

This paper studies honest confidence intervals for a prescribed linear functional of a fully observed Gaussian tensor mean subject to supplied Tucker or TT rank and Frobenius bounds, including zero and arbitrarily weak signals. It combines diagonal compressibility, threshold intervals, full-data residual confidence-set projection and common-target mixture lower bounds to obtain sharp flat-loading minimax expected lengths and squared risks at fixed caps across norm budgets, with a distinctive cubic logarithmic factor. Extensions treat calibrated noise families, approximate structure, selected loading profiles, large growing caps and pointwise inference at strong saturated Tucker means. Simulations document the behavior of executable intervals and a binary exponential benchmark, including failures and uncertainty, but do not implement the general optimal procedure. The sharp full-data theory is substantial enough to merit serious consideration; the current submission package needs integration and targeted empirical corrections, and its strongest generality and practical claims must remain carefully scoped.

## 2. Contribution, novelty and significance

The estimand is a meaningful aggregate contrast. Joint low-rank constraints can make its structural range and distinguishability much smaller than those of an unrestricted mean. The question matters without an AI application: how much can uniform inference gain from a nonconvex class when the rank stratum is unidentifiable near its boundary? This is principally a theoretical statistical contribution with nontrivial tensor-specific arguments. It is not an application paper, and it is not yet a broadly useful high-dimensional algorithm paper.

The strongest contribution of this paper is: **the sharp full-data minimax theory for flat tensor contrasts across norm budgets, especially the sparse harmonic lower bound that matches the cubic logarithmic factor under weak-signal rank-cap honesty.**

There is a real novelty burden, but no established fatal priority conflict in the focused review. Classical nonconvex functional estimation already explains why nonlinear procedures can improve on affine ones, and between-class moduli already explain honest adaptation barriers. These general ideas should remain background, as the current related-work section largely recognizes. [Cai–Low, nonconvex estimation](https://arxiv.org/abs/math/0406427), [Cai–Low, adaptive intervals](https://arxiv.org/abs/math/0503662).

The diagonal sequence rate is explicitly a specialization of existing sparse-functional theory. The new part must be the full-tensor likelihood geometry and matching construction, not another claim of a novel thresholding exponent. The large-cap G1 result is a useful matching consequence of a standard sparse mixture; it should not be promoted as a new lower-bound technique. [Collier–Comminges–Tsybakov](https://arxiv.org/abs/1502.00665).

Finite unions of convex classes already admit sophisticated functional recovery procedures. A final focused comparison should explain the tensor discretization and entropy cost that prevent a direct invocation from delivering the displayed sharp rate. This review did not establish that an existing theorem subsumes the sparse harmonic result; it also cannot certify exhaustive priority. [Juditsky–Nemirovski](https://arxiv.org/abs/1804.00355).

The closest executable tensor-functional comparison is Xu–Chen–Han's regular-signal PCA procedure. Their Section 4.2 uses HOSVD initialization and two simultaneous subspace updates; the general-functional validity conditions include loading alignment and remainder control. The local reimplementation follows those ingredients and uses the fitted-core tangent variance. The honest-cap procedure sacrifices regular-signal precision for a larger coverage class; no general domination is demonstrated or claimed. [Xu–Chen–Han](https://arxiv.org/abs/2501.16223).

Weak-factor inference itself is not new, including bias-aware inference in panel models. The present distinction is the fully observed tensor mean, its specified target and its nonconvex joint constraints. Likewise, low-degree likelihood analysis is an established restricted computational framework; its conclusions must remain limited to the degree classes actually analyzed. [Armstrong–Weidner–Zeleneev](https://arxiv.org/abs/2210.06639), [Choo–d'Orsi](https://arxiv.org/abs/2106.06308).

The local 20-paper novelty matrix and curated eight-paper collection are valuable, but they partly predate the final supplement. Their full-text inspection claims are historical records, not new checks by this review. This review freshly checked the closest comparator's relevant local PDF sections and focused primary-source records. A full bibliography/priority audit is deferred as requested in guideline 27.

## 3. Theorem strength and minimax matching

Put $\ell=\log(ep)$ and $x=M/(\tau\sqrt\ell)$. At fixed $K\ge3$ and positive fixed caps, the main flat-loading result is

$$R_K(p,M,\tau)=\frac{\tau\sqrt\ell}{\sqrt p}
\begin{cases}
\min\{x,1+\log_+x,\ell\},&K=3,\\
\min\{x,1\},&K\ge4.
\end{cases}$$

The two honest expected-length criteria have this order; minimax squared risk has order $R_K^2$. At $M=\tau\sqrt p$, the rates are $\tau\ell^{3/2}/\sqrt p$ for $K=3$ and $\tau\sqrt{\ell/p}$ for $K\ge4$. The logarithms here are matched, not upper-bound artifacts. The all-budget squared-risk proof uses an integrated residual tail, avoiding the invalid inference that any fixed-confidence midpoint has uniformly bounded risk as $M/\tau$ grows.

| Regime | Matched quantity | Review of the comparison |
|---|---|---|
| Fixed caps, flat orthogonal loading, all $M,\tau>0$ | Both honest length criteria $R_K$; squared risk $R_K^2$ | Same full Gaussian experiment, norm/cap class and target in upper and lower bounds. Constants fixed in caps/order. |
| Diagonal-only observation use | Classical $\ell_{2/K}$ functional rate | Correctly restricted procedure class; not a full-data lower bound. |
| Arbitrary fixed $L$, $M\le\tau$ | Length $M\rho(L)$; risk its square | Fixed caps; injective norm $\rho(L)$ may be hard to evaluate. |
| Fixed positive polynomial weight decay | Length $\lvert w_1\rvert\min(M,\tau)$; risk its square | Decay constants fixed; no uniform extension as the exponent tends to zero. Ideal block fits supply the upper bound. |
| Minimum cap $r\ge c\sqrt p$ | Length $\min\{M\sqrt{r/p},\tau\}$; risk its square | Same full-data class; constants uniform over growing caps at fixed $c>0$. Direct/structural selection is executable. |
| Strong saturated diagonal Tucker mean | Pointwise honest expected length $\tau\sqrt{r/p}$ | Same outer honesty class for the upper and local lower bound. Extra conditions are on the point where length is evaluated, not on coverage. No midpoint-risk theorem. |
| Unknown jointly sub-Gaussian noise family | Upper rates and family-wise minimax rates | Gaussian subfamily supplies the lower bound; not an equivalence for every individual law. |
| Finite-variance replicate family | Same rates with known covariance bound and sufficient $n$ | Whole-replicate independence and block-count feasibility required. Not arbitrary contamination or dependence robustness. |
| Supplied Frobenius approximation allowance $\varepsilon_A$ | Length $\min\{\tau,R_K+\varepsilon_A\}$ | Matched enlarged class for normalized flat target. The allowance is not estimated from the data. |

Fixed-cap adaptation A1 and growing-cap impossibility G2 are compatible. Every smaller positive fixed-cap class contains the rank-one hard submodel, so the fixed outer-class rate is already optimal on it up to cap-dependent constants. When the outer cap reaches order $\sqrt p$ at $M=\tau\sqrt p$, honesty forces length of order $\tau$ even at zero, while a fixed-cap oracle rate vanishes. This is a statistical obstruction even for exponential computation. Neither statement characterizes all pointwise geometries.

P1 is correctly scoped but restrictive. For fixed order/confidence its sufficient signal condition is approximately $a\gtrsim\tau p^{K-1/2}$, with norm slack and $M$ comparable to $a\sqrt r$. The empirical $p=16$, cap-one amplitude is about 310,930 noise standard deviations. The theorem proves that pointwise shortening is possible under outer honesty; it does not establish an optimal signal threshold or general growing-rank adaptation.

## 4. Adversarial proof audit

The result-by-result audit gives all 59 statement judgments and proof paths. The most consequential dependency chains are:

1. Canonical Tucker/TT weights $\to$ diagonal $\ell_{2/K}$ envelope $\to$ scalar threshold error $\to$ simultaneous finite-sample interval. Matrix functional duality supplies the structural competitor.
2. Finite product nets $\to$ injective-norm control $\to$ ordered residual-diagonal bounds $\to$ uniform confidence-set diameter. Intersecting these with the norm envelope *before summation* gives the all-budget phase diagram.
3. Common-target CI testing lemma $\to$ coordinate mixture and sparse harmonic full-tensor mixtures $\to$ matching expected-length lower bounds. Gaussian testing also yields squared-risk lower bounds.
4. Measurable approximate residual minimizer $\to$ controlled excess-noise tail on every observation $\to$ integrable squared risk. This is separate from fixed-confidence interval midpoint logic.
5. Simultaneous pilot operator bounds $\to$ capped subspace error bounds, including unresolved errors bounded by one $\to$ second-order product projection bias $\to$ conditional validation interval. A shrinking pilot failure budget and direct intersection give P1 expected-length control.
6. Sparse diagonal rank-$r$ mixture $\to$ large-cap matching G1 $\to$ growing-outer versus fixed-inner adaptation impossibility G2. Dyadic block fits separately yield W1 and the fixed-decay W2 corollary.

Specific failure modes were examined. TT canonical paths are not all orthogonal; the proof uses the correct prefix recursion for the squared weights. The three weighted sign sums in the preliminary cubic argument are dependent; Holder is used rather than a false factorization. Full-data support overlap is evaluated in the full tensor likelihood, with its tensor power, not replaced by the easier diagonal likelihood. Product-net cardinalities enter the union bounds. Differences of feasible tensors have doubled rank/norm bounds. The parameter classes are compact, but no unique minimizer is assumed; a countable dense approximate selection handles measurability.

The conditional validation Gaussian statement uses an independent pilot. Artificial splitting with $Z\pm\tau G'$ gives independent errors of scale $\sqrt2\tau$; using $\tau$ after splitting would be wrong, and the code uses the larger scale. Intersections use allocated confidence budgets and a union bound, not a false independence assertion. The cap-valid projector omits tensor components with at least two bad mode factors, so the bias is second order. It can be larger than the exact manifold tangent space. Unsaturated caps deliberately use a conservative unresolved-error bound; no hidden eigengap is used for coverage there.

New finite mathematical probes passed **1,377 checks**: rank-one diagonal identities including signs/zeros, nonorthogonal TT path expansions, exact small-support harmonic mixtures, weighted target equalization, hypergeometric second moments for all $1\le r\le p\le40$, low-degree moments in small cases, and cap-valid bias certificates for arbitrary loadings, rectangular modes, zero/unsaturated ranks and signals ranging to $10^5$. These are falsification attempts, not a machine proof of asymptotic or uniform claims. No essential missing proof step was identified in the supplied arguments. A human specialist should still scrutinize the sparse harmonic and residual-fit arguments before a strong-journal submission.

### Explicit boundary tests

For equicorrelated diagonal Gaussian noise, the naive unit-variance 95% interval has coverage

$$2\Phi\!\left(\frac{z_{.975}}{\sqrt{1+(p-1)\rho}}\right)-1.$$

At $p=256$, $\rho=.8$, this is about 0.109. Marginal Gaussianity does not imply the required joint unit proxy. The calibrated procedure can restore coverage when the covariance bound is known. A nonzero noise mean is not corrected by inflating variance.

For $p=4$, $A=E_1+E_2$ and $M=\sqrt2$, the flat target is 1. An incorrectly supplied cap of one produces structural radius $M/\sqrt p=1/\sqrt2$ and excludes the target deterministically. This is a concrete misspecified-class failure, not a counterexample under valid supplied caps. At zero or vanishing eigengap, the cap-valid interval remains calibrated, while the separated rank selector can fail outside its domain. With full ranks, the structural bound approaches the norm-ball range and the weak-signal gain can disappear.

Finite-variance robustness becomes unavailable when the required block count exceeds $n/2$; it does not silently continue with fewer blocks. Replicate dependence can invalidate its binomial argument. The supporting coordinate-median proposition tolerates a stated number of corrupted whole replicates, but neither it nor the main scan theorem supplies an optimal general contamination threshold. Near-singular but known covariance is compatible with a valid upper proxy; marginal variances alone are insufficient. Underestimated approximation allowances can miss the target, as the simulation stressors demonstrate.

## 5. Ranked findings

### Critical issues

**None established.** No false central theorem, unidentified target, fundamentally invalid central comparison, or demonstrated priority conflict was found. This does not certify that none exists. Known computational and application limits are not relabeled as mathematical errors.

### F01 — MAJOR: coverage tolerance can count a genuine miss as a hit

At `empirical_study/code/common.py:66`, coverage uses `1e-11 * max(1., abs(target))` as its tolerance. The same policy appears in `analyze_results.py:74`. In case S03_007, the target magnitude makes this tolerance approximately $9.369\times10^{-5}$. For the 90% oracle interval at trial 41, an independent regeneration of the original Gaussian noise gives contraction $-0.5816030754$ and radius $0.5815435768$. The miss is $5.950\times10^{-5}$, whereas the target's floating-point spacing is $1.863\times10^{-9}$. This is about 31,943 spacings, so it is not cancellation at one rounding unit.

Both the oracle and `xch_known` rows report 134/150 covered under this tolerance; the corrected event count is 133/150, or 0.8867 instead of 0.8933. These rows share the same offending observation; they are not two independent failures. The 95% headline results are not changed by this particular count correction.

The audit found 26 strict/tolerant row differences altogether. The other 24 arise at exact structural boundaries from differences of one floating-point unit (roughly $10^{-17}$). They are harmless rounding effects, not true zero-coverage counterexamples. Therefore simply removing every tolerance is also inadequate. Use an explicitly justified ULP-scale comparison, exact noise-centered coverage for Gaussian reference procedures where available, and a recorded sensitivity audit. Regenerate affected summaries and diagnostics from the same saved observations, preserving the original outputs. Repeating the same tolerance in a validator tests consistency, not correctness of the event definition. Evidence: [raw audit](results/raw_results_audit.json) and [independent implementation probes](results/implementation_probes.json).

### F02 — MAJOR: the no-bias ablation changes three components

At `empirical_study/code/tensor_methods.py:100–103`, the comment says “Omit only bias and fallback.” The implementation also changes the validation quantile. At $p=16,r=1,\alpha=.05$, the full quantile is 2.24748; the ablation uses 1.95996. It removes the bias term, removes the direct/structural fallback and intersections, and reallocates confidence. The design describes this comparison as testing the need for correction/caps. Such a combined diagnostic can demonstrate that the unprotected procedure fails, but it cannot identify how much failure is caused specifically by omitting the bias correction.

The repair is either to label it explicitly as a multicomponent diagnostic and limit the causal interpretation, or to add a controlled ablation with the same pilot, projector, split, confidence allocation, candidate selection rule and fallback policy, varying the chosen component only. No guarantee is asserted for the current ablation, which limits the damage to interpretation rather than the main coverage theorem.

### F03 — MAJOR: the submission has no synchronized final manuscript

The main abstract ends with “general unseparated rank adaptation remain open.” Its “What remains unresolved” paragraph in `norm_loading_section.tex` and its discussion predate A1, A4, G1, G2, W2 and P1. Broad adaptation still is open, but the unqualified historical wording misses precise new positive and negative results. The 55-page document also retains preliminary harmonic bounds and a lead rate figure showing an intermediate full-data gap before the final sharpening. Its empirical sections do not contain the new million-dataset study or the new comparator and failure audits.

The root README makes the chronology transparent, so this is not concealment. It is nevertheless a submission-level coherence problem. Produce one canonical manuscript, prioritize the all-budget full-data theorem and sparse harmonic mechanism, integrate only the most consequential supplement results, and move preliminary stages to a historical appendix or archive. Update abstract, contribution list, rate table, figure, methods, experiment section and discussion together. Replace vague “adaptation” with fixed-cap rate adaptation, growing-outer-class obstruction, or the specified pointwise conclusion as appropriate.

### F04 — MODERATE: the interval API's midpoint has a severe risk pathology

The empty-intersection replacement is `{0}` in `high_dimensional_extension/code/methods.py:191–193` and the empirical counterpart. The saved report already discloses its consequence. In S03_002, one such replacement among 500 trials contributes approximately **99.999999%** of the total squared loss; unconditional MSE is about **12,084,661**, while the conditional mean squared loss on the other 499 draws is about **0.1242**. The latter is a diagnostic, not a replacement performance estimate.

This does not refute P1, which controls honesty and expected length, and it does not refute the separate residual-fit MSE theorem. It does make a generic “estimate = interval midpoint” API misleading for estimation. Return a clearly distinguished scalar estimator, document the midpoint convention, and retain unconditional risk and failure frequencies. Any replacement estimator or changed fallback needs its own analysis; conditional deletion of bad draws is unacceptable.

### F05 — MODERATE: the signal sweep also changes the honesty class

`run_study.py:89` sets $M$ to the maximum of $\sqrt p\tau$, $1.1\|A\|_F$ and $\|A\|_F+\tau$. In the S04 amplitude sweep, $M$ therefore rises from 4 to about 342,023. This is fixed before each observation and is not test-outcome leakage. It is appropriate for P1's norm-comparability regime, but a curve against amplitude does not isolate signal strength at one fixed outer class. Add a fixed-$M$ sweep or state this coupling directly in the figure caption. Keep the existing sweep as the matched-class experiment.

### F06 — MODERATE: comparator applicability needs case-level labels

The local Xu–Chen–Han method is substantively implemented, rather than an intentionally weak proxy. However, the row-level `asymptotic_regular_signal` label records the type of guarantee, not that initialization, signal, loading alignment and remainder assumptions hold in that row. Zero, weak and deliberately incorrect-rank cases need an explicit out-of-domain flag; very strong signals alone do not verify every asymptotic alignment condition. The prose already warns about weak-signal failures. Extend that distinction to the exported tables and use the PCA theorem relevant to the implemented method in the integrated literature/methods comparison.

### F07 — MODERATE: computation and optimality evidence must remain separated

The general full-data residual fit and the W1 block fits remain unimplemented. Analytic loading envelopes do not establish computational attainment. The binary rank-one solver ran 2,160 solves on 240 independent observations across confidence levels and budgets. At 95% and 3,000 nodes, 146/240 reach tolerance and 94/240 do not. Float64 guarded bounds are not formal directed interval arithmetic. The new finite grid checks found no outer-containment violation, but cannot prove a global numerical certificate. The current report states these limits well; the eventual integrated paper must retain them in its main methods and results, not just repository notes.

The lack of a general efficient minimax algorithm is not by itself a reason to reject a focused statistical minimax paper. It does prevent marketing this package as a scalable general method or treating the experiments as attainment of the central ideal estimator. A useful refinement is a fixed-loading, fixed-tolerance solver budget study: the present signal cases use different prescribed loadings, and the first budget uses a looser tolerance than the later two.

### F08 — MODERATE: direct empirical checks are missing for two retained calibration refinements

The integrated supporting proposition on bounded whole-replicate corruption and the independent Gaussian residual variance-calibration proposition have supplied proofs. The current S06 checks a centered finite-variance full-net envelope; it is not a test of either refinement. The XCH residual plug-in is also not the independent chi-square upper-noise-bound method. If these results remain part of a broad practical robustness claim, add focused checks of their actual block-count/noise-scale conditions. Otherwise present them as theoretical refinements without implying that the current study validates their implementations.

### F09 — MINOR: exported MSE rows need an estimator-level identifier

The raw estimates are shared across the three confidence levels. For the pointwise method, the scalar estimate is specifically the 95% interval midpoint, so the same squared loss appears in 90%, 95% and 99% rows. This convention is disclosed in metadata and the 95% report is interpretable. Add `estimator_alpha=0.05` and an estimator identity to flat exports so a reader does not assume each row evaluates that row's midpoint.

### F10 — MINOR: notation and historical presentation need consolidation

Local definitions mostly work, but $D$ is used for ambient dimension and polynomial degree, $q$ for compressibility and normal quantiles, $\eta$ for approximation and pilot error, and $J$ for component counts and overlap variables across stages. Introduce a unified notation table and rename the colliding auxiliary variables when integrating. The presentation audit found no banned-vocabulary or em-dash hits in its active-source scan and no repeated grammar defect warranting a grammar-rule finding. The main writing problem is prioritization and chronology, not sentence-level English.

## 6. Simulation, uncertainty, fairness and reproducibility

The [detailed simulation audit](simulation_and_claims.md) maps each of S01–S13 to its question, theorem, design, competitors, repetitions and interpretation. There are **402 statistical/envelope configurations: 318 stochastic and 84 analytic-only**, plus a separate 18-setting runtime study. The stored study comprises **1,084,640 Monte Carlo datasets** and **3,444 summary rows**. These counts are not independent replications of the ideal minimax optimizer.

Substantive strengths include shared observations and valid artificial splits, paired differences with standard errors, explicit known-information oracles, retained poor outcomes, separately registered follow-ups, correctly standardized heavy-tail examples, and a local published-method implementation. The initial 95% direct-Gaussian result 131/150 at the largest tensor was retained. An independent 10,000-draw follow-up covered 9,492 times; it was not used to replace the original realization. This is responsible diagnostic handling, not evidence of selective reseeding.

Wilson intervals are retained at boundary empirical proportions. At nominal 95%, a single case has MCSE about .00308 with 5,000 draws, .0178 with 150 draws, and .0398 with 30 draws. The full-tensor and solver grids cannot measure small coverage deviations precisely. Pointwise confidence intervals across many cases are not simultaneous intervals. The Bonferroni screen over 2,526 in-scope rows is conservative; no flag does not establish uniform honesty. Coverage event F01 must be repaired before relying on its exact counts.

The observed large-cap noise-branch RMSE slope is about $-.4980$ with MC slope SE $.0023$, consistent with the $-1/2$ prediction on that grid. Deterministic interval-length slopes verify the implemented formulas, not stochastic minimax attainment. P1 length slopes $-.4745$ and $-.1791$ differ from $-1/2$ and $-1/4$ beyond their MC errors. The report correctly labels them finite-grid diagnostics. Cap rounding, fixed-grid curvature and direct-interval intersection affect the apparent slope; the separately labeled frozen-subspace calculation explains the eight measured mean lengths within two MCSE but uses unavailable true geometry and is not a new theorem.

Runtime is measured separately from data generation, with fixed threads, a warmup and ten calls. Traced allocations exclude preallocated input and untraced native workspace; they are not total process memory. Explicit tensor access scales with $p^K$, even for a polynomial method. Report both tensor entries and $p$ when describing scalability. Methods based only on a coordinate diagonal have a genuinely different access model; their $O(p)$ costs should not be compared as if they read the full input.

### Newly run verification versus saved evidence

During this review, **60,496 raw-result checks** independently recomputed stored coverage under its existing policy, uncertainty, interval lengths, risks, paired differences, rejection counts and count totals. The strict/rounded comparison and exact regenerated oracle contraction discovered F01. The **1,377 mathematical probes** and **nine new binary outer-grid containment checks** were newly run. Passing finite probes does not establish asymptotic sharpness or global floating-point validity.

The original empirical code was then copied into an isolated temporary tree with its protected dependencies. Newly executed analysis, plot, report and validation scripts all completed successfully. All compared CSV/JSON tables and report/caption/manuscript Markdown were byte-identical to the saved versions. PDFs were rebuilt and validated; timestamp metadata precludes a byte-identity claim. The inherited artifact validator passed 87 checks in that isolated rebuild. Logs and comparisons are retained in [results/reproduction.json](results/reproduction.json).

The full million-dataset simulation and full exponential benchmark were **not rerun** during the review. Seeds, frozen registries, source hashes, pinned numerical packages and rebuild scripts make the saved study unusually reproducible, but a successful rebuild reproduces methodological errors too. Original manuscript, proof, simulation and result files are preserved. Only root review-status documentation is updated outside this review directory, with a final hash audit recording that allowlist.

## 7. Real-data and AI/LLM applicability

There is no real-data analysis in the active inference package. The application audit accurately marks the dataset/model requirement pending. Thus sample selection, preprocessing, missingness, real-data train/test leakage, tuning and uncertainty cannot be endorsed; they are not applicable to an executed analysis. The theoretical paper does not need an arbitrary convenient dataset to be worthwhile. A method-focused submission would benefit from genuinely replicated tensor measurements with a fixed interpretable contrast and defensible noise calibration.

No LLM-generated observations enter this empirical study. Prompt, model, token and repeated-generation dependence therefore do not contaminate these synthetic results. They would matter immediately in an AI application: repeated outputs within a prompt are not automatically independent replicates of an entire mean tensor, and conditional independence does not imply marginal iid sampling. A future design needs an independent sampling unit, a prespecified loading, dependence/covariance calibration, and an honest account of estimated norm/rank/approximation bounds. A tensor-shaped array alone does not justify the Gaussian location experiment. These are future model requirements, not demonstrated application validity or new theorems.

## 8. Writing, exposition and proposed abstract

The current abstract accurately summarizes its historical stage but is crowded and no longer describes the full package. The introduction's six contribution bullets combine central rates, standard refinements and historical constructions at nearly equal prominence. The strongest story is: joint nonconvex tensor geometry creates a sharp full-data advantage at a rank boundary; the cubic likelihood geometry differs from higher orders; computation and adaptation have explicitly delimited regimes.

The final methods section should distinguish the diagonal procedure, ideal residual fit, binary global search and cap-valid split projection. Each needs its input assumptions and output guarantee adjacent to its definition. The main paper alone is not a complete implementation specification for the two later supplements; their current code and stopping rules are in separate directories. The appendix proofs are individually accessible, but the chronological insertion of weaker bounds interrupts the final dependency chain. The 14 displayed figures across the main manuscript and new empirical study are legible vector plots; the initial gap plot should be replaced or moved because it gives visual priority to a gap the final theory closes. Full figure/table findings and notation recommendations are in [presentation_audit.md](presentation_audit.md).

A replacement abstract for a focused integrated paper is supplied in [proposed_abstract.md](proposed_abstract.md). It should be adopted only after the manuscript is actually integrated; the review does not silently rewrite the scientific sources. It foregrounds the sharp flat-loading theory, explicitly calls the general optimizer statistical, and limits empirical claims to implemented procedures.

## 9. Three simulated referee perspectives

### Reviewer 1: theoretical statistician

**Assessment.** The tensor-specific full-data upper/lower matching, especially the cubic sparse harmonic construction and all-budget risk argument, is the reason to consider publication. The exact diagonal reduction and separation of honesty classes are clear. The most serious theoretical presentation risk is burying this contribution among many consequences that follow from established testing and structural-range arguments.

**Concerns unique to this perspective.** Verify constants uniformly in the declared norm/noise budgets, preserve the distinction between fixed and growing caps, explain why general convex-union theory does not directly recover the sharp tensor result, and supply a compact final proof dependency map. Do not promote low-degree estimation evidence to a universal computational impossibility. The lack of a general efficient optimizer is compatible with a statistical minimax contribution. I found no central mathematical counterexample in the supplied proofs, but would seek a specialist check of the harmonic mixture and residual-tail steps.

**Recommendation: Major revision.** Focus and reconcile the results; correct the empirical event definition. The four open problems need not all be solved to publish a sharply scoped theorem paper.

### Reviewer 2: statistical methodologist

**Assessment.** Supplied-cap honesty is interpretable, and the simulation design is more informative than a collection of favorable coverage averages. The direct method and regular-signal competitor provide useful calibration. The observed conservatism, unresolved solver gaps and catastrophic midpoint losses are practically important results.

**Concerns unique to this perspective.** The attractive ideal rate has no general executable method, and the pointwise theorem operates at exceptionally strong signals with supplied bounds. Fix F01, isolate the ablation, show a fixed-honesty-class signal sweep, and distinguish an interval from a scalar estimator in the interface and tables. A method paper needs defensible bound selection and actual use cases; a theory paper can state those as limitations.

**Recommendation: Major revision.** A viable theory-led contribution, but current practical evidence does not support a broadly deployable minimax procedure.

### Reviewer 3: AI/ML researcher

**Assessment.** The polynomial-versus-statistical distinction and rank-boundary problem are interesting abstractions. The current work is not empirically about foundation models, compression quality or LLM evaluation. Full tensors at $p=64$ remain small in mode count but have $64^3$ entries; input and memory conventions matter.

**Concerns unique to this perspective.** A claim of scalable AI inference would require a realistic observation model, dependence-aware experimental units, target construction independent of evaluation outcomes, and stronger general-dimensional computation. Those claims are currently absent and should stay absent. HOOI-style or other approximate optimizers could be exploratory benchmarks, but local convergence would not certify global minimax attainment.

**Recommendation: Major revision as a statistics submission.** Poor fit for an AI application paper in its current form; no additional LLM dataset is required merely to decorate the statistical theory.

## 10. Associate-editor assessment and journal fit

The contribution is potentially important and technically substantial in its sharp full-data core. Focused prior comparisons support a plausible distinct contribution, not an exhaustive novelty certificate. The empirical study is informative and reproducible but contains a correctable event-count error and one overinterpretable ablation. Most current limitations are candidly stated. The main issues can be repaired without replacing the central statistical problem or solving every open problem.

**Editorial recommendation: Major revision; do not submit the current package unchanged.** The most serious weakness that could lead to rejection is: **the absence of a single focused submission that connects the sharp theorem, its actual computational status and the empirical evidence without requiring the referee to reconstruct several research stages.** Repair this by integrating one final manuscript around the sharp rate theorem, carrying F01–F07 into the main results and limitations, and presenting derivative refinements proportionately.

These fit scores are reasoned scientific judgments on a revised, focused version, not acceptance probabilities or statements of journal policy.

| Venue | Fit, 1–5 | Main acceptance obstacle |
|---|---:|---|
| Annals of Statistics | 2 | Must establish that the tensor-specific sharp likelihood geometry is a sufficiently broad conceptual advance beyond classical nonconvex/sequence inference; many routine corollaries do not add that depth. Current fragmentation is unacceptable. |
| JASA, Theory and Methods | 2 | Statistical importance is plausible, but general computability, practical supplied-bound calibration and a meaningful application are underdeveloped for the methodological framing. A particularly strong theory narrative could offset some of this. |
| JRSS-B | 2 | Needs a more compelling synthesis of a new inferential principle, usable methodology and relevance beyond a narrowly chosen loading. |
| Biometrika | 3 | The sharp cubic/higher-order distinction could support a concise focused paper; the present sprawling sequence of extensions is a poor format. |
| Bernoulli | 4 | Good match to a rigorous probability/statistical theory paper if novelty and the central proofs withstand specialist review. Integration, exact claim scope and correction of empirical counts still required. |
| Electronic Journal of Statistics | 4 | Natural home for detailed sharp-rate theory and reproducible computation, subject to the same correctness and novelty requirements. |

Overall scientific readiness is **6/10**: viable and substantial core, strong reproducibility, incomplete integration and targeted empirical validity issues. This score does not average away the required corrections.

## 11. Missing theory, missing experiments and material to cut

The ranked [revision plan](revision_plan.md) gives locations, actions, priorities and expected impact. The highest-impact missing theorem is a general-dimensional algorithm with a proved statistical and numerical error contract in the diffuse fixed-cap weak-signal regime. It is also difficult and not a prerequisite for a clearly statistical minimax paper. Next are intermediate growing-cap matching, a characterization of arbitrary loading profiles beyond fixed decay/small budgets, and a broader pointwise theory with substantially weaker signal thresholds. The current positive and negative adaptation results are valuable boundary pieces, not that characterization.

The experiments requested first by a skeptical referee are a corrected coverage-boundary audit on unchanged draws, a controlled bias ablation, a fixed-$M$ signal sweep, and a solver budget comparison with fixed loading and tolerance. Direct tests of the retained unknown-variance and corrupted-replicate refinements, larger-replication pointwise checks near the onset of shortening, and a justified real-data design follow. More favorable repetitions of already conservative deterministic intervals are lower priority.

Move the preliminary harmonic lower bound and superseded gap narrative out of the main theorem sequence; shorten elementary G1/A1 consequences; consolidate repeated “what remains open” paragraphs; retain only figures that explain final rates or reveal a distinct practical limitation. Keep failure audits and primary comparator details available. A smaller, better ordered paper would be stronger than a longer list of partially related extensions.

### Questions for the authors before submission

1. Which single manuscript and supplement set will be submitted, and which three results are intended as the principal contributions?
2. Will the scalar output of the cap-valid procedure be an explicitly labeled midpoint diagnostic or a separately analyzed estimator?
3. Which comparator configurations actually satisfy the invoked PCA theorem's initialization/alignment conditions?
4. Can the corrected coverage comparison be made stable to rescaling and exact structural-boundary rounding without using target-sized statistical tolerances?
5. Is the intended paper a statistical minimax theory paper or a practically general inference method? The current general computation and data evidence support different claims.

## 12. Final scientific checklist and verdict

| Requirement | Status after this review |
|---|---|
| Identifiable tensor functional | Satisfied in the stated Gaussian mean experiment. Factor identifiability is unnecessary. |
| Every active theorem audited; complete supplied main proofs | 59 entries reviewed; no essential defect identified. Fallible proof review, not formal verification. |
| Sufficient assumptions and no hidden extrapolation | Sufficient within explicit scopes; integration must preserve fixed/growing-cap, law-family, loading and pointwise distinctions. |
| Matching rates/losses/classes for optimality | Checked for the stated matched regimes. General loading/intermediate-cap/complete pointwise claims remain open. |
| Fair theoretical comparisons | Correctly separates diagonal information, affine procedure restrictions and enlarged honesty classes. |
| Theory-led simulations and strong comparator | Substantial coverage; full ideal estimator remains unimplemented. Case-level comparator eligibility and F02 need revision. |
| Monte Carlo uncertainty | Reported extensively, including paired differences and Wilson intervals; limited precision at 150 and 30 draws. |
| Correct coverage event and reproducibility | Reproducible, but F01 requires correction before submission. |
| Fair tuning and useful violations | No test-outcome tuning found. Signal-dependent supplied $M$ and multicomponent ablation require clearer design interpretation. |
| Real-data preprocessing, leakage and dependence | No real-data or LLM experiment executed; pending, not validated. |
| Conclusions proportional to evidence | Largely careful in latest supplements/report. Historical manuscript needs synchronization and midpoint-risk distinction. |
| Abstract, introduction, notation and limitations | Major integration revision; sentence-level presentation generally sound. |
| Seeds, parameters, environment and regeneration | Available; isolated saved-result rebuild newly passed. Full simulation rerun not performed in this review. |
| Remaining requirements | All four general theory problems remain open. Review findings do not close them. |

**Final verdict: C — Major revision required.** The sharp full-data contribution appears viable, and the present review has not established a fatal theoretical flaw. Correct the coverage-count rule, isolate or relabel the ablation, and produce one coherent manuscript that distinguishes proved statistical rates, executable procedures and still-open regimes. Submission should wait for those revisions and their verification; solving every remaining research problem is not necessary for a focused paper.


\newpage

# Result-by-result theorem audit

Audit date: 2026-09-13. The 45 distinct numbered theorem/proposition/lemma statements in the integrated manuscript and 14 numbered supplement results are audited below. Generated TeX copies of supplement statements are not counted twice. No separately stated corollaries occur in this active inventory.

**Meaning of the judgment.** The statements and supplied proof arguments were read and reconstructed. “No defect identified” is a fallible review judgment, not a formal verification or a certificate of priority. The new finite checks can falsify selected steps but cannot prove a uniform theorem. Novelty judgments are relative to the focused closest-work review, not an exhaustive literature search.

The machine-readable table has all requested columns (statement, proof completeness, novelty, strength and issue), plus source locations and proof reasoning. Detailed entries use a vertical layout for legibility.

## T01. Orthogonal diagonal compressibility

**Result:** `thm:diagonal`. **Location:** [robust_adaptive_extension/paper/main.tex](../robust_adaptive_extension/paper/main.tex), line 207.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Canonical CP expansion, scalar Holder over modes, and concavity over squared component weights give the exponent 2/K and coefficient J^(1-1/K). The TT proof uses canonical prefix identities, not orthogonality of all paths.

**Novelty:** Useful tensor specialization; the quasi-norm exponent itself is established geometry.

**Strength and issue:** Uniform at zero and arbitrarily weak signals. Rank constants are not uniform over growing caps.

## T02. Finite-sample honest interval

**Result:** `thm:coverage`. **Location:** [robust_adaptive_extension/paper/main.tex](../robust_adaptive_extension/paper/main.tex), line 219.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** On the simultaneous Gaussian diagonal event, the scalar threshold envelope bounds each error by min(abs(a_i),2 lambda). Compressibility gives the radius; singular-value duality gives the structural option. Selection uses deterministic radii.

**Novelty:** Concrete finite-sample procedure built from classical thresholding and structural bounds.

**Strength and issue:** Efficient diagonal method; not the sharper full-data minimax optimizer. Random selection by observed widths would need a new argument.

## T03. Fixed-radius affine intervals

**Result:** `thm:affine`. **Location:** [robust_adaptive_extension/paper/main.tex](../robust_adaptive_extension/paper/main.tex), line 240.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** At zero, Gaussian variance forces a noise radius; the positive and negative coordinate atoms force maximum bias. Combining these yields the harmonic-mean lower bound.

**Novelty:** Tensor application of known affine/nonlinear distinctions.

**Strength and issue:** Only deterministic W, offset and radius. Does not exclude every interval with an affine center and a random radius.

## T04. Cost of a single unfolding honesty class

**Result:** `thm:unfolding`. **Location:** [robust_adaptive_extension/paper/main.tex](../robust_adaptive_extension/paper/main.tex), line 259.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Rank-one matrix alternatives in the enlarged unfolding class have a common target. The full matrix likelihood mixture has bounded second moment at theta <= tau sqrt(p)/4.

**Novelty:** Meaningful comparison of honesty classes.

**Strength and issue:** Does not prove that merely storing data as an unfolding loses information. The lower bound is deliberately for a larger class.

## T05. Strict length separations

**Result:** `thm:separation`. **Location:** [robust_adaptive_extension/paper/main.tex](../robust_adaptive_extension/paper/main.tex), line 270.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Combine the deterministic selected radius with the affine and enlarged-class lower bounds at fixed K and caps, M=tau sqrt(p). Powers of p separate the lengths.

**Novelty:** Useful synthesis, not a new proof ingredient.

**Strength and issue:** Correct comparison categories; later full-data sharp results supersede the initial upper bound as the headline rate.

## T06. Within-class lower bound

**Result:** `thm:jointlower`. **Location:** [robust_adaptive_extension/paper/main.tex](../robust_adaptive_extension/paper/main.tex), line 283.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Coordinate-axis Gaussian alternatives lie in every positive cap class. Their common target and likelihood second moment give a positive E_0 length bound.

**Novelty:** Classical testing applied to tensor atoms.

**Strength and issue:** Valid but not cubic-sharp. Retain as a short ingredient rather than an unresolved final gap.

## T07. Classical diagonal-information benchmark

**Result:** `prop:diagonal_minimax`. **Location:** [robust_adaptive_extension/paper/main.tex](../robust_adaptive_extension/paper/main.tex), line 310.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** The rank-one diagonal image is exactly the ell_(2/K) ball. Sparse diagonal mixtures yield the lower bound in the diagonal observation experiment; thresholding matches it.

**Novelty:** Classical sequence-functional rate after an exact tensor reduction.

**Strength and issue:** The mixture second moment here is not the full-tensor second moment. Correctly restricted to diagonal-based intervals.

## T08. A full-data interval with short expected length at zero

**Result:** `thm:scan`. **Location:** [robust_adaptive_extension/paper/full_data_section.tex](../robust_adaptive_extension/paper/full_data_section.tex), line 23.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Finite product nets control the injective norm; canonical weights turn this into an ordered-diagonal residual bound. Scan acceptance at zero yields short expected length.

**Novelty:** Nontrivial use of off-diagonal information.

**Strength and issue:** Statistical existence result with exponential search. Later uniform-diameter theorem is stronger.

## T09. A harmonic obstruction in order three

**Result:** `thm:harmonic`. **Location:** [robust_adaptive_extension/paper/full_data_section.tex](../robust_adaptive_extension/paper/full_data_section.tex), line 46.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Sign coupling fixes the diagonal target. The full likelihood exponent is a product of dependent weighted sign sums; Holder and the cubic exponential moment bound control it without independence.

**Novelty:** Nontrivial preliminary cubic construction.

**Strength and issue:** Correct but weaker than the sparse harmonic lower bound; move to historical appendix or remove from final proof chain.

## T10. Sparse harmonic lower bound

**Result:** `thm:sparse_harmonic`. **Location:** [robust_adaptive_extension/paper/gap_section.tex](../robust_adaptive_extension/paper/gap_section.tex), line 6.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Use nonnegative harmonic factors on random size-m supports. Norm and common target are explicit; the full tensor overlap is bounded by 27 b^2 times support overlap. Hypergeometric factorial moments control chi-square.

**Novelty:** Strongest candidate for a substantive new lower-bound ingredient.

**Strength and issue:** Produces the necessary cubic logarithm. Verified against exact small-support enumeration; finite checks supplement the analytic proof.

## T11. Uniform diameter and full-data minimax length

**Result:** `thm:full_minimax`. **Location:** [robust_adaptive_extension/paper/gap_section.tex](../robust_adaptive_extension/paper/gap_section.tex), line 42.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Subtract two feasible tensors, doubling caps and norm. The finite-net residual event bounds every ordered diagonal coordinate and hence deterministic functional diameter. Coordinate and sparse harmonic alternatives match the bound.

**Novelty:** Central sharp full-data tensor-functional result.

**Strength and issue:** At M=tau sqrt(p), fixed K/caps; both E_0 and worst-case expected length match. Constants may depend on fixed caps.

## T12. Squared-error consequence

**Result:** `prop:mse_sharp`. **Location:** [robust_adaptive_extension/paper/gap_section.tex](../robust_adaptive_extension/paper/gap_section.tex), line 63.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Use a confidence level decreasing as p^-2 and control failure loss by the structural range at M=tau sqrt(p). The testing lower bound transfers to squared loss.

**Novelty:** Standard consequence once the confidence-set rate is known.

**Strength and issue:** Does not justify fixed-confidence P1 interval-midpoint MSE, and does not by itself handle arbitrary huge M/tau.

## T13. Truncated scans

**Result:** `prop:truncated`. **Location:** [robust_adaptive_extension/paper/gap_section.tex](../robust_adaptive_extension/paper/gap_section.tex), line 76.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Retain only scan supports up to the supplied budget. The short-support bound and remaining deterministic envelope give the stated residual term and operation count.

**Novelty:** Useful restricted computational upper bound.

**Strength and issue:** Not an efficient minimax solution in the original diffuse weak-signal regime; budget dependence must remain explicit.

## T14. A low-degree estimation separation

**Result:** `thm:low_degree`. **Location:** [robust_adaptive_extension/paper/gap_section.tex](../robust_adaptive_extension/paper/gap_section.tex), line 115.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Expand the planted likelihood in Gaussian Hermite degrees. Sparse tensor overlap moments control the truncated norm, producing a polynomial-estimation obstruction in the stated degree range.

**Novelty:** Specialized restricted computational lower bound, related to sparse tensor PCA.

**Strength and issue:** Does not establish hardness of every polynomial-time estimator or honest interval. Fixed-order and support/degree exponent conditions matter.

## T15. What an efficient short interval would imply

**Result:** `prop:ci_detection`. **Location:** [robust_adaptive_extension/paper/gap_section.tex](../robust_adaptive_extension/paper/gap_section.tex), line 147.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** A short honest interval covering the null rarely reaches a separated common target. Markov's inequality on length and coverage create a test.

**Novelty:** Standard CI-to-testing reduction.

**Strength and issue:** An implication only; a separate computational testing lower bound is required to conclude general algorithmic hardness.

## T16. Diameter using both norm and scan constraints

**Result:** `thm:norm_diameter`. **Location:** [robust_adaptive_extension/paper/norm_loading_section.tex](../robust_adaptive_extension/paper/norm_loading_section.tex), line 12.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Intersect the scan coordinate envelope with the norm-induced ordered-coordinate envelope before summing. This prevents a spurious logarithm at small budgets.

**Novelty:** Important technical refinement of the sharp rate.

**Strength and issue:** Doubled residual ranks/norm enter constants. Separate small and large M regimes explicitly.

## T17. Full-data length for every positive norm budget

**Result:** `thm:all_norm_rates`. **Location:** [robust_adaptive_extension/paper/norm_loading_section.tex](../robust_adaptive_extension/paper/norm_loading_section.tex), line 32.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Apply the norm-sensitive sum lemma for the upper bound. A coordinate mixture and truncated sparse harmonic construction with m controlled by both p and M/tau match it.

**Novelty:** Central all-budget completion of the flat-loading theory.

**Strength and issue:** Uniform in p,M,tau for fixed positive caps and K; no extrapolation to arbitrary loading profiles or intermediate growing caps.

## T18. Squared risk uniformly over norm budgets

**Result:** `thm:all_norm_mse`. **Location:** [robust_adaptive_extension/paper/norm_loading_section.tex](../robust_adaptive_extension/paper/norm_loading_section.tex), line 58.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** A measurable approximate residual fit has controlled Gaussian excess tails on every observation. Integrating those tails gives squared risk without multiplying a fixed failure probability by M^2.

**Novelty:** Substantive risk refinement beyond a fixed-confidence midpoint argument.

**Strength and issue:** All positive budgets, but ideal residual optimization. The estimator differs from the empirical cap-valid interval midpoint.

## T19. Loading-dependent full-data bounds

**Result:** `thm:weighted_bounds`. **Location:** [robust_adaptive_extension/paper/norm_loading_section.tex](../robust_adaptive_extension/paper/norm_loading_section.tex), line 83.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Rearrange absolute weights against ordered residual coordinates for the upper bound. Equalize target weights in one factor of a nonnegative mixture; overlaps contract, so the full likelihood lower bound remains valid.

**Novelty:** Useful explicit loading envelopes.

**Strength and issue:** Upper and lower bounds need not match for arbitrary weights. Sign handling relies on the specified construction, not monotonicity of arbitrary signed inner products.

## T20. Sharp rates for a flat orthogonal loading

**Result:** `prop:flat_loading`. **Location:** [robust_adaptive_extension/paper/norm_loading_section.tex](../robust_adaptive_extension/paper/norm_loading_section.tex), line 95.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Restrict to the m-dimensional orthogonal product span, normalize by sqrt(m), and apply the all-budget theorem. The unused orthogonal observations are pure noise.

**Novelty:** Sharp corollary with useful ambient-dimension invariance.

**Strength and issue:** Flat signed orthogonal weights only. Arbitrary nonorthogonal loadings require the separate residual correction.

## T21. Full-data robustness under directional tails

**Result:** `thm:sg_full`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 14.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Replace Gaussian net tails by a joint directional moment-generating-function bound. Gaussian noise is a member of the unknown-law family for the minimax lower bound.

**Novelty:** Calibrated robustness extension.

**Strength and issue:** Joint proxy and known scale required. Minimax over a noise family does not give the lower rate for each fixed member.

## T22. Full scans with only finite-variance replicates

**Result:** `thm:mom_full`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 30.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Independent whole-tensor replicates give Chebyshev block bounds for every net direction. Median/binomial and union bounds calibrate simultaneous scans; the polynomial excess tail is integrable for squared risk.

**Novelty:** Meaningful finite-variance extension with strong replication requirements.

**Strength and issue:** Requires n at least twice the largest block count, of order p at fixed K/confidence, and a known covariance upper bound. Still exponential in scan complexity.

## T23. Two limits of a noise relaxation

**Result:** `prop:noise_limits`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 43.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Equicorrelated coordinates show why marginal variance/tail control is insufficient. A bounded scalar Rademacher-noise experiment with small signal range permits exact recovery, refuting a per-law Gaussian lower transfer.

**Novelty:** Useful explicit boundaries.

**Strength and issue:** Counterexamples are outside the sufficient assumptions or refute an overextension, not the stated robustness theorem.

## T24. Sharp length under a Frobenius approximation allowance

**Result:** `thm:approx_sharp`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 50.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Inflate scan constraints and projected endpoints by the supplied Frobenius allowance. Direct Gaussian inference caps the length; nested exact-rank and residual-ball submodels give matching lower terms.

**Novelty:** Sharp model-approximation consequence.

**Strength and issue:** Allowance must be supplied and deterministic/certified. Does not license estimating it from the same data without calibration.

## T25. A growing-rank lower bound and the unrestricted endpoint

**Result:** `prop:growing_caps`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 60.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Sparse diagonal tensors of support s have all relevant unfolding ranks s. Their full-data likelihood depends on hypergeometric overlap; the unrestricted endpoint follows from the norm-ball direction.

**Novelty:** Classical sparse lower bound identifying a tensor rank transition.

**Strength and issue:** Intermediate ranks are lower bounded, not sharply characterized here. G1 later matches only the large-cap branch.

## T26. A confidence interval for any certified loading decomposition

**Result:** `prop:loading_transfer`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 74.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** For L=L0+R, combine the interval for L0 with a Gaussian interval for the known residual contraction using allocated error probabilities.

**Novelty:** Standard and useful calibration device.

**Strength and issue:** No independence between the two intervals is needed. Same-data loading selection is not covered without simultaneous control.

## T27. Two efficiently attained minimax regimes

**Result:** `thm:efficient_regimes`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 90.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** In the small-budget or unrestricted-rank regimes, structural/direct choices meet the relevant lower bounds.

**Novelty:** Straightforward attained endpoints.

**Strength and issue:** Does not imply efficiency for diffuse fixed-cap weak signals at moderate/large budgets.

## T28. Why full convexification loses the weak-signal gain

**Result:** `prop:convex_loss`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 98.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** The convex hull of admissible signed tensor atoms contains a segment in the loading direction. A Gaussian two-point argument restores the noise-scale lower bound.

**Novelty:** Concrete convex-hull obstruction using classical nonconvex inference ideas.

**Strength and issue:** Concerns honesty over the enlarged convex class, not every algorithm using convex subroutines.

## T29. An adaptation obstruction at nonzero tensors

**Result:** `thm:shifted_adaptation`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 108.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Place the base tensor and weak rank-one mixture in orthogonal coordinate blocks. Rank subadditivity, Pythagorean norm slack and Gaussian translation preserve the lower bound.

**Novelty:** Useful nonzero refinement of an adaptation obstruction.

**Strength and issue:** Requires spare ranks and norm budget. Does not characterize every point or saturated stratum.

## T30. Finite-sample rank calibration with a computable bias correction

**Result:** `thm:adaptive_tangent`. **Location:** [robust_adaptive_extension/paper/robust_adaptive_section.tex](../robust_adaptive_extension/paper/robust_adaptive_section.tex), line 140.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** One simultaneous pilot operator-norm event identifies separated mode ranks. Conditional on the independent pilot, validation is Gaussian. The omitted tensor projection has at least two subspace errors, giving a second-order bias certificate.

**Novelty:** Finite-sample constructive regular-signal refinement.

**Strength and issue:** Coverage stated on the separated class only. Its product-space projector may be larger than the exact Tucker tangent space; severe signal requirements are disclosed.

## T31. Controlled squared component weights

**Result:** `lem:cp`. **Location:** [robust_adaptive_extension/paper/appendix.tex](../robust_adaptive_extension/paper/appendix.tex), line 7.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Tucker mode orthogonalization and TT canonical prefix recursions give a finite unit-product expansion with a bounded number of components and exact sum of squared weights.

**Novelty:** Standard factor geometry assembled for this problem.

**Strength and issue:** TT paths need not be mutually orthogonal. The supplied argument does not make that erroneous assumption.

## T32. Exact diagonal reduction

**Result:** `lem:image`. **Location:** [robust_adaptive_extension/paper/appendix.tex](../robust_adaptive_extension/paper/appendix.tex), line 69.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Holder gives one inclusion; product factors proportional to signed abs(a_i)^(1/K) give the reverse inclusion and correct norm.

**Novelty:** Exact useful reduction; related factor geometry is established.

**Strength and issue:** Rank-one diagonal image only. Positive caps contain this class.

## T33. Scalar threshold envelope

**Result:** `lem:soft`. **Location:** [robust_adaptive_extension/paper/appendix.tex](../robust_adaptive_extension/paper/appendix.tex), line 94.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Case analysis on thresholding with abs(noise)<=lambda yields error <=min(abs(signal),2lambda), then the q-envelope bound.

**Novelty:** Elementary scalar inequality.

**Strength and issue:** Valid for q=2/K in (0,1); the selection/event calibration is handled separately.

## T34. Matrix functional bound

**Result:** `lem:structural`. **Location:** [robust_adaptive_extension/paper/appendix.tex](../robust_adaptive_extension/paper/appendix.tex), line 108.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Von Neumann trace inequality followed by Cauchy--Schwarz over at most r singular values gives the functional range.

**Novelty:** Standard matrix inequality.

**Strength and issue:** Rank is required; replacing the rank-restricted bound by the full Frobenius norm can lose the useful factor.

## T35. Common-target alternatives

**Result:** `lem:mixture`. **Location:** [robust_adaptive_extension/paper/appendix.tex](../robust_adaptive_extension/paper/appendix.tex), line 175.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Coverage of zero and a common alternative target, followed by total variation transfer and a union bound, forces expected length at least target separation times 1-2alpha-TV.

**Novelty:** Classical testing principle.

**Strength and issue:** Common target is essential. Independent procedure randomization can be appended without changing total variation.

## T36. Finite product nets and injective norm

**Result:** `lem:net_scan`. **Location:** [robust_adaptive_extension/paper/full_data_proofs.tex](../robust_adaptive_extension/paper/full_data_proofs.tex), line 4.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** A telescoping product-net approximation bounds the injective norm by twice the finite maximum; canonical expansion then gives the rank-dependent norm comparison.

**Novelty:** Standard net argument adapted to the tensor class.

**Strength and issue:** Exponential net cardinality is explicit. Constants depend on tensor order.

## T37. Uniform cubic moment for a weighted sign sum

**Result:** `lem:cubic_moment`. **Location:** [robust_adaptive_extension/paper/full_data_proofs.tex](../robust_adaptive_extension/paper/full_data_proofs.tex), line 70.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Split the decreasing weighted sign sum into head and tail, control the tail's sub-Gaussian scale, and integrate its cubic exponential moment at the supplied small constant.

**Novelty:** Technical ingredient for the preliminary harmonic bound.

**Strength and issue:** No independence of the three coupled likelihood sums is asserted. Redundant if the preliminary lower bound is removed.

## T38. Smaller rank coefficient

**Result:** `prop:budget`. **Location:** [robust_adaptive_extension/paper/refinements.tex](../robust_adaptive_extension/paper/refinements.tex), line 7.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Combine canonical component counts, the universal m-based diagonal bound, and mode/cut rank bounds; take the minimum of valid coefficients.

**Novelty:** Useful coefficient sharpening, largely algebraic.

**Strength and issue:** May improve constants or cap dependence but does not solve intermediate-cap minimax matching.

## T39. Structural range and fixed affine optimum

**Result:** `prop:affine_exact`. **Location:** [robust_adaptive_extension/paper/refinements.tex](../robust_adaptive_extension/paper/refinements.tex), line 41.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Symmetrize coordinate biases and lower bound variance by the sum of diagonal weights. Monotonic Gaussian absolute-error quantiles reduce the optimum to one scalar t in [0,1].

**Novelty:** Exact specialization of classical bounded-normal affine inference.

**Strength and issue:** Requires alpha<1/2 and deterministic affine radii. Structural-optimum criterion is a bounded-normal calculation, not a universal estimator claim.

## T40. Envelope and approximation calibration

**Result:** `prop:envelope`. **Location:** [robust_adaptive_extension/paper/refinements.tex](../robust_adaptive_extension/paper/refinements.tex), line 81.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** A calibrated simultaneous noise envelope permits the same pathwise threshold proof. Approximation adds deterministic diagonal and target allowances.

**Novelty:** General calibration lemma.

**Strength and issue:** Its input event must actually have the claimed probability; marginal bounds alone do not imply a full directional event.

## T41. Replicate median calibration

**Result:** `prop:mom`. **Location:** [robust_adaptive_extension/paper/refinements.tex](../robust_adaptive_extension/paper/refinements.tex), line 139.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Whole-replicate corruptions spoil at most c blocks. With b>=8c, b>=32 log(m/alpha), n>=2b, Chebyshev plus a binomial tail controls the coordinate medians.

**Novelty:** Standard robust-block construction with explicit constants.

**Strength and issue:** This supporting coordinate-envelope result allows bounded row corruption; the main full-scan finite-variance theorem and S06 do not establish general contamination minimax rates.

## T42. Independent residual calibration

**Result:** `prop:variance`. **Location:** [robust_adaptive_extension/paper/refinements.tex](../robust_adaptive_extension/paper/refinements.tex), line 184.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Under iid Gaussian replicates, centered residual sums of squares are independent of sample means. A lower chi-square quantile yields a valid upper noise scale; allocate errors with the interval event.

**Novelty:** Standard Gaussian residual calibration.

**Strength and issue:** Requires retained independent replicates and the stated common variance model. XCH plug-in variance is not this finite-sample construction.

## T43. Calibrated lower bounds

**Result:** `prop:levels`. **Location:** [robust_adaptive_extension/paper/refinements.tex](../robust_adaptive_extension/paper/refinements.tex), line 214.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Choose mixture amplitude and testing constants as functions of the desired confidence level, preserving a positive common-target lower factor.

**Novelty:** Calibration refinement.

**Strength and issue:** Track the stated confidence-level range; constants are not uniform as alpha approaches its boundary.

## T44. A norm-sensitive harmonic sum

**Result:** `lem:norm_sum`. **Location:** [robust_adaptive_extension/paper/norm_loading_proofs.tex](../robust_adaptive_extension/paper/norm_loading_proofs.tex), line 19.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Split the ordered-coordinate sum near s=x^2 and integrate the harmonic tail. Order three accumulates a logarithm; higher orders have a summable tail.

**Novelty:** Key analytic step behind all-budget sharpness.

**Strength and issue:** The minimum of envelopes must precede summation. It correctly retains the small-budget linear branch.

## T45. Residual fit and its noise tail

**Result:** `lem:residual_fit`. **Location:** [robust_adaptive_extension/paper/norm_loading_proofs.tex](../robust_adaptive_extension/paper/norm_loading_proofs.tex), line 103.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Compactness/continuity permit a countable dense approximate minimizer, avoiding uniqueness assumptions. Gaussian net excess tails control the fitted residual at every observation.

**Novelty:** Important existence and risk-control lemma.

**Strength and issue:** An arbitrarily selected local numerical solution does not satisfy this contract; C1 specifies the needed certified gap.

## T46. A quantitative contract for approximate minimax optimization

**Result:** `C1`. **Location:** [certified_weak_signal/theory/results.md](../certified_weak_signal/theory/results.md), line 29.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Certified lower/upper objective bounds and an O(tau) objective gap control the ideal residual-fit error. Feasible witnesses and global endpoint outer bounds distinguish inner approximation from honest projection.

**Novelty:** Useful numerical/statistical error contract.

**Strength and issue:** For squared risk the contract must hold on every observation or have its own integrated failure control. No general-dimensional implementation or polynomial complexity is supplied.

## T47. An implemented global solver on the binary rank-one class

**Result:** `C2`. **Location:** [certified_weak_signal/theory/results.md](../certified_weak_signal/theory/results.md), line 85.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Parameterize the continuous binary rank-one ball by amplitude in [-M,M] and projective angles. Global trigonometric box bounds prune only infeasible/uncompetitive cells; retained cells enclose endpoint extrema.

**Novelty:** Executable global benchmark in a very small class.

**Strength and issue:** Valid in exact real arithmetic; float64 safety guards are not directed interval arithmetic. Finite node budgets may leave large unresolved gaps; neither general ranks nor p>2 is implemented.

## T48. Sharp small-budget rates for every loading tensor

**Result:** `L1`. **Location:** [certified_weak_signal/theory/results.md](../certified_weak_signal/theory/results.md), line 140.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** A maximizing unit product contraction supplies a two-point lower bound at M<=tau. Canonical expansion bounds the structural range by sqrt(J) M rho(L), giving the upper bound.

**Novelty:** General small-ball geometry rather than a new testing principle.

**Strength and issue:** Every fixed loading tensor, fixed caps; evaluating the injective norm rho(L) can itself be hard. Does not extend beyond the small-budget regime for arbitrary L.

## T49. An optimized common-target lower bound for unequal weights

**Result:** `L2`. **Location:** [certified_weak_signal/theory/results.md](../certified_weak_signal/theory/results.md), line 190.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Choose common-target axis amplitudes Delta/w_i. Minimize the diagonal-mixture second moment over prior weights by Cauchy--Schwarz, yielding the inverse sum of inverse exponential costs.

**Novelty:** Useful optimized axis-family certificate.

**Strength and issue:** Optimized within this family only; cannot replace the cubic harmonic prior or claim arbitrary-loading minimax sharpness.

## T50. Unseparated rate adaptation across positive fixed caps

**Result:** `A1`. **Location:** [certified_weak_signal/theory/results.md](../certified_weak_signal/theory/results.md), line 228.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** The ideal outer-class procedure has the fixed-cap upper rate; every smaller positive-cap class contains the rank-one least favorable submodel with the same rate.

**Novelty:** Immediate but clarifying corollary.

**Strength and issue:** No actual-rank estimation; excludes the known-zero class; constants depend on the fixed outer caps and cannot be used for growing caps.

## T51. A computable projection certificate without separation

**Result:** `A2`. **Location:** [certified_weak_signal/theory/results.md](../certified_weak_signal/theory/results.md), line 256.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Conditional pilot/validation Gaussian inference plus norm-ball or mode nuclear-norm residual certificates gives honest projected intervals. Triangle inequalities show the elementary certificate cannot improve the direct bound under the stated conservative calibration.

**Novelty:** Useful certificate and explicit limitation.

**Strength and issue:** No separation needed, but the basic certificate can be vacuous for shortening. The later supplied-cap second-order construction is different.

## T52. The adaptation obstruction at an arbitrary orientation

**Result:** `A3`. **Location:** [certified_weak_signal/theory/results.md](../certified_weak_signal/theory/results.md), line 324.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Rotate the spare orthogonal product block and use the induced residual loading in the shifted-mixture argument. Norm and rank feasibility remain unchanged under modewise orthogonal transformations.

**Novelty:** Geometric extension of the nonzero obstruction.

**Strength and issue:** Requires an unused block, rank slack and norm slack. Not an all-point local modulus characterization.

## T53. A cap-valid tangent interval on the original unseparated class

**Result:** `A4`. **Location:** [certified_weak_signal/theory/results.md](../certified_weak_signal/theory/results.md), line 357.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Retain supplied cap dimensions. On a simultaneous operator-noise event, resolved subspace errors follow Weyl/Wedin; unresolved errors are bounded by one. The product projector omits at least two bad modes, yielding the pairwise error certificate.

**Novelty:** Useful honest weak-signal extension of the split projection method.

**Strength and issue:** Covers zero and unsaturated caps. No weak-signal minimax rate asserted. TT use is via induced Tucker mode caps, not an exact TT tangent theory.

## T54. Sharp growing-cap rates with a polynomial algorithm

**Result:** `G1`. **Location:** [high_dimensional_extension/theory/results.md](../high_dimensional_extension/theory/results.md), line 16.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Structural/direct selection meets the sparse-diagonal full-data lower bound when r>=c sqrt(p). Hypergeometric factorial moments make chi-square <=exp(1/4)-1 uniformly.

**Novelty:** Matched large-cap consequence of a classical mixture.

**Strength and issue:** Sharp min(M sqrt(r/p),tau), with constants depending on alpha,c but not growing caps/order. O(p) accesses only for coordinate loading; no intermediate-cap conclusion.

## T55. General adaptation across positive growing caps is impossible

**Result:** `G2`. **Location:** [high_dimensional_extension/theory/results.md](../high_dimensional_extension/theory/results.md), line 79.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Apply G1 at zero in the growing outer class and compare with the vanishing fixed-cap oracle rate. Orthogonal-block translation provides the stated nonzero variant.

**Novelty:** Direct, valuable consequence identifying a real adaptation barrier.

**Strength and issue:** Rules out simultaneous oracle-rate adaptation across these classes even with unlimited computation. Does not contradict A1 for fixed outer caps.

## T56. A dyadic loading bound using the full weight profile

**Result:** `W1`. **Location:** [high_dimensional_extension/theory/results.md](../high_dimensional_extension/theory/results.md), line 116.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Decompose ordered weights into dyadic blocks. Apply ideal block residual fits and an allocated confidence budget; sum widths and use Minkowski for root risk. Geometric budgets control the accumulating logarithms.

**Novelty:** Useful profile-sensitive upper envelope.

**Strength and issue:** The dyadic lower/upper envelope calculation in code is not an implemented residual fit. Arbitrary profiles need not have matching lower bounds.

## T57. Sharp rates at every budget for polynomially decreasing loadings

**Result:** `W2`. **Location:** [high_dimensional_extension/theory/results.md](../high_dimensional_extension/theory/results.md), line 171.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Fixed positive power decay makes the W1 dyadic sum bounded by a beta-dependent multiple of the first weight. A single largest-weight atom yields the matching two-point lower bound at all budgets.

**Novelty:** A meaningful special-family corollary, not a general-loading solution.

**Strength and issue:** Sharp abs(w_1)min(M,tau); constants deteriorate as beta approaches zero. Small residual perturbations require the stated norm bound and fixed epsilon<1.

## T58. A restricted computational separation for these newly matched loadings

**Result:** `W3`. **Location:** [high_dimensional_extension/theory/results.md](../high_dimensional_extension/theory/results.md), line 224.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Reweight one nonnegative planted factor to equalize the target. Overlap contractions and Hermite-degree bounds reproduce a sparse-tensor low-degree separation in the displayed beta/support/degree ranges.

**Novelty:** Specialized restricted computational extension.

**Strength and issue:** Requires 0<beta<1/K and admissible exponents; does not imply hardness for every efficient interval or the fast G1 regime.

## T59. Efficient pointwise optimality at strong saturated Tucker means

**Result:** `P1`. **Location:** [high_dimensional_extension/theory/results.md](../high_dimensional_extension/theory/results.md), line 292.

**Statement:** No defect identified within the stated scope. **Proof completeness:** Supplied argument checked; no missing essential step identified.

**Proof audit:** Use A4 with pilot error budget proportional to alpha r/p. Strong saturated singular values control subspace errors; the pairwise bias is O(tau sqrt(r/p)), as is the projected noise. Direct intersection controls expected length on pilot failure. A supported local Gaussian submodel supplies the matching lower bound.

**Novelty:** Useful constructive pointwise rate at a restricted geometry.

**Strength and issue:** Honest on the full supplied-cap class, but the short-length conclusion needs strongly separated saturated diagonal Tucker means, norm slack and M comparable to signal norm. Sufficient amplitude grows roughly as tau p^(K-1/2); no optimal threshold, complete TT theory or midpoint MSE claim.


\newpage

# Assumptions, formulation and tuning audit

This table covers the principal assumptions and the extra assumptions introduced by the retained refinements and supplements. IDs R01–R20 are review IDs, not replacements for the manuscript's own labels. Locations use result labels from [theorem_audit.md](theorem_audit.md). “Standard” describes the kind of condition; it does not imply empirical plausibility or necessity of the exact constants.

| Assumption | Purpose and use | Standard? | Restrictiveness / interpretability | Could weaken? |
|---|---|---|---|---|
| R01. Fully observed $Z=A+\tau G$ with iid standard Gaussian entries | Exact linear pivots, split independence, full likelihood lower bounds; all principal Gaussian results | Standard Gaussian sequence benchmark | Strong for naturally collected tensor data; one must justify what is independently replicated. Not a completion, regression or LLM sampling theorem | Joint directional tails give upper bounds; covariance-aware or incomplete-data inference needs further theory |
| R02. Known $\tau>0$; or known $\sigma$ and $n$ with $\tau=\sigma/\sqrt n$ | Thresholds, direct radii, likelihood scaling and split noise | Standard in minimax benchmarks | Not inferred from a single noisy tensor in the main theory. Signal and noise can be hard to separate near weak rank boundaries | Independent Gaussian replicates permit the separate residual chi-square calibration; arbitrary plug-in estimates are not automatically valid |
| R03. Supplied $\|A\|_F\le M$ | Structural interval, compact feasible sets, small-budget bounds, bias certificates | Standard parameter-space radius | Often difficult to know scientifically. In the simulations it defines the class before drawing noise; truth-based class construction is not observation-based tuning | An independent upper bound with allocated failure probability is plausible; no such general bound is currently supplied |
| R04. Correct supplied Tucker mode or TT cut caps | Canonical complexity, diagonal envelope, class membership and A4 | Standard low-rank modeling | Overstatement preserves coverage but can cost length; understatement may fail deterministically. Exact low rank is not certified by fitting the observation | Approximate class plus a supplied residual allowance is treated; data-selected caps need calibration |
| R05. $K\ge3$ and fixed positive caps in central asymptotics | $2/K<1$, summation exponents, rank-independent-of-$p$ constants | Natural for this phenomenon | Excludes using constants as uniform in arbitrary growing rank; zero-rank oracle is a different singleton class | G1 handles $r\gtrsim\sqrt p$ with uniform constants. Intermediate caps remain open |
| R06. Known orthonormal product loading and usually $\|w\|_2=1$ | Exact diagonal noise, sorted loading bounds and flat-loading sharpness | Restrictive structured functional | Rotations are allowed, but arbitrary scientific contrasts need not have this form. Normalization is a units convention; independently fixing the target is substantive | Known residual-loading calibration; L1 for every loading at small budgets; W2 for fixed weight decay |
| R07. Equal mode size $p$ for main phase formulas | Clean support-mixture and entropy scaling | Simplifying symmetry | Flat loading on $m$ orthogonal atoms extends to unequal ambient modes; arbitrary aspect ratios and targets are not all characterized by replacing $p$ mechanically | Unequal dimensions can be handled for the stated embedded flat block; broader profiles need new matching arguments |
| R08. Fixed confidence level, generally $0<\alpha<1/4$ for sharp comparisons | Positive common-target testing constant | Standard | Upper validity can allow larger ranges; lower constants deteriorate at boundaries. Uniform claims over vanishing or near-one-half confidence need separate tracking | Calibrated lower-bound proposition covers its displayed levels; do not erase its conditions |
| R09. Joint sub-Gaussian proxy $E e^{t\langle U,E\rangle}\le e^{v^2t^2\|U\|_F^2/2}$ with known $v$ | Full-net tails and all-direction residual control; `thm:sg_full` | Standard directional concentration | Allows dependence if the full covariance/tail proxy is valid. Marginal tails alone are insufficient; not directly testable with one realization | Different direction-dependent thresholds may improve constants but require a calibrated net event |
| R10. Independent identically distributed whole-tensor replicates and $\operatorname{Cov}(\operatorname{vec}W_j)\preceq\sigma^2 I$ | Median block Chebyshev and binomial bounds; `thm:mom_full` | Standard robust mean premise | Heavy tails permitted, but independent replicates and a known covariance upper bound are substantial. Common prompts/subjects may violate independence | Mixing/cluster extensions are possible research directions, not current guarantees |
| R11. Odd block counts $b_s$ with $n\ge2\max_s b_s$ | Feasible block means, union and excess-tail control | Standard feasibility condition with conservative constants | At fixed order/confidence the full scan needs replication of order $p$; too few replicates make the theorem unavailable | Sharper concentration constants may help; a radically smaller replication requirement needs a new argument |
| R12. At most $c$ adversarially corrupted whole replicates, $b\ge8c$, $b\ge32\log(m/\alpha)$, $n\ge2b$ | Supporting `prop:mom` coordinate-median envelope | Standard block-contamination idea | Concerns whole-replicate corruption and a known count; does not prove arbitrary entrywise/Huber-contamination minimax rates | Exact breakdown and optimal contamination dependence are unproved |
| R13. Retained independent Gaussian replicates with common variance | Independence of sample means and residual chi-square statistic; `prop:variance` | Classical normal theory | Stronger than merely a variance bound; invalid under general heavy tails or serial correlation | Different independent scale bounds could be substituted if proved |
| R14. Supplied Frobenius approximation allowance and known loading decomposition | Deterministic target-bias correction; `thm:approx_sharp`, `prop:loading_transfer` | Standard sensitivity formulation | An externally meaningful allowance is interpretable; choosing it because the same data fit well is not covered | Independent calibration or simultaneous model selection would require extra uncertainty terms |
| R15. Pilot independent of validation, with correct $\sqrt2\tau$ scale after artificial splitting | Conditional Gaussian pivot and pilot-selected candidate validity; A2/A4/P1 | Standard sample-split reasoning | Artificial splitting requires Gaussian noise and known scale; it adds noise. Direct and split intervals need not be independent for the union bound | Real independent replicates or a correctly calibrated joint construction may replace artificial splitting |
| R16. Spectral separation above the pilot threshold for rank selection | Weyl/Wedin and exact mode-rank recovery; `thm:adaptive_tangent` | Standard perturbation requirement | Explicitly excludes weak nonzero components. The assumption is not imposed by A4 coverage, which keeps supplied caps | A4 removes separation for coverage by conservative unresolved-error bounds; it does not guarantee weak-signal shortening |
| R17. Strong saturated diagonal Tucker point, $\|A_0\|_F+\tau\le M\le c_0a\sqrt r$, $a\ge\max(4\eta,\eta^2\sqrt p/\tau)$ | Second-order bias and local-submodel lower bound; P1 | Strong sufficient condition, not an optimal known threshold | Signal of order $\tau p^{K-1/2}$ is very restrictive; saturation and norm slack are essential to this proof. Coverage itself holds on the wider unseparated cap class | Highest-value adaptation strengthening: weaker signal, unsaturated and rotated geometry, TT points |
| R18. Spare ranks, unused orthogonal product block and norm slack at $A_0$ | Embed a translated hard mixture; shifted adaptation and A3 | Standard local testing mechanism | Interpretable geometric obstruction but does not include every mean. A saturated point need not admit this prior | A full between-class local modulus would generalize this construction |
| R19. Fixed positive weight decay exponent and fixed constants; small known residual for W2 extension | Summable dyadic upper envelope and largest-atom lower bound | Standard regularity of a weight profile | Covers many decays but not diffuse flat weights by taking the exponent to zero with $p$ | Arbitrary slowly varying/multiscale profiles remain open |
| R20. Global optimization gap contract, or explicitly restricted low-degree class | C1 risk control and C2 outer projection; degree-restricted lower results | Standard distinction between estimator and algorithm class | A local stationary point is insufficient. Float64 guards differ from formal interval arithmetic. Low-degree results do not cover all efficient procedures | General efficient global approximation or a carefully defined stronger obstruction is open |

No incoherence, restricted eigenvalue, strong convexity or mixing assumption is hidden in the central full Gaussian-location theorem. The regular-signal competitor has its own initialization, alignment and remainder conditions; these must be checked separately rather than imputed to the cap-uniform result. The assumptions above are compatible because the noise families, separated procedures and pointwise submodels are presented as different results. They would become incompatible if merged into one unqualified “general robust adaptive” claim.

## Tuning audit

| Quantity | Theory and implementation | Review action |
|---|---|---|
| Gaussian diagonal threshold $\lambda$ | Simultaneous Gaussian tail allocation over $m$ contractions, proportional to $\tau\sqrt{\log(m/\alpha)}$ | Known scale required; it is not cross-validated on observed coverage |
| Structural/direct/threshold selection | Uses valid supplied bounds and deterministic radii | Valid without a new selection penalty; choosing among arbitrary observed widths would need a joint event |
| Norm and cap inputs | Registered before each observation, sometimes functions of the chosen signal configuration | No observed-outcome leakage found; add fixed-$M$ signal sensitivity (F05) |
| A4/P1 pilot budget | $\delta=\alpha r/(8p)$ for P1 and a simultaneous operator bound | Essential to expected length when $p/r$ grows; a fixed pilot error budget is not interchangeable |
| Split validation quantile | Uses remaining error after the pilot budget; direct intersection gets its own allocation | Implemented in the full method; the ablation changes this too (F02) |
| Solver nodes and endpoint tolerance | Fixed registry; 100 nodes uses $.5\tau$, later 600/3000 use $.1\tau$ | Disclosed, but cannot interpret a certification curve as a pure node-budget effect unless tolerance is held fixed |
| Residual objective tolerance | C1 requires a controlled global objective error of order $\tau$ | No general fit implementation; do not substitute an optimizer's convergence flag |
| Median block counts and covariance proxy | Explicit logarithmic cardinality/confidence rule and $n$ feasibility | Validity is only within stated replication/noise assumptions; do not silently reduce blocks |
| XCH ranks, initialization and noise | HOSVD, two simultaneous iterations; supplied ranks; known and residual plug-in noise variants | No truth-assisted initialization found. Add row-level assumption status; the oracle remains separately labeled |
| Polynomial-degree cutoff | Defines a lower-bound class | Not a tuning choice proving hardness for all algorithms |

## Notation needed to keep the experiment well posed

Use $D_{\mathrm{amb}}=\prod_kp_k$ for the number of observed entries and $d_{\mathrm{poly}}$ for polynomial degree; $q_K=2/K$ for the diagonal exponent; $z_u$ for Gaussian quantiles; $\varepsilon_A$ for approximation allowance; $\eta_{\mathrm{op}}$ for pilot operator error; $J_{\mathrm{cap}}$ for canonical component complexity and $H$ for support overlap. State explicitly when probabilities include the artificial splitting seed. Use $R_K$ for a rate and reserve $\mathcal L_0,\mathcal L_{\max}$ for infima over honest procedures. These changes prevent cross-supplement ambiguity without changing the mathematics.


\newpage

# Simulation design and claim-to-evidence audit

Review of the saved September 13 empirical study. F01–F10 refer to findings in [report.md](report.md). Exact configurations are in the preserved initial and follow-up JSON registries. The table below assesses experimental questions; favorable finite results cannot prove a minimax lower bound or honesty over a continuum.

## Suite-by-suite review

| Suite / repetitions | Question, design and theorem | Methods / metrics | Review judgment |
|---|---|---|---|
| S01: 54 cases, 5,000 each | G1 large-cap structural/noise transition; coordinate diagonal Gaussian signals at zero and boundary; vary $p,n,M$ and $r=\sqrt p$ | Direct, structural and G1 choice; coverage, length, MSE, paired differences, normalized rates | Valid exact sufficient-statistic experiment. Stochastic noise-branch RMSE is useful; deterministic length slopes mostly check the formula. Does not address fixed-cap ideal computation. |
| S02: 44 cases, 1,000 each | Diagonal threshold theorem and diagonal-only rate; vary $K,p,n$ and rank-one support profiles near threshold | Direct, structural, raw/selected threshold and scalar estimates | Good stress test of an executable weak-signal interval. Very conservative tested coverage does not establish minimax attainment; sharper full-data rates are references only. |
| S03: 8 cases, 150–500 each | P1 strong saturated Tucker means at $p=8,16,32,64$, cap 1 or rounded $\sqrt p$, amplitude eight times the sufficient bound | Pointwise, XCH known/plug-in, direct, oracle, split diagnostic; coverage, length, loss, projected geometry | Demonstrates shortening and constant costs in a very strong regime. Slopes differ from asymptotic references; F01 affects two 90% rows. Unconditional midpoint loss has a rare-fallback pathology (F04). |
| S04: 28 cases, 500 each | A4 validity and separated-rank selection limits; zero-to-strong signals, rank/cap changes, non-diagonal/rotated and violation cases | Same paired tensor methods plus separated selector where defined; coverage, selection, length, loss | Useful failures, with comparator domain restrictions. Signal sweep also changes supplied $M$ (F05). The no-bias diagnostic is not an isolated ablation (F02). Unsaturated/rotated points do not test P1's specific rate claim. |
| S05: 10 cases, 5,000 each | Noise-limits and directional calibration; $p=256$, equicorrelation, signs, standardized t3/t5, centered mixtures and mean shift | Naive iid Gaussian versus known covariance/proxy/Chebyshev calibration; coverage and length | Clearly shows that joint covariance and centering matter. Heavy-tail finite-sample validity comes from the stated conservative bound. No general Huber-contamination theorem is tested. |
| S06: 15 cases, 500 each | Finite-variance full binary-net feasibility across replication/tails and deliberately dependent replicates | Directional medians versus Gaussian sample-mean envelope; simultaneous acceptance event | Tests a calibration component, not optimized interval length or full minimax risk. Small-$n$/dependence violations need their existing out-of-domain labels. Does not test the corrupted-row or chi-square scale refinements (F08). |
| S07: 168 cases; 84 with 5,000 draws, 84 analytic-only | Small-budget orthogonal loading geometry and larger-budget envelopes; flat, decay, plateau, logarithmic and spike profiles | Direct/structural small-budget intervals; dyadic/axis envelopes and analytic ratios | The small-budget experiment is executable. Larger-budget bounds do not implement W1 residual fits or prove general profile matching. The 336 loading calculations are not additional MC configurations. |
| S08: 8 cases, 30 observations each | C2 binary continuous rank-one optimization; orders 3/4, signal/loading cases, three budgets and three levels | Direct and global outer endpoints; gaps, witnesses, certification, width, coverage, time | 2,160 solves reuse 240 observations. At 95%/3,000 nodes 94/240 remain unresolved. Fixed loading/tolerance would be needed for clean budget or signal effects. Numerical guards are not formal interval arithmetic (F07). |
| S09: 11 cases, 1,000 each | Loading-residual and approximate-rank calibration; $p=4096,K=4$, explicit off-diagonal mean contributions | Direct, corrected and omitted-correction intervals; paired coverage and length | Convincing adversarial examples for the need to account for discarded target contribution. Uses conservative executable constructions, not the general sharp projection. |
| S10: 5 cases, 1,000 each | CI inversion and regular-signal scalar pivots; opposite strong diagonal signals with local target shifts, $p=16,r=2$ | Direct, pointwise, XCH and oracle; rejection rates, exact direct power, pivot QQ plots | Supports tested power/normal-pivot comparisons. No optimal testing claim or CLT for the pointwise midpoint follows. Oracle access and regular-signal restrictions are explicit. |
| S11: 18 runtime settings; ten calls after warmup | Computational scaling of actual diagonal access, full tensors and binary optimization | Runtime mean/SE and traced allocations | Useful descriptive comparison with fixed threads. Input memory and native workspaces are excluded; time uncertainty is not a stochastic theorem. Ten calls do not establish stable wall time on all hardware. |
| S12: 50 cases, 5,000 each; registered follow-up | Intermediate-cap upper/lower gap under sparse common-target diagonal signals; vary caps/budgets/dimensions | Direct, structural, cap upper interval and analytic testing lower reference | Demonstrates an unresolved envelope gap, not a sharp intermediate rate. Strict endpoints differ from analytic structural boundaries by one ULP in four configurations; this is distinct from F01's genuine miss. |
| S13: 1 case, 10,000 draws; registered follow-up | Independent exact Gaussian calibration investigation after the retained S03 low-coverage realization | Direct Gaussian; coverage and Wilson interval | 9,492/10,000 is consistent with nominal 95%. Original 131/150 result is preserved. Appropriate diagnostic, not a replacement seed or proof that every other implementation is correct. |

The principal stochastic metrics include nominal levels 90%, 95% and 99%; Wilson coverage intervals; mean length, MSE and bias with appropriate Monte Carlo uncertainty; and paired method differences on shared observations. t3 fourth moments are infinite, so ordinary squared-loss MCSE is not justified there and is not claimed. Per-point uncertainty and a Bonferroni undercoverage screen serve different purposes. Repeated confidence levels and optimizer budgets are dependent observations, not extra independent sample size.

## Current claims and recommended wording

Quoted phrases below occur in the identified user-owned source files. Some claims are already well scoped and should be retained, not weakened merely to make the review more negative. The conclusions of every main Results subsection are covered by the suite map above and the claim families below.

| Current claim / source | Evidence classification | Too strong? | Recommended wording / action |
|---|---|---|---|
| “Final analysis independently recomputes all interval coverages” — empirical report, Design and checks | Directly supported as a reproduction of the same event rule; scientifically incomplete because F01 changes the event | Needs qualification | “Raw endpoints and losses are recomputed; a separate rounding-policy audit verifies that numerical tolerances do not count statistical misses as hits.” Adopt only after correction. |
| “A bias-omitted split projection ... test[s] the need for the new correction/caps” — simulation design, Part B | Weak support for a component-specific interpretation; direct evidence for an unprotected combined variant | Yes if read as an isolated bias effect | “A split projection omitting bias protection, fallback and the full confidence allocation is a combined diagnostic.” Add a controlled ablation to attribute individual effects. |
| “general unseparated rank adaptation remain open” — main abstract, line 39 | Broad statement remains true but predates precise A1/G2/P1 conclusions | Incomplete, rather than mathematically false | State fixed-positive-cap rate adaptation, growing-cap impossibility and restricted strong-pointwise optimality separately; then name the remaining complete pointwise problem. |
| “absence of actual-rank adaptation” — main manuscript, line 406 | A constant selected radius does not track changing actual rank in that plot; positive fixed caps can nevertheless share the same minimax rate | Ambiguous use of adaptation | “The procedure does not estimate actual rank or shorten its radius as this singular value vanishes; fixed-positive-cap rate adaptation is a separate statement.” |
| “Sharp growing-cap rates with a polynomial algorithm” — G1 title | Direct mathematical matching for $r\ge c\sqrt p$ | No within the stated condition | Keep the condition adjacent to every shortened summary. For coordinate loadings, say $O(p)$ accessed entries; do not imply it reads a rotated full tensor in $O(p)$. |
| “Sharp rates at every budget for polynomially decreasing loadings” — W2 title | Directly supported by W1 and largest-coordinate lower bound for fixed decay exponent | No within fixed-decay scope | “Every budget, for the stated fixed positive power-decay family.” Do not replace this by arbitrary-loading sharpness. |
| “Efficient pointwise optimality at strong saturated Tucker means” — P1 title | Matched length theorem on a sharply restricted point family; empirical shortening in that family | No as stated | Retain “expected length,” “strong,” “saturated,” and “Tucker”; add that it is rate optimality rather than optimal constants or signal threshold. |
| “The cap-valid implementation replaces empty interval intersections by {0}” — empirical report, estimator failure | Directly supported by code and raw sentinel events | No; crucial disclosure | Keep the observed unconditional MSE and identify the midpoint as a separate empirical estimator. The general residual-fit MSE theorem does not apply to it. |
| “The P1 slopes do not equal their limiting references” — empirical report, rate validation | Directly supported; fixed/growing cap slopes -.4745/-.1791 and uncertainty | No | Retain. Describe frozen geometry as a post-hoc explanation, not exact validation of estimated-subspace asymptotics. |
| “Simulations do not prove minimax optimality, uniform honesty, or impossibility” — empirical report opening | Correct inferential scope | No | Retain; use analytic/implemented distinctions in every figure and summary table. |
| “Gaps are numerical float64 bounds with guards, not formal interval arithmetic” — caption 06 | Directly supported by solver arithmetic and documentation | No | Retain prominently. “Certified” should always specify the numerical convention and requested tolerance. |
| “No normality claim is made for the cap-valid interval midpoint” — caption 08 | Appropriate separation of Gaussian pivots from nonlinear midpoint | No | Retain; do not summarize the QQ panel as validating all estimators. |
| “minimax rates when ... over that family” — joint sub-Gaussian theorem | Gaussian subfamily lower bound and joint-proxy upper bound | No with family quantifier | Retain the unknown-law family quantifier; avoid “distribution-free optimality for each noise law.” |
| “No real-data result ... has been run” — real-data README | Directly supported by artifact inventory | No | Retain pending status. Synthetic stressors and injected noise are not real-data inferential validation. |

No current active-source claim of universal scalability, state-of-the-art dominance, “first” general weak-factor inference, or significance without uncertainty was identified. Such hypothetical claims are not entered as if the authors made them. The exact current wording is often appropriately cautious; F01–F03 are the main changes required rather than a wholesale retraction of the results.

## Fairness, sensitivity and limitations

All paired procedures access the same observation and share artificial split noise when relevant. The direct method is exact in its stated Gaussian experiment; the support oracle receives unavailable information and is clearly marked. The XCH known-noise and plug-in variants are present, with no truth-assisted initialization. A faithful comparator on a smaller regular class need not remain honest at zero, and its weak-signal failures are not evidence against its theorem.

Robustness across parameter/noise changes is better supported than robustness across independent seeds at every full-tensor configuration. The separate calibration follow-up is useful, but solver B=30 and largest-tensor B=150 leave wide uncertainty. Fixed-$M$ sweeps, a fixed-loading solver study, case-level regularity labels and controlled ablations would make interpretation stronger without rerunning every cheap case. Additional HOOI iterations or another carefully justified regular-signal comparator could be exploratory sensitivities; they are lower priority than repairing the event definition and are not substitutes for a certified full-data minimax fit.


\newpage

# Writing, notation, figures and tables

The pre-submission-reviewer skill informed this audit. The user's scientific severity definitions take precedence over automatic stylistic severity: an obsolete figure or long paragraph is not called a CRITICAL mathematical defect. A theory paper is not required to manufacture an architecture diagram, three datasets or an LLM application. Proposed edits are review recommendations; the original documents are preserved.

## Five-dimensional presentation assessment

| Dimension | Judgment and evidence | Severity / action |
|---|---|---|
| Macro logic | The integrated paper explains the Gaussian experiment and honesty-class comparison, but its 55 pages predate the two supplements and the new empirical study. Six contribution bullets mix central sharpness with routine and historical refinements | MAJOR, F03: one final narrative and proof chain, focused on sharp full-data rates; concise method-status table |
| Writing details | Paragraph topics are generally explicit; the running flat-diagonal example is consistent. Repeated gap/open-question paragraphs and sequential stages dilute the final result. Abstract is dense and historically scoped | F03/F10: replace obsolete gap narrative; proposed abstract supplied; move superseded material rather than adding another layer |
| English grammar | No repeated article, agreement, tense, relative-clause or nonidiomatic construction was identified as a material defect in the active text | No invented grammar-rule violation. Mathematical precision and organization deserve attention before cosmetic rewriting |
| LaTeX / references | 132 integrated labels; no duplicate or unresolved reference labels; all 34 cited keys exist in the integrated bibliography. Five active PDFs parse with no text spans outside page bounds and no replacement characters | Mechanical source/PDF checks newly run; full citation accuracy and exhaustive priority are outside this stage's scope. Global symbol consistency still needs F10 |
| Figure/table quality | Four integrated manuscript figures and ten current empirical figures freshly inspected; all 14 are vector PDFs with no embedded raster images. Labels, legends and uncertainty generally readable | Replace the obsolete leading gap figure; keep scope/uncertainty conventions in captions. Details below |

The active-source scan covered 22 files, including the integrated TeX inputs, both supplement theory files and their generated TeX, the new empirical report and manuscript insert. It found **zero hits** for the skill's listed banned vocabulary patterns and em-dash patterns; [style_scan.json](tables/style_scan.json) records the result and `code/inventory.py` records the exact search patterns. Bibliographic author/title punctuation is not treated as prose to rewrite. This is a reproducible lexical scan, not a universal detector of writing quality.

Visual inspection included all 14 individual figures and integrated manuscript pages 1, 9, 16, 26, 36 and 55. All five active PDFs were also scanned programmatically across every page. The integrated paper was compiled in an isolated copy; the build log and result are in [presentation_checks.json](results/presentation_checks.json). Visual sampling cannot exclude every local typesetting issue on unrendered pages, and a syntactically resolvable citation does not establish its scientific accuracy.

## Figure audit

| Figure | What it communicates / visual checks | Scientific or presentation action |
|---|---|---|
| Main: `theoretical_comparison` | Readable log-scale rate comparison with labeled classes and an intermediate full-data gap | Move to a historical appendix or replace by the final all-budget cubic/higher-order rate diagram. Caption acknowledges its early-stage status, but this should not be the lead visual of the final theorem |
| Main: `weak_rank_coverage` | Clear coverage/length panels near a vanishing second singular value; categorical spacing is identified | Retain only if it adds to the new signal sweep. “No actual-rank adaptation” should mean no rank tracking/width change here, not failure of A1's fixed-cap rate statement |
| Main: `adaptive_intervals` | Readable length ratio and coverage against singular value/pilot bound; shaded region marks separation violation | The separated selector is not A4/P1. Keep the distinction explicit when integrating the newer honest-cap method |
| Main: `robustness_and_loadings` | Full binary-net feasibility versus noise laws, and calibrated loading-residual length; appropriate bars/units | Explain that feasibility is a component event. Could move to supplement when current figures 05/07 cover the same concepts |
| Empirical 01: growing rates | Log axes and deterministic length curves; clear $p$ and $n$ sweeps | Retain as a computable matched regime; zero bars reflect deterministic lengths, not extraordinary empirical precision |
| Empirical 02: weak threshold | Separate orders three/four; readable log scale and selected/raw method legend | Good executable weak-signal example; caption correctly denies full-data ideal attainment |
| Empirical 03: pointwise rates | Cap-one and growing-cap panels; 1.96-SE length bars; XCH/oracle overlap visible | Retain strong-signal and cap-rounding qualifications. Overlap is substantive, not missing curves. Prefer explicit rate-normalized inset if main space allows |
| Empirical 04: signal sweep | Symlog axes preserve zero; Wilson coverage and mean-length bars; regular/separated failures visible | Add that $M$ changes along the sweep; a fixed-$M$ panel would isolate the signal effect (F05) |
| Empirical 05: noise | Correlation and noise-law panels clearly distinguish naive and calibrated methods | Valid illustration of calibration and mean-shift limits. Category labels and captions explain standardization/proxy types |
| Empirical 06: solver | Log mean endpoint gaps and Wilson certification fractions; bootstrap gap bars | Nonmonotone certification can reflect the changed tolerance at the first budget. Different signal cases also use different fixed loadings. Keep current caveats; add a fixed-tolerance/loading experiment before a causal budget interpretation |
| Empirical 07: corrections | Two distinct loading/approximation bias mechanisms with visible catastrophic misses | Keep: materially informative adversarial construction. These corrections are conservative implemented bounds, not the general sharp fit |
| Empirical 08: power and pivots | Exact direct power reference and regular-signal/oracle comparisons; QQ axes readable | No normality result for the nonlinear midpoint is tested. Prefer mathematical $\tau\sqrt{r/p}$ in final label instead of code-like text |
| Empirical 09: runtime | Log time and traced-allocation scaling with explicit uncertainty conventions | Current caption properly says one SE and excludes native/input memory. Add tensor entry count for readers comparing mode dimensions |
| Empirical 10: intermediate caps | Shows the upper interval and ratio to an analytic lower bound across caps | Useful visualization of a remaining gap. The lower reference is a testing bound with constants, not an attained competitor; cap grid does not establish a sharp transition |

No new AI-generated figure was appropriate: these are scientific vector plots and PDF review artifacts. A final paper could use three main figures: the final theoretical rate comparison, representative weak/strong coverage and length, and computational gaps or correction failures. Additional suites belong in the supplement. An architecture diagram would add little to a Gaussian inference paper.

## Table audit

The integrated analytic assumption/comparison tables use explicit procedure and honesty classes, which prevents a common misreading of lower bounds. The selected-interval rate in the historical comparison is an attainable diagonal upper bound, not the final full-data optimum; the final row correctly points to the stronger theorem. When integrating, replace historical cross-references with the final rate notation and avoid making the reader jump through superseded bounds.

The empirical report's count, coverage, slope, finite-geometry, precision, failure and power tables have appropriate units and uncertainty. Coverage rounded to three decimals and short significant-digit length/SE displays are reasonable. Full machine-readable precision in CSV/JSON is appropriate for reproducibility and should not be copied verbatim into publication tables. Length/risk ratios must identify the analytic scale, not imply exact minimax constants. Highlighting does not appear to conceal inferior results; the regular comparator is often shorter than the cap-valid method in its favorable regime.

F01 requires correction in the underlying coverage rows and any derived paired-coverage/diagnostic tables. F09 requires an estimator-level identifier for losses repeated across confidence levels. All stored risk and paired-difference summaries were recomputed during review; no rounding of table displays was used to assess their numerical agreement. Original and follow-up calibration tables must remain separate, and solver counts must remain solves versus independent observations.

## Global notation audit

| Current collision / ambiguity | Where it matters | Suggested convention |
|---|---|---|
| $D$ as ambient dimension, degree or envelope coefficient | Integrated setup, low-degree theory, refinements | $D_{\rm amb}$, $d_{\rm poly}$ and $C_{\rm diag}$ |
| $q$ as $2/K$ and Gaussian critical value | Threshold geometry versus split projection | $q_K$ and $z_u$ |
| $\eta$ as approximation budget, pilot bound or total-variation constant | Robust section and both supplements | $\varepsilon_A$, $\eta_{\rm op}$ and $\varepsilon_{\rm TV}$ |
| $J$ as component count or overlap | CP/TT geometry and mixture proofs | $J_{\rm cap}$ and $H$ |
| Loading tensor and loading-dependent bound both indexed by $w$ | Weighted-rate envelopes | $L_w$ for the tensor; $\underline R(w)$ and $\overline R(w)$ for bounds |
| Supplied rank versus actual rank and effective minimum cap | Main theory, G1 and P1 | $\bar r_k$, $r_k(A)$ and $r_{\min}$; state when all supplied mode caps equal $r$ |
| “Tangent” for a larger product-subspace projector | A4/P1 versus XCH exact manifold tangent variance | Name the cap projection $\mathcal T_Q$ and separately define $P_{T_A}$ for the exact manifold tangent space |
| “Minimax optimizer” for existence fit versus executable search | C1/C2 and empirical comparisons | “Ideal residual fit,” “binary global search,” and “cap-valid split interval,” each with its own error/output contract |

No dimensionally invalid tensor operation was identified in the reviewed statements. Fixed-order constants and Kronecker projection dimensions are explicitly used in the proof audit. The task is consolidation of local notation, not correction of an established dimension mismatch.

## Integrity gate

The review preserves pre-existing research files, stores its own evidence and reproduction logs, and does not claim new experiments where it only recomputes saved data. Its simulated reviewers are explicitly labeled. Source-key and rendering checks do not certify citation accuracy or prove theorems. No fabricated real-data section or general efficient optimizer is introduced. Scientific submission remains blocked by the P0 revisions, rather than by a stylistic checkbox or an unsolicited approval rule.


\newpage

# Prioritized revision plan

This is a concrete review plan, not a claim that these revisions have been implemented. Paths are relative to `honest_tensor_functional_paper/`. Existing sources and saved outcomes are preserved in this review. F01–F10 are the ten classified findings in [report.md](report.md): three MAJOR, five MODERATE and two MINOR; no CRITICAL issue was established.

## Priority 0: must resolve before submission

| Problem / location | Recommended fix | Completion criterion and expected impact |
|---|---|---|
| F01. Target-sized coverage tolerance; `empirical_study/code/common.py:66`, `code/analyze_results.py:74`; S03_007 rows/raw results | Use a justified ULP-scale event comparison, Gaussian noise-centered checks where available, and an exact structural-boundary policy. Preserve old outputs and recompute on unchanged draws | Trial 41's 90% oracle/XCH-known miss is counted as a miss; true structural endpoints survive harmless rounding; all affected aggregates/plots/report diagnostics regenerated. Removes a documented empirical validity error |
| F03. Unsynchronized submission; `robust_adaptive_extension/paper/main.tex:39,57–63,406,454–458`, `norm_loading_section.tex:99`, both later supplement `theory/results.md` files, new empirical insert | Select and assemble one canonical manuscript/supplement; rewrite the abstract/contribution list/discussion around the final theorem scope, and integrate the actual study | One reading order, one final rate table, precise adaptation/computation status and no obsolete main gap figure. Prevents a referee assessing an earlier theorem/experiment package |

## Priority 1: strongly recommended

| Problem / location | Recommended fix | Completion criterion and expected impact |
|---|---|---|
| F02. Confounded ablation; `empirical_study/code/tensor_methods.py:92–103`, `simulation_design.md` Part B | Hold split, projector, quantile, selection and fallback fixed for an isolated bias contrast, or relabel current variant as multicomponent | Shared draws and paired uncertainty, with an explicit list of the sole changed component; removes unsupported causal attribution |
| F04. Midpoint risk; `high_dimensional_extension/code/methods.py:191–193`, empirical counterpart and report's estimator-failure section | Expose interval and scalar estimator separately; keep unconditional loss and sentinel diagnostics. If changing the estimator/fallback, state and prove its risk target | A user cannot mistake P1 for midpoint-risk optimality. Existing bad outcomes remain visible |
| F05. Signal and supplied norm budget coupled; `empirical_study/code/run_study.py:89`, caption 04 | Add a fixed-$M$ sensitivity sweep with all signals in the same class; label existing norm-comparable sweep | Onset-of-shortening statements distinguish signal effects from changes in the honesty class |
| F06. Regular comparator domain; `empirical_study/code/run_study.py:138`, comparator documentation, integrated `main.tex:83` | Add per-case flags for weak/zero, wrong rank and unverified regularity; cite/check XCH PCA Section 4 and relevant alignment/initializer conditions | Tables separate guarantee type from verified applicability; strong-signal comparisons stay fair |
| F07. Ideal versus implemented method; `gap_section.tex:42–76`, certified C1/C2, high-dimensional W1, empirical methods/captions 02/06/10 | Add a concise method table with input model, target class, computational status, stopping error and proved loss | No reader mistakes analytic envelopes or a local/global binary benchmark for an implemented general high-dimensional optimizer |
| Novelty focus; `main.tex` Introduction/Related work; `literature/novelty_matrix.md` | Explain the sharp tensor likelihood mechanism relative to sequence functionals, nonconvex functional recovery and finite convex unions; seek a specialist check of the central lower/upper proofs | Demonstrates the distinct mathematical contribution without asserting firstness or requiring all open extensions |

## Priority 2: material improvements

| Problem / location | Recommended fix | Completion criterion and expected impact |
|---|---|---|
| F07 solver sensitivity; `empirical_study/configs/cases.json`, S08; caption 06 | Fix the same loading and endpoint tolerance across budgets; add signal amplitude as a separate factor | Certification curves identify computation effects; retained unresolved endpoints and missing witnesses remain visible |
| F08 retained calibration results; `robust_adaptive_extension/paper/refinements.tex:139,184` | Add bounded whole-replicate corruption and independent chi-square noise-bound experiments using the actual proposed calibrations | Empirical robustness discussion maps to the refinements it claims to demonstrate |
| Pointwise precision; S03/S04 and P1 proof | Prioritize more replications near the practical transition and largest dimension; compare to exact/finite-geometry references and show cap rounding | Better coverage precision and a clearer finite-grid explanation; do not label slope agreement as a proof |
| Real-data requirement; `empirical_study/real_data/README.md` | Develop an application only after the sampling unit, target, noise/bound calibration and dependence model are justified | A genuine application can support a methodological framing; no convenient tensor-shaped substitute |
| Complexity reporting; S11/runtime tables | Add explicit input entries/bytes and distinguish traced allocations, native workspace and input-access cost | Makes polynomial complexity interpretable as dimensions/order change |

## Priority 3: polish

| Problem / location | Recommended fix | Completion criterion and expected impact |
|---|---|---|
| F09. Repeated scalar loss across levels; `empirical_study/code/common.py:81–96`, flattened summary exports | Add estimator identity and `estimator_alpha`; specify whether point estimate depends on interval level | Prevents 90/99% rows being read as those intervals' midpoint risks |
| F10. Notation collisions; active TeX and both supplement Markdown sources | Adopt the notation table in the assumption/presentation audit | Consistent ambient dimension, polynomial degree, noise envelope, approximation and overlap notation |
| Chronological clutter; main Sections 5–7 and preliminary lower-bound appendix | Remove or move superseded gap narrative/harmonic proof; combine routine corollaries and repeated limitations | A shorter final argument without lost substantive evidence |
| Figure hierarchy; initial theoretical comparison and duplicated rate examples | Show final rate regimes first; use only one weak-boundary illustration and one computational/failure figure in main text | Reader sees the central scientific result and its practical limit promptly |

## Ranked missing theory

| Rank | Missing result | Impact / feasibility | Importance for publication |
|---|---|---|---|
| 1 | Efficient general-dimensional fixed-cap weak-signal optimizer with a global statistical/numerical error contract, or an appropriately scoped stronger obstruction | Very high impact; low/uncertain feasibility. Low-degree results alone do not settle all polynomial algorithms | Essential only for a general efficient-method claim; not required for a clearly statistical minimax theorem paper |
| 2 | Sharp intermediate growing-cap rates with explicit uniform cap dependence | High impact; moderate/uncertain feasibility via stronger upper geometry and matched mixtures | Would turn boundary results into a convincing rank phase diagram; current partial characterization must remain explicit |
| 3 | Arbitrary-loading local/global modulus or matching profile envelope beyond small budgets and fixed positive decay | High impact; low/uncertain feasibility, especially nonorthogonal loadings | Necessary for a general-loading optimality claim; a focused flat-loading paper can proceed without it |
| 4 | Pointwise expected-length characterization with weaker signal thresholds, unsaturated/rotated geometry and TT structure | High impact; a weaker sufficient threshold may be more feasible than a complete characterization | Needed for broad optimal adaptation claims; current P1 is a useful restricted theorem |
| 5 | A practical scalar estimator paired with the cap-valid interval and a proved unconditional risk bound | Moderate/high practical impact; potentially feasible but requires control on failure events | Necessary before claiming a jointly optimal interval/estimator from the current midpoint API |
| 6 | Unknown directional scale, dependent replicates and selected loading/allowance calibration | High application value; feasibility depends on a concrete sampling model | Pursue after selecting a defensible application, not as unsupported generic robustness language |

## Ranked missing experiments

1. Corrected boundary-event audit on the existing draws (P0; mandatory), including rescaling sensitivity and the exact regenerated miss.
2. Controlled bias/fallback/confidence-allocation ablations (P1), with the same paired observations.
3. Fixed-$M$ signal sweep and case-level comparator eligibility (P1).
4. Fixed-loading, fixed-tolerance optimizer budget curves and complete unresolved-gap reporting (P2).
5. More precise pointwise transition checks and explicit unconditional midpoint-loss tails (P2); preserve all rare events.
6. Actual independent-variance and bounded-row-corruption calibration experiments if retained as practical claims (P2).
7. Justified real-data repeated-tensor analysis if targeting a method-led venue (conditional P2). An unrelated LLM benchmark is not an adequate substitute.

## Suggested final paper organization

Use one setup and notation table; one central all-budget flat-loading theorem with the cubic/higher-order mechanism; a short diagonal/affine/enlarged-honesty comparison; then a section delimiting computable regimes and adaptation. Keep only the most substantive robustness/loading extensions in the main text. Put complete proofs, numerical contracts, additional regime consequences and full empirical tables in a coherent supplement. Archive superseded development steps. A full phase diagram or algorithm for every open regime is not a required P0 action.


\newpage

# Proposed abstract for a focused integrated revision

This is proposed wording for a future synchronized manuscript. It has not been inserted into the research sources.

We study honest confidence intervals for prescribed linear functionals of a Gaussian tensor mean under supplied Tucker or tensor-train rank and Frobenius bounds. The parameter classes include zero and arbitrarily weak nonzero components. For flat orthogonal loadings and fixed positive rank caps, we characterize minimax expected interval length, both at zero and in the worst case, uniformly over positive norm and noise budgets; minimax squared error has the square of this rate. A full-data residual construction and a sparse harmonic mixture identify a logarithmic distinction between third-order and higher-order tensors. The general optimal construction is statistical and can require exponential computation. We also identify efficiently attained large-cap rates, sharp regimes for nonuniform loadings, and contrasting possibilities for fixed-cap and growing-cap adaptation. A computable interval remains honest without separation and attains a pointwise rate at sufficiently strong saturated Tucker means. Simulations evaluate available procedures, a regular-signal comparator and a binary global-search benchmark, documenting conservative intervals, unresolved optimization gaps and a distinction between interval length and midpoint risk. General efficient weak-signal minimax computation, arbitrary loading profiles, intermediate growing caps and complete pointwise adaptation remain open.


\newpage

# Complete guideline coverage

The supplied attachment contains 50 numbered items, including the final deliverable list. All are mapped below. “Addressed” means reviewed, not that the underlying manuscript requirement is satisfied. Real-data/LLM execution is absent and explicitly assessed as such.

| Item | Guideline | Review artifact / evidence |
|---|---|---|
| 1 | First understand the paper independently | [Section 1: reconstruction, experiment, target and procedure](report.md) |
| 2 | Give a one-paragraph referee summary | [Section 1: one-paragraph referee summary](report.md) |
| 3 | Evaluate the statistical contribution | [Section 2: statistical contribution and significance](report.md) |
| 4 | Review the mathematical formulation | [Formulation and notation; report Section 1](assumption_audit.md) |
| 5 | Review every assumption | [R01–R20 assumption audit with use, standardness, restrictiveness and weakening](assumption_audit.md) |
| 6 | Audit every theorem | [59 distinct results; statement/proof/novelty/strength/issues and source lines](theorem_audit.md) |
| 7 | Check theorem strength | [Individual strength judgments; report Section 3 rates](theorem_audit.md) |
| 8 | Check minimax and optimality claims | [Section 3: matched classes, losses, budgets, logs and constants](report.md) |
| 9 | Independently audit the proofs | [Section 4 dependency chains; individual proof reconstructions in theorem audit](report.md) |
| 10 | Look specifically for proof failures | [Section 4 dependence, nets, doubled ranks, conditioning, measurability and tail checks](report.md) |
| 11 | Stress-test the theory | [Section 4 explicit counterexamples and boundary stress tests; new proof probes](report.md) |
| 12 | Check identifiability | [Section 1: mean/functional identifiable, factors need not be](report.md) |
| 13 | Check computational feasibility | [F07 and Section 6: ideal estimator, binary search, polynomial regimes and input size](report.md) |
| 14 | Review tuning-parameter theory | [Tuning audit with theoretical/empirical choices and scope](assumption_audit.md) |
| 15 | Review the simulation design | [All suites S01–S13, including separate runtime and follow-ups](simulation_and_claims.md) |
| 16 | Check rate validation | [Sections 3 and 6: rate slopes, logs, finite-grid curvature and cap rounding](report.md) |
| 17 | Review simulation fairness | [Pairing, exact baselines, oracles, comparator eligibility, F02/F05/F06](simulation_and_claims.md) |
| 18 | Check whether uncertainty is reported | [Section 6: Wilson intervals, MCSE, paired differences and simultaneous screening](report.md) |
| 19 | Review ablation experiments | [F02: three-component ablation and concrete controlled replacement](report.md) |
| 20 | Review the real-data analysis | [Section 7: no executed real-data analysis; existing applicability audit reviewed](report.md) |
| 21 | For AI/LLM applications, audit experimental independence | [Section 7: no LLM observations used; future sampling/dependence requirements](report.md) |
| 22 | Check whether empirical results support the claims | [Claim-to-evidence classifications and suite conclusions](simulation_and_claims.md) |
| 23 | Review figures | [All 14 active manuscript/current-study figures](presentation_audit.md) |
| 24 | Review tables | [Analytic and empirical tables, precision, uncertainty and comparison classes](presentation_audit.md) |
| 25 | Review the Abstract | [Proposed integrated abstract; report Section 8 critique](proposed_abstract.md) |
| 26 | Review the Introduction | [Section 8 and revision plan: introduction focus and contribution hierarchy](report.md) |
| 27 | Review the Related Work section | [Section 2: focused primary-source novelty comparison, explicit citation-audit boundary](report.md) |
| 28 | Review the Methods section | [Tuning and computation; report Sections 1,5,8 specify missing integrated methods](assumption_audit.md) |
| 29 | Review the Theory section as exposition | [Sections 3,4,8: main theorem hierarchy and explanatory proof structure](report.md) |
| 30 | Review the Discussion | [Sections 5,7,8: limitations and stale discussion wording](report.md) |
| 31 | Review the Appendix | [Proof-by-proof audit; presentation/revision plan reorganizes appendix dependencies](theorem_audit.md) |
| 32 | Check internal consistency | [F03, Section 3 and claims audit: fixed/growing caps, noise laws, pointwise/risk scope](report.md) |
| 33 | Check notation globally | [Global notation audit with proposed unifying symbols](presentation_audit.md) |
| 34 | Evaluate reproducibility | [Section 6: new checks versus saved evidence; isolated byte-identical rebuild](report.md) |
| 35 | Evaluate robustness of conclusions | [Fairness and sensitivity; changed-seed, parameter and noise conclusions delimited](simulation_and_claims.md) |
| 36 | Separate fatal issues from fixable issues | [Three MAJOR, five MODERATE, two MINOR; no CRITICAL established](revision_plan.md) |
| 37 | Produce a skeptical referee report | [Summary, substantive strengths, ranked concerns, author questions, revisions and recommendation](report.md) |
| 38 | Simulate multiple reviewers | [Section 9: three explicitly simulated referee perspectives](report.md) |
| 39 | Give an editor-style assessment | [Section 10: associate-editor assessment and Major revision recommendation](report.md) |
| 40 | Assess target-journal fit | [Section 10: six venue fit scores from 1 to 5 and obstacles](report.md) |
| 41 | Identify the single strongest contribution | [Section 2: single strongest contribution sentence](report.md) |
| 42 | Identify the single biggest weakness | [Section 10: single biggest weakness and exact repair](report.md) |
| 43 | Determine whether any claims should be weakened | [Current-claim/evidence/too-strong/recommended-wording table](simulation_and_claims.md) |
| 44 | Identify missing theoretical results | [Six ranked missing-theory recommendations with impact, feasibility and publication relevance](revision_plan.md) |
| 45 | Identify missing experiments | [Seven ranked missing experiments](revision_plan.md) |
| 46 | Identify unnecessary material | [Cuts, moves and suggested final organization; presentation figure audit](revision_plan.md) |
| 47 | Produce a prioritized revision plan | [P0–P3 action tables with exact source locations and completion criteria](revision_plan.md) |
| 48 | Final scientific checklist | [Section 12: final scientific checklist with pending/not-applicable distinctions](report.md) |
| 49 | Final verdict | [C — Major revision required; viable core and concrete remaining corrections](report.md) |
| 50 | Final deliverables | [Deliverable index; complete_review.pdf includes all main review and audit documents](README.md) |
