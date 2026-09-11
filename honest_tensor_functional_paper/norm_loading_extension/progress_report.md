---
title: "Tensor functional inference across norm budgets and loadings"
date: "September 11, 2026"
---

The fixed norm/noise scaling is no longer needed for the sharp equal-diagonal results. This update supplies complete derivations of matching interval-length and squared-error rates for all positive $M$ and $\tau$, with fixed tensor order and supplied rank caps. It also identifies the sharp support-size dependence for flat orthogonal loadings. Efficient minimax computation and general rank adaptation remain unresolved.

## 1. Scope and rate

The experiment remains $Z=A+\tau G$ with fully observed independent standard Gaussian coordinates in $G$, known $\tau>0$, and a supplied Frobenius bound $\|A\|_F\le M$. Tucker or TT rank caps are supplied and fixed; actual ranks and nonzero signal strengths may be smaller. The first target is $\psi(A)=p^{-1/2}\sum_i A_{i,\ldots,i}$.

Let $\ell_p=\log(ep)$ and $x=M/(\tau\sqrt{\ell_p})$. The matched rate is

$$
\mathfrak r_K(p,M,\tau)=\frac{\tau\sqrt{\ell_p}}{\sqrt p}
\begin{cases}
\min\{x,1+\log_+x,\ell_p\},&K=3,\\
\min(x,1),&K\ge4.
\end{cases}
$$

For fixed $0<\alpha<1/4$, both the best expected length at zero and the minimax worst-case expected length are comparable to this expression, with constants uniform over $p\ge1$ and $M,\tau>0$. Minimax squared error has its square. The lower bounds already use rank-one alternatives.

When $x\le1$, the rate is $M/\sqrt p$: the known parameter range limits the problem. For orders at least four the rate then saturates at $\tau\sqrt{\log(ep)/p}$. For order three it grows logarithmically in $x$ before saturating at the earlier cubic rate. These are orders up to constants, not exact transition locations. The special choice $M=\tau\sqrt p$ recovers the previous theorem.

## 2. New upper and lower arguments

For two feasible tensors their difference has norm at most $2M$ and doubled rank caps. Its $s$th largest absolute diagonal entry obeys both a norm bound and a scan bound. With the paper's explicit constants,

$$
|a|_{(s)}\le\min\{P_2M,Q_2\lambda_s\}s^{-K/2}.
$$

Taking this minimum before summing improves the former bound in the intermediate cubic regime. The elementary sum splits at $s=x^2$: its head is harmonic and its tail is summable. This supplies a deterministic confidence-set diameter, hence worst-case expected-length control.

For the lower bound, the coordinate mixture covers small norm budgets and all higher-order cases. In the cubic case choose the sparse harmonic support size

$$
m=\left\lfloor\min\{p^{1/4},x^2\}\right\rfloor
$$

when $p\ge256$ and $x>1$. The original amplitude minimum enforces both the Frobenius budget and the full-likelihood second-moment constraint. Its common target has the required logarithmic dependence. Smaller dimensions are covered by the coordinate construction with fixed constants. This is a new optimization of the previous tensor construction, not a new generic Gaussian-mixture method.

## 3. Why the squared-error proof needed a different estimator

The earlier midpoint proof used a failure probability $p^{-2}$ and an error bound proportional to $M$ off coverage. That upper bound is inadequate uniformly over arbitrarily large $M/\tau$.

The new estimator approximately minimizes the maximum positive excess of residual contractions over fixed scan thresholds. A countable dense candidate family and a tolerance $\tau$ give a measurable choice without invoking an efficient optimization oracle. The true residual excess $T_0$ satisfies

$$
\Pr(T_0>t)\le\tfrac18 e^{-t^2/(2\tau^2)},\qquad
\mathbb E T_0^2\le\tfrac14\tau^2.
$$

The scalar error is bounded by the norm-sensitive diameter plus a constant times $(T_0+\tau)/\sqrt p$. Integrating this tail removes the problematic $M$-dependent off-coverage term. Small norm budgets use the deterministic structural range. This supplies the all-budget MSE upper bound; the same hard mixtures yield the matching lower bound.

## 4. Loading geometry

For a prescribed orthogonal product loading with decreasing absolute weights $w_s^*$, the new full-data upper envelope is

$$
U_w=\sum_{s=1}^m w_s^*\min\{P_2M,Q_2\lambda_s^{(m)}\}s^{-K/2}.
$$

Every honest interval also satisfies a lower bound proportional to

$$
L_w=\max_{1\le d\le m}w_d^*\sqrt d\,\mathfrak r_K(d,M,\tau).
$$

The lower construction rescales one factor of the nonnegative hard alternatives by $w_d^*/w_i$. The map is a contraction, preserves rank one and the norm budget, equalizes the weighted target, and cannot increase the full Gaussian likelihood second moment.

For flat signed weights $w_i=\pm m^{-1/2}$, the sharp rate is exactly the dimension-$m$ rate above, up to constants. Deterministic orthogonal rotations and embedding in larger unequal mode dimensions preserve the conclusion. At $m=1$ this becomes the ordinary bounded-normal-mean scale $\min(M,\tau)$. For general unequal weights, the displayed envelopes need not match; arbitrary loading tensors without an orthogonal product representation remain outside the theorem.

## 5. Verification and limits

The new finite checks passed:

- 3,267 norm/rate configurations, including small dimensions, the $p=256$ proof boundary, and six orders of magnitude on either side of the norm/noise threshold.
- 240 random Tucker/TT differences, checking doubled unfolding caps and ordered norm envelopes.
- 144 signed-weight mixture configurations with 23,268 exact support-pair comparisons; the largest likelihood second moment was approximately 1.014, below $e^{1/4}$.
- 90 residual-tail checks using exact Gaussian tail probabilities and combinatorial net counts.
- 60 orthogonal-loading embeddings in unequal ambient dimensions; maximum target discrepancy was below $1.6\times10^{-15}$.

The analytic lower target divided by the proposed rate was at least 0.074 on the finite grid. This is a numerical check of the explicit constructions, not an empirical estimate of a minimax constant or a substitute for the proofs. No simulation of the ideal residual optimizer was performed.

The updated full manuscript includes the new statements and complete proofs. The previous stage is preserved and checked by hashes. The most consequential remaining work is an efficient interval construction or a valid interval-specific computational reduction. Sharp unequal-weight geometry, growing-cap constants, and actual-rank adaptation remain open. Independent proof and priority review is still needed before submission.
