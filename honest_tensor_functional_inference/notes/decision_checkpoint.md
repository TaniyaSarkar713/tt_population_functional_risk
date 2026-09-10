# Final research decision checkpoint

Date: September 9, 2026. This evaluates the delivered working draft, not a hypothetical completed minimax paper.

## Recommendation

**Promising — theory requires further work.** Proceed with a focused theoretical investigation of the full-tensor functional-length problem. Do not submit the present draft as a completed solution to honest inference across unknown Tucker/TT ranks. The current threshold construction alone is incremental; the explicit honesty-class separation is the main candidate contribution, and its novelty remains subject to deeper reduction checks against general nonconvex functional theory.

The delivered artifact is a complete working research note: a statistical formulation, six proved propositions/theorems with full derivations, an exact diagonal-image lemma, a literature assessment, simulations and a manuscript. “Complete working draft” does not mean that the original broad research program or every candidate theorem has been solved.

## Answers to the requested checkpoint

**Novelty — what exactly is potentially new?** The concrete joint-constraint comparison for an orthogonal tensor contrast: at fixed tensor order K>=3, fixed caps and M=tau sqrt(p), an interval honest on the full joint Tucker/TT cap class has length o(tau), whereas every interval honest on the enlarged class retaining one unfolding constraint has expected length at zero at least c_alpha tau. No equivalent explicit statement was found in the inspected sources. This does not certify priority. Nonlinear-versus-affine advantage, weak-rank inference, thresholding, the 2/K exponent, and mixture testing are already known ideas.

**Mathematical contribution — what was established?** Complete finite-dimensional derivations are supplied for T1 diagonal compressibility; T2 honest interval; T3 affine-radius obstruction; T4 one-unfolding expected-length obstruction; T5 their strict asymptotic separation; T6 a lower bound inside the joint class. A reverse construction also proves that the rank-one diagonal image is exactly an ell_(2/K) ball. These are checked working derivations, not independently refereed proofs. The audit does not justify calling all six results new to the literature; T5 is the strongest candidate new tensor specialization.

**Improvement — which guarantee changes?** Let beta=(K-2)/(2K), and J be the explicit cap factor. Two precisely delimited comparisons hold:

$$\begin{array}{rcl}
\text{fixed-radius affine CI on the joint class: } |C|\gtrsim\tau
&\longrightarrow&
\text{nonlinear honest CI: } |C_*|\le2\tau J^{1-1/K}\{8\log(2p/\alpha)/p\}^{\beta},\\
\text{any CI honest on one-unfolding relaxation: } E_0|C|\gtrsim\tau
&\longrightarrow&
\text{joint-class honesty: } |C_*|=o(\tau).
\end{array}$$

The first changes the procedure class while holding the parameter class fixed. The second changes the honesty class while allowing arbitrary procedures. Neither is a minimax improvement over all existing tensor inference methods. Strong-signal oracle intervals are not dominated. Matricization does not discard data.

**Generality.** The mathematics is independent of LLMs. It concerns real Gaussian tensor means and prescribed orthogonal contrasts. It is not a random-design regression, missing-data, heteroskedastic, dependent or contaminated-data theorem. Actual rank is unknown and may be weak; the procedure uses supplied caps and does not adapt its radius to actual rank.

**Simulation validation.** There are 175 configurations with 2,000 replications each, totaling 350,000 simulated tensor-observation replicates, generated through their exact required marginals. In the 172 Gaussian configurations, selected coverage ranges from 0.9975 to 1. The deterministic length ratios show the K>=3 decay and the K=2 control. The weak-second-component experiment shows cap-based coverage and the absence of rank adaptation. Variance contamination gives selected coverage 0.383 at the tested zero signal, ruling out a robustness narrative. Exact binomial uncertainty and configuration-level bias/RMSE are saved. Monte Carlo cannot verify uniform coverage or theorem novelty.

**Remaining weakness.** The within-class lower scale is tau sqrt(log(p)/p), while the upper scale is tau(log(p)/p)^beta. The polynomial ratio is (p/log(p))^(1/K). The estimator ignores off-diagonal information, the rank factor is loose, the loading is special, M and tau are known, and empirical coverage is highly conservative. No real-data model has been justified. These are substantive limitations, not editing tasks.

## Scorecard: 1 low, 5 high

Scores are research judgments rather than acceptance probabilities. “Sharp full-tensor theory” and “honest actual-rank adaptation” columns assess potential if solved; they are not delivered results.

| Criterion | Current separation note | Sharp full-tensor minimax project | Honest actual-rank / loading adaptation |
|---|---:|---:|---:|
| Statistical depth | 3 | 5 | 5 |
| Theoretical depth | 2 | 5 | 5 |
| Apparent novelty | 3 | 4 | 3 |
| Generality beyond LLMs | 5 | 5 | 5 |
| LLM/AI relevance under current model | 1 | 2 | 2 |
| Technical feasibility | 5 | 2 | 2 |
| Potential for substantial theorems | 3 | 5 | 5 |
| JASA/JRSS-B/Biometrika fit | 2 | 4 | 4 |
| Annals of Statistics potential | 1 | 4 | 4 |

The original broad idea gains precision from the separation, but not enough technical depth for an Annals-level claim. No inference about the user's personal research capacity is made; technical feasibility refers to the mathematical task.

## Venue assessment

| Venue | Present assessment | What is missing |
|---|---|---|
| Annals of Statistics | No-go in current form | A sharp and general statistical theorem: matching minimax length, an informative nonconvex functional geometry, or a deep adaptation/impossibility characterization beyond one special contrast |
| JASA, Theory and Methods | Not ready | A substantial methodological/inferential advantage over the best relevant procedures, stronger calibration and a credible measurement model; a general theorem could compensate for limited application scope |
| JRSS-B | Not ready | A broader inferential principle with useful calibration, strong comparative evidence and substantially more than a classical sequence reduction |
| Biometrika | Potential concise-note direction, still not ready | A sharp, elegant central result with a clear novelty claim; present polynomial gap and the amount of elementary machinery weaken the case |
| Bernoulli | Possible after stronger probability/statistical theory | Matching lower/upper bounds or a genuinely informative tensor testing geometry; correctness of a conservative bound alone is insufficient |
| Statistica Sinica | Possible after sharpening | Clear nonincremental novelty, stronger finite-sample usefulness, and a fuller comparison with cap-based matrix inference |
| COLT | Not ready | General nonconvex functional complexity or a proved statistical/computational distinction; no computational lower bound is supplied |
| NeurIPS / ICML / AISTATS theory | Not ready as an LLM paper | A broader theoretical question or a justified modern learning experiment; tensor notation and a fast scalar formula do not by themselves supply ML novelty |

## Skeptical reviewer attack and response

| Objection | Assessment | Defensible response / required work |
|---|---|---|
| “This is Gaussian sequence thresholding on an ell_q ball.” | Correct for the diagonal-only method; exact image lemma proves it | Claim no new thresholding estimator. A stronger paper must use or characterize full-tensor information |
| “Nonconvex functional theory already explains the affine failure.” | Correct | Present T3 as an explicit comparison, not a new general mechanism; check whether the entire specialization is already available |
| “The unfolding lower bound is a familiar spiked-matrix mixture.” | Correct about the tool | The candidate contribution is its coupling to a joint-tensor upper bound for the same contrast. The coupling may still be too modest |
| “The estimator does not adapt to unknown rank.” | Correct if adaptation means shorter actual-rank-dependent width | Describe union honesty under a supplied cap; no stronger wording is used |
| “Your best competing method is a weak baseline.” | Partly rebutted | T3 compares all deterministic-width affine intervals; T4 compares all relaxed-class intervals. These are genuine classes, but unrestricted full-tensor competitors remain unresolved |
| “The real minimax rate is much faster.” | Unresolved and plausible | Show the bracket plainly. Investigate a procedure using off-diagonal observations and a matching lower bound |
| “Known M, tau and special L make the setting artificial.” | Substantive limitation | Establish a meaningful measurement application or a loading-geometry theorem; do not plug in unvalidated bounds |
| “Coverage 100% means the intervals are inefficient.” | Strong criticism of calibration | Length can still beat the specified baselines, but there is no efficiency claim. Better calibration is a research target |
| “The LLM framing is superficial.” | Correct under the present model | Omit an LLM experiment; do not use it as a novelty argument |
| “Six theorems overstate the amount of new theory.” | Fair presentation concern | Treat T1–T4 and T6 as supporting results; T5 is the single central comparison, not six independent innovations |

## Meaningful next theorem targets and stopping rules

1. **Sharp rank-one functional length.** Determine r_0(K,p,M,tau,alpha) such that L_0(Theta_1) is bounded above and below by constant multiples of r_0, and distinguish it from worst-case expected length. The present bracket is the starting information. Do not choose the upper rate merely because it is available.
2. **Value of off-diagonal observations.** Compare the full experiment with the diagonal marginal, whose parameter image is exactly an ell_(2/K) ball. Prove either an improved full-data interval or a lower bound showing that this extra information cannot improve the relevant criterion. This directly tests whether the tensor structure adds statistical content beyond approximate sparsity.
3. **Loading-dependent criterion for a joint-constraint advantage.** For prescribed L, characterize when L_0(Theta_joint,L) / L_0(Theta_one-cut,L) tends to zero. A useful theorem must identify an interpretable geometry and include cases with and without a gain; an arbitrary new loading example is insufficient.
4. **Honest adaptation within the outer class.** Construct intervals honest over a supplied larger cap, and derive attainable and impossible expected lengths on smaller-rank or stronger-signal submodels. Do not promise tangent-oracle length at every boundary. Testability over a nonconvex union, not rank consistency alone, must control the result.

Start with K=3, rank one, known M/tau and the same loading. Seek a full-data upper bound or a stronger mixture lower bound before adding regression, contamination or LLM dependence. If the exact diagonal reduction and existing nonconvex theory account for all attainable improvements and no full-tensor insight emerges, classify the current standalone contribution as **Incremental — reformulate**, preserve the note, and pivot the main paper. Adding more simulations or terminology would not change that decision.
