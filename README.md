# Tensor Functional Risk and Honest Inference

This repository contains two connected research directions: population functional risk for tensor-train (TT) compression of conditional generators, and honest confidence intervals for scalar functionals of noisy low-rank tensors. The original compression study and successive inference drafts are preserved separately.

**Status updated: 2026-09-15.** The latest research is in `honest_tensor_functional_paper/minimax_frontier/`. M1 gives an efficient full-model minimax interval for every loading, budget and rank cap when **one unfolding is constrained**. L3 proves the exact rate up to constants for **every orthogonal loading profile in order four and higher**, under fixed caps. P5 gives optimal coordinate-wise interval lengths at **unknown rank-one axis signals**. M2 proves a limitation of deterministic affine intervals. This stage newly ran **320,000 Monte Carlo data sets in 160 configurations**, **20,489 finite checks**, and 385 analytic calculations, with full proofs and reproducible code. General simultaneous-cap minimax computation, general cubic/nonorthogonal loading and intermediate-cap rates, and complete pointwise theory remain open. The expanded program retains internal verdict **C**. The preceding 122-subject EEG analysis and all earlier results are preserved; its finite-sample uncertainty remains wide, with no demonstrated tensor precision gain. The accumulated research stages and this status update are included together in the requested repository commit.

## Start here

- **Latest theory and computation:** [research report](honest_tensor_functional_paper/minimax_frontier/paper/report.pdf), [complete proofs](honest_tensor_functional_paper/minimax_frontier/paper/technical_supplement.pdf), [code and reproduction guide](honest_tensor_functional_paper/minimax_frontier/README.md), and [continued issue registry](honest_tensor_functional_paper/minimax_frontier/audit/issue_registry.csv).

- **Preserved preceding science and application:** [research and real-data report](honest_tensor_functional_paper/scientific_extension/paper/report.pdf), [complete new proofs](honest_tensor_functional_paper/scientific_extension/paper/technical_supplement.pdf), [methods and reproduction guide](honest_tensor_functional_paper/scientific_extension/README.md), and [continued review registry](honest_tensor_functional_paper/scientific_extension/audit/issue_registry.csv).

- **Preserved focused submission:** [revised main paper](honest_tensor_functional_paper/review_revision/paper/main.pdf), [complete proof supplement](honest_tensor_functional_paper/review_revision/paper/technical_supplement.pdf), and [empirical supplement](honest_tensor_functional_paper/review_revision/empirical_report.pdf).
- **Revision record:** [scientific summary](honest_tensor_functional_paper/review_revision/revision_summary.md), [responses to all concerns](honest_tensor_functional_paper/review_revision/response_to_review.md), [second adversarial review](honest_tensor_functional_paper/review_revision/second_review.md), [reproduction/file guide](honest_tensor_functional_paper/review_revision/README.md), and [current requirements](requirements.md).
- [Complete scientific review and all audits](honest_tensor_functional_paper/independent_review/complete_review.pdf), [main referee report](honest_tensor_functional_paper/independent_review/report.md), [review evidence/code guide](honest_tensor_functional_paper/independent_review/README.md), and [P0–P3 revision plan](honest_tensor_functional_paper/independent_review/revision_plan.md).
- [Beginner-friendly mathematical summary](summary.md).
- [Preserved pre-review simulation report](honest_tensor_functional_paper/empirical_study/report.pdf), [readable report](honest_tensor_functional_paper/empirical_study/report.md), [study/code guide](honest_tensor_functional_paper/empirical_study/README.md), and [current requirements](requirements.md).
- [Closest reference papers and comparison guide](references/README.md), with eight downloaded PDFs and [BibTeX](references/references.bib).
- [Preserved pre-review theoretical supplement](honest_tensor_functional_paper/high_dimensional_extension/paper/main.pdf), [progress report](honest_tensor_functional_paper/high_dimensional_extension/progress_report.md), [complete derivations](honest_tensor_functional_paper/high_dimensional_extension/theory/results.md), and [audit/remaining problems](honest_tensor_functional_paper/high_dimensional_extension/theory/audit.md).
- [Preserved global optimizer benchmark](honest_tensor_functional_paper/certified_weak_signal/README.md), including its explicit binary rank-one scope and optimization gaps.
- [Preceding full inference manuscript](honest_tensor_functional_paper/robust_adaptive_extension/paper/main.pdf) and [LaTeX source](honest_tensor_functional_paper/robust_adaptive_extension/paper/main.tex); read the new supplement for current computation and adaptation status.
- [Previous sharp-rate stage](honest_tensor_functional_paper/gap_development/README.md), including the limited scan prototype and computational obstruction.
- [Original compression manuscript](paper/main.pdf), [source](paper/main.tex), and [scope decisions](notes/theory_decisions.md).

## Current project status

| Area | Current status | Main limitation or remaining work |
|---|---|---|
| Preserved scientific revision | 13 concerns resolved, one partial, five open; current main/proof/empirical PDFs; verdict B for focused theory paper | External priority/significance and venue preparation remain; four broad theory problems remain open |
| Preserved scientific review | 59 result audits, 20 assumption families and all 50 review items; original verdict C | Review preserved; its P0/P1 remedies are implemented in review_revision; neither stage is external peer review or formal verification |
| Latest scalar and pointwise methods | P5 learns its rank-one axis anchor and attains the optimal coordinate-distance hierarchy; P2/P3/P4 remain preserved | Complete coordinate-axis expected-length theory in a sufficient localization regime; arbitrary points/loadings and higher ranks remain open |
| Revision experiments | 87,200 new datasets, 55 configurations, 600 solver calls; fixed-M and isolated ablations; row/scale calibration; larger pointwise runs | 593 optimizer calls remain unresolved; strong-signal and numerical scope explicitly limited |
| Original TT compression theory | Complete working draft of regular-stratum oracle and modelwise lower bounds; saved synthetic experiments | Geometry, functional identifiability, likelihood regularity, and optimization conditions remain explicit assumptions; no unrestricted-transformer theorem |
| Honest tensor-functional intervals | Baseline weak-signal cap-uniform theory plus robust-noise, approximate-rank, and certified arbitrary-loading extensions | Known norm/noise bounds and stated dependence/replication assumptions remain necessary |
| Latest full-data statistical theory | L3 matches the Abel proxy for every orthogonal profile and budget, K >= 4, fixed positive Tucker/TT caps | Upper prefix fits remain ideal; arbitrary cubic/nonorthogonal profiles remain open |
| Loading geometry | L3 closes the higher-order critical-profile gap; M1 handles every loading on its full one-unfolding class | Additional rank constraints change the parameter space; exact general multi-cap loading rates remain open |
| Computation | M1 uses a known-loading SVD and scalar convex solve; M2 proves an affine constant-radius obstruction; binary exponential benchmark preserved | General efficient nonlinear minimax computation under simultaneous fixed caps remains open |
| Rank adaptation | P5 gives unknown-axis coordinate adaptation; M1 covers every intermediate cap on one unfolding; prior positive/negative growing-cap results preserved | General simultaneous intermediate caps, arbitrary pointwise geometry and optimal thresholds remain open |
| Relaxed observations/ranks | Same upper rates under joint sub-Gaussian tails; family-wise minimax finite-variance replicate rates with sufficient replication; sharp approximate-rank length | Marginal-only bounds are insufficient; per-law Gaussian lower transfers fail; removing all rank restrictions changes the rate to $\min(M,\tau)$ |
| New experiments and application | 320,000 new MC datasets, 160 configurations, 20,489 finite checks, 385 analytic calculations; 2,097,152-entry computation timed | Spectral gains modest; rank-two violation fails; prior 122-subject EEG application preserved without rerun |
| Earlier empirical work | Preserved synthetic interval simulations: 175 configurations, 2,000 replications each; later small scan benchmarks | Saved historical evidence; not pooled into the new study |
| Preceding theory-stage experiments | Saved 7,200 growing-cap trials, 1,900 pointwise trials through $64^3$, 96 loading calculations, eight adaptation comparisons and 224 finite checks | The earlier pointwise tests emphasize deliberately very strong signals; largest-dimension uncertainty is wide |
| Saved pre-review simulation study | 1,084,640 saved Monte Carlo data sets; 318 stochastic and 84 analytic-only configurations; 10 vector figures; paired published-method comparison, uncertainty, violations, power and numerical audits | General block/residual fits remain absent; finite-grid pointwise slopes differ from limiting references; no real-data execution in that preserved stage |
| Preserved pre-review empirical limits | At 95% confidence, 94/240 binary solver cases miss endpoint tolerance at 3,000 nodes; empty-intersection `{0}` replacements can make pointwise midpoint MSE enormous | Outer intervals and unresolved gaps are retained; the new R1 companion repairs scalar loss, while P1 remains a length theorem |
| Closest literature | Eight version-pinned PDFs downloaded, checked, and indexed in `references/`; primary-source comparison and updated publication metadata | Focused reference selection, not an exhaustive priority or independent proof review |
| Repository | Standalone private GitHub repository on `main`, with project summary and persistent README-maintenance instructions | Root README must be refreshed with status and file organization before every commit/push |

“Proved” in the internal ledgers means a complete supplied derivation, supported by finite checks where recorded. It does not mean independent peer review or machine-verified mathematics. Earlier drafts retain historical statements of gaps that later stages address; use minimax_frontier for the latest research, scientific_extension for the preserved application, review_revision for the preserved unified submission, and requirements.md for remaining work.

## Main mathematical results

### Original compression study

The main experiment uses finitely many independent stochastic teacher responses. For a coded collection of rank-separated TT models, the oracle bound has the schematic form

$$
\mathbb E\,\mathcal D_w(\widehat W,W^0)
\lesssim
\inf_{\lambda}
\left\{
A_w^2(\lambda)
+\frac{d_\lambda+\log H_\lambda+\log(1/\pi_\lambda)}{n}
\right\}.
$$

Here $A_w^2$ is approximation error in teacher-relative conditional KL, $d_\lambda$ is the gauge-adjusted TT dimension, $H_\lambda$ counts charts, and $\pi_\lambda$ codes the model. The full theorem includes regularity factors, sample-split terms, and optimization errors. Matching local modelwise lower bounds require the stated separation and information conditions. Exact teacher probabilities and white-box teacher weights are different experiments; a universal positive $d/n$ lower bound does not apply to them.

### Established flat-loading results and preceding extensions

Observe $Z=A+\tau G$ with independent standard Gaussian entries in $G$, known $\tau$, and supplied Frobenius/rank bounds. The principal target is

$$
\psi(A)=p^{-1/2}\sum_{i=1}^p A_{i,\ldots,i}.
$$

For fixed $K\ge3$, fixed positive Tucker or TT rank caps, and fixed confidence level $0<\alpha<1/4$, the latest supplied proofs match the full-data minimax expected interval length both at zero and in the worst case for every $M,\tau>0$. Put $\ell_p=\log(ep)$ and $x=M/(\tau\sqrt{\ell_p})$. Then

$$
\mathcal L_0(\Theta)\asymp\mathcal L_{\max}(\Theta)
\asymp\frac{\tau\sqrt{\ell_p}}{\sqrt p}
\begin{cases}
\min\{x,1+\log_+x,\ell_p\},&K=3,\\
\min(x,1),&K\ge4.
\end{cases}
$$

Here $\log_+x=\max(0,\log x)$. The constants are uniform in $p,M,\tau$. The corresponding squared-error minimax rates are their squares, attained statistically by an approximate residual fit with controlled Gaussian excess tails. For flat prescribed orthogonal loadings on $m$ terms, replace $p$ by $m$, even in larger unequal ambient dimensions. For $M=\tau\sqrt p$, this recovers the previous cubic rate $\tau(\log p)^{3/2}/\sqrt p$ and higher-order rate $\tau\sqrt{\log p/p}$.

The general-dimensional confidence-set projection and residual fit remain existence constructions. The preserved `certified_weak_signal/` supplement implements their full finite-net criterion on the continuous binary rank-one ball, with global bounds and explicit optimization gaps. It does not establish polynomial complexity. Earlier work proves the same upper rates under a joint sub-Gaussian noise proxy and matching family-wise rates with independent finite-variance replicates, a known covariance upper bound, and enough replicates. For a supplied Frobenius approximation allowance $\eta$, sharp Gaussian interval length is $\min\{\tau,\mathfrak r_K+\eta\}$.

For arbitrary known $L$, the previous supplement proves length $\asymp M\rho(L)$ and squared risk $\asymp M^2\rho(L)^2$ when $M\le\tau$, where $\rho(L)$ is its maximum absolute contraction with a unit product tensor. The latest supplement extends all-budget sharp rates to orthogonal weights satisfying $|w_i|\le C|w_1|i^{-\beta}$ for fixed $\beta>0$: length is $\asymp |w_1|\min(M,\tau)$ and risk has its square. Small nonorthogonal perturbations are included. The upper construction uses ideal block fits; L3 below now resolves every orthogonal profile in order four and higher, while general cubic/nonorthogonal profiles remain open. A new full-data low-degree argument gives a restricted computational separation for $0<\beta<1/K$.

The earlier rank-free SVD interval required spectral separation. The cap-valid tangent interval retains supplied cap dimensions, bounds unresolved subspace errors conservatively, and remains honest at zero and under weak signals. Correctly calibrated artificial Gaussian splitting implements it from one observation. It can shorten at strong signals but has no weak-signal minimax guarantee. Separately, the existing ideal outer interval already attains the minimax rate over all smaller positive fixed-cap classes without separation, since those classes share a rank-one lower bound. General rank-dependent factors and pointwise adaptation remain separate questions; the newest positive and negative results below address specific regimes.

The latest growing-cap result is sharp uniformly over all budgets and growing caps when the smallest supplied unfolding cap $r\gtrsim\sqrt p$:

$$
\mathcal L_0\asymp\mathcal L_{\max}\asymp\min\{M\sqrt{r/p},\tau\}.
$$

Structural/direct interval selection attains this rate in polynomial time for both Tucker and TT classes. At $M=\tau\sqrt p$ the rate is $\tau$, which rules out simultaneous oracle-rate adaptation to positive fixed-cap classes. A separate pointwise theorem gives rate $\tau\sqrt{r/p}$ at strong diagonal Tucker means saturating their supplied caps, under the same unseparated outer honesty requirement. Their support and amplitudes are unknown to the algorithm. The implemented interval uses a pilot failure budget shrinking as $r/p$ and economy SVDs; its sufficient signal threshold is conservative, not claimed optimal.

## Latest scientific results (2026-09-15)

For a tensor model with one constrained unfolding, let its loading singular values be sigma and its rank cap r. M1 proves that the minimax interval-length rate for M > tau is

$$T_r=\max_{b\ge0,\,\|b\|_1\le M\sqrt r,\,\|b\|_2\le\tau}\sigma^T b
=\min_{t\ge0}\{M\sqrt r\,t+\tau\|(\sigma-t)_+\|_2\}.$$

For M <= tau the rate is M times the Euclidean norm of the largest r loading singular values. The squared-error rate is its square. Soft thresholding the known loading gives an efficient attaining interval and a separate scalar estimate. On flat orthogonal loadings this yields min(M sqrt(r/p), tau) for every intermediate cap in the **one-unfolding full tensor model**. Its lower bound does not extend automatically to additional simultaneously restrictive caps.

For every decreasing absolute orthogonal loading profile and K >= 4, L3 now proves

$$\mathcal L_0\asymp\mathcal L_{\max}\asymp\sum_{s=1}^p w_s(F_s-F_{s-1}),\qquad F_s=\min(M,\tau\sqrt{\log(es)}),\quad F_0=0.$$

The new multiscale rank-one lower bound matches the earlier ideal Abel-prefix upper bound, including critical and dimension-dependent profiles. Computing this rate proxy does not compute its ideal attaining interval. M2 separately shows why deterministic affine constant-radius intervals cannot attain the diffuse fixed-cap rate.

P5 constructs an O(D) honest interval on the rank-one ball that learns its anchor from an independent artificial pilot. At an unknown axis mean a E_J and target coordinate at Hamming distance d, its optimal expected-length rate is tau for d = 0 or 1, and tau^d / |a|^(d-1) for d >= 2, when |a| exceeds a sufficient constant times tau sqrt(log(eD)). Honesty needs no separation; the optimality condition is sufficient, not claimed necessary. General points, loadings and higher ranks remain open.

## Preserved scientific results (2026-09-14)

For decreasing absolute orthogonal weights, put $F_s=\sqrt{s}\,\mathfrak r_K(s,M,\tau)$. The new upper/lower proxies satisfy

$$B=\max_s w_sF_s\le A=\sum_s(w_s-w_{s+1})F_s\le B[1+\log(F_p/F_1)]\le B[1+\nu_K\log\log(ep)].$$

Minimax length lies between fixed multiples of B and A, and minimax squared risk between fixed multiples of their squares. The constants depend on fixed caps, order and confidence. For $w_i=c[\log(ei)]^{-\beta}$, the full new proof gives matching all-budget formulas away from the stated critical exponents. Computing these proxies does not implement their ideal prefix fits.

The new P2 scalar guards the **pre-intersection** candidate center, retaining uniform noise-scale risk and shrinking risk at favorable points. P3 gives arbitrary-core Tucker and single-cut TT pointwise length optimality and local two-point risk lower bounds under explicit strong-signal and alignment conditions. P4 handles a prespecified rank-one minor with zero tangent loading, attaining expected length $\asymp\tau^2/a$ at an axis mean of strength a. D2's sharp all-cap diagonal method requires exact diagonal means; its deliberate full-model misuse has zero coverage in the new negative control.

The EEG application uses 122 subjects, not 10,962 retained trials, as inferential units. Its fixed-stratum bounded target and independent bias calibration avoid asserting exact population rank or Gaussian entry noise. The primary 95% finite-sample interval is [-77.920, 82.364] microvolts and the calibrated projection interval spans [-200, 200]. This executed application is informative about the limits of certified projection inference; it does not validate the original Gaussian minimax assumptions.

## Closest references

- **Mathematical precursor:** Collier, Comminges, and Tsybakov (2017), [*Minimax estimation of linear and quadratic functionals on sparsity classes*](https://arxiv.org/abs/1502.00665). It provides the classical sequence-functional benchmark behind the diagonal reduction.
- **Direct tensor-functional comparison:** Xu, Chen, and Han (2025), [*Statistical Inference for Low-Rank Tensor Models*](https://arxiv.org/abs/2501.16223). Its regular-signal conditions and broader loadings differ from our cap-uniform restricted target.
- **Original compression comparison:** Michel and Nouy (2022), [*Learning with tree tensor networks: complexity estimates and model selection*](https://arxiv.org/abs/2007.01165).

The [reference guide](references/README.md) also covers both Cai–Low papers, Agterberg–Zhang, Choo–d'Orsi, and Fu–Sohn. It distinguishes publication years from the downloaded preprint versions and explains the remaining mathematical differences.

## File organization

```text
.
├── README.md                         Current status, reading order, and file map
├── AGENTS.md                         Standing README-update rule
├── summary.md                        Beginner-friendly mathematical explanation
├── requirements.md                   Current open theory and application ledger
├── references/
│   ├── README.md                     Closest-paper comparisons and reading guide
│   ├── references.bib                Eight bibliographic entries
│   ├── download_manifest.json        Sources, versions, timestamps, hashes, and checks
│   └── closest_papers/               Eight downloaded reference PDFs
├── paper/                            Original TT compression manuscript and proofs
├── notes/                            Original scope, novelty, and review records
├── code/                             Original synthetic experiments and smoke tests
├── results/                          Original saved numerical outputs
├── figures/                          Original generated figures
├── honest_tensor_functional_inference/
│                                     Earlier complete inference research note
└── honest_tensor_functional_paper/
    ├── paper/                        Complete-paper revision before theory review
    ├── theory/                       Theory and historical open-question ledgers
    ├── simulations/                  Interval code, design, and saved results
    ├── literature/                   Earlier literature comparisons and PDF library
    ├── notes/                        Publication checkpoints and revision records
    ├── real_data/                    Application status and unmet model requirements
    ├── theory_review/                Preserved intermediate review and revised paper
    ├── gap_development/              Preserved sharp-rate and computational stage
    │   ├── paper/                    Earlier full-data manuscript and proofs
    │   ├── theory/                   Earlier derivations and audit
    │   ├── code/                     Checks, limited scan prototype, and rebuild
    │   ├── results/                  Saved checks and scan benchmarks
    │   └── literature/               Computational literature update
    ├── norm_loading_extension/       Preserved all-budget and flat-loading stage
    ├── robust_adaptive_extension/    Preserved robustness/adaptation full manuscript
    │   ├── paper/, theory/           Full manuscript, proofs, earlier audit
    │   ├── code/, results/, figures/ Saved code and 76,600 historical trials
    │   └── literature/               Primary-source positioning
    ├── certified_weak_signal/        Preserved binary optimizer and 2026-09-11 proofs
    │   ├── code/, theory/            Exponential benchmark and earlier cap-valid interval
    │   └── paper/, results/          Preserved supplement and 8,320 saved trials
    ├── high_dimensional_extension/   Preserved theoretical supplement (2026-09-12)
    │   ├── README.md                 Scope and reproduction
    │   ├── progress_report.md/.pdf   Matched regimes, saved coverage, runtimes and limits
    │   ├── theory/                   Six numbered results with derivations and audit
    │   ├── paper/main.tex/.pdf       Typeset standalone supplement
    │   ├── code/                     Polynomial intervals, envelopes, checks and builds
    │   ├── results/                  9,100 preserved trials, calculations, source hashes
    │   ├── literature/               Primary-source positioning
    │   └── baseline_manifest.json    Hashes preserving 23 previous-stage files
    ├── empirical_study/              Preserved empirical stage (2026-09-13)
    │   ├── README.md, report.md/.pdf Scope, observed results and reproduction
    │   ├── configs/, code/           Frozen registries, simulation and checked methods
    │   ├── results/, tables/         Per-trial arrays, 3,444 summaries and numerical audits
    │   ├── figures/                  Ten PDF/SVG figures, captions and visual audit
    │   ├── manuscript/               Observed simulation section and application limitation
    │   ├── real_data/                Pending dataset/model applicability audit
    │   └── logs/                     Source hashes, checks, deviations and preservation
    ├── minimax_frontier/              LATEST research (2026-09-15)
    │   ├── theory/, code/             M1/M2/L3/P5 proofs, efficient APIs and finite checks
    │   ├── results/                   320,000 new MC draws; profiles, caps and timings
    │   ├── figures/, paper/           Four vector figures, report and full proof PDF
    │   └── audit/, review_notes.md    Continued issues, numerical and preservation audits
    ├── scientific_extension/          Preserved research/application (2026-09-14)
    │   ├── theory/                    AB1/AB2/P2/P3/P4/D2/B1 proofs and ledger
    │   ├── code/                      General methods, checks, MC and EEG pipeline
    │   ├── results/                   109,000 new MC draws; loading calculations
    │   ├── real_data/                 Locked protocol, subject tensors, provenance
    │   ├── figures/                   Five PDF/SVG figures and previews
    │   ├── paper/                     Research report and new technical supplement
    │   └── audit/                     Continued review, checks and baseline hashes
    ├── review_revision/              PRESERVED scientific revision (2026-09-13)
    │   ├── README.md                 Reading order, status and reproduction
    │   ├── paper/, theory/           Focused main paper; full 60-result proof/status record
    │   ├── empirical_report.md/.pdf  Corrected saved evidence plus 87,200 new datasets
    │   ├── response_to_review.md     Complete individual responses and issue matrix
    │   ├── revision_summary.md      Scientific diff, residual limits and journal assessment
    │   ├── second_review.md         Adversarial re-review and readiness checkpoint
    │   ├── code/, configs/          Revised scalar API, frozen new experiments and rebuilds
    │   ├── results/, tables/        New raw/derived draws, all failures and paired summaries
    │   ├── figures/                 Six new PDF/SVG figures with analytic/empirical labels
    │   ├── empirical/               Reevaluated saved draws, corrected tables, ten figures
    │   └── logs/                    Source hashes, fresh checks and preservation audit
    └── independent_review/           Preserved complete scientific review (2026-09-13)
        ├── report.md/.pdf            Main referee report, findings and verdict
        ├── complete_review.md/.pdf   Report plus every detailed audit and revision plan
        ├── *_audit.md, revision_plan.md, simulation_and_claims.md
        │                             Theory, assumptions, experiments, presentation and actions
        ├── code/, results/           New review checks and isolated reproduction evidence
        ├── tables/                   59-result inventory/audit, all 50 guideline items
        └── logs/                     Initial 1,469-file hashes, environment and build logs
```

Each research-stage directory has its own README and supporting files. Historical literature copies are preserved; `references/` is the curated entry point for the closest papers.

## Reproduction and verification

The latest minimax_frontier stage newly ran **320,000 full-observation MC data sets**, **20,489 finite checks**, and **385 analytic configurations**. Its [guide](honest_tensor_functional_paper/minimax_frontier/README.md) documents methods and exact scopes; its [validation](honest_tensor_functional_paper/minimax_frontier/audit/validation.json) checks saved outputs, current PDFs, source hashes, and the 2,902-file pre-stage baseline. The four-ULP coverage convention and all strict differences are retained. Both ten-page PDFs pass layout checks, and 6,205 artifact checks also pass in an isolated copy of the staged files, with no missing scientific files. From the repository root:

```bash
bash honest_tensor_functional_paper/minimax_frontier/reproduce.sh
# Add --rerun-mc to regenerate all 160 Monte Carlo configurations.
```

The preceding scientific_extension stage ran 109,000 MC data sets, 504 analytic configurations and 40,553 finite checks, and processed the full public EEG archive under the locked protocol. These are preserved results, not rerun in the latest stage. The [stage guide](honest_tensor_functional_paper/scientific_extension/README.md) distinguishes raw-data download/parsing from reanalysis of saved subject tensors. Its [validation](honest_tensor_functional_paper/scientific_extension/audit/validation.json) checks the 2,733-file pre-stage baseline and all new artifacts. From the repository root:

```bash
bash honest_tensor_functional_paper/scientific_extension/reproduce.sh
```

The following verification records belong to the **preserved preceding stages**.

The preserved review revision newly ran 87,200 independent datasets, 120,026 method assertions/pathwise cases, 40 public-API timing calls and 3,125 new-summary checks. It reevaluated all 303 saved interval cases, including 606 power-of-two coverage checks. The original 1,084,640 datasets were reused rather than newly simulated. All saved-study tables and ten figures were regenerated; six new figures and the current PDFs were built. [Final artifact validation](honest_tensor_functional_paper/review_revision/logs/final_validation.json) records source checks, current PDF checks and preservation of the 1,514-file baseline except the root README/requirements updates.

```bash
# Rebuild the current revision from preserved observations and the new raw runs.
bash honest_tensor_functional_paper/review_revision/reproduce.sh
# Add --rerun-new to re-execute the 55 new configurations before rebuilding.
```

The following verification history concerns the explicitly preserved earlier stages.

The preserved independent review ran 60,496 saved-result recomputations, 1,377 finite mathematical probes, nine binary outer-grid checks, and an exact regeneration of the offending oracle noise contraction. In S03_007 at 90%, the saved target-scaled tolerance counts one real miss as covered in the oracle and XCH-known rows: 134/150 becomes 133/150. Another 24 strict/tolerant differences are harmless one-ULP structural-boundary effects. The original coverage policy and outputs remain preserved; review_revision contains the completed all-observation correction. Passing the original validator did not endorse that old policy.

The review freshly rebuilt empirical analysis/plots/reports in an isolated copy, with compared tables and report text byte-identical, and forced a clean calculation of the integrated manuscript in a copy. All 14 active figures were visually reviewed, five PDFs scanned, and label/bibliography-key resolution checked. The full million-dataset simulation and full exponential benchmark were not rerun. The final review validator checks that all preceding research files remain unchanged except this root README and `requirements.md`, which record review status. Reproduction commands and evidence are in the [review guide](honest_tensor_functional_paper/independent_review/README.md). The older checks below belong to the explicitly identified earlier stages.

Original compression experiments, from the repository root:

```bash
python3 code/test_simulations.py
python3 code/run_simulations.py --quick
latexmk -pdf -interaction=nonstopmode -halt-on-error -cd paper/main.tex
```

Remove `--quick` for the larger original Monte Carlo run. For the interval simulations, follow [their project README](honest_tensor_functional_paper/README.md). The limited scan prototype remains in `gap_development/`. For the preserved robustness experiments and full manuscript, run from `honest_tensor_functional_paper/robust_adaptive_extension/`:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 code/run_experiments.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 code/check_extensions.py
MPLCONFIGDIR=/private/tmp/tt-robust-mpl XDG_CACHE_HOME=/private/tmp/tt-robust-cache python3 code/render_results.py
python3 code/rebuild.py
python3 code/validate.py
```

Consult the stage-specific requirements and READMEs before rebuilding. These commands generate artifacts. Saved manifests document previous runs; adding the reference collection did not rerun simulations or rebuild manuscripts.

For the 2026-09-10 reference update, all eight PDFs were checked for PDF signatures, parsability, title identity, page count, and SHA-256 integrity. New documentation links and bibliography/manifest consistency were checked. The update adds the curated references, refreshes this repository-wide status and file map, and records the owner's standing rule in `AGENTS.md`.

For the earlier 2026-09-11 norm/loading update, finite checks were run separately from the existing simulations. The manuscript and progress report were rebuilt, result/proof counts and cross-references checked, and all 34 tracked files in `gap_development/` verified unchanged against their baseline hashes. Those outputs remain in `norm_loading_extension/results/`. The subsequent stage below advances its remaining requirements.

The preserved robustness/adaptation update added six theorems and four propositions, complete proofs, and four experiment suites. All 34 tracked files of the preceding `norm_loading_extension/` stage were preserved. The report includes failures when separation, loading correction, or approximation inflation is omitted. Its full manuscript/report were rebuilt and validated; at that stage, the ideal full-data minimax optimizer and real-data experiments remained outstanding. For rare-outlier noise, the robust full-net envelope covered in 400/400 trials while Gaussian sample-mean calibration covered in 349/400; these are saved finite experimental results with binomial uncertainty, not a proof of uniform coverage.

The preserved `certified_weak_signal/` work advanced that historical optimizer status. It ran 320 confidence-projection trials, 8,000 single-observation interval trials, and 27 loading calculations. Checks passed for 1,000 cosine ranges, 1,800 box-containment points, five optimizer cases, 120 mixture identities, 250 first-order bias certificates, and 180 cap-valid tangent certificates. All 47 tracked files of `robust_adaptive_extension/` were preserved. These are now saved earlier results. Numerical certificates use double precision with conservative guards, not formal interval arithmetic.

The preserved `high_dimensional_extension/` stage ran 36 growing-cap configurations (7,200 trials), 12 pointwise configurations (1,900 trials), 96 loading calculations and eight adaptation comparisons. Its 224 finite checks cover exact likelihood moments, attained structural bounds, dyadic sums, bias certificates, projection equivalence, weighted low-degree moments and unknown-support pointwise geometry. All 23 previous-stage files, including uncommitted files, were preserved by hashes. Its report and supplement were built and validated at that stage. These are saved preceding results.

To reproduce that theoretical supplement, run from `honest_tensor_functional_paper/high_dimensional_extension/`:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 code/check_results.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 code/run_experiments.py
python3 code/rebuild.py
python3 code/validate.py
```

The preserved pre-review empirical study ran 1,084,640 Monte Carlo data sets across 318 stochastic configurations, with 84 additional analytic-only configurations and a separate 18-setting runtime study. Its 2,160 optimizer solves reuse 240 observations across levels/budgets; they are not 2,160 independent coverage trials. The initial design is preserved, and the intermediate-cap/calibration follow-up is explicitly registered separately. The study includes a local Xu–Chen–Han PCA reimplementation, paired comparisons, 90/95/99% coverage uncertainty, noise/rank violations, correction ablations, local power, and scalar/interval losses.

At that empirical stage, checks comprised 329 implementation checks, 8,159 result checks and 87 artifact checks. All 330 protected earlier inference-stage files remain unchanged, and earlier Monte Carlo results are not pooled. The large-cap RMSE slope is -0.498 versus the -1/2 reference. Pointwise slopes -0.474 and -0.179 differ from their limiting references; a separately labeled true-subspace calculation explains finite-dimension clipping. An unusually low original Gaussian coverage realization is retained alongside independent confirmation, not replaced. The [reviewer audit](honest_tensor_functional_paper/empirical_study/reviewer_audit.md) records computational, precision, estimator-risk and application limits.

To reproduce the empirical stage from the repository root:

```bash
bash honest_tensor_functional_paper/empirical_study/reproduce.sh
```

The study README also provides commands to rebuild tables, vector figures and PDFs from saved results without rerunning Monte Carlo. The root [requirements.md](requirements.md) is the current open-problem ledger; historical ledgers remain in their original research-stage directories.

## Commit and push rule

Before every commit and push, update this `README.md` with the current project status and file organization, and include the update in the commit. The persistent instruction is in [AGENTS.md](AGENTS.md).
