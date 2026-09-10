# New full-data results from the adversarial audit

Status: **PROVED IMPROVEMENTS**, based on the complete derivations below. These are mathematical conclusions of this audit, not a claim of literature priority or independent refereeing. Original input is preserved in input_snapshot.

## S7: finite scan and the full-data expected length at zero

Assume the original full Gaussian experiment, equal dimensions p, fixed K>=3, normalized diagonal loading and either positive Tucker/TT cap class. Write q=2/K, J for the original expansion bound, h0=M sqrt(s_cap/p), s_cap=min(p,smallest cap). Define the injective norm
rho(B)=sup_{||u_k||=1}|<B,u_1 tensor ... tensor u_K>|.

For every nonempty coordinate subset S of size s, fix in advance a 1/(2K)-net of the unit sphere in R^s for each mode. Its cardinality can be at most (1+4K)^s. Let N_S(B) be the largest absolute contraction over the product net, for the subtensor B_(S,...,S).

For gamma in (0,1), define

$$\lambda_s=\tau\sqrt{2\{s\log(ep/s)+Ks\log(1+4K)+\log(2p/\gamma)\}},$$
$$R_\gamma=\frac{4J^{K/2}}{\sqrt p}\sum_{s=1}^p\lambda_s s^{-K/2}.$$

Accept the zero test if N_S(Z)<=lambda_s for every nonempty S. On acceptance use [-min(h0,R_gamma),min(h0,R_gamma)]; on rejection use [-h0,h0]. Call this interval C_scan. It is honest at level 1-gamma over the entire cap class.

For any alpha0+gamma<=alpha, intersect C_scan with the original C_*(alpha0), replacing an empty intersection by {0}. Denote the resulting interval C_dagger and its deterministic original length bound ell_*=|C_*(alpha0)|. Then

$$\inf_A P_A\{\psi(A)\in C_\dagger\}\ge1-\alpha,\qquad
\sup_A E_A|C_\dagger|\le\ell_*,$$
$$E_0|C_\dagger|\le \min\{\ell_*,\,2R_\gamma+\ell_*\gamma\}.$$

For fixed alpha in (0,1/4), fixed caps, M=tau sqrt(p), alpha0=alpha/2 and gamma=alpha/(2p), this gives

$$E_0|C_\dagger|\lesssim_{K,J,\alpha}
\frac{\tau\sqrt{\log p}}{\sqrt p}
\sum_{s=1}^p s^{-(K-1)/2}.$$

Thus the original T6 lower bound matches this upper order for every fixed K>=4:

$$\mathcal L_0(\Theta)\asymp \tau\sqrt{\log p/p}\quad(K\ge4).$$

For K=3 it yields the improved upper bound tau (log p)^(3/2)/sqrt(p). Worst-case expected length remains bounded by the original diagonal rate; no matching full-data worst-case minimax result is obtained.

### Proof roadmap

Construct finite nets; bound all Gaussian net contractions; on a common noise event, test acceptance bounds every subtensor's injective norm; canonical expansions control its Frobenius norm and its ordered diagonal entries; sum those bounds; form an honest interval and control its null expected length.

### Complete proof

1. A maximal epsilon-separated subset of the unit sphere is an epsilon-net. Disjoint radius-epsilon/2 balls around its points fit in the radius-(1+epsilon/2) ball. Comparing Euclidean volumes gives cardinality <=(1+2/epsilon)^s. Compactness ensures a finite maximal set. With epsilon=1/(2K), the stated bound follows. Telescoping the difference of two product tensors one factor at a time gives a contraction error <=K epsilon rho(B)=rho(B)/2. Therefore rho(B)<=2N_S(B), for any tensor B on S^K. No low-rank assumption is used in this net bound.

2. There are at most (ep/s)^s supports of size s. Indeed binomial(p,s)<=p^s/s!, and log(s!)>=integral_1^s log(x)dx>=s log(s)-s. Each net contraction of tau G is normal with variance tau^2 because its product vector has norm one. The two-sided Gaussian Chernoff inequality and a union bound give

$$P\{\exists S:N_S(\tau G)>\lambda_{|S|}\}
\le\sum_{s=1}^p 2(ep/s)^s(1+4K)^{Ks}e^{-\lambda_s^2/(2\tau^2)}
=\gamma.$$

Call the complementary event E_gamma. Dependence between the scanned contractions is allowed.

3. For any cap-class tensor B, its controlled CP expansion gives

$$\|B\|_F^2
=\sum_j\langle B,X_j\rangle
\le\rho(B)\sum_j\|X_j\|_F
\le\rho(B)\sqrt J\left(\sum_j\|X_j\|_F^2\right)^{1/2}
=\rho(B)\sqrt J\|B\|_F.$$

Hence ||B||_F<=sqrt(J)rho(B), including B=0. Cauchy–Schwarz and the squared-weight identity are the precise reasons for the second inequality and final equality. Every subtensor A_(S,...,S) retains the same rank caps: coordinate restriction multiplies any constrained unfolding by selection matrices.

4. If the test accepts and E_gamma holds, the triangle inequality for the finite maximum gives N_S(A)<=2lambda_s. The net inequality implies rho(A_S)<=4lambda_s. Apply original T1 to A_S and then step 3:

$$\sum_{i\in S}|A_{i,\ldots,i}|^q
\le J^{1-q/2}\|A_S\|_F^q
\le J\,\rho(A_S)^q.$$

Let |a|_(s) be the s-th largest absolute diagonal coordinate, and take S to contain the s largest. It follows that s|a|_(s)^q<=J(4lambda_s)^q, and therefore

$$|a|_{(s)}\le4J^{K/2}\lambda_s s^{-K/2}.$$

Summing over s and using |sum_i a_i|<=sum_i|a_i| proves |psi(A)|<=R_gamma on acceptance and E_gamma. On rejection the structural range gives |psi(A)|<=h0 unconditionally. This proves uniform coverage of C_scan.

5. The intersection covers whenever both component intervals cover, so its failure probability is at most alpha0+gamma. Replacing an empty intersection by a singleton does not affect that argument or its length bound. Its length is at most ell_* for every data value. At zero the test rejects with probability at most gamma; on acceptance the intersection has length <=2R_gamma. This proves both expectation inequalities. No independence between the two interval procedures is assumed.

6. For gamma=alpha/(2p), use s log(ep/s)<=s(1+log p), log(2p/gamma)<=2log(2p/alpha), and s>=1. Consequently lambda_s<=C_K tau sqrt{s log(2p/alpha)}, with a constant independent of p. For K>=4, sum_s s^{-(K-1)/2}<=1+2/(K-3). For K=3 the sum is at most 1+log p. The term ell_* gamma is smaller than the displayed upper orders. T6 supplies the matching lower bound at zero for K>=4. It does not supply a matching K=3 lower bound or a worst-case lower bound of the original diagonal order.

### Computational and novelty limits

The scan uses a finite but exponentially large family of contractions: the number is bounded by sum_s binomial(p,s)(1+4K)^(Ks)=(1+(1+4K)^K)^p-1. It is a statistical existence result, not a practical polynomial-time algorithm. No computational lower bound is proved. The scan and confidence-set intersection are classical constructions; their tensor diagonal consequence requires a separate priority assessment.

## S8: a cubic rank-one mixture refutes the draft's Q2 conjecture

Fix K=3, p>=1, 0<alpha<1/4 and M=tau sqrt(p). For any interval honest over a class containing the rank-one Frobenius ball,

$$E_0|C|\ge (3/4-2\alpha)\frac{\tau H_p}{200\sqrt p},
\qquad H_p=\sum_{i=1}^p i^{-1}.$$

The lower order tau log(p)/sqrt(p) is larger than the conjectured tau sqrt(log(p)/p) by a diverging factor sqrt(log p). Q2 is therefore **FALSE for K=3**, in precisely the regime asserted as plausible in the input. The central proved T1–T6 statements are not invalidated.

### Proof roadmap

Use two independent sign vectors to construct a rank-one tensor with a positive harmonic diagonal; show that weighted Rademacher sums have uniform exponential moments of their cubes; use Hölder without assuming independence of the three sums; bound the full Gaussian mixture divergence and apply the common-target interval lemma.

### Complete proof

1. For sign vectors u,v in {-1,1}^p define x_u,i=u_i i^(-1/3) and

$$A_{u,v}=\frac{\tau}{200}\,x_u\otimes x_v\otimes x_{uv}.$$

Its diagonal is tau/(200i), independent of the signs. Its Frobenius norm is

$$\frac{\tau}{200}\left(\sum_{i=1}^p i^{-2/3}\right)^{3/2}
\le\frac{3^{3/2}}{200}\tau\sqrt p\le M.$$

The first bound uses 1+integral_1^p x^(-2/3)dx<=3p^(1/3). Every tensor has rank at most one in every constrained unfolding, and the common target is delta=tau H_p/(200sqrt(p)).

2. Let S_p=sum_(i=1)^p i^(-2/3)epsilon_i for independent uniform signs. For x>=12, let m=floor((x/6)^3). If m>=p the sum has absolute value <=3p^(1/3)<=x/2. Otherwise the absolute contribution of the first m terms is <=3m^(1/3)<=x/2. The remaining sum has sub-Gaussian proxy

$$V_m=\sum_{i>m}i^{-4/3}\le3m^{-1/3}\le24/x.$$

Here m>=0.5(x/6)^3, since (x/6)^3>=8, and 18*2^(1/3)<24. The inequality cosh(t)<=exp(t^2/2), multiplied over the independent tail signs, gives the Chernoff bound

$$P(|S_p|>x)\le 2\exp[-(x/2)^2/(2V_m)]
\le2e^{-x^3/192}\qquad(x\ge12).$$

3. Put u0=1/40000. Tonelli applied to e^(u0 Y)=1+integral_0^Y u0 e^(u0 t)dt, with Y=|S_p|^3, gives

$$E e^{u_0|S_p|^3}
\le e^{1728u_0}
+\frac{2u_0}{1/192-u_0}e^{-(1/192-u_0)1728}
\le\frac{20}{19}+\frac1{100}<\frac54.$$

The final inequalities use 1728/40000<1/20, e^x<=1/(1-x) for 0<=x<1, and 1/192-u0>=1/200. These are uniform in p.

4. Mix the full Gaussian laws of A_(u,v) over independent uniform signs. For independent copies (u',v'), the full tensor inner product divided by tau^2 is

$$\frac1{40000} S_1S_2S_3,$$

where S1=sum_i i^(-2/3)epsilon_i, S2=sum_i i^(-2/3)eta_i, S3=sum_i i^(-2/3)epsilon_i eta_i. Each has the S_p marginal distribution, but the three are dependent. The Gaussian likelihood identity, the arithmetic-geometric mean inequality and Hölder give

$$1+\chi^2(Q,P_0)
=E e^{u_0 S_1S_2S_3}
\le E e^{u_0(|S_1|^3+|S_2|^3+|S_3|^3)/3}
\le\prod_{j=1}^3(E e^{u_0|S_j|^3})^{1/3}
<5/4.$$

Thus TV(Q,P0)<1/4. This calculation uses the **full** tensor likelihood, not its diagonal marginal.

5. All alternatives have common target delta and belong to the original class. The common-target interval lemma yields E0 length>=delta(1-2alpha-TV)>=(3/4-2alpha)delta. Since H_p grows as log p, no honest full-data procedure can have the zero-point length order conjectured in Q2 at K=3.

### Updated full-data conclusions

For fixed positive caps and M=tau sqrt(p):

- K>=4: L0 is PROVED to have order tau sqrt(log p/p), by S7 and original T6.
- K=3: c tau log(p)/sqrt(p) <= L0 <= C tau (log p)^(3/2)/sqrt(p), by S8 and S7. A factor sqrt(log p) remains.
- Lmax: the original diagonal upper order remains valid; no matching full-data worst-case rate is proved.
- No computational-statistical separation or practical optimal scan implementation is claimed.
