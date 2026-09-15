# Second adversarial review of the revised submission

**Verdict: B — Near ready for a focused theory submission.** The review's P0 and P1 items have substantive fixes, not only softer wording. The broader research program remains incomplete. This is an internal adversarial self-review of the revised artifacts, not external peer review or a second independent human assessment.

## Did the revision solve the original concerns?

**Correctness and proof completeness.** The 59 reviewed results retain their statements and supplied proofs. The main all-budget rates agree with the supplement and final analytic figure. The cubic rate has denominator sqrt(p), with the additional logarithmic multiplier; the residual-fit risk proof is distinct from interval midpoint behavior. R1 is new, has a complete elementary pathwise proof, and does not rely on a successful pilot. The public API preserves interval endpoints in paired RNG checks. No central mathematical defect was identified in this revision audit. The machine checks verify implementations, identities and artifacts, not a theorem prover's formal derivation.

**Coverage bookkeeping.** The genuine S03_007 miss now remains a miss; two paired 90% summaries change, with one underlying observation. Strict and bounded-ULP comparisons are both retained. There is no target-proportional statistical tolerance. One-ULP structural endpoints are not mislabeled as substantive undercoverage. Re-evaluation covers every saved interval case and uses the same observations, so it does not add Monte Carlo information.

**Ablation and budget confounding.** The new fixed-M design isolates signal from the supplied class. Bias-only removal freezes the candidate choice. Pure fallback removal uses the saved tangent candidate and retains both calibrated intersections. Quantile-only removal changes only its critical value. The revised conclusion is weaker and more accurate: bias removal is irrelevant where fallback dominates, while the historical combined diagnostic fails dramatically at a weak nonzero signal. No attempt is made to attribute that combined failure uniquely to the bias term. No-intersection diagnostics are retained separately.

**Risk versus length.** The raw midpoint losses remain visible. The new companion makes the observed catastrophic failure disappear on the same data and supplies uniform noise-scale risk. It does not prove the desired tau² r/p pointwise squared-risk order. That stronger interpretation is explicitly excluded in the abstract's scope, theorem interpretation, implementation and discussion. The correction adds no new signal requirement, but still requires a valid supplied structural bound and Gaussian direct scale.

**Computation.** The paper no longer permits a binary numerical search to stand in for the ideal high-dimensional optimizer. V02 holds loading, direction, budget class and tolerance fixed; seven of 600 solves reach tolerance, 593 do not. Unresolved intervals and gaps are retained. A guarded float64 certificate is not formal interval arithmetic. Fresh full-input, diagonal-access and allocation accounting prevents an O(p)-access claim from being mistaken for O(p) storage of an explicitly supplied tensor.

**Baselines and assumptions.** The XCH implementation matches the tensor-PCA procedure's initialization/update/projection structure, and source locations and variance construction are documented. Case-level regularity is not certified simply from a large amplitude. Strong-signal comparator/oracle lengths remain smaller than the finite-sample certificate. V03/V04 test actual available refinements, including correlated coordinates, finite-variance heavy tails, small chi-square degrees of freedom, and deliberate corruption-cap failure. Favorable coverage is not treated as proof of a theorem outside its assumptions.

**Presentation and internal consistency.** The main paper presents a single all-budget result and its mechanism, followed by computational/loading/adaptation scope and new empirical evidence. Preliminary bounds remain in the full technical supplement as ingredients and comparisons. Numerical claims are generated from checked summaries; the abstract was written after those results stabilized. The notation dictionary and cross-reference checks cover active sources. Figures use vector formats, explicit analytic-versus-empirical labels, dual visual encodings and reported uncertainty. The historical drafts and independent review remain preserved.

## Residual weaknesses and classification

| Item | Classification | Consequence / next action |
|---|---|---|
| Efficient fixed-cap diffuse weak-signal minimax computation | FUTURE WORK for the focused statistical paper; SUBMISSION RISK for a computational-method claim | No general implemented optimizer. A computationally optimal-method framing would still require major work. |
| General arbitrary-loading and intermediate growing-cap rates | FUTURE WORK | Matching special regimes are substantial but not a complete characterization. Keep dimension/rank constants explicit. |
| Complete pointwise/TT theory and optimal SNR | FUTURE WORK | P1 is a strong saturated Tucker length theorem. R1 does not establish pointwise minimax squared risk. |
| Narrow loading and ideal optimal procedure | SUBMISSION RISK | A reviewer can reasonably question breadth and practical impact. The defensible response is the full-data cubic/all-budget distinction, not a claim that the generic machinery is new. |
| External novelty priority | SUBMISSION RISK | A targeted specialist and latest-version citation check remains advisable. Internal source comparisons do not certify priority. |
| Conservative P1 and robust calibration constants | ACCEPTABLE LIMITATION | State the actual signal/budget/block conditions and retain conservative results. Do not claim optimal thresholds or leading constants. |
| No defensible real-data application | ACCEPTABLE LIMITATION for a theory paper; unresolved broader project work | Do not invent independent units or known bounds. A future application needs its own sampling/target justification. |
| Finite Monte Carlo precision and float64 comparisons | ACCEPTABLE LIMITATION | Wilson intervals, raw rare losses, strict counts, numerical gaps and scope statements are retained. No formal arithmetic claim. |
| Venue formatting, authorship and final citation preparation | ACCEPTABLE LIMITATION / pre-submission task | The generic submission draft must be adapted to the selected venue after author decisions. No submission was made. |

No known **BLOCKING ISSUE** remains for the specifically framed theory manuscript after the final artifact checks. This does not mean the general open problems are resolved. If the intended contribution were a complete efficient, arbitrary-loading, all-rank and pointwise-adaptive method, the appropriate verdict would remain **C**, because those claims are not established.

## Final readiness checkpoint

| Question | Assessment |
|---|---|
| Are the central results believed correct? | Yes, within stated assumptions; no central defect found in the supplied derivations and dependency audit. |
| Are main proofs complete? | Yes: all 59 retained results plus R1 have complete supplied derivations and explicit internal status. |
| Are assumptions explicit and justified? | Yes; known norm/scale, supplied caps, fixed versus growing constants and pointwise geometry are visible. Weakenings and failed proof steps are documented. |
| Is the theoretical contribution substantial? | The full-data cubic harmonic lower bound and all-budget residual geometry provide a coherent specialized contribution. Broader journal impact remains a judgment call. |
| Do simulations test the theory? | They test executable guarantees, calibration, pointwise scale and limitations. They cannot empirically demonstrate attainment by the unimplemented ideal optimizer. |
| Are comparisons fair? | Common observed data, paired pilots for ablations, explicit oracle access and comparator eligibility; no claimed finite-case XCH theorem certification. |
| Is real-data inference valid? | No application is claimed. The broader real-data task remains unresolved. |
| Is the narrative synchronized? | Yes: the central rates, computational limits and R1/P1 distinction agree across the current documents. |
| Can results be reproduced? | Seeds, complete configurations, raw endpoints/estimates, code, dependencies, source manifests and rebuild commands are included. New and saved evidence are separated. |
| Strongest remaining criticism? | The optimal method is ideal and loading-specific; a specialist must judge whether the tensor likelihood geometry is sufficiently novel and broad for the selected journal. |

The move from the previous C verdict to B is justified by numerical correction, a new proved scalar method, controlled experiments and an integrated submission. It is not justified by resolving the four general theory problems, which remain open.
