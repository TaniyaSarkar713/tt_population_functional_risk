# Complete guideline coverage

The supplied attachment contains 50 numbered items, including the final deliverable list. All are mapped below. “Addressed” means reviewed, not that the underlying manuscript requirement is satisfied. Real-data/LLM execution is absent and explicitly assessed as such.

| Item | Guideline | Review artifact / evidence |
|---|---|---|
| 1 | First understand the paper independently | [Section 1: reconstruction, experiment, target and procedure](report.md) |
| 2 | Give a one-paragraph referee summary | [Section 1: one-paragraph referee summary](report.md) |
| 3 | Evaluate the statistical contribution | [Section 2: statistical contribution and significance](report.md) |
| 4 | Review the mathematical formulation | [Formulation and notation; report Section 1](assumption_audit.md) |
| 5 | Review every assumption | [R01–R20 assumption audit with use, standardness, restrictiveness and weakening](assumption_audit.md) |
| 6 | Audit every theorem | [59 distinct results; statement/proof/novelty/strength/issues and source lines](theorem_audit.md) |
| 7 | Check theorem strength | [Individual strength judgments; report Section 3 rates](theorem_audit.md) |
| 8 | Check minimax and optimality claims | [Section 3: matched classes, losses, budgets, logs and constants](report.md) |
| 9 | Independently audit the proofs | [Section 4 dependency chains; individual proof reconstructions in theorem audit](report.md) |
| 10 | Look specifically for proof failures | [Section 4 dependence, nets, doubled ranks, conditioning, measurability and tail checks](report.md) |
| 11 | Stress-test the theory | [Section 4 explicit counterexamples and boundary stress tests; new proof probes](report.md) |
| 12 | Check identifiability | [Section 1: mean/functional identifiable, factors need not be](report.md) |
| 13 | Check computational feasibility | [F07 and Section 6: ideal estimator, binary search, polynomial regimes and input size](report.md) |
| 14 | Review tuning-parameter theory | [Tuning audit with theoretical/empirical choices and scope](assumption_audit.md) |
| 15 | Review the simulation design | [All suites S01–S13, including separate runtime and follow-ups](simulation_and_claims.md) |
| 16 | Check rate validation | [Sections 3 and 6: rate slopes, logs, finite-grid curvature and cap rounding](report.md) |
| 17 | Review simulation fairness | [Pairing, exact baselines, oracles, comparator eligibility, F02/F05/F06](simulation_and_claims.md) |
| 18 | Check whether uncertainty is reported | [Section 6: Wilson intervals, MCSE, paired differences and simultaneous screening](report.md) |
| 19 | Review ablation experiments | [F02: three-component ablation and concrete controlled replacement](report.md) |
| 20 | Review the real-data analysis | [Section 7: no executed real-data analysis; existing applicability audit reviewed](report.md) |
| 21 | For AI/LLM applications, audit experimental independence | [Section 7: no LLM observations used; future sampling/dependence requirements](report.md) |
| 22 | Check whether empirical results support the claims | [Claim-to-evidence classifications and suite conclusions](simulation_and_claims.md) |
| 23 | Review figures | [All 14 active manuscript/current-study figures](presentation_audit.md) |
| 24 | Review tables | [Analytic and empirical tables, precision, uncertainty and comparison classes](presentation_audit.md) |
| 25 | Review the Abstract | [Proposed integrated abstract; report Section 8 critique](proposed_abstract.md) |
| 26 | Review the Introduction | [Section 8 and revision plan: introduction focus and contribution hierarchy](report.md) |
| 27 | Review the Related Work section | [Section 2: focused primary-source novelty comparison, explicit citation-audit boundary](report.md) |
| 28 | Review the Methods section | [Tuning and computation; report Sections 1,5,8 specify missing integrated methods](assumption_audit.md) |
| 29 | Review the Theory section as exposition | [Sections 3,4,8: main theorem hierarchy and explanatory proof structure](report.md) |
| 30 | Review the Discussion | [Sections 5,7,8: limitations and stale discussion wording](report.md) |
| 31 | Review the Appendix | [Proof-by-proof audit; presentation/revision plan reorganizes appendix dependencies](theorem_audit.md) |
| 32 | Check internal consistency | [F03, Section 3 and claims audit: fixed/growing caps, noise laws, pointwise/risk scope](report.md) |
| 33 | Check notation globally | [Global notation audit with proposed unifying symbols](presentation_audit.md) |
| 34 | Evaluate reproducibility | [Section 6: new checks versus saved evidence; isolated byte-identical rebuild](report.md) |
| 35 | Evaluate robustness of conclusions | [Fairness and sensitivity; changed-seed, parameter and noise conclusions delimited](simulation_and_claims.md) |
| 36 | Separate fatal issues from fixable issues | [Three MAJOR, five MODERATE, two MINOR; no CRITICAL established](revision_plan.md) |
| 37 | Produce a skeptical referee report | [Summary, substantive strengths, ranked concerns, author questions, revisions and recommendation](report.md) |
| 38 | Simulate multiple reviewers | [Section 9: three explicitly simulated referee perspectives](report.md) |
| 39 | Give an editor-style assessment | [Section 10: associate-editor assessment and Major revision recommendation](report.md) |
| 40 | Assess target-journal fit | [Section 10: six venue fit scores from 1 to 5 and obstacles](report.md) |
| 41 | Identify the single strongest contribution | [Section 2: single strongest contribution sentence](report.md) |
| 42 | Identify the single biggest weakness | [Section 10: single biggest weakness and exact repair](report.md) |
| 43 | Determine whether any claims should be weakened | [Current-claim/evidence/too-strong/recommended-wording table](simulation_and_claims.md) |
| 44 | Identify missing theoretical results | [Six ranked missing-theory recommendations with impact, feasibility and publication relevance](revision_plan.md) |
| 45 | Identify missing experiments | [Seven ranked missing experiments](revision_plan.md) |
| 46 | Identify unnecessary material | [Cuts, moves and suggested final organization; presentation figure audit](revision_plan.md) |
| 47 | Produce a prioritized revision plan | [P0–P3 action tables with exact source locations and completion criteria](revision_plan.md) |
| 48 | Final scientific checklist | [Section 12: final scientific checklist with pending/not-applicable distinctions](report.md) |
| 49 | Final verdict | [C — Major revision required; viable core and concrete remaining corrections](report.md) |
| 50 | Final deliverables | [Deliverable index; complete_review.pdf includes all main review and audit documents](README.md) |
