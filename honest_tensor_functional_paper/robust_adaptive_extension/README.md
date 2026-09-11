# Robust observations, loading geometry, and rank adaptation

**Status: 2026-09-11.** This stage reviews the previous progress report and develops its remaining computational, loading, rank-adaptation, and assumption questions. The earlier `norm_loading_extension/` is preserved by hashes.

Start with the [progress report](progress_report.md) ([PDF](progress_report.pdf)), then the [full manuscript](paper/main.pdf), [new statements](paper/robust_adaptive_section.tex), and [complete proofs](paper/robust_adaptive_proofs.tex).

## What changed

- Full-data upper bounds extend to joint sub-Gaussian errors, including suitable dependence. Minimax rates match over an unknown-law family containing Gaussian noise, not for every fixed non-Gaussian law.
- With independent finite-variance replicates and a known covariance upper bound, directional medians give matching full-data length and squared-risk rates when the number of replicates is at least a stated constant times the loading dimension. Exact scan optimization remains computationally unresolved.
- A supplied Frobenius approximation allowance $\eta$ changes the sharp interval scale to $\min\{\tau,\mathfrak r_K+\eta\}$.
- Arbitrary known loadings admit certified orthogonal-surrogate intervals with a direct residual correction. Efficient minimax intervals are proved for small norm budgets and loadings with a certified constant product overlap.
- An explicit rank-free SVD/projection algorithm is honest on a spectrally separated class, with a computable bias correction. The assumptions exclude weak extra components; a shifted-mixture lower bound explains an obstruction at nonzero lower-rank tensors.
- A convex-hull lower bound and a growing-rank lower bound delimit what naive relaxations can retain. Sharp unrestricted efficient inference and sharp geometry for every loading remain open.

## Experiments and files

| Location | Contents |
|---|---|
| `paper/` | Full integrated manuscript, earlier sources/figures, new theory/proofs, and experiment section |
| `code/methods.py` | Computable split-sample adaptive interval, loading correction, and complete small full-net median scan |
| `code/run_experiments.py` | Adaptive-rank, arbitrary-loading, and robust-scan experiments |
| `code/check_extensions.py` | Independent finite checks and approximate-rank interval simulations |
| `code/render_results.py` | Figures and summaries generated from saved results |
| `code/rebuild.py`, `code/validate.py` | Manuscript/report build and provenance checks |
| `results/` | 106 experiment configurations, uncertainty intervals, runtimes, seeds, source hashes, and mathematical checks |
| `figures/` | Exportable PDF and PNG experiment figures |
| `theory/` | Proof audit and remaining theoretical/experimental requirements |
| `literature/` | Primary-source positioning and distinctions from existing work |
| `baseline_manifest.json` | Hashes of all 34 tracked files of the previous stage |
| `deliverable_manifest.json` | Hashes of this stage's deliverables |

There are 76,600 Monte Carlo repetitions across the four suites. The small full scan tests the simultaneous noise envelope, not an implementation of the ideal minimax confidence-set optimizer. The adaptive algorithm deliberately includes 12 configurations outside its spectral assumptions to expose failure. The source and report identify them explicitly.

## Reproduction

From this directory, using Python with NumPy, SciPy, Matplotlib, and pypdf, plus LaTeX and Pandoc:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 code/run_experiments.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 code/check_extensions.py
MPLCONFIGDIR=/private/tmp/tt-robust-mpl XDG_CACHE_HOME=/private/tmp/tt-robust-cache python3 code/render_results.py
python3 code/rebuild.py
```

`python3 code/validate.py` checks the existing artifacts after a build. Numerical corroboration and successful coverage experiments are not formal proofs, independent review, or a novelty certificate. See the [audit](theory/proof_audit.md) and [remaining requirements](theory/remaining_requirements.md).
