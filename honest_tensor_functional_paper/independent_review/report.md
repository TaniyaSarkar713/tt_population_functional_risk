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
