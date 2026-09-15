# High-dimensional, loading, and adaptation results

**Status: 2026-09-12.** This stage follows the preserved
`certified_weak_signal/` benchmark. Start with the
[progress report](progress_report.md), [complete derivations](theory/results.md),
or [typeset supplement](paper/main.pdf).

- **Efficient growing-cap minimax inference:** for smallest supplied cap
  $r\gtrsim\sqrt p$, sharp length is $\min(M\sqrt{r/p},\tau)$ for all
  budgets. An implemented structural/direct interval attains it using only
  $p$ diagonal accesses. This covers both Tucker and TT cap classes.
- **Larger-budget loading rates:** fixed polynomial decay
  $|w_i|\le C|w_1|i^{-\beta}$, $\beta>0$, gives sharp length
  $|w_1|\min(M,\tau)$ and its squared risk, at every budget. A class of
  arbitrary nonorthogonal residual perturbations is also covered. The
  matching block-fit construction remains statistical, not efficient.
- **Adaptation limits:** under growing outer caps, simultaneous minimax
  adaptation to positive fixed-cap classes is impossible. A shifted result
  also applies at nonzero means with unused rank capacity.
- **Positive pointwise result:** an implemented polynomial interval is
  honest throughout the unseparated Tucker class and pointwise optimal in
  rate at sufficiently strong diagonal means saturating the supplied caps.
  Their support and signed amplitudes are not given to the algorithm.
- **Restricted computational obstruction:** for power exponents
  $0<\beta<1/K$, polynomial estimators of a growing bounded degree cannot
  attain the new all-budget rate in the original budget regime. This is
  not a hardness theorem for all efficient intervals.

General fixed-cap weak-signal minimax computation, arbitrary loading
profiles, intermediate growing-cap rates, and a complete pointwise theory
remain open. The sufficient signal strength for the pointwise theorem is
conservative. See the [audit](theory/audit.md).

## Files and reproduction

| Location | Purpose |
|---|---|
| `theory/results.md`, `theory/audit.md` | Six numbered results, complete supplied derivations, scope audit |
| `code/methods.py` | Growing-cap interval, economy-SVD pointwise interval, analytic envelopes |
| `code/check_results.py` | Independent mixture, profile, projection, and computational checks |
| `code/run_experiments.py` | Newly run high-dimensional and pointwise experiments |
| `code/rebuild.py`, `code/validate.py` | Build reports/PDFs and verify artifacts |
| `results/` | 9,100 new trials, 96 loading calculations, eight adaptation comparisons, checks and hashes |
| `paper/main.tex`, `paper/main.pdf` | Generated standalone technical supplement |
| `literature/update.md` | Primary-source positioning and attribution |
| `baseline_manifest.json` | Hashes of 23 previous-stage files, including its uncommitted work |

From this directory, with Python, NumPy, SciPy, Pandoc and XeLaTeX:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 code/check_results.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 code/run_experiments.py
python3 code/rebuild.py
python3 code/validate.py
```

The growing-cap experiment simulates exactly the diagonal Gaussian
observations used by its interval; it does not allocate the irrelevant
$p^K-p$ noise entries. Pointwise experiments use complete tensors through
$64^3$. Both are original single-observation experiments, with correct
artificial-split scales where splitting is used. All earlier suites remain
saved historical results and are not rerun by these commands.
