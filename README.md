# Tensor Functional Risk and Honest Inference

This repository contains two connected research directions: population functional risk for tensor-train (TT) compression of conditional generators, and honest confidence intervals for scalar functionals of noisy low-rank tensors. The original compression study and successive inference drafts are preserved separately.

**Status updated: 2026-09-10.** This is a research repository with mathematical drafts, proofs, synthetic experiments, and literature resources. The latest inference results are in `honest_tensor_functional_paper/gap_development/`.

## Start here

- [Beginner-friendly mathematical summary](summary.md).
- [Closest reference papers and comparison guide](references/README.md), with eight downloaded PDFs and [BibTeX](references/references.bib).
- [Latest inference manuscript](honest_tensor_functional_paper/gap_development/paper/main.pdf) and [LaTeX source](honest_tensor_functional_paper/gap_development/paper/main.tex).
- [Latest progress report](honest_tensor_functional_paper/gap_development/progress_report.md), [proved-result ledger](honest_tensor_functional_paper/gap_development/theory/proved_results.md), and [internal mathematical audit](honest_tensor_functional_paper/gap_development/theory/final_audit.md).
- [Original compression manuscript](paper/main.pdf), [source](paper/main.tex), and [scope decisions](notes/theory_decisions.md).

## Current project status

| Area | Current status | Main limitation or remaining work |
|---|---|---|
| Original TT compression theory | Complete working draft of regular-stratum oracle and modelwise lower bounds; saved synthetic experiments | Geometry, functional identifiability, likelihood regularity, and optimization conditions remain explicit assumptions; no unrestricted-transformer theorem |
| Honest tensor-functional intervals | Finite-sample interval construction under supplied Tucker/TT rank and norm bounds, known Gaussian noise, and a prescribed loading | Actual-rank adaptation and arbitrary loadings remain open |
| Latest full-data statistical theory | Supplied matching expected-length rates at zero and in the worst case, including the cubic logarithmic factor, and corresponding squared-error rates | Sharp characterization is restricted to equal diagonal loading, fixed order/caps, and $M=\tau\sqrt p$ |
| Computation | Proved truncated-scan tradeoff, complete level-one/two prototype, and a low-degree polynomial-estimation obstruction | A polynomial-time minimax interval and unconditional hardness for all efficient intervals are not established |
| Empirical work | Saved synthetic interval simulations: 175 configurations, 2,000 replications each; later small scan benchmarks | Intervals can be conservative; limited scan benchmarks show no precision improvement at their small dimensions; no real-data or LLM experiment |
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

For fixed $K\ge3$, fixed Tucker or TT rank caps, fixed confidence level $0<\alpha<1/4$, and $M=\tau\sqrt p$, the latest supplied proofs match the full-data minimax expected interval length both at zero and in the worst case:

$$
\mathcal L_0(\Theta)\asymp\mathcal L_{\max}(\Theta)
\asymp
\begin{cases}
\tau(\log p)^{3/2}/\sqrt p,&K=3,\\
\tau\sqrt{\log p/p},&K\ge4.
\end{cases}
$$

The corresponding squared-error minimax rates are their squares. The exact confidence-set projection is an existence construction; the limited scan prototype does not compute an efficient minimax interval.

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
    └── gap_development/              Latest research stage
        ├── README.md                 Latest-stage entry point
        ├── progress_report.md        Statistical/computational progress and limits
        ├── paper/                    Updated full manuscript and proofs
        ├── theory/                   Result statements, derivations, and final audit
        ├── code/                     Checks, scan prototype, validation, and rebuild
        ├── results/                  Saved checks, benchmarks, and validation
        └── literature/               Literature update for the later results
```

Each research-stage directory has its own README and supporting files. Historical literature copies are preserved; `references/` is the curated entry point for the closest papers.

## Reproduction and verification

Original compression experiments, from the repository root:

```bash
python3 code/test_simulations.py
python3 code/run_simulations.py --quick
latexmk -pdf -interaction=nonstopmode -halt-on-error -cd paper/main.tex
```

Remove `--quick` for the larger original Monte Carlo run. For the interval simulations, follow [their project README](honest_tensor_functional_paper/README.md). For the latest checks and prototype, run from `honest_tensor_functional_paper/gap_development/`:

```bash
python3 code/check_theory.py
OPENBLAS_NUM_THREADS=1 python3 code/benchmark_scan.py
python3 code/rebuild.py
python3 code/validate.py
```

Consult the stage-specific requirements and READMEs before rebuilding. These commands generate artifacts. Saved manifests document previous runs; adding the reference collection did not rerun simulations or rebuild manuscripts.

For the 2026-09-10 reference update, all eight PDFs were checked for PDF signatures, parsability, title identity, page count, and SHA-256 integrity. New documentation links and bibliography/manifest consistency were checked. The update adds the curated references, refreshes this repository-wide status and file map, and records the owner's standing rule in `AGENTS.md`.

## Commit and push rule

Before every commit and push, update this `README.md` with the current project status and file organization, and include the update in the commit. The persistent instruction is in [AGENTS.md](AGENTS.md).
