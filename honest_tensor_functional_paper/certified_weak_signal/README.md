# Certified optimization and weak-signal inference

**Status: 2026-09-11.** This stage advances the remaining computation,
loading, and adaptation questions. The preceding full manuscript in
`robust_adaptive_extension/` is preserved. This directory contains a
standalone technical supplement rather than another copy of that manuscript.

Start with the [progress report](progress_report.md), then the
[statements and complete derivations](theory/results.md) or their
[typeset supplement](paper/main.pdf).

- The full finite-net residual criterion and confidence-set projection now
  have a continuous global optimizer on the complete binary rank-one ball.
  It reports lower/upper bounds, feasible endpoint witnesses, and explicit
  budget stops. It is exponential and uses guarded floating point arithmetic.
- Every loading tensor has sharp small-budget length and MSE rates for
  $M\le\tau$, expressed through its product overlap. Larger budgets remain
  unresolved in general. Unequal orthogonal weights have an optimized
  common-target mixture lower bound implemented numerically.
- Positive fixed-cap minimax **rate** adaptation follows without separation
  from the existing outer interval and rank-one lower bounds.
- A supplied-cap tangent interval is now honest under arbitrarily weak
  signals, without a separation assumption. Correctly scaled artificial
  splitting makes it usable from the original single observation. This is
  a conservative efficient interval, not an efficient weak-signal minimax
  solution or actual-rank selector.

## Files

| Location | Purpose |
|---|---|
| `theory/results.md` | Eight numbered results/constructions, proofs, limits, and a negative result for a simpler bias correction |
| `theory/audit.md` | Claim dependencies, scope, and remaining problems |
| `code/certified_optimizer.py` | Continuous global residual fit and outer confidence endpoints |
| `code/loading_and_adaptation.py` | Unequal-weight lower bounds, bias certificates, and cap-valid intervals |
| `code/check_results.py` | Independent range, objective, mixture, and bias checks |
| `code/run_experiments.py` | Original-model coverage experiments and optimizer benchmarks |
| `code/rebuild.py`, `code/validate.py` | Report/PDF generation and artifact checks |
| `results/` | Trials, aggregate coverage with uncertainty, gaps, source hashes, and validation |
| `paper/main.tex`, `paper/main.pdf` | Generated standalone technical supplement |
| `literature/update.md` | Focused primary-source positioning |
| `baseline_manifest.json` | Preserved previous-stage tracked-file hashes |

## Reproduce

From this directory, with Python, NumPy, SciPy, Pandoc and XeLaTeX:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 code/check_results.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 code/run_experiments.py
python3 code/rebuild.py
python3 code/validate.py
```

The saved run records the actual package versions. The experiment run uses
fixed seeds and takes a few minutes. A returned outer interval remains the
reported interval when its endpoint optimization hits the node budget;
inner witnesses must never be substituted for it. Earlier simulation suites
are saved historical results and are not rerun by these commands.
