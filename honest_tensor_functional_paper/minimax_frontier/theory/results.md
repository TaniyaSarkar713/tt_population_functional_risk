---
title: "Minimax frontiers for Gaussian tensor functionals"
subtitle: "Full proofs, precise parameter spaces, and computational limits"
date: "2026-09-15"
geometry: margin=1in
fontsize: 11pt
---

# Experiment, criteria, and scope

Observe the entire tensor $Z=A+\tau G$, where the entries of $G$ are independent
standard normal variables, $\tau>0$ is known, and $\|A\|_F\le M$ is supplied.
The loading $L$ is deterministic and known, and the target is
$\theta(A)=\langle L,A\rangle$. Fix $0<\alpha<1/4$. An honest interval covers
this target with probability at least $1-\alpha$ at **every** mean in the stated
parameter space. Write $\mathcal L_0$ and $\mathcal L_{\max}$ for the infima,
over such intervals, of expected length at zero and worst-case expected length;
write $\mathcal R$ for minimax squared error. Randomization independent of the
observation is permitted. Constants in $\asymp$ do not depend on dimension,
budget, noise level, or loading; any additional dependencies are stated.
Zero loadings and $M=0$ have identically zero risk and length.

This supplement supplies four results with complete derivations. They are
internally labelled **PROVED**, meaning that the arguments have been checked
within this project, not externally peer reviewed or machine verified.

| Result | Exact scope | Remaining boundary |
|---|---|---|
| M1 | Every loading and every cap/budget in a full tensor model with one constrained unfolding | Additional simultaneously restrictive caps change the minimax problem |
| M2 | Exact obstruction for deterministic affine, constant-radius intervals at flat loadings | Does not rule out nonlinear efficient algorithms |
| L3 | Every orthogonal loading profile and every budget, order at least four, fixed positive Tucker or TT caps | Attaining prefix fits remain ideal; cubic and general nonorthogonal profiles are unresolved |
| P5 | All coordinate functionals at unknown rank-one axis means, with uniformly honest inference on the entire rank-one ball | Other means, general loadings, higher ranks, and optimal localization thresholds remain unresolved |

These are rates up to fixed multiplicative constants, not exact finite-sample
minimax constants. The one-cap model in M1 observes all tensor entries and
places no diagonal-support restriction on the mean.

# A common lower-bound lemma

Let $P_0$ be the distribution at zero, and let $Q$ mix distributions of admissible
means whose targets all equal $\Delta>0$. If $\operatorname{TV}(Q,P_0)\le v$,
honesty gives

$$E_0|C|\ge \Delta(1-2\alpha-v),\qquad
\sup_A E_A(\widehat\theta-\theta(A))^2\ge
\frac{\Delta^2}{8}(1-v).$$

For the first inequality transfer $Q\{\Delta\in C\}\ge1-\alpha$ to $P_0$
and intersect with $\{0\in C\}$. For the second, the test
$1\{\widehat\theta>\Delta/2\}$ has sum of errors at most
$8\sup_A E_A(\widehat\theta-\theta(A))^2/\Delta^2$, whereas every test has
sum of errors at least $1-v$. The same interval argument works between a
specified mean $A_0$ and an alternative $A_1$ by translation. Gaussian mean
mixtures satisfy

$$1+\chi^2(Q,P_0)=E_{A,A'}\exp\{\langle A,A'\rangle/\tau^2\},
\qquad \operatorname{TV}\le\tfrac12\sqrt{\chi^2}.$$

Deterministic Gaussian shifts obey $\operatorname{TV}\le\|A-A'\|_F/(2\tau)$
by Pinsker's inequality.

# M1: an efficient full-model theorem for one constrained unfolding

Choose one mode unfolding or TT cut, of matrix shape $m\times n$, and impose
only its rank bound $1\le r\le q=\min(m,n)$. All other tensor caps are unrestricted
(equal to their ambient maxima). Let $\sigma_1\ge\cdots\ge\sigma_q\ge0$ be the
singular values of this unfolding of $L$, and $H_r=(\sum_{i\le r}\sigma_i^2)^{1/2}$.
Define

$$T_r(L,M,\tau)=
\begin{cases}
MH_r,&M\le\tau,\\
\displaystyle\max_{b\ge0,\ \|b\|_1\le M\sqrt r,\ \|b\|_2\le\tau}
\sum_i\sigma_i b_i,&M>\tau.
\end{cases}$$

**Theorem M1 (PROVED).** On this full one-unfolding parameter space,

$$\mathcal L_0\asymp_\alpha\mathcal L_{\max}\asymp_\alpha T_r,
\qquad \mathcal R\asymp T_r^2.$$

Constants are uniform in $m,n,r,M,\tau,L$. An interval and estimator attaining
these rates require one SVD of the known loading and a convex scalar solve;
there is no signal-strength or separation assumption.

## Upper bound, algorithm, and convex duality

Write the loading unfolding as $U\operatorname{diag}(\sigma)V^T$ and, for $t\ge0$,
let $W_t=U\operatorname{diag}((\sigma-t)_+)V^T$. Von Neumann's trace inequality
and Cauchy--Schwarz give the exact maximum bias

$$\sup_{\operatorname{rank}(A)\le r,\|A\|_F\le M}
|\langle L-W_t,A\rangle|
=M\left(\sum_{i\le r}\min(\sigma_i,t)^2\right)^{1/2}\le M\sqrt r\,t.$$

Thus the interval centered at $\langle W_t,Z\rangle$ with radius

$$M\left(\sum_{i\le r}\min(\sigma_i,t)^2\right)^{1/2}
+z_{1-\alpha/2}\tau\| (\sigma-t)_+\|_2$$

is honest. Its choice of $t$ depends only on the known loading and supplied
bounds, not on $Z$. Independently choose the zero-centered interval
$[-MH_r,MH_r]$ if it has smaller radius. Intersect the selected interval with
this structural range; replace an empty intersection by $\{0\}$. On the event
that the original interval covers the target, the intersection is nonempty
and covers it, so this convention preserves honesty. This also bounds length
uniformly by twice the chosen deterministic radius.

For $a,v>0$, the scalar identity

$$\min_{t\ge0}\{a t+v\| (\sigma-t)_+\|_2\}
=\max_{b\ge0,\|b\|_1\le a,\|b\|_2\le v}\sigma^T b \tag{M1.1}$$

follows by dualizing the constraint $\sum b_i\le a$: maximizing the remaining
linear form over the nonnegative Euclidean ball gives the soft-threshold norm.
Strict feasibility for both positive budgets gives strong duality; zero-budget
cases follow directly. At an interior optimum the derivative is
$a-v\sum_i(\sigma_i-t)_+/\| (\sigma-t)_+\|_2=0$.
It is nondecreasing, so bisection finds the optimum. At $t=0$ or
$t=\sigma_1$ the one-sided optimality conditions suffice. A proportional
soft-threshold vector (or a uniform vector on maximal ties at the latter
endpoint) gives an explicit feasible dual witness.

Use $a=M\sqrt r$, $v=z_{1-\alpha/2}\tau$ for the interval. Its objective is at
most $z_{1-\alpha/2}$ times the objective with $v=\tau$; use the structural
choice for $M\le\tau$. For squared error, independently optimize with $v=\tau$,
use the center $\langle W_t,Z\rangle$, and choose the zero estimator if its
bound $(MH_r)^2$ is smaller. The sum of squared bias and variance is bounded by
the square of (M1.1). Clip the estimate to the structural range. The estimate
is specified separately from the interval midpoint.

An economy SVD takes $O(mn\min(m,n))$ arithmetic operations and the scalar solve
takes $O(q\log(1/\epsilon))$ operations for an additive numerical threshold
tolerance. Each subsequent observation needs $O(mn)$ operations. The code
returns primal and feasible-dual objective values, their gap, and the dual
vector. These are floating-point diagnostics, not rigorous directed-rounding
certificates for the SVD. Scale, tie, and residual tests accompany the code.
No iterative optimization over the unknown mean occurs.

## A rank-r mixture lower bound at all intermediate caps

Suppose $M\ge\tau$ and let $b$ maximize (M1.1) with $a=M\sqrt r,v=\tau$.
Partition its coordinates into at most $r$ groups $G_j$ so that, writing
$s_j=\sum_{i\in G_j}b_i$,

$$\sum_j s_j^2\le \frac{\|b\|_1^2}{r}
+(1-1/r)\|b\|_2^2\le M^2+\tau^2\le2M^2. \tag{M1.2}$$

For completeness, assign coordinates successively to the currently smallest
group load. If the previously assigned mass is $S$, assigning $b_i$ increases
the sum of squared loads by at most $2b_iS/r+b_i^2$. Sum over coordinates and
use $2\sum_i b_i\sum_{h<i}b_h=\|b\|_1^2-\|b\|_2^2$ to obtain (M1.2).

Let $\varepsilon_i$ be independent Rademacher signs, and let $U_i,V_i$ be the
corresponding singular vectors of $L$. Define

$$A_\varepsilon=\frac18\sum_{j=1}^r
\left(\sum_{i\in G_j}\sqrt{b_i}\varepsilon_i U_i\right)
\left(\sum_{i\in G_j}\sqrt{b_i}\varepsilon_i V_i\right)^T.$$

The groups have mutually orthogonal left and right spans. Consequently these
are rank-at-most-$r$ matrices with squared norm
$\sum_j s_j^2/64\le M^2/32$, and every target equals
$\Delta=\sigma^Tb/8=T_r/8$. After unfolding is reversed these are admissible
**full tensor means** for the stated one-cap model.

For two independent sign draws put $X_j=\sum_{i\in G_j}b_i\varepsilon_i
\varepsilon_i'$. Their likelihood inner product is $\sum_j X_j^2/(64\tau^2)$.
The $X_j$ are independent with sub-Gaussian proxies
$v_j^2=\sum_{i\in G_j}b_i^2$. Integrating their moment generating bounds against
a standard Gaussian gives

$$E e^{uX_j^2}\le(1-2u v_j^2)^{-1/2},\qquad 2u v_j^2<1.$$

Here $u=1/(64\tau^2)$, $\sum_jv_j^2\le\tau^2$, and
$2u v_j^2\le1/32$. Therefore

$$\log(1+\chi^2)\le-\tfrac12\sum_j\log(1-v_j^2/(32\tau^2))
\le \frac{1}{62},$$

and $\operatorname{TV}<0.065$. The common-target lemma proves both lower bounds.
For $M\le\tau$, compare zero to $A=(M/2)L_r/H_r$, where $L_r$ is the truncated
loading SVD; it has target $MH_r/2$ and TV at most $1/4$. This completes M1.

## Interpretation and the multi-cap boundary

For a flat orthogonal loading on $p$ components, its nonzero singular values
in each nontrivial unfolding equal $1/\sqrt p$. Equation (M1.1) becomes

$$T_r\asymp\min\{M\sqrt{r/p},\tau\},\qquad 1\le r\le p,$$

including **every intermediate cap**. For $M\le\tau$ the first term is smaller
and the formula is exact as a rate proxy. This is a full-model result for the
one-unfolding class; it is neither a sparse sequence reduction nor an
exact-diagonal mean assumption.

If additional caps are imposed, every M1 interval remains honest because the
parameter space shrinks. One can deterministically choose the shortest of the
loading-based radii from available unfoldings without a multiplicity penalty.
However, the above mixture need not satisfy the additional caps. The matching
lower bound must **not** be transferred to their intersection. For example,
with all caps fixed and $M=\tau\sqrt p$, the established flat-loading rates
are $\tau(\log(ep))^{3/2}/\sqrt p$ in order three (up to the all-budget cutoff)
and $\tau\sqrt{\log(ep)/p}$ in higher order, whereas M1's radius can stay at
noise scale. This rules out claiming M1 as the general fixed-cap minimax
optimizer. Computing the singular values of a general loading is also not a
solution to the multiple-cap optimization problem.

# M2: why deterministic affine intervals cannot solve the fixed-cap problem

Take dimensions $p$ in all $K\ge3$ modes, flat loading
$L=p^{-1/2}\sum_{i=1}^p E_{i,\ldots,i}$, and any fixed positive supplied caps.
Consider intervals $[\langle W,Z\rangle+b-h,\langle W,Z\rangle+b+h]$ with
deterministic $W,b,h$. These are the **unintersected**, constant-radius affine
intervals; the claim is not about all data-dependent interval lengths.

**Proposition M2 (PROVED).** Every such honest interval has

$$h\ge \min\{M/\sqrt p,z_{1-\alpha}\tau\}.$$

Conversely, either the structural interval or direct Gaussian interval has
radius at most a constant multiple of $\min(M/\sqrt p,\tau)$ for fixed caps
(with cap-dependent constants for the structural range). At
$M=\tau\sqrt p$, deterministic affine intervals therefore cannot attain the
vanishing ideal fixed-cap rates. Any solution within this radius/center class
must change its form, not merely improve its optimization tolerance.

To prove the lower bound, restrict the class to its symmetric rank-one ball,
and put $\rho(H)=\sup_{\|u_k\|=1}|\langle H,\otimes_k u_k\rangle|$.
For some admissible mean the absolute center bias is at least
$M\rho(L-W)+|b|$. Considering the one-sided Gaussian tail at that mean gives

$$h\ge M\rho(L-W)+|b|+z_{1-\alpha}\tau\|W\|_F.$$

This remains valid for zero variance by direct interpretation. Average $W$
over the following loading-preserving orthogonal transformations: choose
independent signs $s_{k,i}$ for $k<K$; multiply coordinate $i$ in mode $k<K$
by $s_{k,i}$ and in mode $K$ by $\prod_{k<K}s_{k,i}$. Averaging kills every
entry except the superdiagonal. Next average over common permutations of all
modes, giving $\overline W=cL$ for a scalar $c$. Convexity and invariance of
$\rho$ and the Frobenius norm imply that this averaging cannot increase the
right-hand side without $|b|$. Since $\rho(L)=1/\sqrt p$ and $\|L\|_F=1$,
minimizing over $c\in\mathbb R$ gives
$\min_c (M/\sqrt p)|1-c|+z_{1-\alpha}\tau|c|$, equal to the stated lower bound.
The identity $\rho(L)=1/\sqrt p$ follows from generalized Holder and is
attained by a single coordinate product. The structural upper for fixed caps
is the previously proved rank-sensitive diagonal contraction bound.

M1's pre-intersection intervals belong to this affine class for each known
loading and supplied cap. M2 explains their failure to exploit simultaneous
small caps. It is an unconditional statement about a specified procedure
class, not computational hardness for all polynomial-time procedures.

# L3: all orthogonal profiles in order four and higher

Let $K\ge4$ be fixed and impose fixed positive Tucker or TT caps. Suppose
$L=\sum_{i=1}^p w_i u_{1i}\otimes\cdots\otimes u_{Ki}$, with orthonormal columns
in every mode. Rotate these known bases, absorb signs into one mode, and order
the weights so that $w_1\ge\cdots\ge w_p\ge0$. Set

$$F_s=\min\{M,\tau\sqrt{\log(es)}\},\quad F_0=0,\qquad
\mathcal A(w)=\sum_{s=1}^p w_s(F_s-F_{s-1}).$$

**Theorem L3 (PROVED).** For every profile, including dimension-dependent
profiles and zeros, and every norm budget,

$$\mathcal L_0\asymp\mathcal L_{\max}\asymp\mathcal A(w),
\qquad \mathcal R\asymp\mathcal A(w)^2.$$

Constants depend only on $K$, the fixed positive caps, and $\alpha$ for length.
The lower bound uses one rank-one mixture. The upper bound uses the ideal
prefix fits of the established AB1 theorem in
`scientific_extension/theory/results.md`. This theorem closes its
$O(\log\log p)$ statistical gap for **all** profiles when $K\ge4$; it does not
implement those ideal fits.

## Upper bound and the earlier dependence

With $w_{p+1}=0$, write the functional as the sum of prefix functionals with
coefficients $w_s-w_{s+1}$. The established full-data flat-prefix theorem gives
length $F_s$ for the unnormalized prefix sum. Allocate failure probabilities
proportionally to $1/[s(s+1)]$; the extra logarithm changes its Gaussian scan
threshold by only a fixed factor. The Minkowski sum of the resulting intervals
is honest and has length at most a constant times
$\sum_s(w_s-w_{s+1})F_s=\mathcal A(w)$. Minkowski's inequality in $L^2$ applied
to the corresponding scalar estimators gives the squared-error upper bound.
This invokes exactly the already supplied AB1 upper proof, with its stated
fixed-cap constants and ideal optimizers; no new efficient upper is inferred.

## A multiscale rank-one mixture

If $M\le\tau$, $\mathcal A=Mw_1$ and a single shift on the largest-weight
coordinate proves the lower bound. Assume $M>\tau$. Put
$Q=\min\{\log p,(M/\tau)^2\}$ and retain all $q_j=4^j\le Q$, for
$j=0,\ldots,J$. Let $N_j=\lfloor e^{q_j}\rfloor$, $N_{-1}=1$, and
$G_j=\{N_{j-1}+1,\ldots,N_j\}$. If there are no scales use only coordinate one.
The groups are disjoint and $n_j=|G_j|\ge e^{q_j}/4$: this is immediate for
$q_0=1$ and follows from $e^q-1-e^{q/4}\ge e^q/4$ for $q\ge4$ otherwise.
Choose $S_j$ independently and uniformly from $G_j$, and define

$$v_S=e_1+\sum_{j=0}^J q_j^{1/(2K)}e_{S_j},\qquad
C_K=1+\frac{1}{1-4^{-1/K}},\qquad
\epsilon_K=\frac{1}{16 C_K^{K/2}}.$$

Let $D$ be a diagonal contraction: $D_{11}=1$ and
$D_{ii}=w_{N_j}/w_i$ on each group, taking the ratio as zero when its numerator
is zero. A zero denominator can occur only in that case. Set

$$A_S=\epsilon_K\tau(Dv_S)\otimes v_S^{\otimes(K-1)}.$$

Each mean has rank one and therefore satisfies every positive supplied cap.
Its norm is bounded by

$$\epsilon_K\tau\left(1+\sum_{j\le J}q_j^{1/K}\right)^{K/2}
\le\epsilon_K\tau C_K^{K/2}\sqrt{q_J}
\le M/16.$$

Without scales the norm is $\epsilon_K\tau\le M$. The target does not depend
on the sampled coordinates:

$$\Delta=\epsilon_K\tau\left(w_1+\sum_j w_{N_j}\sqrt{q_j}\right)
=\epsilon_K\mathcal P(w). \tag{L3.1}$$

For independent draws $S,T$, their normalized mean inner product is at most
$\epsilon_K^2(1+\sum_j q_j^{1/K}B_j)^K$, where the collision indicators
$B_j=1\{S_j=T_j\}$ are independent with probabilities $1/n_j$. On the event
that $j$ is the largest colliding scale this is at most
$\epsilon_K^2 C_K^K q_j=q_j/256$. Splitting into no collision and largest
collision gives

$$\chi^2\le e^{\epsilon_K^2}-1+
\sum_j n_j^{-1}(e^{q_j/256}-1)
\le\frac{1}{128}+\frac{1}{64}\sum_{j\ge0}q_j e^{-q_j/2}
\le\frac{1}{128}+\frac{1}{64}\sum_{n\ge1}ne^{-n/2}<0.07.$$

Here $e^x-1\le xe^x$ and $\epsilon_K^2\le1/256$ were used. Consequently
$\operatorname{TV}<0.133$ uniformly in the number of scales. This calculation
bounds the likelihood ratio of the **entire tensor experiment**; it does not
discard off-diagonal observations.

## Comparing the multiscale target with the full profile rate

The first increment contributes $\tau w_1$ to $\mathcal A$. In each range
$N_j\le s<N_{j+1}$, monotonicity gives $w_s\le w_{N_j}$ and its total
contribution is at most $w_{N_j}F_{N_{j+1}}\le\sqrt5\tau w_{N_j}\sqrt{q_j}$.
For the final range $N_J\le s\le p$, exclusion of the next scale implies
either $\log p<4q_J$ or $M<2\tau\sqrt{q_J}$, giving the same bound. These
ranges start at $N_0=2$ and cover every remaining increment. If there are no
scales, $p<e$, so $F_p\le\sqrt2\tau$ and
$\mathcal A\le\sqrt2\tau w_1$. In all cases

$$\mathcal A(w)\le\sqrt5\mathcal P(w). \tag{L3.2}$$

Apply the common-target lemma to (L3.1)--(L3.2). Its constants depend only on
$K$ and $\alpha$, and rank one supplies the lower bound for every positive
fixed-cap class. This proves L3.

## Critical profiles and the unresolved cubic case

In particular, for $w_i=c[\log(ei)]^{-1/2}$ put
$T=\min\{\log(ep),(M/\tau)^2\}$. The sharp length rate is
$cM$ for $M\le\tau$ and

$$c\tau[1+\log T],\qquad M>\tau,$$

up to universal constants (and its square for risk). This follows either by
integrating $t^{-1/2}d\sqrt t=dt/(2t)$ or bounding the corresponding discrete
increments above and below. It includes the previously unresolved critical
exponent, with any chosen normalization $c$. The exact discrete proxy
$\mathcal A$ is preferable for finite dimension and arbitrary profiles.

The multiscale prior also defines admissible cubic means, but its target has
the higher-order envelope $\min(M,\tau\sqrt{\log(es)})$. It does **not** produce
the additional harmonic factor in the established cubic $F_s$. Combining
cubic harmonic mixtures across entropy scales requires a new bound on their
cross-scale likelihood moments. No such bound is asserted here. Likewise,
rotating a general nonorthogonal loading to the diagonal form above is not
permitted: an orthogonal decomposition of this kind need not exist.

# P5: optimal coordinate adaptation at unknown axis means

Now restrict the mean to the entire rank-one tensor ball (including zero), of
fixed order $K\ge2$ and dimensions at least two. Let $D$ be the product of the
dimensions, and fix any target coordinate $I$. The mean of interest is
$A_0=aE_J$, with **unknown** location $J$, $0<|a|\le M$. Let $d$ be the Hamming
distance between $I$ and $J$. Define

$$h_d(a,\tau)=
\begin{cases}\tau,&d=0,1,\\
\tau^d/|a|^{d-1},&2\le d\le K.
\end{cases}$$

**Theorem P5 (PROVED).** There is an $O(D)$ randomized interval, honest over
the entire rank-one ball without separation, such that whenever
$|a|\ge C_{K,\alpha}\tau\sqrt{\log(eD)}$,

$$E_{A_0}|C_I|\le C'_{K,\alpha}h_d(a,\tau).$$

Every interval honest over that same ball has
$E_{A_0}|C_I|\ge c_{K,\alpha}h_d(a,\tau)$ for $|a|\ge\tau$.
Thus the expected-length rate at every axis mean and every coordinate is
optimal in the stated localization regime. The signal threshold is sufficient,
not proved necessary. This is pointwise expected length under global honesty,
not minimax squared error at a singleton.

## Adaptive anchor and globally honest construction

Generate an independent standard Gaussian tensor $G'$ and split
$Z^+=Z+\tau G'$, $Z^-=Z-\tau G'$. These are independent Gaussian observations
of the same mean with variance $2\tau^2$ per entry. Choose
$\widehat J=\arg\max_j|Z_j^+|$ with deterministic tie breaking. Start with the
original-data direct interval for $A_I$ at error $\alpha/2$, intersected with
$[-M,M]$. Its radius is $z_{1-\alpha/4}\tau$.

Let $\widehat d$ be the number of modes in which $I$ differs from $\widehat J$.
If $\widehat d\le1$, keep this interval. Otherwise take $X=Z^-_{\widehat J}$
and the $\widehat d$ validation fibers $B_k$, replacing only the $k$th changed
index of $\widehat J$ by that of $I$. Form intervals for these
$\widehat d+1$ means with common radius

$$q_{\widehat d}\sqrt2\tau,\qquad
q_e=z_{1-\alpha/[4(e+1)]}.$$

Conditional on the pilot they simultaneously cover their true means with
probability at least $1-\alpha/2$. If the anchor interval excludes zero, use
interval arithmetic to bound the rank-one identity

$$A_I=\frac{\prod_{k\text{ changed}} A_{\widehat J\text{ with index }k\text{ replaced}}}
{A_{\widehat J}^{\widehat d-1}}. \tag{P5.1}$$

Intersect this range with the original interval and structural range. If the
denominator interval includes zero, omit the ratio constraint. Replace an empty
intersection by $\{0\}$. Equation (P5.1) follows directly from a product
factorization whenever the anchor is nonzero. On the simultaneous coverage
event a denominator interval excluding zero guarantees a nonzero true anchor.
Consequently the construction is honest for every rank-one mean, including
zero, arbitrarily weak means, and factors with zero coordinates. A union bound
with the original direct interval gives failure probability at most $\alpha$;
independence between the original and validation intervals is not required.

Choosing an anchor costs $O(D)$; extracting fibers and propagating product
intervals costs $O(K)$ for a fixed target. The algorithm uses no supplied
location or amplitude. A prespecified target is essential: arbitrary
observation-based target selection would require additional calibration.

## Expected-length upper bound at the axis

Write $t=|a|/\tau$. If every pilot noise entry has magnitude below $|a|/2$,
the selected anchor equals $J$. Thus

$$P_{A_0}(\widehat J\ne J)\le2D e^{-t^2/16}. \tag{P5.2}$$

For $d=0,1$ the direct interval always bounds expected length by $C_\alpha\tau$.
For $d\ge2$, conditional on a correct pilot anchor, validation retains its
original independent Gaussian distribution. On
$|Z_J^- -a|\le |a|/2$ and $|a|\ge4q_d\sqrt2\tau$, the absolute value of every
point in the denominator interval is at least $|a|/4$. All changed fibers have
zero means and independent $N(0,2\tau^2)$ observations. The ratio interval
therefore has length at most

$$2(4/|a|)^{d-1}\prod_{k=1}^d(|B_k|+q_d\sqrt2\tau).$$

Its expectation is at most $C_{K,\alpha}\tau^d/|a|^{d-1}$. The complementary
denominator event has probability at most $2e^{-t^2/16}$. On this event and on
incorrect anchor selection, the final length is still at most
$2z_{1-\alpha/4}\tau$. Hence

$$E_{A_0}|C_I|\le C_{K,\alpha}\left\{
\tau^d/|a|^{d-1}+\tau(D+1)e^{-t^2/16}\right\}. \tag{P5.3}$$

If $t^2\ge32\log(eD)$, the exponential term is bounded by
$C_K t^{-(d-1)}$, since $\sup_{t>0}t^{K-1}e^{-t^2/32}<\infty$.
Enlarging $C_{K,\alpha}$ handles the fixed quantile condition, proving the
claimed upper bound. The argument applies to negative $a$ by absolute values;
interval arithmetic retains the denominator sign and its power parity.

## Matching pointwise lower bound, including boundary norms

For $d=0$, reduce the absolute amplitude by $\tau/2$ in its own sign. This
keeps norm at most $M$, changes the target by $\tau/2$, and is within Gaussian
mean distance $\tau/2$ of $A_0$. For $d\ge1$, rotate each of the $d$ changed
mode vectors from $e_{J_k}$ toward $e_{I_k}$ through an angle with
$\sin u=\tau/(4d|a|)$, and retain all other factors and the signed amplitude
$a$. The resulting rank-one mean has norm exactly $|a|\le M$, target
magnitude

$$|a|(\sin u)^d=\frac{\tau^d}{(4d)^d|a|^{d-1}},$$

and distance at most $2d|a|\sin u=\tau/2$ from $A_0$, by telescoping the
product factors. Its Gaussian TV distance is at most $1/4$. The two-point
interval lemma gives the lower bound, even at the boundary $|a|=M$. The same
argument includes $d=1$. This proves P5.

# What has not been solved

General efficient weak-signal minimax computation under several simultaneously
restrictive Tucker or TT caps remains open. The previous binary optimizer is
still an exponential benchmark. M1 is polynomial and statistically optimal
on a substantial full tensor subfamily, but it does not achieve the sharp
fixed-cap diffuse rates. Existing bounded-degree polynomial lower bounds do
not establish hardness for every polynomial-time algorithm or every honest
interval procedure.

L3 resolves every orthogonal profile for fixed caps in order at least four.
Arbitrary cubic profiles, arbitrary nonorthogonal larger-budget profiles, and
uniformly sharp intermediate rates for general vectors of simultaneous growing
caps remain unresolved. M1 resolves all intermediate caps only for its
explicit one-unfolding parameter space. P5 completes the coordinate-axis
hierarchy, not the full theory of arbitrary points, loadings, or growing rank.
These boundaries are retained in the requirements and review registry.

# Relation to primary literature and earlier project stages

The one-cap proof is based on classical spectral duality and a block sign
mixture. Related $\ell_1/\ell_2$ convex geometry appears in Argyriou, Foygel,
and Srebro, *Sparse Prediction with the k-Support Norm* (2012),
<https://arxiv.org/abs/1204.5043>. The experiment and inference claims above
are proved here rather than imported from that prediction paper. The new
proofs establish progress relative to this project's earlier theorems; an
exhaustive literature search establishing external priority has not been made.

Conditional computational barriers in tensor models require carefully matched
experiments and assumptions; see Luo and Zhang, *Tensor Clustering with Planted
Structures: Statistical Optimality and Computational Limits* (2020),
<https://arxiv.org/abs/2005.10743>. Recent bounded-degree results include Fu and
Sohn, *Low-degree estimation thresholds in planted hypergraphs and tensor PCA*
(2026), <https://arxiv.org/abs/2605.30113>. Neither reference licenses an
unconditional impossibility claim for the general optimizer sought here.

The flat-loading and AB1 upper results, P2--P4 constructions, and the executed
subject-level EEG analysis are preserved in `scientific_extension/`. No
real-data analysis was newly run in this stage, and no Gaussian or exact-rank
conclusion is transferred to that application.
