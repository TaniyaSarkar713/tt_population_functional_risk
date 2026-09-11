# Remaining theoretical requirements after this extension

Updated 2026-09-11. This ledger supersedes earlier open-question statements only for the new manuscript. The original teacher-query compression draft is a different experiment and is not revised here.

| Requirement | Status after this work | Evidence or precise missing step |
|---|---|---|
| Remove $M=\tau\sqrt p$ from the equal-diagonal sharp theory | RESOLVED for fixed order/caps and known $M,\tau>0$ | Norm-sensitive diameter, tuned harmonic lower bound, and all-budget theorem |
| Match squared-error risk in every norm regime | RESOLVED in the same experiment | Measurable approximate residual fit and Gaussian excess-tail integration |
| Identify loading support-size dependence | RESOLVED for flat prescribed orthogonal weights, including signs and dense rotations | Orthogonal block reduction and full ambient lower bounds |
| General nonuniform orthogonal weights | PARTIAL | Explicit $U_w$ and $L_w$; their uniform equivalence is not proved |
| Arbitrary tensor loadings | OPEN | Need a geometry-dependent modulus without the orthogonal product representation |
| Efficient minimax confidence interval | OPEN | Exact projection and residual optimization remain computationally uncertified |
| Unconditional efficient-interval lower bound | NOT ESTABLISHED | Low-degree squared-risk obstruction is not hardness for every efficient test or interval |
| Actual-rank adaptation | OPEN in its general form | Outer-class honesty prevents a zero-width rank-zero oracle at zero; finer subclass expected-length theory is not characterized |
| Sharp growing-cap dependence | OPEN | Upper constants use doubled-cap expansion bounds; rank-one lower bounds do not match growing-rank factors |
| Unknown norm bound from the same tensor | OPEN | The class-defining $M$ is still supplied; the all-budget theorem does not permit an unvalidated plug-in |
| Noise and random-design extensions | PARTIAL / OPEN | Previous calibrated replicate/envelope results remain separate; no transfer of this minimax phase diagram to regression is supplied |
| Independent mathematical and priority review | REQUIRED before submission | Internal derivations, checks, and a focused search do not certify either |

## Next concrete targets

1. Compare the weighted upper envelope with improved multiple-scale common-target priors; determine whether a sharp functional of $(w_s^*)$ replaces the current sandwich.
2. Develop a certified relaxation of the residual optimization and bound the loss in interval length. A numerical optimizer without an outer certificate is insufficient for honesty.
3. If pursuing computational hardness, supply a reduction for the actual scalar testing problem and an explicitly stated computational assumption. Do not rename the existing low-degree bound as unconditional hardness.
4. Characterize between-rank expected-length adaptation at nonzero means with explicit separation conditions; distinguish order adaptation across fixed positive caps from exact rank recovery.

No claim is made that all submission requirements have been completed.
