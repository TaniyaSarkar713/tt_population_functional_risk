---
title: "Efficient one-cap minimax inference and new tensor rate frontiers"
subtitle: "Research progress, executed experiments, and unresolved generalizations"
date: "2026-09-15"
geometry: margin=0.85in
fontsize: 11pt
---

# Scientific advances and their scope

The new results resolve three substantial parts of the open program. A spectral
clipping interval is computationally efficient and minimax in rate for **every
loading, norm budget, and rank cap when one unfolding is constrained and all
other caps are unrestricted**. A multiscale rank-one mixture proves exact rates
up to constants for **every orthogonal loading profile in tensor order four and
higher**, under fixed positive Tucker or TT caps. A data-selected anchor gives
globally honest intervals with the **optimal coordinate-wise pointwise hierarchy
at unknown rank-one axis signals**. A fourth proposition explains why
deterministic affine intervals cannot attain the ideal fixed-cap diffuse rates.

Complete proofs and parameter-space definitions are in the accompanying
`technical_supplement.pdf` and `theory/results.md`. The new results are internally
labelled PROVED; they have not received independent peer review or formal
verification. Minimax claims are up to constants, not exact finite-sample constants.

The general efficient optimizer under several restrictive caps is still absent.
The preserved binary optimizer is an exponential benchmark. General cubic and
nonorthogonal loading rates, arbitrary simultaneous intermediate growing caps,
and a complete pointwise theory remain open. No experimental success below is
used to claim that those broader questions are closed.

| Result | New conclusion | Boundary |
| --- | --- | --- |
| M1 | Loading SVD + scalar convex solve; full-model all-cap rates | Only one constrained unfolding |
| M2 | Affine constant-radius obstruction at flat loadings | No hardness claim for nonlinear algorithms |
| L3 | Exact Abel-profile rate for every orthogonal loading, all budgets | K at least 4; fixed caps; upper fits ideal |
| P5 | Optimal coordinate lengths at an unknown rank-one axis | Strong enough localization; other points/ranks unresolved |


# Efficient computation and intermediate caps

For the selected unfolding of the known loading, let $\sigma_i$ be its singular
values. At $M>\tau$, the minimax length scale is

$$T_r=\max_{b\ge0,\|b\|_1\le M\sqrt r,\|b\|_2\le\tau}\sigma^Tb
=\min_{t\ge0}\{M\sqrt r\,t+\tau\| (\sigma-t)_+\|_2\}.$$

For $M\le\tau$, use $T_r=M(\sum_{i\le r}\sigma_i^2)^{1/2}$. The squared-error
rate is $T_r^2$. Soft threshold the loading singular values, take the resulting
linear observation, and add the exact rank-constrained bias bound and a Gaussian
quantile. A loading-only comparison with the structural interval protects small
budgets. The scalar estimate has its own squared-bias-plus-variance selection
and structural clipping; it is not defined as an interval midpoint.

The lower bound is a mixture of rank-at-most-r matrices with dense off-diagonal
entries in their singular-vector blocks. It uses all tensor observations after
unfolding. A balanced partition controls the Frobenius norm, while independent
signs yield chi-square divergence at most $\exp(1/62)-1$. No exact-diagonal
restriction, known support, signal separation, or estimated-rank substitution
is used. For flat orthogonal loadings the rate simplifies to
$\min(M\sqrt{r/p},\tau)$ for every cap, including intermediate caps.

The method remains honest if more caps are supplied, but its lower bound does
not transfer to their intersection. At $M=\tau\sqrt p$, all fixed caps allow a
much smaller ideal rate than the noise-scale one-cap rate. M2 shows that merely
optimizing a deterministic affine center and constant radius cannot close this
gap. It does not rule out efficient nonlinear procedures.

The scalar optimizer exposes a feasible dual vector and objective gap. These
are floating-point residual checks, not formal interval-arithmetic certificates.
Preprocessing depends only on the loading and can be reused across observations.
The timings below use one numerical-library thread, medians of three calls,
and full dense input tensors. Input MiB is one array's storage, not peak memory.

| Tensor shape | Entries | Input MiB | Preprocess (s) | Observation (s) |
| --- | --- | --- | --- | --- |
| 16 x 16 x 16 | 4,096 | 0.03 | 0.00073 | 0.00003 |
| 32 x 32 x 32 | 32,768 | 0.25 | 0.00267 | 0.00009 |
| 64 x 64 x 64 | 262,144 | 2.00 | 0.02843 | 0.00094 |
| 32 x 64 x 1024 | 2,097,152 | 16.00 | 0.14210 | 0.01098 |


![Loading preprocessing is reusable. Timings include SVDs and the scalar solve; per-observation timing includes interval and scalar evaluation. Four shapes, three calls per shape, one library thread. These are measured runtimes, not timings of the unresolved multi-cap optimizer.](../figures/computation.pdf){width=80%}

# Exact higher-order loading profiles

For decreasing absolute orthogonal weights, define
$F_s=\min(M,\tau\sqrt{\log(es)})$, $F_0=0$. The exact rate proxy is

$$\mathcal A(w)=\sum_{s=1}^p w_s(F_s-F_{s-1}),\qquad K\ge4.$$

Previously, the lower bound used the largest compensated prefix and left a
possible doubly logarithmic gap. The new prior places one random coordinate in
each of several disjoint groups with entropy scales $1,4,16,\ldots$. Geometric
growth controls the rank-one norm and collision likelihood moments, while all
scales contribute to one common target. Its target is within fixed constants
of the entire Abel sum. This proves the lower bound matching the earlier ideal
prefix upper bound for every profile and every budget.

At the previously critical weights $w_i=c[\log(ei)]^{-1/2}$ the rate is $cM$ for
$M\le\tau$, and $c\tau[1+\log\min\{\log(ep),(M/\tau)^2\}]$ for $M>\tau$.
This includes dimension-dependent normalizations. General cubic profiles still
need a cross-scale harmonic-mixture argument that has not been established.
The easily evaluated proxy is not an implemented attaining interval.

The saved analytic grid contains **120 loading-profile calculations** and **265 cap/budget calculations**. They are separate from Monte Carlo observations. The largest old Abel/prefix ratio on this finite loading grid is 2.204.

![Analytic rate comparisons, not observed interval outputs. Left: normalized logarithmic profiles in order K at least 4 at M/tau = 1000; the new theorem matches the full Abel proxy rather than only its largest prefix. Right: at M/tau = sqrt(p), a single rank cap of one and several fixed caps define different full tensor parameter spaces. Constants are omitted in both rate curves.](../figures/statistical_frontiers.pdf){width=100%}

# Newly executed simulations

This stage generated **320,000 independent full-observation data sets in 160 configurations**, with 2,000 draws per configuration. It includes 81 spectral configurations, 78 correctly specified coordinate configurations, and one deliberate rank-two violation. All seeds and configurations were saved before their draws. Every endpoint, scalar output where applicable, and selected-anchor outcome is retained. Methods use paired observations within a configuration. No earlier Monte Carlo data set or application result is counted as new.

Coverage uses Wilson binomial intervals and the preserved four-endpoint-ULP comparison convention. Strict counts are also stored. One structural-boundary target (F037) is one representable step beyond an SVD-based bound: all 2,000 method counts and 1,890 direct counts differ from strict comparison. This is exposed in `audit/rounding_audit.json`; no target-scaled tolerance or statistical slack is used. These comparisons do not constitute rigorous numerical interval certification.

Among the 159 configurations inside the stated models, observed method coverage ranges from 0.9415 to 1.0000. A one-sided 95% coverage discrepancy screen with Holm correction has **0 rejections**. Such a finite screen is not proof of uniform coverage. Width and MSE uncertainty use empirical Monte Carlo standard errors.

## Dense loadings and the full one-cap mean space

The tensor dimensions are 16 x 16 x 16, the selected mode cap is 1, 4, or 16, and M/tau is 0.3, 3, or 30. Three loading spectra (flat, spike plus tail, logarithmic decay) use dense random singular vectors. Means include zero, a rank-constrained worst-bias direction, and a dense random rank-constrained matrix reshaped as a tensor. Other caps are unrestricted. The direct Gaussian baseline uses the same known structural range and clipping.

The smallest observed spectral/direct mean-width ratio is 0.956. The finite grid therefore shows modest width gains at best, despite the rate-optimal guarantee. The theory does not predict universal improvement in constants. The worst observed scalar MSE divided by its proved upper bound is 1.063; sampling variability can move an empirical ratio slightly above one.

![Executed full one-unfolding cases at the worst-bias mean. Solid lines show the proposed interval, dashed lines the direct interval intersected with the same structural range. Colors indicate supplied rank caps. Each marker uses 2,000 paired observations; error bars are 1.96 Monte Carlo standard errors. The mean does not have exact diagonal support in observation coordinates.](../figures/spectral_performance.pdf){width=100%}

## Pointwise coordinate hierarchy and adaptation

For the full rank-one ball, P5 selects an anchor using an independent artificial pilot. Validation intervals for that anchor and the changed coordinate fibers are combined through a rank-one product identity. A denominator interval crossing zero triggers the honest direct fallback. The original direct interval always bounds the final width. At an axis mean a E_J, coordinate Hamming distance d determines the optimal pointwise rate: tau for d = 0 or 1, and tau^d / |a|^(d-1) for d at least 2. The unknown axis location is never provided to the method.

The sufficient localization condition is |a|/tau at least a constant times sqrt(log(eD)), where D is the number of tensor entries. Honesty does not need this condition. The finite runs use orders 3, 4 and 5, every distance d, and amplitudes 3, 10, 30, 100 and 1,000 with a fixed supplied budget M = 1,000. Additional zero, negative-axis, dense rank-one and rank-two-violation cases probe scope. Slope estimates below use only the two stated levels 100 and 1,000; they are finite-range descriptive contrasts, not estimates of an exact asymptotic exponent from an unlimited sequence.

| Order K | Distance d | Observed slope | MCSE | Limit |
| --- | --- | --- | --- | --- |
| 3 | 2 | -1.009 | 0.003 | -1 |
| 3 | 3 | -2.037 | 0.004 | -2 |
| 4 | 2 | -1.015 | 0.003 | -1 |
| 4 | 3 | -2.024 | 0.004 | -2 |
| 4 | 4 | -3.050 | 0.005 | -3 |
| 5 | 2 | -1.015 | 0.003 | -1 |
| 5 | 3 | -2.032 | 0.004 | -2 |
| 5 | 4 | -3.046 | 0.005 | -3 |
| 5 | 5 | -4.060 | 0.005 | -4 |


![Unknown-anchor coordinate intervals show the hierarchy across Hamming distances d. Each point has 2,000 independent data sets; error bars are 1.96 Monte Carlo standard errors. Dotted segments have the theoretical exponent 1-d, anchored at the last observed point for visual comparison. They are not additional Monte Carlo outcomes or exact predictions of finite-sample constants.](../figures/coordinate_hierarchy.pdf){width=100%}

| Mean type | Amplitude | Coverage | Width | Anchor accuracy |
| --- | --- | --- | --- | --- |
| axis | 0.0 | 0.9720 | 4.48 | 0.0035 |
| axis | -100.0 | 1.0000 | 0.00135 | 1.0000 |
| dense_rank_one | 30.0 | 0.9770 | 1.81 | 1.0000 |
| rank_two_violation | 1000.0 | 0.0000 | 3.83e-09 | 1.0000 |


The rank-two negative control adds a target entry of 5 to a separated axis of amplitude 1,000. It has coverage 0.000, because the rank-one product identity is false. Its narrow or empty intersections are retained, including 1994 empty replacements. This failure prevents extending P5 to a higher-rank honesty class without a new bias argument. No pointwise scalar-risk claim is made for this interval.

# Verification, real data, and remaining work

The newly executed mathematical and implementation suite passes **20,489 finite checks**. These include an independent scalar convex optimizer, feasible dual constraints, exact small sign-mixture likelihoods, greedy norm partitions, compensated multiscale targets, full likelihood collision bounds, affine symmetry, rank-one ratio identities, and pointwise rotation alternatives. The largest relative scalar primal-dual gap is 6.7e-15. Source and artifact checks are separately recorded in `audit/validation.json`.

The earlier 122-subject EEG analysis is preserved without rerunning it. Its primary cohort contrast is 2.222 microvolts, the finite-sample interval is [-77.920, 82.364], and the bias-calibrated projection interval is [-200, 200]. Those saved results demonstrate no tensor precision gain and do not establish the Gaussian or exact-rank assumptions of the new theorems. Subject independence and potential family dependence remain application limitations.

The expanded research program retains verdict **C: additional scientific work
required**. M1 and L3 have complete supplied upper/lower proofs on their stated
spaces, and P5 has a complete coordinate-axis theorem. The main remaining
requirements are a nonlinear efficient minimax procedure under simultaneous
fixed caps; full nonorthogonal and cubic profile rates; intermediate rates for
arbitrary simultaneous growing caps; and pointwise theory beyond the axis and
strong aligned families. The preserved focused review manuscript retains its
historical B assessment and is not silently presented as the new unified paper.

External novelty is not certified by these internal developments. Classical
convex geometry related to M1 is discussed by Argyriou, Foygel and Srebro,
*Sparse Prediction with the k-Support Norm* (2012),
<https://arxiv.org/abs/1204.5043>. Computational barriers require precisely
matched assumptions; see Luo and Zhang (2020),
<https://arxiv.org/abs/2005.10743>, and the bounded-degree setting of Fu and Sohn
(2026), <https://arxiv.org/abs/2605.30113>. A targeted priority check and eventual
integration of the new theorems into a coherent submission remain necessary.
