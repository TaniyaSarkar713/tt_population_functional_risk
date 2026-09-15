# Final figure and report inspection

Inspected 2026-09-13. The figures were generated from the checked numerical tables, then inspected as rendered PNGs. Report pages were also rendered to check tables, captions, and embedding. The accompanying `results/validation.json` records the automated PDF, vector, source-hash and artifact checks separately from this visual audit.

## Figure role and design

These are experimental-results figures. Ordered dimension, sample-size, signal, cap and budget sweeps use connected marker plots; unordered noise laws use offset points with error bars. Gaussian diagnostics use a QQ plot, and computational scaling uses logarithmic axes. No conceptual or motivated-example figure is required for this empirical deliverable.

Each figure uses a 6.8-by-3.8-inch two-panel canvas, vector PDF/SVG exports, serif 9–10pt base axes text and 8pt legends below the panels. Distinct markers and line styles supplement the Okabe–Ito colors. Mathematical superscripts are smaller. Native figure size is the typography reference; recheck readability if a journal reduces the figure width.

## Inspected outputs

| Figure | Visual and scientific presentation check |
|---|---|
| 01 Growing rates | Common readable length ticks; explicit p/n values; deterministic error bars explained |
| 02 Weak threshold | Order-three/four panels; log scales labeled; diagonal method distinguished from the unavailable ideal optimizer |
| 03 Pointwise rates | Explicit p ticks; cap regimes separated; nearly overlapping XCH/oracle curves explained |
| 04 Signal sweep | Zero retained on symlog axes; extraneous negative signal range removed; failures and zero-width intervals visible |
| 05 Noise | Nominal line and Wilson bars; unordered laws shown as points; mean-shift failure retained |
| 06 Solver | Gap and certification panels; budget-dependent tolerances and finite-witness conditioning disclosed |
| 07 Corrections | Known loading and approximation omissions separated; zero and small allowances remain legible |
| 08 Power and pivots | Exact direct-power reference, local shifts and QQ axes identified; no midpoint CLT implied |
| 09 Runtime | Positive runtime error bars, log cost scales and traced-memory units; small timing sample and memory exclusions disclosed |
| 10 Intermediate caps | Readable cap and ratio ticks; analytic lower bound distinguished from attained performance |

## Uncertainty, captions and integrity

Coverage/rejection bars are Wilson 95% intervals. Mean-length bars use 1.96 Monte Carlo standard errors; solver gap bars use the stated fixed-seed bootstrap. Runtime bars are descriptive plus/minus one SE, explicitly not 95% confidence intervals. A wider symmetric interval would cross zero at one timing point; the unaltered means and SEs remain in the table. Deterministic radii have zero width uncertainty, which is disclosed rather than represented as stochastic rate confirmation.

Captions identify the observed finding, model dimensions, replication count, uncertainty convention and relevant limits. The solver caption discloses differing tolerances and separately fixed arbitrary loadings; the runtime caption discloses preallocated-input/native-memory exclusions. No unsupported significance stars, decorative effects, dual axes or hidden unfavorable outcomes are used.

Axes, legend placement and caption/table wrapping were checked in rendered outputs. The final layouts have no critical or major clipping or overlap issues. Earlier crowded logarithmic ticks, negative symlog padding and clipped symmetric timing bars were corrected without changing simulation observations. Scientific limitations, including finite-grid slopes, unresolved certificates and the absence of a real-data analysis, remain explicit in the report and reviewer audit.
