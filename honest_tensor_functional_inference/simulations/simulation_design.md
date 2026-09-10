# Simulation protocol, fixed before implementation

Date: 2026-09-09. Theory prerequisite: T1–T6 in the result ledger. These experiments check consequences and implementation; they cannot establish honesty over an infinite class or prove novelty.

## Core experiment

Use equal dimensions, the normalized diagonal loading, M=1, sigma=1, n=p, and tau=n^(-1/2). Observe only the diagonal Gaussian coordinates used by the procedures. This is an exact marginal simulation of the full tensor experiment, not a simulation of tensor regression. Unused independent coordinates need not be generated. K ranges over 2, 3, 4, 6 and p over 128, 512, 2048, 8192. K=2 is a control where the proposed polynomial separation disappears. Use 2,000 independent replications per configuration, seed 20260909, independent reproducible streams and bounded-memory batches.

For each (K,p), simulate rank-one tensors A=a u^(tensor K), where u is uniform on a support of size s. Vary a in {0, 0.02, 0.2, 1}. For nonzero a, use s=1, s=p and s near (a/lambda)^(2/K), truncated to [1,p]. This last choice places individual means near the threshold; it is not a claim to have found the least favorable full-tensor signal. Coordinate sparsity is varied as a signal geometry, not imposed as an additional model assumption. All have ||A||_F=a and a_i=a/s^(K/2) on their support. The positive signals saturate the diagonal q-power inequality at rank one.

Methods: direct Gaussian interval; deterministic zero-centered norm-bound interval; nonlinear threshold interval; deterministic smallest-radius choice. The last two use the proved rank-cap radius. Include a clearly marked, infeasible known-direction oracle for nonzero rank-one signals: if U=u^(tensor K) were supplied, its interval is c<U,Z> +/- z tau |c|, c=<L,U>. Simulate the joint law of <U,G> and the diagonal Gaussian coordinates exactly, adding an independent normal for the remaining variance. This oracle is not the estimated-subspace procedure of Xu, Chen and Han and has a different honesty class.

## Unknown and weak actual ranks

Set K=3, p in {512,2048,8192}, and supplied Tucker/TT rank caps all equal to 2. Generate A=sqrt(1-epsilon^2) U_1 + epsilon U_2, where U_1,U_2 have disjoint mode supports, unit norms and orthogonal mode factors. Take epsilon in {0,0.001,0.01,0.1,0.5}. Every constrained unfolding has nonzero singular values sqrt(1-epsilon^2), epsilon when epsilon>0; epsilon=0 has actual rank one. Use both concentrated and threshold-scale supports. The radius uses the cap throughout and therefore cannot adapt to epsilon. This experiment checks coverage across the boundary, not rank adaptation.

## Noise level and assumption stress tests

At K=3,p=2048, vary n/p in {0.25,1,4,16}, holding M fixed, and vary the valid threshold multiplier in {1,1.5}. Larger multipliers preserve the proof after updating the radius. Run separate, explicitly out-of-model tests at K=3,p=512,n=p: independent variance-one Student t_3 errors, a variance-contaminated Gaussian mixture, and equicorrelated Gaussian coordinates with correlation 0.2. Do not claim robustness from them. Correlated Gaussian marginals still support the nonlinear union-bound argument, but invalidate the direct interval's iid variance calibration. Unknown tau, unknown M and wrong rank caps are not solved by these experiments.

## Metrics and uncertainty

For every method report coverage, its binomial Monte Carlo standard error, and an exact 95% Clopper–Pearson interval (including when empirical coverage is one); mean length and Monte Carlo standard error; center bias and its Monte Carlo standard error; root mean squared center error. Deterministic widths have zero Monte Carlo error. No hypothesis of exact 95% coverage is imposed on conservative intervals.

## Theorem-to-experiment map

| Result | Empirical check | What it cannot show |
|---|---|---|
| T1 | Small dense random Tucker and left-canonical TT tensors satisfy the diagonal q bound; TT squared path weights sum to squared Frobenius norm | Sharp rank dependence |
| T2 | Coverage across amplitude, support, rank boundary and noise level; deterministic minimum agrees with stated radius | Uniform coverage cannot be inferred from a finite grid |
| T3–T5 | Plot exact analytic width ratios against dimension, including affine and unfolding lower bounds | The lower-bound curves are not observed algorithm performance |
| T5 | K=2 control, K>=3 decay of length/tau; larger caps make conservative bound less useful | An unrestricted minimax rate or oracle efficiency |
| T6 | Check exact mixture chi-square calculations and display the remaining upper/lower bracket | That the coordinate mixture is least favorable |

The analytic width plot may extend beyond simulated dimensions; its caption must say so. Do not simulate huge tensors merely to reproduce a deterministic formula. Figures use vector PDF exports, labeled log axes, color plus line/marker distinctions, and exact binomial error bars. All generated tables must be traceable to the saved CSV and manifest.

## Computational scope

No tensor-estimation algorithm is fitted. The proposed scalar procedure does not need one. Direct inference, the structural interval and the known-direction oracle are relevant exact comparisons; T3 additionally compares an entire class of affine procedures. Published strong-signal tensor methods are compared theoretically, with their assumptions, rather than inaccurately reimplemented and advertised as uniform baselines.
