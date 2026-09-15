# Minimax frontiers: 15 September 2026

This stage supplies four new results, executable methods, and new simulations.
Read the [research report](paper/report.pdf), [full proof supplement](paper/technical_supplement.pdf),
and [continued issue registry](audit/issue_registry.csv). Earlier stages are preserved.

| Result | Proven scope | Computational status |
|---|---|---|
| M1 | Every loading and budget, every rank cap, full tensor model with **one constrained unfolding** | Loading SVD and a scalar convex solve; reusable linear evaluation |
| M2 | Flat-loading lower bound for deterministic affine intervals with constant radius | Explains an obstruction for this procedure class; no general algorithmic hardness claim |
| L3 | Every orthogonal loading profile, all budgets, order **K >= 4**, fixed positive Tucker or TT caps | Exact statistical rate proxy computed; attaining prefix fits remain ideal |
| P5 | Optimal lengths for every coordinate at an **unknown rank-one axis mean** | Globally honest rank-one interval; sufficient localization threshold for pointwise optimality |

“Proved” means a complete supplied derivation checked internally. These are rates
up to constants, not exact finite-sample minimax constants or externally reviewed results.
M1 observes all entries and allows dense mean matrices after unfolding; it does not
assume exact diagonal support. Additional simultaneously restrictive tensor caps
preserve its honesty but invalidate its matching lower-bound argument.

General efficient minimax computation for simultaneous fixed caps, arbitrary
cubic/nonorthogonal loading rates, general intermediate cap vectors, and complete
pointwise theory remain open. The binary optimizer remains an exponential benchmark.
The expanded program retains internal verdict **C**.

This stage newly generated **320,000 independent full-observation Monte Carlo data
sets in 160 configurations**, with **20,489 finite checks**, 120 analytic loading
calculations and 265 analytic cap/budget calculations. The cap count is also read
and checked against the saved JSON by the validator. Each stochastic case has
2,000 draws. One configuration deliberately violates the rank-one assumption.
All endpoints and scalar outputs are retained, and seeds regenerate observations.
The correctly specified cases have no Holm-adjusted coverage-screen rejection;
this finite screen does not prove uniform coverage.

Coverage uses four representable endpoint steps solely for rounding evaluation,
with strict counts preserved. F037 has a one-step structural-boundary discrepancy
affecting 2,000 proposed and 1,890 direct counts; see the
[rounding audit](audit/rounding_audit.json). The negative control fails with zero
coverage and is retained. The finite spectral grid shows modest width gains at
best. No simulation is presented as general ideal-optimizer attainment.

The preceding 109,000 simulations and 122-subject EEG analysis in
`../scientific_extension/` were **not rerun**. The application continues to show
wide finite-sample intervals and no certified tensor precision advantage.

## Reproduction

From the repository root:

```bash
# Recalculate saved summaries, figures and both PDFs, then verify artifacts.
bash honest_tensor_functional_paper/minimax_frontier/reproduce.sh

# Also regenerate the 160 new Monte Carlo configurations and timings.
bash honest_tensor_functional_paper/minimax_frontier/reproduce.sh --rerun-mc
```

Dependencies: Python with NumPy, SciPy, matplotlib, threadpoolctl and PyMuPDF;
Pandoc and XeLaTeX for PDFs. Exact executed versions, platform, seeds, threads
and elapsed time are in [run metadata](results/run_metadata.json).
All statistical methods use known noise scale, norm bound, and the stated supplied
rank restriction. Gaussian splitting in P5 uses additional independent randomness.
The pre-stage baseline also includes 77 local build/metadata files excluded by
the existing `.gitignore`. Their hashes are checked when present; the validator
permits their absence in a clean checkout, as recorded in
`audit/distribution_exclusions.json`. Scientific sources and saved results are
not exempted from preservation checks.

Minimal API, after putting this stage's `code/` directory on the Python path:

```python
from methods import spectral_plan, spectral_interval, adaptive_coordinate_interval

# L and Z are same-shaped tensors; only this mode rank is restricted for M1 optimality.
plan = spectral_plan(L, M=10.0, rank=2, tau=1.0, mode=0)
answer = spectral_interval(Z, plan)
# TT unfolding alternative: use cut=1 instead of mode=0.

# A separate rank-one procedure; target must be fixed before observing Z.
coordinate = adaptive_coordinate_interval(Z, target, M=10.0, rng=rng, tau=1.0)
```

The spectral API reports separate interval endpoints and a scalar estimate. Its
plan exposes floating-point primal/dual diagnostics. Numerical residuals are not
formal SVD or interval-arithmetic certificates.

## Files

- `theory/results.md`: M1, M2, L3 and P5, complete lower/upper proofs, open boundaries.
- `code/methods.py`: public spectral and adaptive-coordinate APIs, rate proxy and lower-bound diagnostics.
- `code/check_theory.py`: independent optimizer, exact mixture, symmetry, geometry and API checks.
- `code/run_experiments.py`: frozen configurations, full-observation simulations, analytic grids and timings.
- `code/numerics.py`, `code/reanalyze.py`: bounded-ULP/strict evaluation and saved-observation reanalysis.
- `code/plot_results.py`, `code/build_report.py`, `code/validate.py`: evidence-based figures, report and audits.
- `code/pdf_audit.py`, `code/figure_pages.lua`: rendered-page and content-bound checks; complete figure/caption pages.
- `results/`: 160 per-configuration NPZ files, configurations, summaries, analytic grids, slopes and timings.
- `figures/`: four vector PDF/SVG figures and PNG previews.
- `paper/`: generated research report and complete technical supplement PDFs.
- `audit/`: continued 19-issue registry, check results, coverage/rounding audits, baseline and artifact hashes.
- `review_notes.md`: adversarial proof checks, scientific before/after comparison, and remaining risks.

The root README and requirements ledger identify this as the current research
stage; the focused `review_revision/` manuscript remains the preserved submission draft.
