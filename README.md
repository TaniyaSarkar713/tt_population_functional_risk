# Tensor Functional Risk and Honest Inference

This repository contains two connected research directions: population functional risk for tensor-train (TT) compression of conditional generators, and honest confidence intervals for scalar functionals of noisy low-rank tensors. The original compression study and successive inference drafts are preserved separately.

**Status updated: 2026-09-11.** This is a research repository with mathematical drafts, proofs, synthetic experiments, and literature resources. The latest inference results are in `honest_tensor_functional_paper/robust_adaptive_extension/`; the earlier stages are preserved.

## Start here

- [Beginner-friendly mathematical summary](summary.md).
- [Closest reference papers and comparison guide](references/README.md), with eight downloaded PDFs and [BibTeX](references/references.bib).
- [Latest inference manuscript](honest_tensor_functional_paper/robust_adaptive_extension/paper/main.pdf) and [LaTeX source](honest_tensor_functional_paper/robust_adaptive_extension/paper/main.tex).
- [Latest progress report](honest_tensor_functional_paper/robust_adaptive_extension/progress_report.md), [new theorem statements](honest_tensor_functional_paper/robust_adaptive_extension/paper/robust_adaptive_section.tex), [proof audit](honest_tensor_functional_paper/robust_adaptive_extension/theory/proof_audit.md), and [remaining requirements](honest_tensor_functional_paper/robust_adaptive_extension/theory/remaining_requirements.md).
- [Previous sharp-rate stage](honest_tensor_functional_paper/gap_development/README.md), including the limited scan prototype and computational obstruction.
- [Original compression manuscript](paper/main.pdf), [source](paper/main.tex), and [scope decisions](notes/theory_decisions.md).

## Current project status

| Area | Current status | Main limitation or remaining work |
|---|---|---|
| Original TT compression theory | Complete working draft of regular-stratum oracle and modelwise lower bounds; saved synthetic experiments | Geometry, functional identifiability, likelihood regularity, and optimization conditions remain explicit assumptions; no unrestricted-transformer theorem |
| Honest tensor-functional intervals | Baseline weak-signal cap-uniform theory plus robust-noise, approximate-rank, and certified arbitrary-loading extensions | Known norm/noise bounds and stated dependence/replication assumptions remain necessary |
| Latest full-data statistical theory | Matching expected-length and squared-error rates uniformly over every positive supplied norm budget $M$ and noise level $\tau$; complete new proofs | Fixed order/caps and equal or flat orthogonal loadings; efficient optimization remains unproved |
| Loading geometry | Sharp flat-loading rates; arbitrary known loadings handled by an orthogonal surrogate plus a measured residual; efficient minimax constant-product-overlap regime | Sharp minimax geometry for every loading or unequal weight sequence remains open |
| Computation | Efficient minimax small-budget/product-overlap regimes; polynomial separated-rank interval; convex-outer-class obstruction and earlier scan/low-degree results | Efficient minimax diffuse-loading weak-signal intervals and general algorithmic hardness remain open |
| Rank adaptation | Rank-free SVD/projection interval with a computable bias certificate on a separated mode-rank class; nonzero-baseline adaptation lower bound | Bias certificate is conservative; weak-signal adaptation and sharp growing-cap factors are not characterized |
| Relaxed observations/ranks | Same upper rates under joint sub-Gaussian tails; family-wise minimax finite-variance replicate rates with sufficient replication; sharp approximate-rank length | Marginal-only bounds are insufficient; per-law Gaussian lower transfers fail; removing all rank restrictions changes the rate to $\min(M,\tau)$ |
| Empirical work | Saved synthetic interval simulations: 175 configurations, 2,000 replications each; later small scan benchmarks | Intervals can be conservative; limited scan benchmarks show no precision improvement at their small dimensions; no real-data or LLM experiment |
| Latest experiments/checks | 106 new configurations, 76,600 Monte Carlo repetitions; 200 projector/bias cases, 26,595 robust-tail comparisons, 112,086 support pairs, and 100 shifted blocks | Explicit assumption violations are retained; robust scan experiments test the envelope, not the ideal minimax optimizer |
| Closest literature | Eight version-pinned PDFs downloaded, checked, and indexed in `references/`; primary-source comparison and updated publication metadata | Focused reference selection, not an exhaustive priority or independent proof review |
| Repository | Standalone private GitHub repository on `main`, with project summary and persistent README-maintenance instructions | Root README must be refreshed with status and file organization before every commit/push |

“Proved” in the internal ledgers means a complete supplied derivation, supported by finite checks where recorded. It does not mean independent peer review or machine-verified mathematics. Earlier drafts retain historical statements of gaps that later stages address; use the latest progress report for current status.

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

### Latest tensor-inference study

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

Exact confidence-set projection and the ideal residual fit remain existence constructions. The latest extension proves the same upper rates under a joint sub-Gaussian noise proxy and matching family-wise rates with independent finite-variance replicates, a known covariance upper bound, and enough replicates. For a supplied Frobenius approximation allowance $\eta$, sharp Gaussian interval length is $\min\{\tau,\mathfrak r_K+\eta\}$.

A new SVD/projection interval uses no supplied rank caps, but requires spectral separation and independent pilot/validation noise. Its computable bias correction selects the direct interval at moderate signal strength. Strong-signal experiments show shorter lengths; deliberately removing separation gives zero coverage. A separate shifted-mixture lower bound explains an obstruction from weak additional components at nonzero means. Efficient minimax weak-signal intervals and general unseparated rank adaptation remain open.

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
    └── robust_adaptive_extension/    Latest research stage (2026-09-11)
        ├── README.md                 Entry point, scope, and reproduction
        ├── progress_report.md/.pdf   Theory progress, experiment review, remaining work
        ├── paper/                    Full manuscript and ten new proofs
        ├── theory/                   Proof audit and theoretical/experimental ledger
        ├── code/                     Implemented intervals, experiments, checks, build
        ├── results/                  Coverage, lengths, runtimes, uncertainty, hashes
        ├── figures/                  Exportable experiment figures in PDF/PNG
        ├── literature/               Primary-source positioning
        ├── baseline_manifest.json    Hashes protecting the previous stage
        └── deliverable_manifest.json Hashes of new deliverables
```

Each research-stage directory has its own README and supporting files. Historical literature copies are preserved; `references/` is the curated entry point for the closest papers.

## Reproduction and verification

Original compression experiments, from the repository root:

```bash
python3 code/test_simulations.py
python3 code/run_simulations.py --quick
latexmk -pdf -interaction=nonstopmode -halt-on-error -cd paper/main.tex
```

Remove `--quick` for the larger original Monte Carlo run. For the interval simulations, follow [their project README](honest_tensor_functional_paper/README.md). The limited scan prototype remains in `gap_development/`. For the latest experiments, checks and manuscript, run from `honest_tensor_functional_paper/robust_adaptive_extension/`:

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

The subsequent robustness/adaptation update adds six theorems and four propositions, complete proofs, and four newly run experiment suites. All 34 tracked files of the preceding `norm_loading_extension/` stage are preserved. The report includes failures when separation, loading correction, or approximation inflation is omitted. The full manuscript/report are rebuilt and validated; the ideal full-data minimax optimizer and real-data experiments remain outstanding. For rare-outlier noise, the robust full-net envelope covered in 400/400 trials while Gaussian sample-mean calibration covered in 349/400; these are finite experimental results with binomial uncertainty, not a proof of uniform coverage.

## Commit and push rule

Before every commit and push, update this `README.md` with the current project status and file organization, and include the update in the commit. The persistent instruction is in [AGENTS.md](AGENTS.md).
