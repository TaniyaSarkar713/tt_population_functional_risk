# Closing the statistical gaps and delimiting computation

Status: **PROVED** for G1, G2, G2b, G3 and G4; G5 is a proved conditional implication. Complete derivations have passed the saved finite checks. No polynomial-time optimal confidence interval or unconditional algorithmic-hardness result is claimed.

## G1. Sparse harmonic mixture, cubic lower bound

Fix p>=1, 1<=m<=p, K=3 and the original full Gaussian experiment and equal diagonal target. Put
\[
 b_m=\min\left\{\frac M{\sqrt{27m}},
 \frac{\tau}{\sqrt{27}}\sqrt{\log(1+p/(4m^2))}\right\},\quad
 c_{\alpha,d}=1-2\alpha-\tfrac12\sqrt{e^{1/4}-1}>0
\]
for 0<alpha<1/4.
For every honest interval over a class containing the rank-one Frobenius ball,
\[
 E_0|C|\ge c_{\alpha,d}b_mH_m/\sqrt p.
\]

Proof. On each size-m support S, assign the values j^(-1/3), j=1,...,m, in increasing coordinate order; write the vector as x_S and set A_S=b_m x_S^(tensor 3). Norm <=b_m(3m^(1/3))^(3/2)<=M. Target is b_m H_m/sqrt p for every S. For H=|S cap T|, Cauchy–Schwarz gives
\[
 \langle x_S,x_T\rangle
 \le\{\sum_{i\in S\cap T}x_{S,i}^2\}^{1/2}
       \{\sum_{i\in S\cap T}x_{T,i}^2\}^{1/2}
 \le\sum_{j=1}^Hj^{-2/3}\le3H^{1/3}.
\]
For H=0 both sides are zero. Thus the FULL tensor inner product is at most 27b_m²H. With S,T independent uniform supports, Gaussian likelihood integration and hypergeometric factorial moments give
\[
 1+\chi^2(Q,P_0)
 \le E\exp(27b_m^2H/\tau^2)
 \le\exp\{m^2p^{-1}(e^{27b_m^2/\tau^2}-1)\}
 \le e^{1/4}.
\]
The common-target interval lemma proves the bound. No factor signs, random profile permutation or diagonal-marginal likelihood are needed.

Under M=tau sqrt p take m=floor(p^(1/4)). For p>=256,
m>=p^(1/4)/2, H_m>=log(m)>=log(p)/8 and
log(1+p/(4m²))>=log(p)/4.
The noise term is the minimum, since log(1+p/(4m²))<=log p<=sqrt p<=p/m.
Consequently b_mH_m/sqrt p >=tau(log p)^(3/2)/(16sqrt(27p)).
This matches the cubic full-data upper rate. The older harmonic sign-mixture lower bound remains correct but is not sharp.

## G2. Residual-scan confidence set, uniform diameter

Use the original product nets and thresholds lambda_s(alpha), with the fixed error budget alpha, not alpha/p. Let
\[
 {\cal F}(Z)=\{B\in\Theta(M,\bar r):
             N_S(Z-B)\le\lambda_{|S|}(\alpha)\quad\forall S\ne\varnothing\}.
\]
If nonempty, define C_F as the interval between the minimum and maximum of psi on F. Otherwise define C_F={0}. Put J_2=J(2rbar), the expansion constant for doubled caps, and
\[
 W_\alpha=\frac{4J_2^{K/2}}{\sqrt p}
                   \sum_{s=1}^p\lambda_s(\alpha)s^{-K/2}.
\]
Then C_F is honest at level 1-alpha and |C_F|<=min(2h0,W_alpha) for every data value.

Proof. The noise event in the original scan proof ensures A in F, uniformly with probability >=1-alpha. The class is compact, each finite-net constraint is continuous, and psi is continuous, so nonempty sections are compact and extrema are attained. The feasible-data set is closed: if Z_j converges and B_j are feasible, extract a convergent subsequence from the compact parameter class. Similarly {Z: F(Z) has a B with psi(B)>=t} is closed for every t. Thus the endpoint functions on nonempty sections, extended by zero otherwise, are Borel measurable.

For B,B' in F, Delta=B-B' has each constrained rank <=2rbar by matrix-rank subadditivity. Coordinate restrictions preserve this bound. The finite-net seminorm obeys N_S(Delta)<=2lambda_s, hence rho(Delta_S)<=4lambda_s. The canonical expansion and original diagonal inequality imply
\[
 \sum_{i\in S}|\Delta_{i,\ldots,i}|^{2/K}
 \le J_2\,\rho(\Delta_S)^{2/K}.
\]
Taking S as the s largest absolute diagonal entries gives
\[
 |\Delta|_{(s)}\le4J_2^{K/2}\lambda_s s^{-K/2}.
\]
Summation gives |psi(B)-psi(B')|<=W_alpha. The structural range gives the other diameter bound. Apply this to the attained extrema. Empty sections have length zero and do not occur on the coverage event.

For fixed K/caps/alpha and M=tau sqrt p, the old logarithm calculation with fixed alpha still gives lambda_s<=C tau sqrt(s log p). Combine G1, the old coordinate-mixture lower bound and the diameter upper:
\[
 {\cal L}_0(\Theta)\asymp{\cal L}_{\max}(\Theta)
 \asymp \begin{cases}
 \tau(\log p)^{3/2}/\sqrt p,&K=3,\\
 \tau\sqrt{\log p/p},&K\ge4.
 \end{cases}
\]
All comparisons use the same full-data experiment and same outer honesty class. This is a new use of a standard confidence-set projection argument, not a novel generic projection principle.

## G2b. Squared-error minimax consequence

Let r_K(p) denote the preceding length rate. The midpoint of C_F with calibration alpha_p=p^(-2) stays in [-h0,h0], including empty sections. Its MSE is at most
W_(alpha_p)^2/4+4h0²alpha_p=O(r_K(p)^2).
The lower mixtures have common target delta of order r_K(p) and TV<=constant<1.
For any estimator T, test T>=delta/2. Markov bounds the sum of null error and mixture error by 8 sup_A E_A(T-psi(A))²/delta²; testing risk is at least 1-TV. Hence the minimax squared error is of order r_K(p)^2.

## G3. Truncated finite scans: certified computation tradeoff

Fix t<=p and use only supports of sizes <=t in the zero test, with thresholds still calibrated simultaneously over all sizes up to p. Let B_q=J^(1-1/K)M^(2/K), q=2/K, a_t=4J^(K/2)lambda_t t^(-K/2). Define
\[
 R_t=\frac{4J^{K/2}}{\sqrt p}\sum_{s=1}^t\lambda_s s^{-K/2}
       +\mathbf1_{\{t<p\}}\frac{B_q}{\sqrt p}a_t^{1-q}.
\]
On test acceptance and the simultaneous noise event, all top-t diagonal bounds hold. Every remaining coordinate has magnitude <=a_t, so
sum_(s>t)|a|_(s)<=a_t^(1-q)sum_(s>t)|a|_(s)^q<=a_t^(1-q)B_q.
This proves |psi|<=R_t. Use the interval [-min(h0,R_t),min(h0,R_t)] on acceptance and [-h0,h0] on rejection. Intersect with C_*(alpha0), with alpha0+gamma<=alpha and singleton convention. Then
E0 length<=min(ell_*,2R_t+ell_*gamma), sup_A length<=ell_*.

For gamma=alpha/(2p), fixed K/caps and M=tau sqrt p,
\[
 R_t\lesssim \frac{\tau\sqrt{\log p}}{\sqrt p}
                   \sum_{s=1}^t s^{-(K-1)/2}
 +\mathbf1_{\{t<p\}}\tau(\log p/p)^\beta t^{-(K-1)\beta},
 \quad\beta=(K-2)/(2K).
\]
The factor t trades additional search for a smaller certified tail contribution. Fixed t gives polynomial computation but does not remove the original power gap.

For explicit computable nets, use grid step h=1/(2K sqrt s) in [-1,1]^s, round a unit vector coordinatewise, and normalize each nonzero grid vector. Rounding error <=1/(4K), and normalization adds at most that error, giving a 1/(2K)-net. Its size is <=(1+4K sqrt s)^s after choosing an endpoint-covering grid with at most 1+4K sqrt s points per coordinate (precise integer rounding is recorded in the implementation). Using the slightly looser integer bound (3+4K sqrt s)^s avoids endpoint ambiguities. Replace net log cardinality in lambda_s by Ks log(3+4K sqrt s). The asymptotic order remains unchanged for s<=p.
Cost <=sum_(s<=t) binom(p,s)(3+4K sqrt s)^(Ks) O(s^K), plus reading needed entries. This is polynomial in p for fixed t and K. The projected confidence set in G2 is not made efficient by this truncated test.

All completed scan levels can share one simultaneous event. Thus intersecting the intervals for adaptively chosen completed levels with one fixed-calibrated C_* remains honest. No error budget is spent per computational update.

## G4. A self-contained low-degree estimation obstruction

Let p be mode dimension, K>=3 fixed, 1<=s<=sqrt p. Draw S uniformly among size-s supports and put
x_S=s^(-1/2)1_S, A_S=tau lambda x_S^(tensor K).
The Frobenius norm is tau lambda, the common target is
delta=tau lambda s^(1-K/2)/sqrt p.
Write mu=s²/p and B_D=(lambda²/s^K)(KD)^K.
For B_D<1 and polynomial degree D>=1, the centered low-degree likelihood norm satisfies
\[
 \chi^2_{\le D}\le\mu e^\mu\,B_D/(1-B_D).
\]

Proof. Normalized multivariate Hermite polynomials are orthonormal under the null; their shift expectations follow by expanding E exp(tY-t²/2)=exp(tA/tau). The degree-d squared coefficient sum is E(<A,A'>/tau²)^d/d! by the multinomial theorem. Here <A_S,A_T>/tau²=lambda²(H/s)^K for H=|S cap T|.
For integer m>=1, factorial moments give
E(H)_j=(s)_j²/(p)_j<=mu^j.
The expansion H^m=sum_j {m brace j}(H)_j and the bound {m brace j}<=j^m/j! yield
\[
 EH^m\le\sum_{j=1}^m j^m\mu^j/j!\le\mu e^\mu m^m.
\]
Thus
\[
 \chi^2_{\le D}=\sum_{d=1}^D\frac{\lambda^{2d}}{d!s^{Kd}}EH^{Kd}
 \le\mu e^\mu\sum_{d=1}^D B_D^d
 \le\mu e^\mu B_D/(1-B_D).
\]
For any degree-D estimator T with worst-case MSE R on {0} union {A_S}, Cauchy–Schwarz in the null Hermite basis gives
|E_QT-E_0T|<=sqrt(Var_0 T)sqrt(chi²_<=D)<=sqrt(R)sqrt(chi²_<=D).
The two bias errors are <=sqrt(R), so
R>=delta²/(2+sqrt(chi²_<=D))².

Take lambda=sqrt p, s=floor(p^a) with
1/K<a<min(1/2,1/(K-2)), and D=floor(p^b), 0<b<a-1/K.
Then mu->0, B_D->0 and R>=(1-o(1))delta²/4.
But delta=tau s^(1-K/2) is polynomially larger than r_K(p).
This proves a statistical-versus-low-degree-MSE separation.
It is NOT an unconditional lower bound for all polynomial-time algorithms or all honest intervals. The low-degree method is classical; the displayed coarse moment proof is supplied independently.

## G5. Interval-to-detection reduction and its limits

Suppose a prior Q is supported on parameters with common target delta>0 and the null has target zero. For any honest interval C, define the test phi=1{delta in C}. Then
Q(phi=0)<=alpha and
P0(phi=1)<=alpha+E0|C|/delta.
Indeed, if 0 in C and |C|<delta, it cannot contain delta; Markov bounds the remaining event. Total testing error <=2alpha+E0|C|/delta.
Consequently a computational hypothesis ruling out polynomial-time tests with total error <=c, for c>2alpha, implies that polynomial-time honest intervals cannot have E0 length <(c-2alpha)delta along that prior.
G4 alone does not imply that computational hypothesis. Low-degree mean separation does not automatically bound arbitrary thresholded or interval-valued algorithms.
