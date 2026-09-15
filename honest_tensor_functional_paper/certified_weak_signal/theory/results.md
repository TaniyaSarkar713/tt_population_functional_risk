# Certified optimization, arbitrary loadings, and the meaning of adaptation

Status: 2026-09-11. These are supplied derivations, not independent review or
machine-verified proofs. They build on the all-budget rates in
`norm_loading_extension/` and preserve the previous stages. Results below do
not assert a polynomial minimax algorithm for diffuse weak signals.

Observe the entire tensor $Z=A+\tau G$, with iid standard Gaussian entries,
known $\tau>0$, and $A\in\Theta(M,\bar r)$, a Tucker or TT Frobenius ball.
The functional is $\psi_L(A)=\langle L,A\rangle$; normalization of $L$ is
unnecessary. Write $J=J(\bar r)$ for the existing canonical expansion bound:
$A=\sum_{j\le J}a_j U_j$, each $U_j$ a unit product tensor, and
$\sum_j a_j^2=\|A\|_F^2$. Zero terms can be appended. Assume positive caps.

For reference, the previously established equal/flat-loading rate is
$\mathfrak r_K(m,M,\tau)=\tau\sqrt{\ell_m/m}\,g_K(x)$, where
$\ell_m=\log(em)$, $x=M/(\tau\sqrt{\ell_m})$, and

$$g_K(x)=\begin{cases}
\min\{x,1+\max(0,\log x),\ell_m\},&K=3,\\
\min\{x,1\},&K\ge4.
\end{cases}$$

The original equal diagonal has $m=p$ and weights $1/\sqrt p$.
Length criteria below mean the infimum expected length at zero
($\mathcal L_0$), or the infimum worst-case expected length
($\mathcal L_{\max}$), over intervals honest on the stated parameter class.

## C1. A quantitative contract for approximate minimax optimization

Use every support and every direction in the calibrated finite product nets.
For their unit directions $U$ and thresholds $\lambda_{s(U)}$, put

$$F_Z(B)=\max\{0,\max_U(|\langle U,Z-B\rangle|-\lambda_{s(U)})\}.$$

This function is 1-Lipschitz in Frobenius norm. Suppose an algorithm returns
$\widehat B\in\Theta$ and numbers $l\le\inf_{B\in\Theta}F_Z(B)\le
F_Z(\widehat B)=u$, with $u-l\le\varepsilon$. On the simultaneous noise
event, the true $A$ is feasible, so $F_Z(A)=0$ and $u\le\varepsilon$.
Consequently, for every support size $s$,

$$N_S(\widehat B-A)\le 2\lambda_s+\varepsilon.$$

With $J_2=J(2\bar r)$, the preceding ordered-diagonal proof gives

$$|\widehat B_{i,\ldots,i}-A_{i,\ldots,i}|_{(s)}
\le \min\{2J_2^{(K-1)/2}M,
4J_2^{K/2}(\lambda_s+\varepsilon/2)\}s^{-K/2}.$$

For known orthogonal loading weights $w_i$, sorted by absolute value, the
sum of the right side against $w_s^*$ is an honest radius about
$\psi_L(\widehat B)$. It may be intersected with the structural range.
Choosing $\varepsilon\le c\tau$ retains the existing all-budget minimax
orders for equal/flat loadings. Indeed every $\lambda_s$ is bounded below
by a positive constant times $\tau$, so the added term changes the existing
minimum by only a fixed factor, including in the norm-limited regime.

For squared error set the scan error budget to $1/8$. If the optimizer
guarantees $\varepsilon\le c\tau$ for *every observation*, the same excess
tail proof as before applies: $F_Z(\widehat B)\le F_Z(A)+\varepsilon$ and
$N_S(\widehat B-A)\le2\lambda_s+2F_Z(A)+\varepsilon$. Thus the existing
all-budget MSE bound follows. A budget-limited run with a larger reported gap
does not establish that MSE guarantee.

**Endpoint version.** Let $\mathcal F=\{B\in\Theta:F_Z(B)=0\}$.
If certified outer endpoints enclose $\psi_L(\mathcal F)$, they define an
honest interval, even at an arbitrary computation stop. If feasible
witnesses establish each outer endpoint within $\varepsilon$ of the exact
endpoint, its length exceeds the ideal projection length by at most
$2\varepsilon$. An inner optimization solution alone does not give an
honest interval. On a certified empty feasible set use $\{0\}$, as before.

**Proof.** Lipschitzness follows from $\|U\|_F=1$, the reverse triangle
inequality, and stability of finite maxima. The objective-gap implication
uses $F_Z\ge0$. Rank caps double under subtraction; the norm budget doubles
as well. The ordered bound is exactly the earlier net comparison and
diagonal quasi-norm inequality with $2\lambda_s$ replaced by
$2\lambda_s+\varepsilon$. The Gaussian union event has probability at least
$1-\alpha$. Endpoint containment proves coverage on the same event. For
the length assertion, use an inner feasible witness at each end. The
squared-risk argument invokes the already supplied excess-tail integration,
with only its deterministic tolerance constant changed. No algorithmic
complexity conclusion follows from this contract.

## C2. An implemented global solver on the binary rank-one class

For $p=2$ and any fixed order $K\ge3$, every rank-one tensor of norm at most
$M$ has a representation

$$B(a,\theta)=a\bigotimes_{k=1}^K(\cos\theta_k,\sin\theta_k),
\quad a\in[-M,M],\quad\theta_k\in[0,\pi].$$

Each vector is represented up to sign on a semicircle; the product of signs
is absorbed into $a$. The zero tensor is included. There is no grid
restriction on the parameter space.

The code includes both singleton supports and the full support. For the
latter it uses $n_K=\lceil\pi K\rceil$ equally spaced angles in $[0,\pi)$
per mode. Every unit vector is within Euclidean distance $1/(2K)$ of a net
point up to sign: its angular discrepancy modulo $\pi$ is at most
$\pi/(2n_K)$. Absolute contractions remove the signs. The same telescoping
proof therefore gives $\rho\le2N$. There are $D_1=2$ singleton directions
and $D_2=n_K^K$ full-support directions. Set

$$\lambda_s=\tau\sqrt{2\log(4D_s/\alpha)},\qquad s=1,2.$$

The sum of the two Gaussian union bounds is at most $\alpha$.

For each parameter box, exact real-arithmetic ranges of cosine and products
enclose every scanned contraction and tensor entry. If their contraction
range is $[b_U^-,b_U^+]$, then

$$l_{\rm box}=\max\{0,\max_U[
\operatorname{dist}(\langle U,Z\rangle,[b_U^-,b_U^+])-\lambda_{s(U)}]\}$$

is a lower bound for $F_Z$ throughout the box. Centers provide actual
rank-one upper witnesses. A largest-scaled-side split covers the parent
with two children. Branch and bound retains global lower and upper bounds;
the objective run ends at its requested gap or reports a budget stop.
It implements the ideal residual criterion itself on this class.

For confidence projection reject a box only when its objective lower bound
is positive. Loading-entry interval arithmetic bounds every surviving
box's target; their hull contains the ideal confidence projection. Feasible
amplitude intervals at fixed central factors supply inner witnesses. An
endpoint gap is reported only when such witnesses exist. Endpoints need
not reach a requested tolerance within a finite node budget, especially
near singular feasibility boundaries. This is recorded, not treated as a
successful exact optimization.

The code supports arbitrary loadings in the binary tensor, but caps above
one and mode dimensions above two are not implemented. Exhaustive scans
and global subdivision are exponential. Tests check range containment and
global certificates against independent finite calculations. Floating
point evaluations include conservative guards; these are numerical
certificates under the derived inequalities, not formal directed-rounding
interval proofs. The real-arithmetic method, rather than any particular
floating point tolerance, is the mathematical result.

## L1. Sharp small-budget rates for every loading tensor

Define the product overlap

$$\rho(L)=\sup_{\|u_k\|_2=1}|\langle L,\bigotimes_k u_k\rangle|.$$

For fixed positive caps, fixed $0<\alpha<1/4$, arbitrary mode dimensions,
and *every* known loading tensor $L$, if $0<M\le\tau$, then

$$\mathcal L_0(\Theta;L)\asymp\mathcal L_{\max}(\Theta;L)
\asymp M\rho(L),\qquad
\inf_{\widehat\psi}\sup_\Theta\mathbb E_A
(\widehat\psi-\psi_L(A))^2\asymp M^2\rho(L)^2.$$

Constants depend only on the fixed caps/order and confidence, not on $L$
or the ambient dimensions. The zero loading has identically zero risk and
length. More generally, for all $M,\tau>0$,

$$c_\alpha\rho(L)\min(M,\tau)
\le \mathcal L_0\le\mathcal L_{\max}
\le 2\min\{\sqrt J M\rho(L),\ z_{1-\alpha/2}\tau\|L\|_F\}.$$

**Proof.** The canonical expansion and Cauchy--Schwarz give
$|\psi_L(A)|\le\rho(L)\sum_j|a_j|\le\sqrt J M\rho(L)$.
This gives a deterministic interval and the risk of estimator zero. The
direct Gaussian interval gives the other upper bound; choose between the
two using known quantities. Compactness gives a maximizing product $U$;
choose its sign so $\langle L,U\rangle=\rho(L)$. Both $0$ and $tU$ belong
to every positive cap class, for $t=\min(M,\tau)/2$. Their Gaussian total
variation is $2\Phi(t/(2\tau))-1\le2\Phi(1/4)-1<1/4$.
Honesty at both parameters implies
$\mathbb E_0|C|\ge t\rho(L)(1-2\alpha-\mathrm{TV})$.
The two-point squared-loss lower bound is a fixed positive multiple of
$t^2\rho(L)^2$: classify an estimate by its nearest target. A classification
error entails squared error at least $t^2\rho(L)^2/4$, while the sum of
the two testing errors is at least $1-\mathrm{TV}$. Therefore the larger
squared risk is at least $t^2\rho(L)^2(1-\mathrm{TV})/8$.
For $M\le\tau$ the bounds match. This proof is a direct
specialization of standard Gaussian two-point reasoning, not a novel
general inference principle.

**Limits.** Computing $\rho(L)$ for a general high-order loading is itself
a global optimization problem. A certified upper bound can replace it in
the interval; a certified product witness supplies a lower bound. Without
a constant ratio between them, an efficient sharp algorithm has not been
obtained. This theorem covers all loading tensors in the stated budget
regime; it does not characterize their larger-budget rates. The flat
loading small-budget theorem extends to $M\lesssim\tau\sqrt{\log m}$,
a larger regime than the arbitrary-loading result here.

## L2. An optimized common-target lower bound for unequal weights

For an orthogonal product loading with decreasing nonzero absolute weights
$w_1\ge\cdots\ge w_m>0$, choose $d\le m$ and $0<\Delta\le Mw_d$.
For signed original weights $\widetilde w_i$, set
$A_i=(\Delta/\widetilde w_i)U_i$, $1\le i\le d$.
All alternatives have target $\Delta$, satisfy the norm budget, and have
rank one. They are orthogonal as full tensors. Let

$$v_i=\exp\{\Delta^2/(\tau^2w_i^2)\}-1,\quad
H_d(\Delta)=\sum_{i=1}^d v_i^{-1},\quad
\pi_i=v_i^{-1}/H_d(\Delta).$$

The optimal chi-square divergence among mixtures on these alternatives is

$$\chi^2(Q,P_0)=\min_{\pi\in\mathcal S_d}\sum_i\pi_i^2v_i
=H_d(\Delta)^{-1}.$$

Thus every interval honest on the full tensor class satisfies

$$\mathbb E_0|C|\ge\Delta\left[1-2\alpha-
\frac{1}{2\sqrt{H_d(\Delta)}}\right]_+.$$

**Proof.** The Gaussian likelihood identity gives overlap 1 for distinct
orthogonal alternatives and $1+v_i$ for equal alternatives. Subtracting 1
leaves $\sum\pi_i^2v_i$. Cauchy--Schwarz bounds this below by
$(\sum v_i^{-1})^{-1}$ and the displayed weights attain equality.
Apply $\mathrm{TV}\le\sqrt{\chi^2}/2$ and the common-target interval lemma.
This uses the full observation; there is no diagonal-data restriction.

`weighted_axis_lower` enumerates $d$ and uses scalar root finding for the
largest $\Delta\le Mw_d$ with $\chi^2\le1/4$. Every reported lower bound
uses the actual recomputed divergence and a feasible prior. This optimizes
the prior at each chosen target within the axis family. It is not an
optimization over all tensor alternatives. For equal weights it recovers
the one-spike logarithmic obstruction. It cannot recover the cubic
harmonic obstruction on its own and is not claimed sharp for all weights.

## A1. Unseparated rate adaptation across positive fixed caps

Fix an outer positive Tucker or TT cap vector $\bar r$. Let $\mathcal R$
contain any collection of positive cap vectors componentwise below it.
For equal or flat orthogonal loadings, the *same* full-data outer-class
interval satisfies

$$\sup_{A\in\Theta(M,r)}\mathbb E_A|C_{\bar r}|
\le C_{K,\bar r,\alpha}\,\mathfrak r_K(m,M,\tau),\qquad r\in\mathcal R.$$

Every smaller class contains the rank-one ball, whose lower bound is
$c_{K,\alpha}\mathfrak r_K$. Therefore the interval is simultaneously
minimax in rate over every such class, uniformly in $m,M,\tau$, without
knowing the actual ranks or imposing singular-value separation. The
analogous MSE conclusion holds for the outer-class ideal residual fit.

**Proof.** Restrict the existing outer supremum upper bound to each subset
and apply the same rank-one lower bound inside each smaller class. No
selection step or new probability argument is required.

This observation resolves the fixed-positive-cap, rate-only statistical
adaptation question. It does not give optimal rank-dependent constants,
growing-cap rates, computation, exact-rank selection, or pointwise oracle
lengths. Rank zero must be excluded: its known-model oracle interval has
length zero, whereas outer-class honesty forces positive length at zero.
The preceding ledgers used the word adaptation broadly; these distinct
objectives must be separated.

## A2. A computable projection certificate without separation

Let $Z^{(1)}=A+E^{(1)}$ and $Z^{(2)}=A+E^{(2)}$ have independent iid
Gaussian errors of known scales $\tau_1,\tau_2$. Only $\|A\|_F\le M$ is
assumed here; supplied rank caps are unnecessary. Let $0<\delta<\alpha$.
Use the simultaneous unfolding operator envelopes from the previous stage:

$$\eta_k=2\tau_1\sqrt{2\{(p_k+\prod_{l\ne k}p_l)\log9+
\log(2K/\delta)\}}.$$

On one event of probability at least $1-\delta$ all
$\|E^{(1)}_{(k)}\|_{op}\le\eta_k$. For any pilot-chosen ranks $r_k$, let
$Q_k$ project onto the first $r_k$ left singular vectors of $Z^{(1)}_{(k)}$.
Set $d_k=\sigma_{r_k+1}(Z^{(1)}_{(k)})+\eta_k$ if $r_k<p_k$, and $d_k=0$
if $Q_k=I$. Singular values beyond the matrix rank are zero. For
$P=\bigotimes_k Q_k$, decompose

$$R=(I-P)L=\sum_{k=1}^K R_k,\quad
R_k=\left[\bigotimes_{l<k}Q_l\right]\otimes(I-Q_k)
\otimes\left[\bigotimes_{l>k}I\right]L.$$

Then the observable bound

$$B=\min\left\{M\|R\|_F,\ \sum_k d_k\|(R_k)_{(k)}\|_*\right\}$$

satisfies $|\langle R,A\rangle|\le B$ on that event. The interval centered
at $\langle PL,Z^{(2)}\rangle$, with radius

$$B+z_{1-(\alpha-\delta)/2}\tau_2\|PL\|_F,$$

is honest over the whole norm ball. Any finite set of pilot-selected
projection choices can be compared by their radii on this same event;
choose the smallest before using validation data. Include $P=I$ for the
direct interval and $P=0$ for the structural interval. Intersect with
$[-M\|L\|_F,M\|L\|_F]$ and use $\{0\}$ for an empty intersection.

**Proof.** Residual SVD optimality and the triangle inequality give
$\|(I-Q_k)A_{(k)}\|_{op}\le d_k$ on the common event, even for selected
$r_k$. The definition of $R_k$ gives $(I-Q_k)(R_k)_{(k)}=(R_k)_{(k)}$.
Operator/nuclear norm duality bounds its contraction with $A$ by
$d_k\|(R_k)_{(k)}\|_*$. Sum and combine with the norm-only bound.
Conditional on the pilot, validation noise in the selected loading is
Gaussian with variance $\tau_2^2\|PL\|_F^2$. No multiplicity correction
over the candidate ranks is required: all bias certificates hold on one
uniform pilot event, and the choice precedes validation. The union bound
gives total error at most $\alpha$. Unfolding SVDs, tensor projections and
nuclear norms are polynomial in the explicit input size.

This algorithm never interprets an undetected component as identically
zero. It does not certify the actual rank. Its bias term can be large,
and no weak-signal or pointwise minimax optimality is claimed. Honesty on
the full norm ball cannot yield the low-rank weak-signal minimax gain:
the earlier unrestricted-class lower bound still applies. Independent
artificial Gaussian splitting of one observation is valid with
$\tau_1=\tau_2=\sqrt2\tau$; using both halves at scale $\tau$ is invalid.

### Why the first-order repair does not solve the original problem

For the A2 construction, if $\min_k\eta_k\ge q\tau_2$, where
$q=z_{1-(\alpha-\delta)/2}$, no projected candidate improves the smaller
of the untruncated direct and norm-only radii. In fact, nonzero $R_k$
have $d_k\ge\eta_k$, so triangle inequalities and nuclear/Frobenius norm
comparison give $B\ge\min(M,\min_k\eta_k)\|R\|_F$. Hence its radius is at
least $\min(M,q\tau_2)(\|PL\|_F+\|R\|_F)$, which is at least
$\min(M,q\tau_2)\|L\|_F$. The explicit envelopes meet this condition in
the equal-noise experiments below. This is a proved limitation of this
particular repair, not a universal computational lower bound.

## A3. The adaptation obstruction at an arbitrary orientation

Let a base tensor $A_0$ have norm $a<M$, and leave at least one unused unit
of every supplied Tucker or TT rank cap. Choose mode subspaces $W_k$ such
that $A_0$ is orthogonal to every tensor in
$\mathcal W=\bigotimes_k W_k$. One sufficient choice is to take at least
one $W_k$ orthogonal to the column space of $A_{0,(k)}$. Put
$M_0=\sqrt{M^2-a^2}$ and $L_{\mathcal W}=P_{\mathcal W}L$.
Then

$$\mathbb E_{A_0}|C|\ge c_\alpha\min(M_0,\tau)\rho(L_{\mathcal W})$$

for every interval honest on the outer class. If the restriction of the
loading to an $m$-dimensional orthogonal diagonal block in $\mathcal W$
equals $b$ times a flat unit loading, the stronger bound is

$$\mathbb E_{A_0}|C|\ge c_{K,\alpha}|b|\,
\mathfrak r_K(m,M_0,\tau).$$

Here $\rho$ is taken within the indicated product subspace. The zero
overlap case gives a zero lower bound and says nothing further.

**Proof.** Add rank-one perturbations $B\in\mathcal W$ with norm at most
$M_0$. Rank subadditivity keeps $A_0+B$ in every outer unfolding cap;
orthogonality gives $\|A_0+B\|_F^2=a^2+\|B\|_F^2\le M^2$.
Translate the Gaussian experiment by $A_0$. The target difference is
$\langle L_{\mathcal W},B\rangle$. Apply the two-point construction of L1
or the existing flat-loading mixtures, all of which have rank one.
Unused observed coordinates contain identical independent Gaussian noise
under both hypotheses and do not change the likelihood calculation.
This is a rotation-invariant extension of the preceding block-supported
shifted bound, not a complete characterization at every mean.

## A4. A cap-valid tangent interval on the original unseparated class

There is a more useful repair when mode caps $\bar r_k\le p_k$ are supplied.
Use the same independent Gaussian pilot and validation data and envelopes
as A2. Let $Q_k$ project onto the leading $\bar r_k$ pilot left singular
vectors. Define

$$e_k=\begin{cases}
0,&\bar r_k=p_k,\\
\min\{1,2\eta_k/(\sigma_{\bar r_k}(Z^{(1)}_{(k)})-\eta_k)\},
&\bar r_k<p_k,\ \sigma_{\bar r_k}(Z^{(1)}_{(k)})>\eta_k,\\
1,&\text{otherwise}.
\end{cases}$$

With the first-order product-space projector from the previous stage,

$$T=\bigotimes_k Q_k+\sum_k(I-Q_k)\otimes\bigotimes_{l\ne k}Q_l,$$

put $R=(I-T)L$ and

$$B_T=M\|R\|_F\min\{1,(\sum_{k<l}e_k^2e_l^2)^{1/2}\}.$$

The interval centered at $\langle TL,Z^{(2)}\rangle$, with radius
$B_T+q\tau_2\|TL\|_F$, is honest on **every** tensor with these supplied
mode caps and norm bound, including zero, arbitrarily weak signals, and
actual ranks strictly below the caps. No singular-value separation is
assumed. Choose the smallest pilot-measurable radius among this candidate,
the direct interval, and the structural norm interval, as before.

**Proof.** Let $V_k$ be the actual left singular subspace of $A_{(k)}$.
On the simultaneous noise event we claim
$\|(I-Q_k)P_{V_k}\|_{op}\le e_k$. This is immediate for $e_k=1$ or
$Q_k=I$. Otherwise $\sigma_{\bar r_k}(Z^{(1)}_{(k)})>\eta_k$ forces
the true mode rank to equal the supplied cap: a smaller true rank would
give that observed singular value at most $\eta_k$ by Weyl's inequality.
The pilot tail after the cap is at most $\eta_k$, so
$\|(I-Q_k)A_{(k)}\|_{op}\le2\eta_k$. Multiplying by the inverse nonzero
singular values and using
$\sigma_{\bar r_k}(A_{(k)})\ge
\sigma_{\bar r_k}(Z^{(1)}_{(k)})-\eta_k$ proves the claim.

Decompose $A$ into the mutually orthogonal mode-projector blocks indexed by
which modes fall in $I-Q_k$. The complement of $T$ consists of blocks with
at least two such modes. Counting each block once is bounded by counting
it for every contained pair. Consequently

$$\|(I-T)A\|_F^2\le\sum_{k<l}
\|(I-Q_k)(I-Q_l)A\|_F^2
\le M^2\sum_{k<l}e_k^2e_l^2.$$

The last inequality restricts each operator to its true mode subspace and
uses that operators on distinct modes commute. Combine with the trivial
bound $\|(I-T)A\|_F\le M$ and Cauchy--Schwarz against $R$.
Conditional Gaussian validation and the common pilot event now prove
coverage and valid radius selection exactly as in A2.

This algorithm is polynomial and honest for the original weak-signal
class. Strong signals can make the second-order bias correction small,
even though separation is not a coverage assumption. It is **not** a
polynomial weak-signal minimax solution or a method of estimating actual
rank. At smaller actual ranks, the unresolved cap singular values trigger
conservative error bounds. For a supplied TT cap vector, valid mode caps
are $\min(p_k,\bar r_{k-1}\bar r_k)$, with boundary TT ranks one;
the interval does not estimate TT bond ranks. Artificial splitting must
use its increased noise scales.

For the original single observation, `single_observation_interval` creates
$Z\pm\tau G'$ with independent artificial $G'$, uses scales
$\sqrt2\tau$ and error $\alpha/2$ for the cap-valid construction, and
intersects with the direct interval based on $Z$ at error $\alpha/2$.
The union bound proves honesty at error $\alpha$ despite the dependence
between these two intervals. The direct component caps the reported
length at $2z_{1-\alpha/4}\tau\|L\|_F$. The split is randomization within
the original experiment, not an extra observed replicate.

## Remaining problems

1. Polynomial minimax intervals for diffuse weak-signal classes at general
   dimensions: open. The new optimizer establishes a working global
   benchmark only for binary rank-one tensors; it does not remove the
   computational obstruction.
2. Sharp larger-budget rates for every loading, including every unequal
   weight sequence: open. L1 resolves all loadings only for $M\le\tau$;
   L2 strengthens the usable lower-bound machinery.
3. General rank-dependent and pointwise adaptation: open, with explicit
   impossibility results for some oracle demands. Rate adaptation over
   fixed positive nested caps is already attained statistically (A1).
4. General Tucker/TT global optimizers, validated directed-rounding
   arithmetic, and high-dimensional runtime scaling: not implemented.
