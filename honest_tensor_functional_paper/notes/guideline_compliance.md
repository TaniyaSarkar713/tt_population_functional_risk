# Guideline completion map

This maps the attached instructions to delivered artifacts. A completed draft is not a claim that every proposed research extension has been proved.

| Requested item | Delivered evidence | Status and scope |
|---|---|---|
| Research-worthiness before claims | literature/literature_review.md; notes/decision_checkpoint.md | Complete assessment; conditional further-theory recommendation |
| Broad literature through 2026 | 44-reference bibliography, prior survey, search update, 20-paper matrix | Cutoff September 9, 2026; primary inspection depth and preprint status recorded |
| Precise experiment and estimand | Paper Section 3; theory/assumptions.md | Full Gaussian tensor mean, known norm/noise/caps, prescribed loading |
| Exact mathematical gap | Paper equation for the full-data minimax bracket; open_questions.md | Unmatched full-data rates, explicitly PARTIAL |
| Candidate theorems before claims | theory/candidate_targets.md; diagonal_minimax.md | Targets and current results separated |
| Complete derivations | paper/appendix.tex; theory/proofs.md; diagonal_minimax.md | Six theorems, one classical proposition, supporting lemmas; no claimed formal verification |
| PROVED / PARTIAL / CONJECTURED labels | Theorem ledger and appendix status table | Consistent with full-data versus diagonal distinction |
| Theoretical baseline comparison | Related Work; theory comparison table; novelty matrix | Affine and relaxed-class lower bounds; no universal dominance claim |
| Theory-driven simulation design | simulations/simulation_design.md | Original protocol preserved; revision additions identified |
| Controlled experiments and uncertainty | 175 configurations, 2,000 repetitions, 817 rows | 172 Gaussian configurations plus three explicit assumption stresses |
| Empirical center accuracy | Precision table plus configuration-level bias/MCSE/RMSE | Reports shrinkage and oracle information; no selective superiority claim |
| Real-data / AI demonstration if appropriate | real_data/README.md and Discussion | Omitted with statistical justification; no fabricated experiment |
| Reproducible project | README, modular code, fixed seeds, manifests | Separate new folder; prior results reused with provenance |
| Complete manuscript | paper/main.pdf and LaTeX sources | Abstract, Introduction, Related Work, Formulation, Method, Theory, Simulations, Discussion, Appendix, References |
| Continuous novelty check | R24 promoted in matrix; D1 attributed to classical theory | New diagonal-rate claim rejected; joint/full-data targets retained cautiously |
| Venue assessment and final checkpoint | notes/decision_checkpoint.md | Explicit novelty, improvement, generality, validation, objections and go/no-go judgment |

The generic instructions list contamination, dependence, sparsity and misspecification as dimensions to vary when relevant. Here the model assumes iid Gaussian noise; three stress configurations expose failures rather than claim robustness. Coordinate support varies as signal geometry, not as an added sparsity assumption. No arbitrary benchmark or unjustified LLM section is added merely to fill a heading.
