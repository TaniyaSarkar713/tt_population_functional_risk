# Additional verified strengthenings

All statements below are **PROVED IMPROVEMENTS** to the indicated restricted result. They are not claimed as novel principles. They do not transfer Gaussian lower bounds to a different experiment without an explicit comparison.

## S1. A smaller deterministic diagonal budget

For Tucker caps define
$$D_{\rm Tu}=\min\left\{J_{\rm Tu}^{1-1/K},\
m^{1-1/K},\
\left(\prod_{k=1}^K\bar r_k\right)^{1/K}\right\}.$$
Then sum_i |a_i|^(2/K)<=D_Tu M^(2/K). For TT caps put rbar_0=rbar_K=1 and rho_k=min(p_k,rbar_(k-1)rbar_k). A valid coefficient is
$$D_{\rm TT}=\min\left\{J_{\rm TT}^{1-1/K},\
m^{1-1/K},\
\left(\prod_{k=1}^K\rho_k\right)^{1/K}\right\}.$$

**Proof roadmap:** retain the original expansion bound; add the ambient diagonal bound and a mode-subspace bound; take their minimum.

**Proof.** Orthonormality of the product atoms gives sum_i|a_i|^2<=||A||_F^2. Hölder for a sequence of length m gives the second coefficient. For a Tucker representation with mode projectors P_k, let l_(ki)=||P_k v_(ki)||^2. Since A lies in the tensor product of those subspaces, Cauchy–Schwarz gives |a_i|<=||A||_F product_k sqrt(l_(ki)). Thus
$$\sum_i|a_i|^{2/K}
\le M^{2/K}\sum_i\prod_k l_{ki}^{1/K}
\le M^{2/K}\prod_k\left(\sum_i l_{ki}\right)^{1/K}
\le M^{2/K}\prod_k\bar r_k^{1/K}.$$
The middle step is Hölder; the final step is the trace bound sum_i||P_k v_(ki)||^2<=rank(P_k). For a TT tensor, fixing the left and right bond indices at core k expresses its mode-k unfolding through at most r_(k-1)r_k physical vectors, so its mode rank is at most rho_k. Apply the Tucker subspace bound. The original CP-weight bound supplies the first coefficient in each minimum.

The improved radius is ||w||_infinity D M^(2/K)(2lambda)^(1-2/K). This reduces dependence on some growing caps; it does not establish optimal rank dependence. For equal Tucker caps r and K>=3 the new subspace coefficient is r, whereas the original is r^((K-1)^2/K). The original experiment code used the original coefficient and remains valid.

For nonorthogonal unit loading families with Bessel bounds sum_i v_(ki)v_(ki)^T <= F_k I, the original CP proof instead gives coefficient J^(1-1/K) product_k F_k^(1/K). Marginal noise calibration remains necessary, and the direct variance must use the actual ||L||_F. This is a relaxation with explicit geometry cost, not an arbitrary-loading theorem.

## S2. Exact structural range and optimal fixed affine radius

The structural radius is exact:
$$\sup_{A\in\Theta}|\psi(A)|
=M\left(\sum_{i=1}^{s_{\rm cap}}w_{(i)}^2\right)^{1/2}=h_0.$$
The upper bound is original Lemma 4. For attainment, let T be the indices of the s_cap largest weights and set
A=M sum_(i in T) w_i V_i /sqrt(sum_(i in T)w_i^2).
The atoms are orthonormal, so the Frobenius norm is M. Every constrained rank is at most |T|, and the functional equals h0. Taking the negative gives the other endpoint; scalar multiples fill the interval.

For the equal diagonal loading put a0=M sqrt(s_cap/p). Let Q_alpha(mu,v) be the smallest h>=0 with P{|N(mu,v^2)|<=h}>=1-alpha, for mu,v>=0, defining Q_alpha(mu,0)=mu. If 0<alpha<1/2, the optimal radius over **all full-data fixed-radius affine intervals** on either cap class is exactly
$$h_{\rm aff}^*=\min_{0\le t\le1}Q_\alpha(a_0(1-t),\tau t).$$
It is attained by center t<L,Z> with zero offset. If a0<=z_(1-alpha)tau, then h_aff^*=a0. In particular, at cap one, M=tau sqrt(p) and alpha=0.05, the optimum length is exactly 2tau. The old harmonic lower bound is valid but loose.

**Proof roadmap:** force a bias using the s_cap largest diagonal coefficient errors; force a variance through projection on L; reduce normal coverage to a scalar bounded-mean problem; attain both bounds by a scalar shrinkage center.

**Proof.** Write any center as <W,Z>+b and t=<W,L>. Set g_i=<W,E_i>-p^(-1/2). The cap class contains every s_cap-sparse diagonal tensor of Frobenius norm at most M. Maximizing the bias over opposite such tensors gives a mean-error magnitude at least
$$|b|+M\left(\sum_{i=1}^{s_{\rm cap}}g_{(i)}^2\right)^{1/2}
\ge a_0|1-t|.$$
The inequality uses sum_top_s g_i^2 >=(s/p)sum_i g_i^2 and ||g||_2>=|sum_i g_i|/sqrt(p)=|t-1|. The noise standard deviation is tau||W||_F>=tau|t|.

For confidence greater than one half, an honest radius h must be at least the absolute mean error at each parameter: otherwise the interval lies strictly on one side of a normal median (and misses a deterministic mean when variance is zero). For h>=mu, the normal interval probability
F(h;mu,v)=Phi((h-mu)/v)+Phi((h+mu)/v)-1
decreases with mu>=0 and with v>0. The first derivative follows by comparing the two normal densities; the second is
-[(h-mu)phi((h-mu)/v)+(h+mu)phi((h+mu)/v)]/v^2<=0.
Therefore h>=Q_alpha(a0|1-t|,tau|t|). Degenerate v=0 follows by its definition. If t<0, this lower bound is at least a0; if t>1 it is at least z_(1-alpha/2)tau. Both endpoints are achievable, so it suffices to optimize t in [0,1]. For center t<L,Z>, the variance is exactly tau^2t^2 and the worst bias is exactly a0(1-t), by the range calculation above. It attains the scalar bound. Continuity of the quantile, including its limit as v decreases to zero, gives existence on the compact interval.

Finally P{|N(mu,v^2)|<=h}<=Phi((h-mu)/v), so Q_alpha(mu,v)>=mu+z_(1-alpha)v. If a0<=z_(1-alpha)tau, every t in [0,1] therefore has radius at least a0; t=0 attains it. This is the classical bounded-normal-mean mechanism, now reduced exactly for the tensor cap class. See Stark (1992), DOI 10.1016/0167-7152(92)90234-V; its scalar result is background, not an unverified external step in this proof.

## S3. General noise envelopes, tuning and approximate ranks

Let d_i=a_i+e_i under any distribution satisfying
$$\inf_A P_A\{\max_i|e_i|\le\lambda_0\}\ge1-\alpha.$$
No independence, Gaussianity, covariance invertibility or mean-zero condition is required beyond this uniform envelope. If Lambda is any measurable tuning value with Lambda>=lambda0 almost surely, then the threshold interval with center sum_i w_i soft_Lambda(d_i) and radius
$$\|w\|_\infty D M^q(2\Lambda)^{1-q}$$
is honest, where D can be original J^(1-q/2) or the improved coefficient. This holds simultaneously for all Lambda>=lambda0 on the same event. A data-dependent choice between this interval and the certain structural interval is also valid. Adding the direct Gaussian interval requires deterministic selection, independent calibration, or a separate joint error allocation.

For independent Gaussian coordinates, the exact envelope threshold is
$$\lambda_0=\tau\Phi^{-1}\{[1+(1-\alpha)^{1/m}]/2\}.$$
It is smaller than the manuscript Chernoff threshold and gives the same rate. With arbitrary dependence and Gaussian marginal variance <=tau^2, the Bonferroni threshold tau Phi^(-1)(1-alpha/(2m)) is valid. With marginal sub-Gaussian mgf E exp(t e_i)<=exp(t^2 v^2/2), use v sqrt(2log(2m/alpha)). With E|e_i|^a<=v^a for a>0, Markov gives lambda0=v(m/alpha)^(1/a). The latter generally worsens dimension dependence.

**Approximation theorem.** Define the outer class
Theta^eta={A: there exists B in Theta(M,rbar) with ||A-B||_F<=eta},
with eta known. Under the same envelope, an honest threshold radius is
$$\|w\|_\infty D M^q(2\Lambda)^{1-q}+\eta.$$
The structural radius becomes h0+eta. For an unchanged Gaussian observation model, the direct radius is unchanged, and deterministic smallest-radius selection remains valid.

**Proof roadmap:** use the original deterministic threshold envelope; identify the correct residual Lipschitz map so that approximation costs eta rather than 2eta.

**Proof.** On the envelope event, original Lemma 3 applies for every Lambda>=lambda0. Its pathwise inequality proves the first assertion. The Gaussian formula follows from the product of m probabilities 2Phi(lambda0/tau)-1; the marginal and moment versions follow respectively from a union bound, Chernoff and Markov. Their assumptions are exactly those stated.

For approximation, at each fixed noise value e, the map f_e(x)=soft_Lambda(x+e)-x equals e-clip(x+e,[-Lambda,Lambda]). It is 1-Lipschitz. Hence, writing a_i=<A,V_i> and b_i=<B,V_i>,
$$\left|\sum_i w_i[f_{e_i}(a_i)-f_{e_i}(b_i)]\right|
\le\|w\|_2\|a-b\|_2\le\|A-B\|_F.$$
Cauchy–Schwarz and Bessel justify the two inequalities. Add the threshold error bound at B. Likewise |psi(A)-psi(B)|<=eta, giving the structural radius. The argument holds for every B simultaneously on the same noise event, yielding the oracle bound
$$|\widehat\psi-\psi(A)|
\le\inf_B\{\|w\|_\infty D_B\|B\|_F^q(2\Lambda)^{1-q}
+\|{\cal D}_L(A-B)\|_2\}.$$
The oracle's right side is unknown; this is not an actual-rank-adaptive confidence interval.

For Tucker approximation, if P_k projects onto rbar_k leading mode singular vectors, B=(tensor_k P_k)A has the required ranks, ||B||_F<=||A||_F, and
||A-B||_F^2<=sum_k sum_(j>rbar_k)sigma_j(A_(k))^2.
The mode projections commute. Decompose I-product P_k into successive orthogonal residual projections; their squared norms add and each is bounded by ||(I-P_k)A||_F^2. This proves the tail certificate without an eigengap; any leading singular subspace works in a tie. The distance-class formulation already covers TT approximation; no unproved sharp TT-tail formula is needed here.

## S4. Finite variance and bounded adversarial row corruption

Suppose clean tensor replicates W_1,...,W_n are independent, have common mean A, and each prescribed contraction has variance at most v^2, with v known. Coordinates within a replicate may be dependent. An adversary may replace at most c entire replicates, even after seeing the clean sample. Choose an odd b satisfying
$$b\ge8c,\quad b\ge32\log(m/\alpha),\quad n\ge2b,$$
put k=floor(n/b), and split the first bk replicates into b deterministic disjoint blocks. Let d_i be the median of the b block means for contraction i. Then
$$P\{\max_i|d_i-a_i|>2v/\sqrt k\}\le\alpha.$$
Applying S3 therefore gives an honest interval under finite variance and this explicit corruption model. With c=0, its threshold is O(v sqrt(log(m/alpha)/n)), recovering the Gaussian order, with larger constants and access to replicates. For general c,
lambda=O(v sqrt(c/n+log(m/alpha)/n)).
No sharp contamination-rate claim for the tensor functional is made.

**Proof.** A clean block mean has variance <=v^2/k, so Chebyshev bounds its probability of error above 2v/sqrt(k) by 1/4. For a fixed coordinate let I_j be the clean-block error indicators. They are independent with sum of expectations at most b/4. At most c block summaries are altered, even by an adaptive adversary. If the final median errs, then sum I_j>=b/2-c>=3b/8.

For an indicator I, h(t)=log E exp[t(I-EI)] has h(0)=h'(0)=0 and h''(t)<=1/4, since it is the variance of an exponentially tilted Bernoulli. Thus h(t)<=t^2/8. Independence and Markov give
P{sum(I_j-EI_j)>=b/8}<=exp(-tb/8+bt^2/8).
At t=1/2 this is exp(-b/32). A union bound over m coordinates proves the event. Since k>=n/(2b), the stated rate follows for the smallest admissible odd b. The structural/approximation argument in S3 finishes the confidence statement. Only block independence is used; martingale or mixing extensions would need an alternative median-tail proof.

Huber contamination is a different model. Under independent Bernoulli replacements of probability epsilon, choose c=ceil(2n epsilon+2log(1/delta)). Since E 2^N<=(1+epsilon)^n<=exp(n epsilon), Markov gives P(N>c)<=delta. S4 applied on that count event, with failure budget alpha0, yields coverage >=1-alpha0-delta when its b,n conditions hold. This conversion is explicit and does not equate random contamination with a deterministic count bound.

## S5. Unknown Gaussian noise with retained replicates

Suppose n>=2 and the original independent Gaussian tensor replicates are retained. Let d_ji=<W_j,V_i>, let nu=m(n-1), and define
$$S^2=\nu^{-1}\sum_i\sum_j(d_{ji}-\bar d_i)^2,\qquad
\sigma_U=S\sqrt{\nu/\chi^2_{\nu,\delta}}.$$
Here chi^2_(nu,delta) is a lower delta quantile and 0<delta<alpha. Let alpha0=alpha-delta, and compute the original three radii with tau_U=sigma_U/sqrt(n) and alpha0. Select the smallest, using only S and supplied quantities. The resulting interval is honest at level 1-alpha.

**Proof.** For each i, an orthogonal transformation in the replicate index separates the mean direction from n-1 residual coordinates. Joint Gaussianity makes all transformed coordinates independent. Across i, loading orthonormality makes the projected replicate arrays independent. Consequently nu S^2/sigma^2 has a chi-square_nu law and is independent of the vector of sample means. Therefore P(sigma_U>=sigma)=1-delta. Conditional on S with sigma_U>=sigma, both Gaussian and threshold radii are conservative at error level alpha0, and the selected index is independent of the mean noise. The structural interval covers surely. Integrating conditional failure and adding delta gives total failure <=alpha0+delta=alpha.

As nu tends to infinity, sigma_U/sigma tends to one in probability: chi-square_nu/nu has mean one and variance 2/nu, and its fixed-delta quantile divided by nu tends to one by Chebyshev. Its second moment is nu/chi^2_(nu,delta), tending to one; thus powers of order at most one are uniformly integrable. The nonlinear expected length has the original order. This uses information in retained residuals; it is not a variance estimate from Z alone or a parameter-free finite-variance theorem.

## S6. Confidence levels and nonisotropic Gaussian noise

The alpha<1/4 restriction in the mixture bounds is a convenient constant choice, not a statistical boundary. For any alpha<1/2 choose eta in (0,1-2alpha). The original coordinate mixture can instead use a=min{M,tau sqrt(log(1+4eta^2p))}, giving
E0|C|>=(1-2alpha-eta)a/sqrt(p).
For the single-unfolding mixture use theta=min{M,c_eta tau sqrt(p)}, where
$$c_\eta^2=\tfrac12\{1-(1+4\eta^2)^{-2}\}.$$
Its chi-square bound is <=4eta^2. For the diagonal support mixture use
b_s=min{M s^(-K/2),tau sqrt(log[1+log(1+4eta^2)p/s^2])}.
The same hypergeometric calculation gives chi-square <=4eta^2. These substitutions prove the claims and retain fixed-alpha rates. Original Theorem 5 must explicitly restrict alpha to the range used by its original constants; its unqualified affine assertion is false at alpha=.9.

For Gaussian noise with known covariance Sigma, the threshold upper bound requires only upper bounds on V_i^T Sigma V_i. The direct radius uses z sqrt(L^T Sigma L), with a zero-radius exact interval if this variance is zero. Gaussian lower bounds can be transferred when Sigma>=s0^2 I: an observation with covariance Sigma is obtained from N(A,s0^2I) by adding independent N(0,Sigma-s0^2I). Applying any Sigma-procedure after this randomization creates an honest isotropic procedure, so all-procedure isotropic lower bounds apply with tau=s0. No pointwise ordering of cross likelihood terms B^T Sigma^(-1)C is used; that ordering would generally be invalid.
