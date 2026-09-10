# Paper logic and introduction outline

Positioning: a theoretical problem/setting note with a constructive separation. The method uses classical thresholding; a new estimator is not the novelty claim. Running example: a third-order p-by-p-by-p mean tensor, n=p Gaussian replicates, Frobenius bound one, and the normalized sum of diagonal entries.

| Background | Limitation | Goal | Challenge | Component | Deliverable |
|---|---|---|---|---|---|
| Weak tensor components make exact-rank regular inference fragile | Strong-stratum CLTs do not imply union honesty | Uniform finite-sample coverage at all ranks up to a cap | Avoid small singular-value inverses | Orthogonal diagonal q-compressibility and threshold envelope | T1–T2, Sections 3–4 |
| A tensor obeys simultaneous rank constraints | Retaining one unfolding enlarges the honesty class | Show a quantitative cost of that enlargement | Compare all intervals, not one poor algorithm | Common-target Gaussian mixture | T4–T5, Section 4 |
| Nonconvex classes may reward nonlinear estimation | Convex or affine optimality does not settle this problem | Exhibit a concrete nonlinear advantage and delimit it | Avoid calling a nonmatching bracket minimax | Affine lower bound and within-class sparse mixture | T3, T6, Section 4 |

## Six-paragraph introduction plan

1. **Purpose: make the inferential object tangible.** Introduce the noisy tensor mean and normalized diagonal sum. Explain that individual components may vanish and singular factor coordinates need not be estimable. State the running example and the honest-coverage criterion. No critical gap; real-data relevance remains a MAJOR limitation.
2. **Purpose: give at most three precise limitations.** Xu–Chen–Han require a regular strong stratum for their functional CLT; general weak-factor and nonconvex-functional theory already establishes the broad mechanisms; a single unfolding relaxation discards joint restrictions in the parameter class. Do not claim generic weak-rank inference is new.
3. **Purpose: define the restricted goal.** Ask whether joint Tucker/TT caps permit o(tau) honest intervals for a prescribed orthogonal contrast when one unfolding requires order tau. Emphasize known M and tau, fully observed Gaussian data, and the special loading. This paragraph carries the formulation.
4. **Purpose: identify three challenges.** Control the functional uniformly without a spectral gap; quantify the difference between joint and relaxed honesty; distinguish a useful upper bound from sharp minimax theory. Each corresponds to one row above.
5. **Purpose: explain the three proof components.** Use canonical expansions to obtain an ell_(2/K) diagonal envelope; threshold with a deterministic error radius; use Gaussian mixtures and affine inequalities for comparisons. Return to the K=3 running example and state the polynomial factor.
6. **Purpose: list three concrete contributions.** (i) T1–T2 uniform interval (Sections 3–4); (ii) T3–T5 two separation statements (Section 4); (iii) T6 lower bracket and experiments demonstrating conservative coverage and the missing sharpness (Sections 4–5). Do not list a literature review or code release as a theoretical contribution.

Integrity: running-example loop passes; named limitations/challenges/modules align; three contributions have delivering sections. The note is not presented as a completed solution of actual-rank adaptation. Remaining MAJOR research gaps: unrestricted sharp rate, general loading geometry and substantive practical model. These are recorded in the decision checkpoint, not hidden by the draft.

## Figure specification

Figure 1: analytic log-log curves of length/tau versus p for K=3,4,6, with fixed-rank affine and relaxed-model lower bounds; a second panel shows the within-class lower bracket. These are theorem evaluations, explicitly labeled analytic. Figure 2: simulated coverage with exact binomial intervals across the weak second component, cap two, with a lower panel giving deterministic length/tau. Use Matplotlib, a 6.5-inch canvas, 9-point fonts, vector PDFs, a colorblind-safe palette plus marker/line distinctions. No method pipeline is necessary for this scalar formula.
