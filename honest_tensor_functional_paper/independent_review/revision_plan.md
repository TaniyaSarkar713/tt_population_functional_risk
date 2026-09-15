# Prioritized revision plan

This is a concrete review plan, not a claim that these revisions have been implemented. Paths are relative to `honest_tensor_functional_paper/`. Existing sources and saved outcomes are preserved in this review. F01–F10 are the ten classified findings in [report.md](report.md): three MAJOR, five MODERATE and two MINOR; no CRITICAL issue was established.

## Priority 0: must resolve before submission

| Problem / location | Recommended fix | Completion criterion and expected impact |
|---|---|---|
| F01. Target-sized coverage tolerance; `empirical_study/code/common.py:66`, `code/analyze_results.py:74`; S03_007 rows/raw results | Use a justified ULP-scale event comparison, Gaussian noise-centered checks where available, and an exact structural-boundary policy. Preserve old outputs and recompute on unchanged draws | Trial 41's 90% oracle/XCH-known miss is counted as a miss; true structural endpoints survive harmless rounding; all affected aggregates/plots/report diagnostics regenerated. Removes a documented empirical validity error |
| F03. Unsynchronized submission; `robust_adaptive_extension/paper/main.tex:39,57–63,406,454–458`, `norm_loading_section.tex:99`, both later supplement `theory/results.md` files, new empirical insert | Select and assemble one canonical manuscript/supplement; rewrite the abstract/contribution list/discussion around the final theorem scope, and integrate the actual study | One reading order, one final rate table, precise adaptation/computation status and no obsolete main gap figure. Prevents a referee assessing an earlier theorem/experiment package |

## Priority 1: strongly recommended

| Problem / location | Recommended fix | Completion criterion and expected impact |
|---|---|---|
| F02. Confounded ablation; `empirical_study/code/tensor_methods.py:92–103`, `simulation_design.md` Part B | Hold split, projector, quantile, selection and fallback fixed for an isolated bias contrast, or relabel current variant as multicomponent | Shared draws and paired uncertainty, with an explicit list of the sole changed component; removes unsupported causal attribution |
| F04. Midpoint risk; `high_dimensional_extension/code/methods.py:191–193`, empirical counterpart and report's estimator-failure section | Expose interval and scalar estimator separately; keep unconditional loss and sentinel diagnostics. If changing the estimator/fallback, state and prove its risk target | A user cannot mistake P1 for midpoint-risk optimality. Existing bad outcomes remain visible |
| F05. Signal and supplied norm budget coupled; `empirical_study/code/run_study.py:89`, caption 04 | Add a fixed-$M$ sensitivity sweep with all signals in the same class; label existing norm-comparable sweep | Onset-of-shortening statements distinguish signal effects from changes in the honesty class |
| F06. Regular comparator domain; `empirical_study/code/run_study.py:138`, comparator documentation, integrated `main.tex:83` | Add per-case flags for weak/zero, wrong rank and unverified regularity; cite/check XCH PCA Section 4 and relevant alignment/initializer conditions | Tables separate guarantee type from verified applicability; strong-signal comparisons stay fair |
| F07. Ideal versus implemented method; `gap_section.tex:42–76`, certified C1/C2, high-dimensional W1, empirical methods/captions 02/06/10 | Add a concise method table with input model, target class, computational status, stopping error and proved loss | No reader mistakes analytic envelopes or a local/global binary benchmark for an implemented general high-dimensional optimizer |
| Novelty focus; `main.tex` Introduction/Related work; `literature/novelty_matrix.md` | Explain the sharp tensor likelihood mechanism relative to sequence functionals, nonconvex functional recovery and finite convex unions; seek a specialist check of the central lower/upper proofs | Demonstrates the distinct mathematical contribution without asserting firstness or requiring all open extensions |

## Priority 2: material improvements

| Problem / location | Recommended fix | Completion criterion and expected impact |
|---|---|---|
| F07 solver sensitivity; `empirical_study/configs/cases.json`, S08; caption 06 | Fix the same loading and endpoint tolerance across budgets; add signal amplitude as a separate factor | Certification curves identify computation effects; retained unresolved endpoints and missing witnesses remain visible |
| F08 retained calibration results; `robust_adaptive_extension/paper/refinements.tex:139,184` | Add bounded whole-replicate corruption and independent chi-square noise-bound experiments using the actual proposed calibrations | Empirical robustness discussion maps to the refinements it claims to demonstrate |
| Pointwise precision; S03/S04 and P1 proof | Prioritize more replications near the practical transition and largest dimension; compare to exact/finite-geometry references and show cap rounding | Better coverage precision and a clearer finite-grid explanation; do not label slope agreement as a proof |
| Real-data requirement; `empirical_study/real_data/README.md` | Develop an application only after the sampling unit, target, noise/bound calibration and dependence model are justified | A genuine application can support a methodological framing; no convenient tensor-shaped substitute |
| Complexity reporting; S11/runtime tables | Add explicit input entries/bytes and distinguish traced allocations, native workspace and input-access cost | Makes polynomial complexity interpretable as dimensions/order change |

## Priority 3: polish

| Problem / location | Recommended fix | Completion criterion and expected impact |
|---|---|---|
| F09. Repeated scalar loss across levels; `empirical_study/code/common.py:81–96`, flattened summary exports | Add estimator identity and `estimator_alpha`; specify whether point estimate depends on interval level | Prevents 90/99% rows being read as those intervals' midpoint risks |
| F10. Notation collisions; active TeX and both supplement Markdown sources | Adopt the notation table in the assumption/presentation audit | Consistent ambient dimension, polynomial degree, noise envelope, approximation and overlap notation |
| Chronological clutter; main Sections 5–7 and preliminary lower-bound appendix | Remove or move superseded gap narrative/harmonic proof; combine routine corollaries and repeated limitations | A shorter final argument without lost substantive evidence |
| Figure hierarchy; initial theoretical comparison and duplicated rate examples | Show final rate regimes first; use only one weak-boundary illustration and one computational/failure figure in main text | Reader sees the central scientific result and its practical limit promptly |

## Ranked missing theory

| Rank | Missing result | Impact / feasibility | Importance for publication |
|---|---|---|---|
| 1 | Efficient general-dimensional fixed-cap weak-signal optimizer with a global statistical/numerical error contract, or an appropriately scoped stronger obstruction | Very high impact; low/uncertain feasibility. Low-degree results alone do not settle all polynomial algorithms | Essential only for a general efficient-method claim; not required for a clearly statistical minimax theorem paper |
| 2 | Sharp intermediate growing-cap rates with explicit uniform cap dependence | High impact; moderate/uncertain feasibility via stronger upper geometry and matched mixtures | Would turn boundary results into a convincing rank phase diagram; current partial characterization must remain explicit |
| 3 | Arbitrary-loading local/global modulus or matching profile envelope beyond small budgets and fixed positive decay | High impact; low/uncertain feasibility, especially nonorthogonal loadings | Necessary for a general-loading optimality claim; a focused flat-loading paper can proceed without it |
| 4 | Pointwise expected-length characterization with weaker signal thresholds, unsaturated/rotated geometry and TT structure | High impact; a weaker sufficient threshold may be more feasible than a complete characterization | Needed for broad optimal adaptation claims; current P1 is a useful restricted theorem |
| 5 | A practical scalar estimator paired with the cap-valid interval and a proved unconditional risk bound | Moderate/high practical impact; potentially feasible but requires control on failure events | Necessary before claiming a jointly optimal interval/estimator from the current midpoint API |
| 6 | Unknown directional scale, dependent replicates and selected loading/allowance calibration | High application value; feasibility depends on a concrete sampling model | Pursue after selecting a defensible application, not as unsupported generic robustness language |

## Ranked missing experiments

1. Corrected boundary-event audit on the existing draws (P0; mandatory), including rescaling sensitivity and the exact regenerated miss.
2. Controlled bias/fallback/confidence-allocation ablations (P1), with the same paired observations.
3. Fixed-$M$ signal sweep and case-level comparator eligibility (P1).
4. Fixed-loading, fixed-tolerance optimizer budget curves and complete unresolved-gap reporting (P2).
5. More precise pointwise transition checks and explicit unconditional midpoint-loss tails (P2); preserve all rare events.
6. Actual independent-variance and bounded-row-corruption calibration experiments if retained as practical claims (P2).
7. Justified real-data repeated-tensor analysis if targeting a method-led venue (conditional P2). An unrelated LLM benchmark is not an adequate substitute.

## Suggested final paper organization

Use one setup and notation table; one central all-budget flat-loading theorem with the cubic/higher-order mechanism; a short diagonal/affine/enlarged-honesty comparison; then a section delimiting computable regimes and adaptation. Keep only the most substantive robustness/loading extensions in the main text. Put complete proofs, numerical contracts, additional regime consequences and full empirical tables in a coherent supplement. Archive superseded development steps. A full phase diagram or algorithm for every open regime is not a required P0 action.
