---
title: "Scientific extensions and an executed subject-level application"
author: "Tensor functional inference: research supplement"
date: "14 September 2026"
geometry: margin=0.8in
fontsize: 11pt
---

# Scientific progress and scope

The new work develops all-budget orthogonal-loading envelopes, sharp rates for new slow-decay profiles, a scalar safeguard with strong-pointwise squared-risk guarantees, general Tucker and TT implementations, and a sharp off-tangent rank-one interval. It also implements the exact diagonal sparse submodel across intermediate caps and executes a public EEG analysis with measured projection bias. Full proofs are in `theory/results.md` and `paper/technical_supplement.pdf`.

The general polynomial fixed-cap weak-signal minimax optimizer remains open. So do exact rates for every loading and every intermediate Tucker/TT cap, and a complete pointwise theory. These results are substantive restricted advances, not a claim that the full research program is complete. The reviewed submission in `review_revision/` and all earlier experimental results are preserved.

| Result | Before this stage | Scientific advance | Remaining boundary |
| --- | --- | --- | --- |
| AB1 | General orthogonal profiles unmatched | All-budget upper/lower proxies within 1 + nu log log(ep) | Ideal prefix optimizers; nonorthogonal tensors remain general |
| AB2 | Fixed power-decay weights only | Sharp logarithmic-decay profiles, all budgets | Critical exponents and varying-exponent constants |
| P2 | R1 protects only noise-scale MSE | Pre-intersection scalar with uniform and strong-pointwise risk | No weak-signal minimax estimator |
| P3 | Strong diagonal Tucker length | Arbitrary-core Tucker and single-cut TT length; local risk lower bounds | Strong signal, saturation/alignment, nonoptimal thresholds |
| P4 | Off-tangent points excluded by alignment | Four-entry rank-one interval, sharp tau^2/a expected length | Prespecified minor and axis base point |
| D2 | General intermediate caps unmatched | O(p) interval/estimator on exact sparse diagonal model | Additional model restriction; classical sparse rate |
| B1/B1a | No executed defensible application | Bounded subject target; fixed-stratum bias calibration | Subject independence; no Gaussian low-rank validation |

# Computation and rate interpretation

For decreasing absolute orthogonal weights $w_i$, let $F_s=\sqrt{s}r_K(s,M,\tau)$. The new Abel upper proxy is $A(w)=\sum_s(w_s-w_{s+1})F_s$ and the compensated-prefix lower proxy is $B(w)=\max_s w_sF_s$. The exact proxy inequality is $B\le A\le B[1+\log(F_p/F_1)]$. Statistical comparison constants also depend on the fixed caps, tensor order, and confidence. These proxies can be evaluated quickly; their attaining confidence-set projection and residual fit are still ideal constructions. No plotted envelope is an observed output of a high-dimensional minimax optimizer.

For weights $w_i=c[\log(ei)]^{-\beta}$, the complete proof supplies all-budget phase formulas. In the large-budget cubic regime $M\ge\tau\sqrt p$ the rate is $c\tau\ell_p^{3/2-\beta}$ for fixed $0<\beta<3/2$ away from critical cases, and $c\tau$ for $\beta>3/2$. In higher order the transition is at $\beta=1/2$. The full budget dependence and excluded boundaries must be retained when applying these formulas.

The general Gaussian implementation accepts unequal dimensions, arbitrary loadings, and supplied Tucker or TT caps. Its SVD candidates have explicit unresolved-subspace bias bounds; a pilot chooses a radius before independent artificial-split validation. This gives uniform honesty, including zero and undersaturation, but can fall back to the noise-scale direct candidate. The new scalar protects the candidate center before narrow-interval intersection. It avoids turning rare empty intersections into enormous scalar errors. A distinct four-entry ratio interval exploits a rank-one minor identity at off-tangent points, with honest denominator fallback at weak signals.

The analytic grid contains **504 calculations**. Its largest observed Abel/prefix proxy ratio is **4.402**. This finite grid does not establish sharpness or rule out worse profiles.

![All orthogonal profiles have a controlled rate bracket. Shading shows the Abel upper and prefix lower proxies for normalized logarithmic weights in order three, not simulated confidence intervals. The right panel varies the norm budget at 65,536 loading terms; critical beta=1.5 is displayed as an unmatched bracket.](../figures/loading_envelopes.pdf){width=100%}

The full public API was also timed on fixed observations, separately from Monte Carlo coverage runs. Each row reports the median of three calls with one library thread, including loading SVDs and artificial splitting. Tensor storage is input-array storage only, not a peak-memory measurement. These timings demonstrate tractability of the cap-valid procedure, not attainment of the ideal weak-signal rate.

| Geometry | p | Cap | Input entries | Input MiB | Median seconds |
| --- | --- | --- | --- | --- | --- |
| tucker | 32 | 1 | 32,768 | 0.25 | 0.0048 |
| tucker | 64 | 1 | 262,144 | 2.00 | 0.0473 |
| tucker | 128 | 1 | 2,097,152 | 16.00 | 0.7433 |
| tt | 8 | 1 | 4,096 | 0.03 | 0.0010 |
| tt | 16 | 1 | 65,536 | 0.50 | 0.0215 |
| tt | 24 | 1 | 331,776 | 2.53 | 0.1394 |

# New simulations

All configurations and seeds were saved before their own Monte Carlo draws. Methods are paired on each observation where appropriate. New results are separate from earlier saved experiments. Coverage intervals use Wilson binomial limits; MSE and width Monte Carlo errors use the empirical standard deviation across independent data sets. MSE error bars can be unreliable for very rare losses, so maximum losses and individual outcomes are retained. Runs use one numerical-library thread.

This stage generated **109,000 independent Monte Carlo data sets in 92 configurations**, plus 504 analytic calculations. The main grid contains 80 configurations and 71,000 data sets. Five follow-ups add 10,000, and seven minor configurations add 28,000. These counts do not include the earlier 87,200 revision data sets or 1,084,640 preserved pre-review data sets.

## Strong and weak tensor means

Strong cases use caps one and two, known rotated flat loadings, Tucker order three and TT order four. The Tucker rank-two core has nonzero off-diagonal entries. Signal levels deliberately satisfy the conservative sufficient theorem inequalities; these runs do not establish optimal SNR thresholds. Zero, weak and strong-undersaturated cases test the same public API. A separate dense TT-core experiment uses unequal dimensions (4,5,4,3), caps (2,3,2), and an arbitrary loading aligned with one cut.

| Geometry | p | Cap | Draws | Coverage | Width | Safe MSE (MCSE) | Direct MSE |
| --- | --- | --- | --- | --- | --- | --- | --- |
| tucker | 8 | 1 | 1000 | 0.973 | 3.007 | 0.2488 (0.0108) | 1.041 |
| tucker | 8 | 2 | 1000 | 0.981 | 3.794 | 0.5236 (0.0228) | 0.978 |
| tucker | 16 | 1 | 500 | 0.974 | 2.273 | 0.1243 (0.0078) | 0.990 |
| tucker | 16 | 2 | 500 | 0.968 | 3.191 | 0.2439 (0.0151) | 1.035 |
| tucker | 32 | 1 | 500 | 0.968 | 1.647 | 0.0582 (0.0035) | 1.045 |
| tucker | 32 | 2 | 500 | 0.980 | 2.399 | 0.1245 (0.0083) | 0.932 |
| tt | 4 | 1 | 1000 | 0.970 | 3.204 | 0.4923 (0.0228) | 0.971 |
| tt | 4 | 2 | 1000 | 0.966 | 3.893 | 0.9637 (0.0426) | 1.011 |
| tt | 8 | 1 | 1000 | 0.964 | 2.261 | 0.2490 (0.0111) | 0.982 |
| tt | 8 | 2 | 1000 | 0.954 | 3.011 | 0.4899 (0.0239) | 1.005 |
| tt | 12 | 1 | 500 | 0.946 | 1.811 | 0.1670 (0.0104) | 1.087 |
| tt | 12 | 2 | 500 | 0.962 | 2.525 | 0.3250 (0.0190) | 0.957 |

![The protected scalar follows the strong-pointwise rank-to-dimension scale in these favorable cases. Error bars are 1.96 Monte Carlo standard errors for root MSE by the delta method, with 500 or 1,000 paired draws per configuration. Dotted sqrt(2r/p) curves are limiting split-noise references, not exact finite-sample predictions or fitted slopes.](../figures/pointwise_risk.pdf){width=100%}

The same-interval midpoint and direct-fallback ablations use the **new pilot calibration**. They are not claimed to be exact reproductions of the preceding R1 algorithm. Empty intervals remain in coverage and loss accounting.

| Case | Geometry | p | Empty | Midpoint MSE | Fallback MSE | P2 MSE |
| --- | --- | --- | --- | --- | --- | --- |
| E008 | tucker | 16 | 2 | 25081383.1 | 0.1880 | 0.1243 |
| E014 | tucker | 32 | 1 | 179868948.2 | 0.0955 | 0.0582 |
| E026 | tt | 8 | 1 | 22117527.0 | 0.2523 | 0.2490 |
| E032 | tt | 12 | 2 | 968116159.7 | 0.2130 | 0.1670 |

The dense-core TT follow-up has core loading norm 0.2, safe MSE **0.08057**, direct MSE **1.02863**, mean width **1.401**, and coverage **0.9635** over 2,000 draws. At strong undersaturated means the general procedure selects split-direct throughout; its scalar MSE is about two rather than the original direct estimator's one. This is the real cost of artificial splitting when the geometry cannot be certified.

## Intermediate caps: a restricted positive result and a negative control

The exact sparse diagonal experiments use dimensions 256, 4,096 and 65,536, caps on both sides of square-root dimension, and three norm-budget multipliers. Equal positive active entries near the hard threshold stress truncation bias. D2 selects structural, direct or threshold intervals from deterministic radius bounds. It is sharp only under the exact diagonal-mean restriction; tensor rank one by itself does not imply this restriction.

![The implemented sparse-diagonal procedure retains bounded rate-normalized loss and width across the tested caps. These are exact-diagonal means at the largest budget multiplier, with 1,000 draws per case; MSE error bars are 1.96 Monte Carlo standard errors transformed by the delta method. This figure does not match the unresolved intermediate-cap rates of the full Tucker or TT model.](../figures/diagonal_caps.pdf){width=100%}

A deliberately invalid use on the diagonal of a **dense rank-one full tensor** gives coverage **0.000** and MSE **15527.0** over 2,000 draws. The threshold interval's mean width is 0.997. This is a counterexample to extending D2 to the full tensor class, not a failure of its stated theorem. The off-diagonal means exist mathematically; no enormous full tensor is allocated because this procedure accesses only the diagonal.

## Off-tangent rank-one points

The P4 target is diagonally opposite a prespecified anchor in a two-by-two rank-one minor. A corresponding supplied unfolding cap of one suffices for honesty, even with larger caps elsewhere. At the axis mean its first derivative vanishes; two small factor rotations produce the target only at second order. The interval handles a denominator whose confidence interval crosses zero by returning to a globally valid range/direct intersection.

| a/tau | Draws | Coverage | Mean width/tau | Width x a/tau^2 |
| --- | --- | --- | --- | --- |
| 0.0 | 4000 | 0.9750 | 1.90002 | 0.000 |
| 2.0 | 4000 | 0.9748 | 4.44889 | 8.898 |
| 5.0 | 4000 | 0.9742 | 4.27668 | 21.383 |
| 10.0 | 4000 | 0.9778 | 2.47822 | 24.782 |
| 30.0 | 4000 | 0.9855 | 0.70655 | 21.197 |
| 100.0 | 4000 | 0.9942 | 0.19852 | 19.852 |
| 1000.0 | 4000 | 0.9992 | 0.01952 | 19.515 |

![The minor interval exhibits inverse-anchor expected length at strong axis means. Each point uses 4,000 draws; error bars are 1.96 Monte Carlo standard errors. The slope-minus-one guide is anchored to the first plotted measured width, and the scaled panel shows the approach to a constant. The sufficient theorem condition is a/tau at least 4 z_(1-alpha/12), so the smallest plotted point is a transition diagnostic.](../figures/minor_pointwise.pdf){width=100%}

## Projection-bias calibration and coverage screen

A bounded Bernoulli-subject experiment chooses a shrinkage map on an independent pilot, then compares signed residual calibration with the uncorrected projected interval. Both target the same original bounded mean when assessing coverage. The latter is deliberately labeled a diagnostic: its interval is valid for the projected mean, not automatically for the original mean.

| Calibration n | Validation n | Corrected coverage | Corrected width | Uncorrected target coverage |
| --- | --- | --- | --- | --- |
| 100 | 100 | 1.0000 | 1.611 | 0.9555 |
| 1000 | 1000 | 1.0000 | 0.327 | 0.0000 |

Among 91 in-model proposed-procedure coverage checks, 0 one-sided binomial tests reject nominal 95% coverage after Holm correction at family error 0.05. The smallest unadjusted p-value is 0.08673. This is a finite diagnostic, not proof of uniform coverage. The deliberate diagonal violation and uncorrected projection diagnostic are excluded from this in-model screen and reported separately.

# Real-data analysis: EEG subject responses

## Source, units and estimand

The full [UCI EEG Database](https://archive.ics.uci.edu/dataset/121/eeg%2Bdatabase), credited to Begleiter (1995), DOI 10.24432/C5TS3D, is distributed under CC BY 4.0. Its training and test versions reuse subjects, so they were not treated as independent samples. We downloaded the full archive and processed the subject files directly. The source, archive/subject/trial checksums, preserved metadata and parser are included in `real_data/`. Raw data remain in the documented temporary download cache and can be downloaded again.

The protocol was hashed before raw download. It fixes the nonmatching-minus-matching S2 response at CZ and PZ, averaged over recorded sample indices 64--127, after clipping each voltage to +/-100 microvolts. We do not equate those indices to a verified post-stimulus physiological window. A subject is one sampling unit: all valid trials are averaged within condition before averaging across subjects. The resulting tensor has condition, recorded-channel and time-bin axes. Auxiliary channels remain in the tensor demonstration; they do not enter the primary contrast. This is an observed-response estimand after clipping and trial-quality filtering, not a causal stimulus effect or diagnostic claim.

Before calculating contrasts, the sampling plan was refined because the source describes separately recruited groups. The primary target is the fixed study-mixture of two within-group means, with archive weights 77/122 and 45/122. Independent subjects with a common distribution **within each group** are assumed. Disease prevalence is not estimated. Family identifiers and sampling probabilities are unavailable, so independence and population representativeness cannot be verified from this archive. Familial dependence would invalidate the independent-subject intervals; the cohort descriptive mean remains descriptive without that assumption. The amendment, its timing and its design-based reason are recorded separately from the immutable initial protocol.

The actual archive contains **11,074 trial files**, of which **10,962** pass the recorded checks. Exclusions are 95 error-flagged trials and 17 files without a recognized condition. All **122 subjects** retain all three conditions. Valid trial counts range from 29 to 119; trials are never counted as independent inferential replications. At the primary clipping level, 0.0494% of retained voltage values are clipped. Missing/error trials may be informative: the target explicitly concerns the retained recorded-response process, and no missing-at-random recovery of unobserved responses is asserted.

## Results and uncertainty

The primary finite-sample interval uses the two-sided empirical Bernstein bound separately by group and combines them at the fixed mixture weights. Its variance and range terms are given in B1/B1a. We additionally report a stratified approximate t interval using a Welch-Satterthwaite degrees-of-freedom calculation. It relies on an approximation and is not promoted to a finite-sample result. Clipping sensitivities change the estimand and are exploratory, without a simultaneous confidence claim.

| Clip (+/- microvolts) | Cohort mean | Stratified 95% EB | Approximate 95% t | Calibrated projection |
| --- | --- | --- | --- | --- |
| 50 | 2.210 | [-38.362, 42.782] | [1.746, 2.675] | [-100.0, 100.0] |
| 100 | 2.222 | [-77.920, 82.364] | [1.739, 2.706] | [-200.0, 200.0] |
| 200 | 2.196 | [-157.057, 161.449] | [1.686, 2.707] | [-400.0, 400.0] |

At the primary threshold the sample standard deviation of subject contrasts is 2.691 microvolts. The descriptive mean is 2.222; its conservative finite-sample interval includes zero. The approximate interval excludes zero, but that stronger empirical conclusion rests on its approximation and subject sampling assumptions. We make no claim of clinical utility, causality, or population-generalizable disease differences.

![Finite-sample uncertainty is much wider than the approximate t interval. Left: the 122 subject contrasts at the prespecified 100-microvolt clipping threshold, grouped by recorded recruitment code; black segments mark group means. Right: the fixed-mixture direct empirical Bernstein (EB), approximate t, and independently bias-calibrated projection intervals, with the full certified ranges retained. Real-data coverage is not observable; these intervals refer to different uncertainty assumptions, with sample allocation stated in the text.](../figures/eeg_intervals.pdf){width=100%}

## What the tensor demonstration does and does not show

The stratified split allocates **30 pilot, 46 calibration and 46 validation subjects**. Selection using only the pilot chooses Tucker caps **(3, 8, 8)** from the prespecified list. The pilot reconstruction residual is **4.74%** of its Frobenius norm. This is a fitted pilot property, not a certificate of exact low population rank.

The projected scalar is clipped to the same known response range. A held-out calibration sample estimates its signed bias relative to the original contrast; the validation sample estimates its projected mean. Four group-by-component bounds share the confidence budget. The resulting certified interval spans the entire feasible target range at every clipping sensitivity. Thus this application supplies **no demonstrated precision advantage** for the tensor procedure. The correction is honest under the stated subject model but costly with this sample size. Direct all-subject and direct nonpilot comparisons, all split memberships and uncorrected bias diagnostics are retained in machine-readable outputs. The protocol's nested projection choices favor the largest cap under its residual-loading criterion; the procedure should not be described as recovering the true rank.

The real-data analysis addresses the absence of an executed application with an explicit target, sampling units and uncertainty. It does not validate iid entrywise Gaussian noise, known norm/noise bounds, exact population rank, the ideal minimax optimizer, or the strong-pointwise sufficient conditions. A scientific application demonstrating those original assumptions and an efficiency gain remains a separate task.

# Scientific audit and readiness

The supplied arguments distinguish rate proxies from computable intervals; fixed from growing cap constants; pointwise length from local minimax risk; and known Gaussian noise from bounded subject data. The negative diagonal example makes the new submodel restriction operational. Projection-bias calibration is tested against an uncorrected counterexample, and the application retains the uninformative certified result.

The central remaining concerns are still substantive. General efficient weak-signal minimax computation is unresolved. AB1 leaves a doubly logarithmic gap in general orthogonal profiles, and critical exponents and general nonorthogonal profiles remain unmatched. D2 does not close the full-model intermediate-cap problem. P3's separation/alignment conditions are sufficient and conservative; P4 covers one prespecified second-order geometry. General weak, undersaturated and higher-order pointwise transitions remain open. Family-level dependence and representative sampling remain unverified in the public application.

The expanded research program receives internal verdict **C: additional theoretical or empirical work required** for the original broad goals. The preserved focused paper's earlier B verdict is not retroactively changed. The supplement can support a focused theory submission after independent proof and priority checks, but a claim to have solved the general program would be premature. Bernoulli or a focused statistics-methodology venue is a more defensible starting discussion than claiming immediate readiness for a broad Annals/JASA minimax-and-application paper; a final venue decision needs external assessment of novelty and significance.

Fresh verification includes **40,553 finite mathematical/implementation checks**, all passing. These are grouped into independent inequality, projector, TT-rank, clipping, sparse-integral and minor checks, not 40,553 independent theorem proofs. Numerical library versions are Python 3.9.6, NumPy 2.0.2, SciPy 1.13.1. Rebuild commands and allocation scope appear in README.md; the validation artifact records the final file hashes and preservation check.
