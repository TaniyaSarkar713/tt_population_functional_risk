---
title: "Loading envelopes, scalar adaptation, and bounded-data calibration"
author: "Scientific development supplement"
date: "14 September 2026"
geometry: margin=1in
fontsize: 11pt
---

# Scope and dependency contract

This stage supplies new derivations and implementations. It preserves the reviewed manuscript in `review_revision/`. PROVED below means a complete supplied mathematical argument checked internally, not independent peer review or machine verification. The general fixed-cap weak-signal polynomial minimax optimizer, exact rates for all loading tensors and intermediate caps, and a complete pointwise characterization remain open. P4 also treats one off-tangent rank-one family exactly.

The Gaussian experiment is the **entire** tensor $Z=A+\tau G$, with independent standard normal entries, known $\tau>0$, $\|A\|_F\le M$, and supplied positive Tucker mode or TT cut rank caps. Loading $L$ is known and deterministic. Confidence level $0<\alpha<1/4$ is fixed. $\mathcal L_0,\mathcal L_{\max}$ denote optimal expected length at zero and optimal worst-case expected length among intervals honest on the stated whole class. $\mathcal R$ denotes minimax squared error. Loading results AB1--AB2 have fixed order and caps; their constants need not be uniform in growing caps. P2--P3 explicitly permit growing caps.

The input theorem, proved in `norm_loading_extension/paper/norm_loading_proofs.tex` and retained in the reviewed supplement, is the all-budget flat-loading rate

$$r_K(s,M,\tau)=\frac{\tau\sqrt{\ell_s}}{\sqrt{s}}
\begin{cases}\min\{x,1+\log_+x,\ell_s\},&K=3,\\
\min\{x,1\},&K\ge4,
\end{cases}\quad \ell_s=\log(es),\quad x=M/(\tau\sqrt{\ell_s}).$$

It holds for flat prescribed orthogonal product loadings on $s$ terms, including larger ambient dimensions. Its upper constructions are ideal confidence projections and ideal residual fits. The compensated nonnegative prefix mixtures in that same proof imply, for decreasing absolute orthogonal weights $w_i$, the lower bound $c\max_s w_s\sqrt{s}r_K(s,M,\tau)$. No computation of these ideal fits is assumed in the new algorithms.

# AB1. Every orthogonal loading profile, every budget

**Status: PROVED.** Let $L_w=\sum_{i=1}^p\widetilde w_i U_i$, where each mode's factors in $U_i$ are a prescribed orthonormal family. Sort $w_i=|\widetilde w_i|$ decreasingly, absorb signs into one mode, and put $w_{p+1}=0$. Define

$$F_s=\sqrt{s}r_K(s,M,\tau),\quad
B(w)=\max_{s\le p}w_sF_s,\quad
A(w)=\sum_{s=1}^p(w_s-w_{s+1})F_s.$$

For nonzero $w$ and $M>0$,

$$c B(w)\le\mathcal L_0\le\mathcal L_{\max}\le C A(w),\qquad
c B(w)^2\le\mathcal R\le C A(w)^2,$$

and the rate proxies obey the explicit, constant-free comparison

$$1\le\frac{A(w)}{B(w)}\le1+\log(F_p/F_1)
\le1+\nu_K\log\log(ep),\quad \nu_3=3/2,\quad\nu_{K\ge4}=1/2.$$

Zero loading or zero norm budget gives zero throughout. The proxy comparison is not an explicit confidence-width constant: $c,C$ above still depend on caps, order, and confidence. Evaluating the proxies takes $O(p)$ after sorting, $O(p\log p)$ including sorting; implementing their attaining interval is still an ideal-optimization task.

**Proof of the statistical upper bound.** Abel decomposition gives

$$L_w=\sum_{s=1}^p(w_s-w_{s+1})\sqrt{s}L_s,$$

where $L_s$ is the signed flat prefix loading. Restrict the observed tensor to each prefix block in the known orthogonal bases. Its norm and every unfolding rank stay within the original bounds. Construct the flat-prefix interval with error $\alpha_s=\alpha/[s(s+1)]$. The sum of these errors is less than $\alpha$. The Minkowski sum of these scalar intervals, with the displayed nonnegative coefficients, is therefore honest. Prefixes overlap; no independence is required for the union bound.

The original finite-net threshold for a block of size $s$ and scan support size $t\le s$ is

$$\lambda_t^{(s)}(a)=\tau\sqrt{2\{t\log(es/t)+Kt\log(1+4K)+\log(2s/a)\}}.$$

Since $\log(2s/\alpha_s)=\log(2s^2(s+1)/\alpha)\le 3\log(2s/\alpha)$, replacing fixed $\alpha$ by $\alpha_s$ multiplies this threshold by at most $\sqrt3$. The original norm-sensitive ordered-sum proof therefore still bounds the prefix diameter by $C r_K(s,M,\tau)$ with a constant uniform in $s$. Summing the diameters gives $C A(w)$. For squared loss use the ideal prefix residual fits at budgets $\beta_s=1/[8s(s+1)]$ with deterministic optimization tolerance $\tau$. The same threshold comparison and excess-tail proof give a uniform $L^2$ error bound $C r_K(s,M,\tau)$. In the small-budget case use the structural error cap; otherwise the extra $\tau/\sqrt{s}$ term is bounded by a constant times $r_K$. Minkowski's inequality in $L^2$, again without independence, gives root risk at most $C A(w)$.

**Lower bound.** For each $s$ use the old rank-one nonnegative flat-prefix hard mixture. Multiply the first-mode coordinate $i\le s$ by $w_s/\widetilde w_i$. This contraction preserves the norm bound and rank one. It equalizes the weighted target at $w_s\sqrt{s}$ times the old flat target. Pairwise full-tensor inner products cannot increase because the original factors are nonnegative and the squared multipliers are at most one. The Gaussian likelihood second moment is consequently no larger. The old interval and testing arguments give $c w_sF_s$ and $c(w_sF_s)^2$. Maximize over $s$. Zero weights need not be included.

**Proxy comparison.** Regard $F$ as a function of $t=\log(es)\ge1$. For $K\ge4$, $F(t)=\min(M,\tau\sqrt t)$. For $K=3$,

$$F(t)=\min\{M,\tau\sqrt t[1+\log_+(M/(\tau\sqrt t))],\tau t^{3/2}\}.$$

Each relevant branch is nondecreasing. On $t\le (M/\tau)^2$, the derivative of the middle branch is $\tau\log(M/(\tau\sqrt t))/(2\sqrt t)\ge0$; beyond that point the constant $M$ is minimal. Thus $F_s$ is nondecreasing, $F_1=\min(M,\tau)$, and $F_p/F_1\le\ell_p^{\nu_K}$. Summation by parts gives

$$A=w_1F_1+\sum_{s=2}^p w_s(F_s-F_{s-1}).$$

The sum defining $A$ dominates $w_sF_s$ for every $s$, because its terms with index at least $s$ total at least $F_s\sum_{j\ge s}(w_j-w_{j+1})$. Also $w_s\le B/F_s$, whence

$$A\le B\left[1+\sum_{s=2}^p\frac{F_s-F_{s-1}}{F_s}\right]
\le B[1+\log(F_p/F_1)].$$

The final inequality integrates $1/x$ over each interval $[F_{s-1},F_s]$. This proves AB1.

**Interpretation and limit.** Arbitrary orthogonal profiles now have an all-budget bracket within a doubly logarithmic factor, substantially narrower than the previous unconstrained gap. This does not give exact sharp rates for every profile, nonorthogonal loading tensors, or a polynomial weak-signal procedure. For a known decomposition $L=L_w+R$, one may add an independent-error-budget direct interval for $R$ (independence is unnecessary); its length cost is $O_\alpha(\tau\|R\|_F)$. This supplies an upper bound, not a matching general nonorthogonal theory.

# AB2. Sharp rates for logarithmically decaying profiles

**Status: PROVED.** Let $w_i=c[\log(ei)]^{-\beta}$, $c>0$, with a fixed noncritical $\beta>0$. All the length criteria in AB1 and the square root of minimax squared risk have the rates below, up to constants depending on the fixed exponent, order, caps, and confidence. The scale $c$ may depend on dimension. If $M\le\tau$, every rate is $cM$. Otherwise write

$$m=M/\tau>1,\quad T=\min\{\ell_p,m^2\},\quad U=\min\{\ell_p,1+\log m\}.$$

For $K\ge4$ the rate is

$$c\tau\begin{cases}T^{1/2-\beta},&0<\beta<1/2,\\1,&\beta>1/2.\end{cases}$$

For $K=3$ it is

$$c\tau\begin{cases}
\min\{T^{3/2-\beta},T^{1/2-\beta}[1+\log(m/\sqrt T)]\},&0<\beta<1/2,\\
U^{3/2-\beta},&1/2<\beta<3/2,\\
1,&\beta>3/2.
\end{cases}$$

Critical exponents $\beta=1/2$, and also $3/2$ in order three, retain the AB1 bracket; sharpness is not claimed there. Constants may diverge as an exponent approaches these boundaries. These profiles decay more slowly than every fixed power $i^{-\epsilon}$, so the old fixed-power-decay result does not imply this theorem.

**Proof.** Homogeneity removes $c,\tau$. For $m\le1$, $F_s=m$ identically, so $A=B=m$. Suppose $m>1$, and set $t_s=\log(es)$. The mesh satisfies $1\le t_{s+1}/t_s\le1+\log2$. Moreover $F(t)$ is nondecreasing and grows at most as $t^{3/2}$ (as $t^{1/2}$ for $K\ge4$). Consequently endpoint comparison on every mesh interval, and summation by parts, give

$$B\asymp\sup_{1\le t\le\ell_p}t^{-\beta}F(t),\qquad
A\asymp F(1)+\ell_p^{-\beta}F(\ell_p)
+\beta\int_1^{\ell_p}F(t)t^{-\beta-1}\,dt.$$

The comparison constants depend only on $\beta$ and order. The formula follows directly from the continuous Stieltjes identity $\int_1^\ell t^{-\beta}\,dF(t)=\ell^{-\beta}F(\ell)-F(1)+\beta\int_1^\ell F(t)t^{-\beta-1}dt$; bounded mesh ratios compare each discrete contribution to the corresponding integral. At $p=1$ use $A=B=1$.

For $K\ge4$, $F(t)=\sqrt t$ until $t=m^2$, then $F=m$. The integral below $T$ is $\int_1^T t^{-\beta-1/2}dt$, of order $T^{1/2-\beta}$ if $\beta<1/2$, and bounded if $\beta>1/2$. Any plateau contribution is at most $mT^{-\beta}$ and occurs only when $T=m^2$. Maximizing the same branches yields the identical rates for $B$.

For order three let $t_0\ge1$ be the unique solution

$$t_0+\tfrac12\log t_0=1+\log m.$$

It satisfies $\frac23(1+\log m)\le t_0\le1+\log m$ and $t_0\le m^2$. The three exact branches are $F(t)=t^{3/2}$ on $[1,t_0]$, $F(t)=\sqrt t(1+\log m-\frac12\log t)$ on $[t_0,m^2]$, and $F(t)=m$ thereafter. For $\beta<1/2$, put $a=1/2-\beta>0$. On the middle branch integration uses the explicit primitive

$$\int t^{a-1}(b-\tfrac12\log t)\,dt
=\frac{t^a}{a}\left(b-\tfrac12\log t+\frac{1}{2a}\right),\quad b=1+\log m.$$

Since $b-\frac12\log t\ge1$ up to $m^2$, the integral ending at $T$ is bounded by a constant times $T^a(b-\frac12\log T)$; the early branch is bounded by the same expression when $T>t_0$. If $T\le t_0$, its power integral instead gives $T^{3/2-\beta}$. On the middle branch its weighted value cannot exceed its value at $T$ by more than $1+1/(2ae)$: writing $t=uT$ bounds $u^a[b-\frac12\log T+\frac12\log(1/u)]$ by that multiple of $b-\frac12\log T$. The plateau contributes at most its starting weighted value. Taking $t=T$ supplies the lower bound, which is precisely the first cubic expression.

For $1/2<\beta<3/2$, the early branch increases to $t_0^{3/2-\beta}$; on the middle branch both $t^{1/2-\beta}$ and its positive logarithmic multiplier decrease. Its integral is at most a constant times $t_0^{1/2-\beta}(1+\log m)\asymp t_0^{3/2-\beta}$. The plateau is no larger. If $\ell_p<t_0$, both maximum and integral end at $\ell_p$ instead. Replace $\min(\ell_p,t_0)$ by its comparable $U$. For $\beta>3/2$, the early integral is bounded and the middle contribution is at most a constant times $t_0^{3/2-\beta}\le1$; $t=1$ supplies the lower constant. Thus $A\asymp B$ with the displayed rates, and AB1 completes the proof.

# P2. A scalar safeguard that retains strong-pointwise squared risk

**Status: PROVED.** Let $s=\tau\|L\|_F>0$, let $h$ be any deterministic valid bound for $|\psi_L(A)|$, and choose deterministic $0<\kappa\le1$. Define

$$d=\sqrt{8\log(2/\kappa)},\qquad
\delta=\frac{\alpha\kappa^4}{64(1+d)^4}.$$

Artificial splitting gives independent $Z^+=Z+\tau G'$ and $Z^-=Z-\tau G'$, each of scale $v=\sqrt2\tau$. Suppose a pilot-measurable collection of linear validation candidates $c_j=\langle L_j,Z^-\rangle$ has pilot-measurable bounds $b_j\ge|\langle L_j-L,A\rangle|$ on a common pilot event $E$ of probability at least $1-\delta$, uniformly over the full class. Include the split-direct candidate and the deterministic structural candidate $(c,b,\|L_j\|)=(0,h,0)$. Choose the smallest radius

$$R_j=b_j+qv\|L_j\|_F,\qquad q=z_{1-(\alpha/2-\delta)/2}.$$

Let $c_*$ be this candidate's center **before** any intersection. Intersect its interval with the original-data direct interval of radius $z_{1-\alpha/4}s$ and $[-h,h]$, replacing an empty intersection by $\{0\}$. This interval is honest at level $1-\alpha$. The new scalar estimator is

$$\widehat\psi=\Pi_{[-h,h]}\Pi_{[Y-ds,Y+ds]}(c_*),\qquad Y=\langle L,Z\rangle.$$

Uniformly over the class,

$$\mathbb E_A(\widehat\psi-\psi_L(A))^2\le C_\alpha\min\{h^2,s^2\}.$$

If at a particular $A_0$ there is a candidate with $R_j\le C s\gamma$ everywhere on $E$, where $\kappa\le\gamma\le1$, then

$$\mathbb E_{A_0}|C|\le C' s\gamma,\qquad
\mathbb E_{A_0}(\widehat\psi-\psi_L(A_0))^2\le C' s^2\gamma^2.$$

**Proof of coverage and good-event risk.** Conditional on the pilot, the selected linear validation error is Gaussian with its certified bias and variance $v^2\|L_j\|^2$. The conditional failure probability on $E$ is at most $\alpha/2-\delta$. Adding the pilot event and direct-interval failure budgets gives $\alpha$. Structural intersection cannot remove the true target. On $E$, selection ensures $R_*\le q\sqrt2s$, and under the pointwise hypothesis $R_*\le Cs\gamma$. Since both its absolute conditional bias and standard deviation are bounded by constant multiples of $R_*$, its conditional squared risk is $O(R_*^2)$. This remains valid although the selected center depends on the validation observation: its **index** is selected using only pilot radii.

**Clipping lemma and bad-event risk.** For any real $c,Y,\theta$ and $D\ge0$,

$$|\Pi_{[Y-D,Y+D]}c-\theta|\le
\max\{|c-\theta|,(|Y-\theta|-D)_+\}.$$

If $\theta$ lies inside the interval, metric projection is a contraction toward $\theta$. Otherwise projecting a $c$ lying between $\theta$ and the interval moves it only to the nearest endpoint; in all other cases it either contracts its error or leaves it unchanged. These cases prove the inequality. Projection onto $[-h,h]$ is also a contraction toward the true target. Since $(Y-\theta)/s$ is standard normal, the expected squared overshoot is at most $4s^2e^{-d^2/2}\le s^2\kappa^2$. On $E^c$, the error is bounded by $s(|g|+d)$, so Cauchy--Schwarz gives

$$\mathbb E[(\widehat\psi-\theta)^2\mathbf1_{E^c}]
\le s^2\{\mathbb E(|g|+d)^4\}^{1/2}\sqrt\delta
\le C s^2(1+d)^2\sqrt\delta\le C_\alpha s^2\kappa^2.$$

No independence of $Y$ and $E$ was assumed. Combine with the good-event estimate to get both risk bounds; the deterministic error cap $2h$ gives the structural minimum. On $E$ the final width is at most $2Cs\gamma$, and everywhere it is bounded by $2z_{1-\alpha/4}s$. Thus its expected width is $O(s\gamma+s\delta)=O(s\gamma)$.

**Why the earlier scalar repair is insufficient here.** The earlier R1 estimator used a direct scalar fallback when the narrow CI intersection was empty. Original direct-interval failure has constant probability even at a strong mean, so that proof yielded only noise-scale MSE. P2 uses the pre-intersection center and a wider guard whose tail probability decreases with $\kappa$. It establishes the smaller risk without losing the uniform noise-scale guarantee. It is not a weak-signal minimax estimator.

# P3. Arbitrary-core Tucker and single-cut TT pointwise families

**Status: PROVED.** This section provides a computational realization of P2 and matching pointwise length lower bounds under explicit sufficient conditions. It does not characterize all points or optimal signal thresholds.

For every mode/cut matrix of dimensions $a_j\times b_j$, use

$$\eta_j=2v\sqrt{2\{(a_j+b_j)\log9+\log(2N/\delta)\}},$$

where $N=K$ for Tucker and $N=K-1$ for TT. A $1/4$-net of each unit sphere has at most $9^{a_j}$ and $9^{b_j}$ points; the matrix operator norm is at most twice the largest net contraction. Gaussian tails and the union bound give a common pilot operator-noise event of probability at least $1-\delta$. Let $Q$ be the top supplied-cap pilot singular projector and set

$$e_j=\begin{cases}\min\{1,2\eta_j/(\widehat\sigma_{r_j}-\eta_j)\},&\widehat\sigma_{r_j}>\eta_j,\\1,&\text{otherwise}.\end{cases}$$

Use zero error for a full ambient projector. When the displayed error is less than one, Weyl's inequality forces the true rank to saturate that cap, and the elementary singular-subspace perturbation inequality bounds each appropriate sine angle by $e_j$. Otherwise the trivial bound one remains valid, including at zero and undersaturated points. This is the cap-valid construction A4 from the previous supplement, with P2's smaller failure budget.

**Tucker candidates.** For pilot mode projectors $Q_k$ define the orthogonal projector onto blocks with at most one missing mode

$$T_Q=\sum_{k=1}^K\bigotimes_{j\ne k}Q_j-(K-1)\bigotimes_{j=1}^KQ_j,$$

with an identity in each omitted mode. Use loading $T_QL$ and bias certificate

$$b_Q=M\|(I-T_Q)L\|_F
\min\{1,(\sum_{j<k}e_j^2e_k^2)^{1/2}\}.$$

To verify the certificate, decompose $A$ into mutually orthogonal blocks according to which pilot mode subspaces are missing. Every discarded block misses at least two modes. For a tensor in its true mode product space, the squared norm of all blocks missing both $j,k$ is at most $M^2e_j^2e_k^2$. Summing over pairs overcounts every discarded block at least once. Cauchy--Schwarz against the discarded loading gives the claim. This first-order product-space projector is larger than the exact Tucker tangent space when caps exceed one; no equality with that tangent is asserted.

Let $A_0$ saturate all supplied Tucker mode caps, with true projectors $P_k$, $P=\bigotimes_kP_k$, and $T_P$ as above. Write

$$\gamma_0=\|PL\|_F/\|L\|_F,\quad
\gamma_T=\|T_PL\|_F/\|L\|_F,\quad
 a=\min_k\sigma_{r_k}(A_{0,(k)}),\quad\eta=\max_k\eta_k.$$

Suppose $\|A_0\|_F+\tau\le M$, $\gamma_0\ge\kappa>0$, $\gamma_T\le C_0\gamma_0$, and

$$a\ge4\eta,\qquad \eta/a\le\gamma_0,\qquad
(M/\tau)(\eta/a)^2\le\gamma_0.$$

Then the implemented interval has expected length at most $C\tau\|PL\|_F$ at $A_0$, and the P2 scalar has risk at most $C\tau^2\|PL\|_F^2$. Constants depend on $K,\alpha,C_0$, not the caps or dimensions. Every interval honest on the original unseparated outer class has expected length at $A_0$ at least $c_\alpha\tau\|PL\|_F$.

**Upper proof.** On the common event, subspace perturbation gives $\|Q_k-P_k\|_{\mathrm{op}}\le C\eta/a$. Telescoping each product in $T_Q-T_P$ gives $\|T_Q-T_P\|_{\mathrm{op}}\le C_K\eta/a$, and the bias is at most $C_K M\|L\|_F(\eta/a)^2$. The assumptions imply $R_Q\le C\tau\|L\|_F\gamma_0$. Apply P2 with $\gamma=\gamma_0$. The assumptions describe favorable points; none is required for global honesty of the algorithm.

**Lower proof and the correct risk criterion.** Put $H=PL/\|PL\|_F$. Both $A_0$ and $A_1=A_0+(\tau/2)H$ belong to the outer Tucker ball: the core perturbation preserves the mode subspaces and the norm slack is sufficient. Their target gap is $\Delta=(\tau/2)\|PL\|_F$, and Gaussian total variation is $2\Phi(1/4)-1<1/4$. At $A_0$, honesty at both points gives $\mathbb E_{A_0}|C|\ge\Delta(1-2\alpha-\mathrm{TV})$. For estimation,

$$\inf_{\widehat\psi}\max_{A\in\{A_0,A_1\}}
\mathbb E_A(\widehat\psi-\psi_L(A))^2
\ge\Delta^2(1-\mathrm{TV})/8.$$

An infimum of risk at a single fixed point is zero (the constant estimator at its target achieves it), so a “pointwise minimax MSE lower bound” without a neighborhood or estimator restriction would be false. The displayed local two-point risk lower bound and the pointwise upper bound are the precise statements here. Uniform upper bounds over neighborhoods follow only if the favorable-point conditions hold uniformly there.

**TT candidates and pointwise result.** For each TT cut $j$, let $Q_U,Q_V$ be its top-cap left and right pilot projectors and use

$$T_j(L_{[j]})=Q_UL_{[j]}+L_{[j]}Q_V-Q_UL_{[j]}Q_V,\qquad
b_j=M\|(I-Q_U)L_{[j]}(I-Q_V)\|_F e_j^2.$$

If the cap equals the smaller matrix dimension the tangent projector is the identity and bias is zero. Otherwise the true rank-at-most-cap matrix has discarded Frobenius norm at most $Me_j^2$: project its left and right singular spaces onto the missing pilot spaces and multiply their operator norm bounds. When $e_j=1$ the trivial $M$ bound suffices. Select among all cut candidates and the split-direct/structural candidates by pilot radius. The common event makes selection valid without a separate validation union penalty.

Suppose **one** cut is saturated at $A_0$, with true left/right projectors $P_U,P_V$, smallest nonzero singular value $a$, and

$$\gamma_0=\|P_UL_{[j]}P_V\|_F/\|L\|_F,\qquad
\gamma_T=\|P_UL_{[j]}+L_{[j]}P_V-P_UL_{[j]}P_V\|_F/\|L\|_F.$$

Impose the same conditions as in the Tucker result using $\eta_j,a,\gamma_0,\gamma_T$, including norm slack. Then the same expected-length and pointwise squared-risk upper rates hold with $\|P_UL_{[j]}P_V\|_F$, and this gives the matching outer-honest pointwise length lower bound.

For the lower bound, take $H$ to be the normalized double projection of the loading at that cut. In an exact TT representation of $A_0$, the left interface and right interface can be orthonormalized at that cut without increasing any bond dimension. They span the cut's singular spaces. Inserting an arbitrary matrix between these two interfaces, then absorbing it into an adjacent core, preserves **all** TT bond dimensions. Thus $A_0+(\tau/2)H$ remains in the full TT cap class, not merely the single-cut matrix relaxation. The same two-point proof applies. The upper proof uses $\|T_Q-T_P\|_{\mathrm{op}}=O(\eta_j/a)$ and the quadratic bias bound, followed by P2.

**Complexity and remaining computation gap.** The implementation uses economy SVDs of $K$ mode matrices or $K-1$ cut matrices. With $D=\prod_kp_k$ explicit input entries, the arithmetic cost is $O(\sum_j a_jb_j\min(a_j,b_j))$ plus tensor contractions, and memory is polynomial in $D$. Balanced TT cuts can be expensive despite being polynomial. This is an implemented general cap-valid method with restricted pointwise optimality, not a minimax weak-signal solver. The prior exponential benchmark remains the only implemented globally controlled residual optimizer in its binary rank-one scope.

# D2. All intermediate caps on the exact diagonal-mean submodel

**Status: PROVED; specialization of classical sparse-sequence theory.** Assume additionally that $A=\sum_i a_iE_i$ with at most $r$ nonzero coefficients. This assumption does **not** follow from a tensor rank cap. The full observation reduces to independent $Z_i=a_i+\tau g_i$ on the diagonal plus irrelevant independent noise. For $1\le r\le p$ and all budgets,

$$\mathcal L_0\asymp_\alpha\mathcal L_{\max}\asymp_\alpha
\min\left\{M\sqrt{r/p},\frac{\tau r}{\sqrt p}
\sqrt{\log(1+p/r^2)}\right\},$$

and minimax squared risk has the square of this rate. The following explicit finite-sample construction takes $O(p)$ operations and has constants uniform in $p,r,M,\tau$.

Set $u=\sqrt{2\log(1+p/r^2)}$, $t=\tau u$ and

$$\widehat\psi_t=p^{-1/2}\sum_iZ_i\mathbf1_{|Z_i|>t},\quad
b=rt/\sqrt p,\quad
V=\{2r(t^2+\tau^2)+(p-r)\tau^2\nu(u)\}/p,$$

where $\nu(u)=2[u\phi(u)+\overline\Phi(u)]$. Choose deterministically the shortest of the structural interval of radius $h=M\sqrt{r/p}$, the direct Gaussian interval, and the threshold interval centered at $\widehat\psi_t$ with radius $b+\sqrt{V/\alpha}$. For estimation choose zero, the direct scalar, or $\widehat\psi_t$ by the smallest respective risk bound $h^2,\tau^2,b^2+V$.

**Proof.** At an active coordinate, bias is $-\mathbb E[Z_i\mathbf1_{|Z_i|\le t}]$ and has magnitude at most $t$. At an inactive coordinate it is zero by symmetry. On the retained event the estimation error equals $\tau g_i$, and on the discarded event its magnitude $|a_i|$ is at most $t+\tau|g_i|$. Thus active coordinate MSE, and hence variance, is at most $2(t^2+\tau^2)$. The inactive variance is exactly $\tau^2\nu(u)$. Summing independent coordinates gives bias at most $b$ and variance at most $V$. Chebyshev's inequality proves threshold coverage and $b^2+V$ bounds its MSE. Deterministic selection preserves honesty.

For $r\le\sqrt p$, $u\ge\sqrt{2\log2}>1$ and Gaussian tail integration gives $\nu(u)\le C(u+1)e^{-u^2/2}\le C(u+1)r^2/p$. Therefore $V\le C\tau^2r^2u^2/p$ and the threshold length and root MSE are at most a constant times the claimed stochastic rate. For $r\ge\sqrt p$ that rate is comparable to $\tau$, so the direct procedure suffices. The structural option yields the budget minimum. Finally, the full-data sparse support mixture from G1 uses amplitude $\min(M/\sqrt r,\tau\sqrt{\log(1+p/(4r^2))})$ and gives the same rate below up to a universal constant, since $\log(1+x/4)\ge\frac14\log(1+x)$. Its interval and squared-risk lower arguments apply unchanged.

The underlying sparse-functional rate was established by Collier, Comminges, and Tsybakov, *Minimax estimation of linear and quadratic functionals on sparsity classes*, Annals of Statistics (2017), [primary preprint](https://arxiv.org/abs/1502.00665). The contribution here is a finite-sample interval implementation and its placement within the tensor scope, not a new sparse-sequence minimax rate. General intermediate Tucker/TT caps remain unresolved: dense rank-one tensors can have many nonzero diagonal entries.

# B1. Bounded subject data with calibrated projection bias

**Status: PROVED; elementary application of an existing concentration inequality.** This is a different observation model from Gaussian tensor denoising. Let independent identically distributed subject tensors $W_i$ induce a prespecified bounded scalar $F(W)\in[a,b]$. A pilot sample chooses an arbitrary measurable scalar transform $G(W)\in[a,b]$, for example a clipped loading projection. Let a disjoint calibration sample estimate $H=F-G\in[-R,R]$, $R=b-a$, and a disjoint validation sample estimate $G$. Neither exact low rank nor known Gaussian variance is assumed.

For $n\ge2$ independent identically distributed $X_i\in[l,u]$, define

$$r_{\rm EB}(X,\epsilon)=
\sqrt{\frac{2S_X^2\log(4/\epsilon)}{n}}
+\frac{7(u-l)\log(4/\epsilon)}{3(n-1)},$$

where $S_X^2$ is the unbiased sample variance. Theorem 4 of Maurer and Pontil (2009), [*Empirical Bernstein Bounds and Sample Variance Penalization*](https://arxiv.org/abs/0907.3740), applied to the rescaled variable and its negative with error $\epsilon/2$ each, gives a two-sided bound for its mean. Conditional on the pilot, apply it to $H$ on calibration subjects and $G$ on validation subjects with errors $\alpha/2$. The interval

$$\overline G_V+\overline H_B\ \pm\
[r_{\rm EB}(G_V,\alpha/2)+r_{\rm EB}(H_B,\alpha/2)]$$

covers $\mathbb EF$ with probability at least $1-\alpha$, because $\mathbb EF=\mathbb EG+\mathbb EH$. Intersect with $[a,b]$, using any singleton in $[a,b]$ if empty. Conditional validity integrates over the pilot. Data-dependent projection choices must use only the pilot; selecting based on calibration/validation requires additional simultaneous calibration. No tensor approximation assumption was needed.

This theorem justifies a cautious real-data application and also exposes its price: the residual mean must be learned, and the bounded finite-sample intervals can be much wider than Gaussian approximations. It does not establish efficient minimax inference in the original Gaussian low-rank model. Independence and a common eligible-subject sampling law are assumptions to audit in the application, not facts inferred from the tensor fit.

# What has and has not been resolved

AB1 narrows every orthogonal-profile all-budget rate gap to $O(\log\log p)$, and AB2 closes new noncritical slow-decay families. P2 adds strong-pointwise MSE upper bounds to a globally protected scalar; P3 extends pointwise length optimality to arbitrary-core Tucker and single-cut TT families, with explicit alignment and strong-signal conditions. D2 implements sharp intermediate-cap inference only on an additional exact diagonal model. B1 permits honest bounded-data inference conditional on a defensible subject sampling model and measures projection bias rather than declaring it zero.

A general polynomial fixed-cap weak-signal minimax method, exact arbitrary-loading and general intermediate-cap rates, critical loading exponents, weak/undersaturated/off-core pointwise rates and optimal transition thresholds are still open. No computation performed here certifies a solution of the ideal minimax optimizer outside its preserved binary benchmark. These are substantive remaining research problems.

## B1a. Fixed-stratum extension used in the application

If subjects are iid only within each of $G$ fixed recruitment strata, use fixed nonnegative mixture weights $\pi_g$ summing to one and target $\sum_g\pi_g\mathbb E_gF$. A direct interval combines stratum means and radii at error $\alpha/G$. In the calibrated projection construction, split within each stratum and use error $\alpha/(2G)$ for each stratum's calibration and validation component. Summing the weighted centers and weighted radii gives coverage at least $1-\alpha$ by the union bound. Independence between strata is not needed for that union bound, but the pilot must be independent of the held-out subjects, and the within-stratum concentration assumptions must hold. Mixture weights are fixed as part of the estimand, not interpreted as disease prevalence. This follows from B1 conditionally on the common pilot and avoids a pooled identical-distribution assumption in separately recruited groups.

# P4. Sharp off-tangent inference from a rank-one minor

**Status: PROVED.** This is a further special case beyond P3's positive core alignment. For $K\ge3$ with at least two coordinates in the first two modes, suppose all means have tensor rank at most one and Frobenius norm at most $M$. Fix all remaining coordinate indices at one. Denote four means by

$$x=A_{1,1,1,\ldots,1},\quad b=A_{2,1,1,\ldots,1},\quad
c=A_{1,2,1,\ldots,1},\quad\theta=A_{2,2,1,\ldots,1}.$$

Rank one implies $x\theta=bc$; no assumption that $x$ is nonzero is imposed on the outer class. Observe the corresponding four independent Gaussian entries $X,B,C,Y$. Make intervals for $x,b,c$, each of radius $q\tau$, $q=z_{1-\alpha/12}$, hence each with failure probability $\alpha/6$. If the interval for $x$ excludes zero, take the range of $bc/x$ over these three intervals; its endpoints are the minimum and maximum of the eight corner quotients. If it includes zero, take $[-M,M]$. Intersect with $[-M,M]$ and the direct interval for $\theta$ of radius $z_{1-\alpha/4}\tau$. Replace an empty intersection by $\{0\}$.

This procedure is honest on the entire unseparated rank-one ball and uses four coordinate accesses and a constant number of scalar operations. At $A_0=aE_{1,\ldots,1}$, for $4q\tau\le a\le M$, its expected length satisfies

$$\mathbb E_{A_0}|C|\le C_\alpha\tau^2/a.$$

Every interval honest on that outer ball has $\mathbb E_{A_0}|C|\ge c_\alpha\tau^2/a$. This rate is smaller than the ordinary noise scale, while both the core and first-order tangent projections of the target loading are zero. The anchor and target coordinates are prespecified; this does not solve selection of unknown favorable minors or general higher-order pointwise geometry.

**Larger outer classes.** The same interval and pointwise rate remain valid if only a supplied mode-1 or mode-2 unfolding cap is one, while other caps are arbitrary positive bounds. A rank-one unfolding forces the displayed two-by-two minor identity. The lower alternative remains a rank-one tensor and therefore belongs to every such outer class. For TT, a supplied first-cut cap of one suffices for this particular minor. More general cut locations require choosing the two varying coordinates on opposite sides of the cut. This extension uses an exact supplied rank-one constraint; estimating that constraint from the same data does not preserve the guarantee.

**Coverage proof.** With probability at least $1-\alpha/2$ all three nuisance entries lie in their intervals. If the denominator interval avoids zero, the polynomial rank-one identity forces the true target into the quotient range. If it crosses zero the norm range is a valid substitute, including true $x=0$. The direct interval fails with probability $\alpha/2$. Their intersection therefore has the claimed coverage, uniformly without separation. The quotient extrema are at corners because its numerator is bilinear on a rectangle and division by a denominator with constant sign is monotone for each fixed numerator.

**Expected length proof.** At $A_0$, $X=a+\tau g_0$, $B=\tau g_1$, $C=\tau g_2$, $Y=\tau g_3$ independently. On $H=\{|X-a|\le a/2\}$ the denominator interval has lower endpoint at least $a/4$. Every quotient has absolute value at most $4(|B|+q\tau)(|C|+q\tau)/a$. Thus

$$|C|\mathbf1_H\le8(|B|+q\tau)(|C|+q\tau)/a,$$

whose expectation is $O_\alpha(\tau^2/a)$. Everywhere, final width is at most $2z_{1-\alpha/4}\tau$. Since $\Pr(H^c)\le2e^{-a^2/(8\tau^2)}$ and $e^{-t^2/8}\le C/t$ for $t\ge1$, the complementary contribution has the same upper order. No exponentially small tuning budget is needed: the proof integrates the data-dependent quotient width directly.

**Lower proof.** Take $A_1=a(\cos u\,e_1+\sin u\,e_2)^{\otimes2}\otimes e_1^{\otimes(K-2)}$ with $\sin u=\tau/(4a)$. It remains rank one of norm $a\le M$, and

$$\|A_1-A_0\|_F^2=2a^2\sin^2u=\tau^2/8,\qquad
\theta(A_1)-\theta(A_0)=a\sin^2u=\tau^2/(16a).$$

The Gaussian total variation is bounded away from $1-2\alpha$. The two-point interval argument therefore gives the asserted expected-length lower bound. Norm slack beyond $a$ is unnecessary, since the alternative is a rotation. The usual local two-point squared-risk lower bound also follows, but this section does not assert a globally risk-protected scalar attaining it. In particular the empty-interval midpoint convention must not be promoted to such a scalar guarantee.


**Ratio-inference context.** Confidence sets for ratios have a long history, including Fieller (1954), [*Some Problems in Interval Estimation*](https://academic.oup.com/jrsssb/article/16/2/175/7026708). P4 uses an elementary rectangular-set projection, not Fieller's exact construction. The contribution claimed here is the rank-one second-order pointwise rate and its explicit safe implementation within this project, not invention of ratio confidence intervals. Independent priority assessment of the tensor consequence remains necessary.
