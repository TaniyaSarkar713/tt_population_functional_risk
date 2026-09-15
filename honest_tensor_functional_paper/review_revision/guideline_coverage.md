# Coverage of all 40 revision instructions

| Item | Requirement | Evidence / disposition |
|---|---|---|
| 1 | Full review before edits | logs/review_read_manifest.json; issue_registry.md |
| 2 | Scientific classification | tables/issue_registry.csv |
| 3 | Correctness before narrative | theory/revision_audit.md; results/saved_corrections.json |
| 4 | Identifiability | theory/revision_audit.md; main Section 2 |
| 5 | Theorem dependency chains | theory/revision_audit.md; technical_supplement.pdf |
| 6 | Theorem status | theory/theorem_status.json: 59 retained PROVED + R1 PROVED |
| 7 | Assumption investigation | theory/revision_audit.md, seven assumption families; prior 20-family audit preserved |
| 8 | Rates and optimality | main Sections 2–5; full-data/marginal/class/algorithm distinctions |
| 9 | Mathematical novelty | novelty_and_baselines.md; main Section 3 |
| 10 | Execute missing simulations | 55 registered cases, all completed |
| 11 | Direct theorem tests | V03/V04 calibrations; V05 P1 normalized lengths; analytic rate plot labeled |
| 12 | Investigate contradiction | R1 proof and all-observation scalar reevaluation; exact Gaussian coverage miss |
| 13 | Strong/fair baselines | XCH source map; common data; oracle information marked |
| 14 | Real-data validity | D01 unresolved; no unsupported application |
| 15 | Better application if needed | No defensible dataset/target established; explicit future-work conditions |
| 16 | Computation and numerical error | C1 contract; 600 fixed-loading solves; fresh runtime/input accounting |
| 17 | Tuning | fixed budgets/tolerance; V04 independent scale calibration; paired allocations |
| 18 | Scientific fixes before claims | registered runs and completed analyses precede final abstract/main |
| 19 | Contribution statements | three final claims mapped to formal results and evidence |
| 20 | Abstract last | code/build_reports.py generates abstract after reading final checked tables |
| 21 | Theory interpretation | main Sections 2–6 explain budget/order/rank and scope |
| 22 | Technical organization | focused main paper plus complete technical supplement |
| 23 | Notation | paper/notation.md and consistent active sources |
| 24 | Reproducibility | reproduce.sh; raw results; seeds/configs/source manifests |
| 25 | Response matrix | tables/issue_registry.csv/json |
| 26 | Individual responses | response_to_review.md: all 19 concerns |
| 27 | Critical engagement | F04 length versus MSE; F05 class change versus leakage; D01; G2 impossibility |
| 28 | All affected outputs | 303 saved interval cases reevaluated; 55 new cases; dependent figures/text regenerated |
| 29 | Downstream claims | new R1 and unchanged central-rate dependency audit |
| 30 | Figures and tables | six new vector figures, ten saved-study figures regenerated; numerical text generated |
| 31 | Negative findings | 593 unresolved solves, weak XCH failure, cap-violation failure, rare losses preserved |
| 32 | Central contribution revisited | novelty_and_baselines.md and revision_summary.md |
| 33 | Journal fit | revision_summary.md compares requested venues |
| 34 | Second adversarial review | second_review.md |
| 35 | Residual classification | second_review.md and revision_summary.md |
| 36 | Specific limitations | main Discussion and revision_summary.md |
| 37 | Final A–J summary | revision_summary.md |
| 38 | Scientific before/after diff | revision_summary.md |
| 39 | Readiness checkpoint | second_review.md |
| 40 | Final verdict | B for focused theory paper; broader four-part research program remains open |
