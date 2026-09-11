# Tensor Functional Risk and Honest Inference

This repository contains two connected research directions: population functional risk for tensor-train (TT) compression of conditional generators, and honest confidence intervals for scalar functionals of noisy low-rank tensors. The original compression study and successive inference drafts are preserved separately.

**Status updated: 2026-09-11.** This is a research repository with mathematical drafts, proofs, synthetic experiments, and literature resources. The latest inference results are in `honest_tensor_functional_paper/norm_loading_extension/`; the earlier stages are preserved.

## Start here

- [Beginner-friendly mathematical summary](summary.md).
- [Closest reference papers and comparison guide](references/README.md), with eight downloaded PDFs and [BibTeX](references/references.bib).
- [Latest inference manuscript](honest_tensor_functional_paper/norm_loading_extension/paper/main.pdf) and [LaTeX source](honest_tensor_functional_paper/norm_loading_extension/paper/main.tex).
- [Latest progress report](honest_tensor_functional_paper/norm_loading_extension/progress_report.md), [new theorem statements](honest_tensor_functional_paper/norm_loading_extension/paper/norm_loading_section.tex), [proof audit](honest_tensor_functional_paper/norm_loading_extension/theory/proof_audit.md), and [remaining requirements](honest_tensor_functional_paper/norm_loading_extension/theory/remaining_requirements.md).
- [Previous sharp-rate stage](honest_tensor_functional_paper/gap_development/README.md), including the limited scan prototype and computational obstruction.
- [Original compression manuscript](paper/main.pdf), [source](paper/main.tex), and [scope decisions](notes/theory_decisions.md).

## Current project status

| Area | Current status | Main limitation or remaining work |
|---|---|---|
| Original TT compression theory | Complete working draft of regular-stratum oracle and modelwise lower bounds; saved synthetic experiments | Geometry, functional identifiability, likelihood regularity, and optimization conditions remain explicit assumptions; no unrestricted-transformer theorem |
| Honest tensor-functional intervals | Finite-sample interval construction under supplied Tucker/TT rank and norm bounds, known Gaussian noise, and a prescribed loading | Actual-rank adaptation and arbitrary loadings remain open |
| Latest full-data statistical theory | Matching expected-length and squared-error rates uniformly over every positive supplied norm budget $M$ and noise level $\tau$; complete new proofs | Fixed order/caps and equal or flat orthogonal loadings; efficient optimization remains unproved |
| Loading geometry | Sharp support-size dependence for flat signed orthogonal loadings, including dense rotations; explicit unequal-weight upper/lower envelopes | Unequal-weight envelopes need not match; arbitrary tensor loadings and sharp growing-cap dependence remain open |
| Computation | Proved truncated-scan tradeoff, complete level-one/two prototype, and a low-degree polynomial-estimation obstruction | A polynomial-time minimax interval and unconditional hardness for all efficient intervals are not established |
| Empirical work | Saved synthetic interval simulations: 175 configurations, 2,000 replications each; later small scan benchmarks | Intervals can be conservative; limited scan benchmarks show no precision improvement at their small dimensions; no real-data or LLM experiment |
| New theory checks | 3,267 rate configurations, 240 tensor differences, 23,268 weighted support pairs, 90 residual-tail checks, and 60 loading embeddings passed | Finite corroboration, not formal proof verification or simulations of the ideal residual optimizer |
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

Exact confidence-set projection and the ideal residual fit are existence constructions; the limited scan prototype does not compute an efficient minimax interval. Actual-rank adaptation remains open beyond the supplied-cap guarantees.

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
    └── norm_loading_extension/       Latest research stage (2026-09-11)
        ├── README.md                 Latest-stage entry point and reproduction
        ├── progress_report.md/.pdf   New results, evidence, and scope
        ├── paper/                    Full manuscript plus norm/loading proofs
        ├── theory/                   Proof audit and remaining requirements
        ├── code/                     Finite checks, rebuild, and validation
        ├── results/                  Rate grids, mixture/tail checks, and validation
        ├── literature/               Positioning of the extension
        ├── baseline_manifest.json    Hashes protecting the previous stage
        └── deliverable_manifest.json Hashes of the new deliverables
```

Each research-stage directory has its own README and supporting files. Historical literature copies are preserved; `references/` is the curated entry point for the closest papers.

## Reproduction and verification

Original compression experiments, from the repository root:

```bash
python3 code/test_simulations.py
python3 code/run_simulations.py --quick
latexmk -pdf -interaction=nonstopmode -halt-on-error -cd paper/main.tex
```

Remove `--quick` for the larger original Monte Carlo run. For the interval simulations, follow [their project README](honest_tensor_functional_paper/README.md). The limited scan prototype remains in `gap_development/`. For the latest theoretical checks and manuscript, run from `honest_tensor_functional_paper/norm_loading_extension/`:

```bash
python3 code/check_theory.py
python3 code/rebuild.py
python3 code/validate.py
```

Consult the stage-specific requirements and READMEs before rebuilding. These commands generate artifacts. Saved manifests document previous runs; adding the reference collection did not rerun simulations or rebuild manuscripts.

For the 2026-09-10 reference update, all eight PDFs were checked for PDF signatures, parsability, title identity, page count, and SHA-256 integrity. New documentation links and bibliography/manifest consistency were checked. The update adds the curated references, refreshes this repository-wide status and file map, and records the owner's standing rule in `AGENTS.md`.

For the 2026-09-11 theory update, the new finite checks were run separately from the existing simulations. The updated manuscript and progress report were rebuilt, the new result/proof counts and cross-references checked, and all 34 tracked files in the previous `gap_development/` stage verified unchanged against their baseline hashes. Detailed outputs are in the latest stage's `results/` directory. The outstanding efficient-computation, general-loading, and rank-adaptation requirements remain explicitly listed.

## Commit and push rule

Before every commit and push, update this `README.md` with the current project status and file organization, and include the update in the commit. The persistent instruction is in [AGENTS.md](AGENTS.md).
