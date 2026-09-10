# D1: classical optimal length benchmark for diagonal observations

This target is formulated and checked before inclusion in the revised manuscript. It is a classical sparse-Gaussian specialization, not a claim of a new lower-bound technique. The full tensor experiment must be kept separate.

## Candidate statement and status

**PROVED**, by the derivation below. Let Theta_1 be the rank-one tensor Frobenius ball, let L=p^(-1/2) sum_i e_i^(tensor K), and restrict interval procedures to the diagonal observation d=(Z_(i,...,i))_(i=1)^p, with possible independent randomization. For any integer 1<=s<=p, define

$$b_s=\min\left\{M s^{-K/2},\;\tau\sqrt{\log\left(1+\frac{p}{4s^2}\right)}\right\},\qquad
c_{\alpha,d}=1-2\alpha-\frac12\sqrt{e^{1/4}-1}.$$

For 0<alpha<1/4, every such interval honest over Theta_1 has

$$E_0|C(d)|\ge c_{\alpha,d}\frac{s b_s}{\sqrt p}.$$

Consequently, for fixed K>=3 and M=tau sqrt(p), both the pointwise-at-zero optimal expected length and the worst-case optimal expected length among diagonal procedures have rate

$$\tau\left(\frac{\log p}{p}\right)^{(K-2)/(2K)}.$$

This matching rate says nothing by itself about optimality among procedures using the entire observed tensor. The original full-data minimax question remains PARTIAL.

## Complete proof

1. **Parameter membership and common target.** The exact-image lemma shows that the diagonal parameter class is {a: sum_i |a_i|^(2/K)<=M^(2/K)}. For each size-s support S, take a^S=b_s 1_S. Its q-power is s b_s^(2/K)<=M^(2/K), and its target is delta_s=s b_s/sqrt(p). A corresponding full tensor is

   A_S=b_s (sum_(i in S)e_i)^(tensor K),

   whose Frobenius norm is b_s s^(K/2)<=M. It has all Tucker/TT ranks at most one. This construction proves feasibility; the lower bound below observes only its diagonal.

2. **Exact diagonal likelihood second moment.** Mix uniformly over the binomial(p,s) supports. Let S,T be independent supports, J=cardinality(S intersection T), and Q_d the mixture of their diagonal Gaussian laws. The Gaussian-shift identity gives

$$1+\chi^2(Q_d,P_{0,d})=E\exp(b_s^2J/\tau^2).$$

3. **Hypergeometric moment bound, with proof.** Conditional on S, J is hypergeometric with population p, success count s and sample size s. For j<=s, counting j-element subsets of S that also belong to T gives

$$E\binom Jj=\binom sj\frac{(s)_j}{(p)_j},$$

where (x)_j=x(x-1)...(x-j+1), and the j=0 value is one. For each factor with 0<=ell<j,

$$(s-\ell)/(p-\ell)\le s/p$$

because s<=p. Hence E binom(J,j)<=binom(s,j)(s/p)^j. Setting t=exp(b_s^2/tau^2)-1>=0 and expanding (1+t)^J gives

$$E e^{b_s^2J/\tau^2}\le\sum_{j=0}^s\binom sj(st/p)^j
=(1+st/p)^s\le\exp(s^2t/p).$$

The definition of b_s implies t<=p/(4s^2), so 1+chi^2<=exp(1/4). Total variation is at most eta_d=0.5 sqrt(exp(1/4)-1)<1/2.

4. **Interval lower bound.** Apply the common-target confidence-interval mixture lemma from P6: E_0 length>=delta_s(1-2alpha-TV). This proves the finite-sample statement. Independent randomization leaves TV unchanged. Since alpha<1/4 and eta_d<1/2, c_(alpha,d)>0.

5. **Asymptotic choice of support.** Let x_p=(p/log p)^(1/K) and s_p=floor(x_p). For sufficiently large p, x_p/2<=s_p<=x_p. Under M=tau sqrt(p), the norm-bound term M s_p^(-K/2) is at least tau sqrt(log p). The other term is at most tau sqrt(log p), because s_p>=1 and 1+p/4<=p for p>=2. Thus b_(s_p) equals the logarithmic noise term for all sufficiently large p. Furthermore s_p<=p^(1/K) for log p>=1, giving

$$\log\{1+p/(4s_p^2)\}\ge\log\{1+p^{1-2/K}/4\}
\ge\tfrac12(1-2/K)\log p$$

for sufficiently large p. Therefore s_p b_(s_p)/sqrt(p) is bounded below by a positive K-dependent constant times tau(log p/p)^((K-2)/(2K)). T2 with J=1 supplies a matching upper bound with deterministic length, covering both expected-length criteria.

6. **Why this is not a full-data lower bound.** For the full tensors constructed in step 1,

$$\langle A_S,A_T\rangle=b_s^2J^K,$$

whereas their diagonal inner product is b_s^2J. The full-data mixture second moment is therefore E exp(b_s^2 J^K/tau^2), which is not bounded by the hypergeometric argument in step 3. Closeness of marginal distributions does not imply closeness of their full distributions. This is the exact point where an invalid minimax claim would arise.

## Attribution and empirical implication

Collier–Comminges–Tsybakov (2017), Theorems 2–3, already establish sharp linear-functional estimation rates over ell_q balls, and their Lemma 1 supplies the hypergeometric mixture mechanism. The present confidence-interval statement is a direct specialization of these classical ideas. It must not be claimed as a new minimax rate. See also Cai–Low (2004). This theorem gives the explicit interval-length specialization needed to identify the statistical limitation of the proposed coordinate method. It is a supporting characterization, not an additional independent novelty claim.

The empirical implication is a deterministic rate comparison, not a new stochastic coverage prediction. Add a diagonal-only lower curve to the existing analytic figure and check finite hypergeometric moments numerically. No new arbitrary simulation benchmark is required.
