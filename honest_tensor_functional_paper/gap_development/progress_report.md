---
title: "Sharp tensor-functional rates and computational limits"
date: "September 9, 2026"
---

The cubic and worst-case **statistical** gaps are now closed in the paper's principal regime. The computational question has advanced to a certified search hierarchy and a rigorous low-degree estimation obstruction. A polynomial-time minimax confidence interval has not been established.

## 1. Exact scope of the matched rates

Observe \(Z=A+\tau G\), with independent standard Gaussian tensor coordinates, equal mode size \(p\), fixed order \(K\ge3\), supplied fixed positive Tucker or TT rank caps, and \(\|A\|_F\le M=\tau\sqrt p\). The loading is the prescribed equal diagonal contrast
\[
 \psi(A)=p^{-1/2}\sum_{i=1}^p A_{i,\ldots,i}.
\]
Actual ranks may be smaller, including zero; no minimum singular value is imposed.

Fix \(0<\alpha<1/4\). For intervals honest at level \(1-\alpha\) over the entire cap class, the completed result is
\[
 \boxed{
 \mathcal L_0(\Theta)\asymp\mathcal L_{\max}(\Theta)
 \asymp
 \begin{cases}
 \tau(\log p)^{3/2}/\sqrt p,&K=3,\\
 \tau\sqrt{\log p/p},&K\ge4.
 \end{cases}}
\]
Here \(\mathcal L_0\) minimizes expected length at zero and \(\mathcal L_{\max}\) minimizes worst-case expected length. Constants may depend on the fixed caps, order and confidence level. The equal rates concern these matched experiments and criteria; arbitrary loadings, growing caps and other \(M/\tau\) regimes are not characterized sharply.

The corresponding unrestricted minimax squared-error rates are the squares of the displayed rates.

## 2. Closing the cubic logarithmic gap

The earlier lower bound used a harmonic profile across all coordinates with coupled signs. A simpler sparse embedding is stronger.

On each uniformly sampled size-\(m\) support \(S\), place values \(j^{-1/3}\), \(j=1,\ldots,m\), in increasing coordinate order, obtaining \(x_S\). Set
\[
 A_S=b_m x_S^{\otimes3},\qquad
 b_m=\min\left\{\frac{M}{\sqrt{27m}},
 \frac{\tau}{\sqrt{27}}\sqrt{\log(1+p/(4m^2))}\right\}.
\]
All alternatives are rank one, have norm at most \(M\), and have the same target
\[
 \delta_m=b_mH_m/\sqrt p.
\]
For two supports with overlap \(H\), decreasing profile weights and Cauchy–Schwarz give
\[
 \langle x_S,x_T\rangle\le3H^{1/3},
 \qquad
 \langle A_S,A_T\rangle\le27b_m^2H.
\]
This bounds the **full tensor** likelihood second moment by \(e^{1/4}\), using the verified hypergeometric factorial-moment calculation. The common-target confidence-interval lower bound therefore applies.

With \(m=\lfloor p^{1/4}\rfloor\), both \(b_m\asymp\tau\sqrt{\log p}\) and \(H_m\asymp\log p\). This supplies the missing factor:
\[
 \mathcal L_0(\Theta)\gtrsim\tau(\log p)^{3/2}/\sqrt p.
\]
It matches the prior full-data upper rate. The older harmonic sign-mixture theorem remains correct but is no longer sharp.

The Gaussian support-mixture mechanism is classical; the tensor-profile overlap bound is the new step in this derivation. [Collier, Comminges and Tsybakov (2017)](https://arxiv.org/pdf/1502.00665).

## 3. Closing the worst-case gap

Let \(N_S\) be the finite product-net contraction maximum from the previous scan, and use its simultaneous Gaussian threshold \(\lambda_s(\alpha)\). Define a residual confidence set
\[
 \mathcal F(Z)=\{B\in\Theta:
       N_S(Z-B)\le\lambda_{|S|}(\alpha)\ \text{for all nonempty }S\}.
\]
The true tensor belongs to this set with probability at least \(1-\alpha\). Project the set onto the functional:
\[
 C_F(Z)=
 [\min_{B\in\mathcal F(Z)}\psi(B),\ \max_{B\in\mathcal F(Z)}\psi(B)],
\]
with \(C_F=\{0\}\) for an empty feasible set.

Compactness and continuity give attained, measurable extrema. If \(B,B'\) are feasible, their difference has **doubled** unfolding-rank caps and satisfies
\[
 N_S(B-B')\le2\lambda_s.
\]
Applying the ordered-diagonal argument with \(J_2=J(2\bar r)\) yields
\[
 |C_F(Z)|\le
 \min\left\{2h_0,\
 \frac{4J_2^{K/2}}{\sqrt p}
       \sum_{s=1}^p\lambda_s(\alpha)s^{-K/2}\right\}
\]
for every observation. This is a deterministic diameter bound, so it controls worst-case expected length directly. It does not rely on a favorable probability of accepting zero.

The sum is harmonic for \(K=3\) and summable for \(K\ge4\). Combining this upper bound with the sparse harmonic and coordinate-mixture lower bounds proves both matched length criteria.

Taking the midpoint and using failure budget \(p^{-2}\) gives squared risk at most
\[
 W_{p^{-2}}^2/4+4h_0^2p^{-2}.
\]
The same mixtures give matching squared-risk lower bounds. All coverage and diameter arguments are finite-sample; asymptotic rates are their consequences.

## 4. What was achieved for computation

### A certified truncated scan

For a completed search through support size \(t\), the leading diagonal magnitudes are bounded by the tested subsets. The untested tail is controlled by the diagonal \(\ell_{2/K}\) budget. The resulting honest zero-test interval has a radius bounded in order by
\[
 \frac{\tau\sqrt{\log p}}{\sqrt p}
        \sum_{s=1}^{t}s^{-(K-1)/2}
 +\mathbf1_{\{t<p\}}\tau(\log p/p)^\beta t^{-(K-1)\beta},
 \qquad \beta=\frac{K-2}{2K}.
\]
A finite normalized grid gives an explicit arithmetic cost
\[
 O\!\left\{\sum_{s=1}^t\binom ps
            (3+4K\sqrt s)^{Ks}s^K\right\}.
\]
For fixed \(t,K\), this is polynomial in \(p\). The polynomially computable fixed-\(t\) version does not attain the full statistical rate. Completed levels can be intersected adaptively using a single simultaneous noise event.

This computes a truncated zero test, **not** the optimization defining \(C_F\).

### A rigorous low-degree estimation obstruction

Draw a uniform size-\(s\) support and let
\[
 A_S=\tau\lambda(s^{-1/2}\mathbf1_S)^{\otimes K}.
\]
Its common target is \(\delta=\tau\lambda s^{1-K/2}/\sqrt p\). For polynomial degree \(D\), put
\[
 \mu=s^2/p,\qquad B_D=(\lambda^2/s^K)(KD)^K.
\]
A self-contained Hermite and factorial-moment calculation proves
\[
 \chi^2_{\le D}\le\mu e^\mu B_D/(1-B_D)\quad(B_D<1).
\]
Consequently every degree-\(D\) scalar polynomial estimator has worst-case squared risk at least
\[
 \frac{\delta^2}{(2+\sqrt{\mu e^\mu B_D/(1-B_D)})^2}.
\]
For \(\lambda=\sqrt p\), \(s=\lfloor p^a\rfloor\), and \(D=\lfloor p^b\rfloor\), with
\[
 1/K<a<\min(1/2,1/(K-2)),\qquad 0<b<a-1/K,
\]
this lower risk is polynomially larger than the unrestricted minimax risk.

This is a proved separation for **low-degree polynomial estimation under squared loss**. It is not a proof against every polynomial-time estimator or confidence interval. Low-degree methods are established in sparse tensor PCA; the present coarse proof is supplied independently for the scalar target. [Choo and d'Orsi (2021)](https://arxiv.org/pdf/2106.06308), [Fu and Sohn (2026)](https://arxiv.org/pdf/2605.30113).

For cubic tensors, one admissible example is \(a=5/12\), \(b=1/24\). The low-degree risk is bounded below by order \(\tau^2p^{-5/12}\), whereas the unrestricted risk is order \(\tau^2(\log p)^3/p\).

### A conditional link to efficient intervals

For any common-target prior, an honest interval gives a test with total error at most
\[
 2\alpha+E_0|C|/\delta.
\]
Thus a genuine polynomial-time testing-hardness hypothesis would imply an interval-length barrier. The low-degree mean-square result alone does not justify that hypothesis. This remaining distinction is explicit in the manuscript.

## 5. Verification and prototype results

The analytic checks include:

- 70,469 exact pairs of sparse harmonic supports across small dimensions.
- Four explicit multivariate Hermite coefficient checks.
- 81 finite low-degree moment-bound configurations.
- 120 differences of random rank-one tensors, checking the doubled-cap geometry.
- Six increasing-dimension checks of the cubic logarithmic lower scale.

All passed. These are finite corroborations of the supplied proofs, not substitutes for them.

The implemented prototype evaluates complete support levels one and two. For \(K=3\), its circle net has 19 points and verified covering distance below \(1/6\). The vectorized contractions were compared with explicit enumeration.

Across nine signal/dimension configurations with 100 replications each, the interval remained at the structural length \(2\tau\), with all replications covering. That behavior is expected at these small dimensions and shows no practical precision improvement. Zero-signal timing results are:

| Mode size | Contractions | Median runtime |
|---|---:|---:|
| 8 | 192,116 | 0.197 ms |
| 16 | 823,208 | 1.304 ms |
| 32 | 3,402,320 | 5.737 ms |

Timing excludes noise generation and net preparation, uses one OpenBLAS thread, and is specific to the recorded macOS ARM64 environment. Saved outputs include Monte Carlo uncertainty. The exact binomial interval for 100/100 coverage is approximately \([0.9638,1]\).

## 6. Current decision and remaining work

| Question | Current status |
|---|---|
| Cubic logarithmic rate | **RESOLVED** in the fixed-cap, equal-loading regime |
| Full-data worst-case optimality | **RESOLVED**, with deterministic confidence-set diameter |
| Full-data squared-error optimum | **RESOLVED** in the same regime |
| Computable search hierarchy | **PROVED and prototyped** at levels one and two |
| Low-degree estimation limitation | **PROVED**, with its restricted meaning |
| Polynomial-time minimax confidence interval | **OPEN** |
| Unconditional hardness for all efficient intervals | **NOT ESTABLISHED** |
| Actual-rank adaptation, arbitrary loadings, sharp growing-cap dependence | **OPEN** |

The project now has a sharper statistical core. The most useful next computational step is a stronger algorithm or a genuine reduction supporting interval-specific hardness, rather than labeling low-degree evidence as a full complexity theorem. Independent mathematical and priority review remains warranted before submission.

The updated manuscript and complete proofs are in [paper/main.pdf](paper/main.pdf). The prior reviewed manuscript is preserved unchanged.
