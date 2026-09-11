---
title: "Progress on robust and adaptive tensor-functional inference"
date: "September 11, 2026"
---

The previous report left three main theory questions and several missing experiments. This update adds six theorems, four propositions, their complete proofs, and four experiment suites. It establishes useful relaxed-assumption and computable regimes. It does **not** solve efficient minimax inference for the original weak-signal, diffuse-loading class, or sharp loading geometry and rank adaptation in full generality.

## 1. What survives beyond Gaussian observations?

The scan proof requires tail control for entire tensor contractions. A sufficient assumption is

$$
\mathbb E\exp(t\langle U,E\rangle)
\le \exp(t^2v^2\|U\|_F^2/2)
$$

for every fixed tensor $U$. This includes independent bounded or sub-Gaussian entries and dependent Gaussian noise with covariance at most $v^2I$. Under this condition, the previous interval-length and squared-risk upper bounds remain valid with $v$ as the noise scale. Matching minimax statements hold when the unknown noise law ranges over this family, because it contains Gaussian noise. They need not hold separately for each non-Gaussian distribution: known scalar noise equal to $\pm v$ permits exact recovery when $|A|\le M<v$.

Finite variance alone also suffices **if independent tensor replicates are retained**. For each scan direction, take a median of independent block averages. We prove a simultaneous envelope and an integrable excess tail,

$$
\Pr(T_0>t)\le\beta\left(1+\frac{t}{12\sqrt2\tau}\right)^{-9},
\qquad \mathbb ET_0^2\le\frac{72}{7}\beta\tau^2,
\quad \tau=\sigma/\sqrt n.
$$

Consequently, full-data minimax length and squared risk retain the previous rates over the family of replicate laws with known covariance upper bound $\sigma^2I$, provided $n\ge C_{K,\beta}p$. The sufficient constant and block rule are explicit in the paper. Coordinates within each replicate can be dependent; replicates must be independent. The directional medians need not form one estimated tensor. Their linear confidence constraints are enough. The exact optimization is still expensive.

Marginal variance or marginal sub-Gaussian bounds alone do not justify full scans. A tensor whose entries all share one random sign gives a counterexample. Unknown noise scale, dependence across replicates, and random-design regression still need separate treatment.

## 2. Rank assumptions: what can be relaxed?

For approximately low-rank means $A=B+R$, with $B$ in the supplied cap class and $\|R\|_F\le\eta$, the new sharp interval scale is

$$
\min\{\tau,\mathfrak r_K(p,M,\tau)+\eta\}.
$$

Here $\mathfrak r_K$ is the previous all-budget rate. The construction enlarges scan thresholds by $\eta$ and target endpoints by $\eta$, with a direct-interval fallback. A residual of order no larger than the original rate preserves its order. This theorem concerns interval length; no new matching MSE theorem for the approximate class is claimed.

Supplied caps may grow with dimension in the finite inequalities, but their constants then grow. A new sparse-diagonal lower bound displays an additional rank cost. If rank restrictions are removed entirely, the sharp scale for a unit loading is $\min(M,\tau)$. The earlier vanishing tensor scale therefore cannot hold uniformly over all ranks.

There is also a positive result without supplied caps. With an independent pilot and validation observation, unfolding SVDs recover the actual mode ranks on a common noise event when each nonzero singular value exceeds twice an explicit pilot operator-norm bound. A projected second-observation interval uses

$$
\text{radius}=\text{certified projection bias}
 +\text{noise quantile}\times\|T L\|_F.
$$

The bias certificate is computable from pilot singular values, the known norm bound, and the loading. The method chooses the direct interval when this certificate is too large. It is polynomial in the explicit tensor size and works for arbitrary prescribed loadings. For Gaussian noise, one observation can be split into two independent noisy observations by adding and subtracting independent artificial Gaussian noise, with the increased noise scales accounted for. Non-Gaussian use requires independent replicate groups.

This is adaptation on a **spectrally separated class**, not on the original class allowing arbitrary weak components. Separation is a model assumption: observed singular values alone cannot certify that undetected components are absent. A new lower bound at nonzero tensors shows why the distinction matters: weak rank-one components in an unused block can force the original hard interval scale even when the baseline tensor has lower rank. Full adaptation over unseparated rank subclasses remains uncharacterized.

## 3. Efficient intervals and general loading geometry

Two minimax regimes are now explicitly computable:

- For equal loading and $M\le\tau\sqrt{\log(ep)}$, the structural interval attains the optimal order $M/\sqrt p$ for fixed caps.
- For any loading with a supplied unit product tensor $U$ satisfying $|\langle L,U\rangle|\ge c\|L\|_F$, with fixed $c>0$, the direct/structural choice attains $\|L\|_F\min(M,\tau)$ without rank recovery. A loading certificate, not a tensor optimization oracle, verifies the condition.

For an arbitrary known loading, write $L=L_0+R$, where $L_0$ has an orthogonal representation. Add $\langle R,Z\rangle$ to the interval center and calibrate its noise. The added radius is proportional to $\tau\|R\|_F$, with error allocation; simply ignoring $R$ is invalid. Prescribed partitions of unequal orthogonal weights give additional upper bounds. These are useful certified constructions, not a sharp formula for every loading.

The computational investigation also rules out one tempting route: every convex outer parameter class containing the rank-one norm ball contains the line $\{tL:|t|\le M/\sqrt p\}$ for equal loading. Honesty on that larger class forces length at least order $\min(M/\sqrt p,\tau)$. At $M=\tau\sqrt p$ this loses the tensor improvement. This limits full convexification; it is not a hardness result for every efficient algorithm or every convex subroutine.

## 4. Experiments completed after reviewing the previous report

All suites have fixed seeds, exact binomial uncertainty, saved configuration outputs, and source hashes. Earlier simulations were preserved rather than rerun.

| Suite | Configurations | Trials each | Main finding |
|---|---:|---:|---|
| Rank adaptation | 54 (12 outside assumptions) | 500 | Shorter intervals require very strong signals. |
| Loading correction | 36 | 1,000 | Ignoring the residual can give zero coverage. |
| Full robust scan | 4 | 400 | Median envelope handles rare outliers. |
| Approximate ranks | 12 | 1,000 | Inflation and direct fallback are needed. |

The adaptive suite uses Gaussian, sign, and correlated Gaussian errors with ordinary and general loadings. Loading correction uses $K=4$, $p=256,4096$, three remainders and three signals. The complete robust scan evaluates all 6,861 directions at $p=2,K=3$, with $n=128$ replicates. Approximate-rank experiments use $K=4,p=4096$ and full-rank perturbations $\eta L$.

Across the 42 valid adaptive configurations, the minimum observed coverage is 0.944, with exact 95% binomial interval approximately $[0.920,0.962]$. These finite experiments neither prove uniform coverage nor establish undercoverage at that setting. For Gaussian equal loading at $p=8$, signal strength $1000$ times the conservative pilot bound gives mean length/direct-length ratios approximately 0.480 for rank one and 0.665 for rank two, with coverages 0.992 and 0.988. At strengths three and 100 times that bound, the bias certificate selects the direct interval. The method therefore needs much stronger signals to improve precision than it needs to identify ranks. The 12 below-gap configurations give zero coverage, exposing a real scope limitation.

For Gaussian $p=4096$ loading corrections on an off-diagonal signal, remainder norms 0, 0.03 and 0.3 give lengths approximately 0.794, 0.928 and 2.102, versus direct length 3.920. The uncorrected intervals have zero coverage at the two positive remainder levels. These are efficient threshold-based corrected intervals, not implementations of the ideal full-data minimax projection.

For the complete small scan, simultaneous median-envelope coverage is 400/400 for each law (exact 95% lower confidence bound approximately 0.991). Gaussian calibration of sample means covers 399/400 for Gaussian and sign errors, 390/400 for Student $t_3$, and 349/400 for rare-outlier errors with variance one. The median thresholds are conservative: this experiment validates the implemented simultaneous envelope, not the statistical rate or precision of an optimized minimax interval.

For approximate ranks, the finite coverage minimum is 0.944 across the 12 configurations. A zero low-rank baseline with allowance $\eta=0.5$ gives coverage one with inflation and zero without it. At $\eta=2$ the direct interval is selected. The full-rank perturbation is analytically represented, so these simulations need only its exactly distributed diagonal observations.

Finite mathematical corroborations additionally cover 200 projector/bias cases, 26,595 median-tail comparisons, 112,086 growing-rank support pairs, and 100 shifted-block constructions. These checks supplement complete supplied proofs; they are not formal or independent mathematical verification.

## 5. Remaining work, stated precisely

1. An efficient interval attaining the original full-data minimax rate for diffuse loadings and arbitrarily weak signals is still missing. The new efficient regimes and separated method do not settle this problem.
2. A sharp expression for every unequal orthogonal weight sequence, and for every arbitrary tensor loading, remains open beyond the new upper constructions and product-overlap regime.
3. Optimal expected length across unseparated actual-rank subclasses, and sharp dependence on growing caps, remain open. The new lower bounds and separated method give partial answers.
4. The ideal robust residual optimizer has not been implemented or simulated. A certified implementation and larger-dimensional full-data experiments remain a prerequisite for practical claims about that optimizer. The small scan experiment cannot substitute for them.
5. The bias certificate needs tightening if the adaptive method is to improve at moderate signal strength. A fair common-model comparison with a published regular-signal method, unknown-scale robust calibration, dependent replicates, and application-specific noise validation remain future experimental/theoretical work.

Independent proof review and a broader priority review remain necessary before submission. Known $M$, known noise proxies or covariance upper bounds, prescribed loadings, and the stated sample independence are still substantive assumptions.
