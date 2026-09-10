# Complete derivations for T1–T6

These proofs use only finite-dimensional inequalities and exact Gaussian calculations. Complete here means every nontrivial step is given. Numerical checks in `simulations/code/check_theory.py` are supplementary sanity checks, not substitutes for these arguments or independent mathematical review.

## P1. CP expansions with controlled squared weights

Write A=sum_(j<=J_A) x_(1j) tensor ... tensor x_(Kj) and a_j=product_k ||x_(kj)||_2. We will construct an expansion with J_A<=J and sum_j a_j^2=||A||_F^2. Terms with a zero vector may be kept with a_j=0.

**Tucker case.** Use an exact orthonormal Tucker representation A=G times_1 U_1 ... times_K U_K, with actual nonzero ranks r_k<=rbar_k. Choose an omitted mode k. Expand the core along every other core index. For each tuple j_-k, take factor U_l[:,j_l] for l!=k and vector U_k G[:,j_-k] in mode k. The other factors have norm one, so a_(j_-k)^2=||G[:,j_-k]||_2^2. Summing gives ||G||_F^2=||A||_F^2. There are product_(l!=k)r_l terms, at most the corresponding cap product. Choose the omitted mode minimizing the cap product. A=0 is handled by the empty or zero expansion.

**TT case.** Use exact left-canonical TT cores G_k of size r_(k-1) x p_k x r_k, with r_0=r_K=1. The unfolding of G_k into (r_(k-1)p_k) x r_k has orthonormal columns for k<K, and ||G_K||_F=||A||_F. These properties follow by sequential QR factorizations: absorb each triangular factor into the next core; contractions by the resulting isometries preserve the Frobenius norm. No inverse of a small singular value is needed.

Expand the TT contraction over paths (a_1,...,a_(K-1)). Each path is one CP term consisting of the physical-index vectors G_k[a_(k-1),:,a_k]. Its squared weight is the product of their squared norms. Define the total prefix weight ending at a_k=b by

$$t_k(b)=\sum_{a_1,\ldots,a_{k-1}}\prod_{l=1}^k\|G_l[a_{l-1},:,a_l]\|_2^2.$$

For k=1, t_1(b)=1 by column normalization. If t_(k-1)(a)=1 for every a, then

$$t_k(b)=\sum_a t_{k-1}(a)\|G_k[a,:,b]\|_2^2=1,$$

again by column normalization. Therefore the total squared path weights equal sum_a t_(K-1)(a)||G_K[a,:,1]||_2^2=||G_K||_F^2=||A||_F^2. The path count is product_(k<K)r_k<=J_TT. Individual path terms need not be mutually orthogonal; the displayed induction is the necessary argument.

## P2. Proof of T1

Let a_i=<A,v_(1i) tensor ... tensor v_(Ki)> and q=2/K<=1. Subadditivity |sum_j t_j|^q<=sum_j|t_j|^q gives

$$\sum_i|a_i|^q\le\sum_j\sum_i\prod_{k=1}^K|\langle x_{kj},v_{ki}\rangle|^{2/K}.$$

Holder's inequality with K equal exponents yields

$$\sum_i\prod_k|\langle x_{kj},v_{ki}\rangle|^{2/K}
\le\prod_k\left\{\sum_i|\langle x_{kj},v_{ki}\rangle|^2\right\}^{1/K}
\le\prod_k\|x_{kj}\|_2^{2/K}=a_j^q.$$

The second inequality is Bessel's inequality for each orthonormal loading family. Finally, Holder for the finite sequence a_j gives

$$\sum_{j=1}^{J_A}a_j^q\le J_A^{1-q/2}\left(\sum_j a_j^2\right)^{q/2}
\le J^{1-q/2}M^q.$$

This proves T1. The exponent 2/K arises from K products and Euclidean factor normalization; tensor Schatten quasi-norms with this exponent already occur in the literature. We do not claim to introduce that exponent.

## P3. Scalar soft-threshold lemma

If |e|<=lambda and s=soft_lambda(x+e), then s lies between 0 and x (with the order reversed if x<0) and

$$|s-x|\le\min\{|x|,2\lambda\}.$$

For x>=0, x+e>=-lambda, so s>=0. Also x+e-lambda<=x, so s<=x. If x>2lambda, then x+e>lambda and x-s=lambda-e<=2lambda; if x<=2lambda use x-s<=x. Negative x follows by oddness. For q in (0,1], min(t,u)<=t^q u^(1-q): when t<=u divide by t to obtain (t/u)^(1-q)<=1, and when t>=u divide by u to obtain (u/t)^q<=1.

## P4. Proof of T2

The product loading atoms V_i=v_(1i) tensor ... tensor v_(Ki) are orthonormal because <V_i,V_j>=product_k<v_(ki),v_(kj)>=1{i=j}. Gaussian isotropy gives d_i=a_i+tau g_i with independent standard normal g_i. The elementary Chernoff bound P(|g|>t)<=2 exp(-t^2/2), followed by a union bound, gives

$$P\{\max_i|\tau g_i|>\lambda\}\le2m\exp[-\lambda^2/(2\tau^2)]=\alpha.$$

On the complementary event, P3 and T1 give

$$|\widehat\psi_{NL}-\psi|\le\|w\|_\infty\sum_i\min(|a_i|,2\lambda)
\le\|w\|_\infty(2\lambda)^{1-q}\sum_i|a_i|^q\le b_{NL}.$$

The direct interval is exact since <L,Z>-<L,A> is N(0,tau^2||L||_F^2)=N(0,tau^2). For the zero-centered interval, select any constrained unfolding. Its loading matrix has singular values |w_i|: both sides of each product atom are orthonormal. For a rank<=r matrix B and loading H, the singular-value trace inequality and Cauchy–Schwarz give |<H,B>|<=||B||_F(sum_(i<=r)s_i(H)^2)^(1/2). This inequality also follows by projecting H onto the row/column singular subspaces of B and maximizing its rank-r Frobenius approximation. Taking the smallest cap gives |psi|<=b_0.

The chosen index minimizing the three radii does not depend on Z. Its individual coverage guarantee therefore remains valid without a union bound across procedures. Its interval length is exactly twice the chosen radius. This completes the finite-sample uniform proof, including all lower-rank strata.

## P5. Proof of T3

Put t=<W,L> and z=z_(1-alpha/2). A normal distribution shifted away from zero has at most the centered probability of falling in [-h,h], so honesty at A=0 implies h>=z tau||W||_F>=z tau|t|. This remains valid if W=0.

At +/-M E_i, E_i=e_i^(tensor K), the center's error mean is b+/-M(<W,E_i>-1/sqrt(p)). At least one sign has absolute mean at least M|<W,E_i>-1/sqrt(p)|. A symmetric interval of radius h strictly less than that absolute mean has coverage less than 1/2 for a nondegenerate normal variable (and zero in the deterministic case). Thus honesty for alpha<1/2 forces

$$h\ge M\max_i|\langle W,E_i\rangle-1/\sqrt p|
\ge\frac M{\sqrt p}|t-1|.$$

The second inequality follows by averaging the p discrepancies: t-1=p^(-1/2)sum_i(<W,E_i>-1/sqrt(p)). Let a=M/sqrt(p), b'=z tau. From h>=a|1-t| and h>=b'|t|, the triangle inequality gives 1<=|1-t|+|t|<=h/a+h/b'. Hence h>=ab'/(a+b'). The rank-one class has b_0=M/sqrt(p), so the matching upper order follows from T2's direct/zero alternatives. No symmetry averaging or unproved affine optimality theorem is needed.

## P6. A confidence-interval mixture inequality

Let P_0 be a reference law with target zero and Q a mixture of alternatives all having the same target delta>0. If C has coverage >=1-alpha at zero and each alternative, then Q(delta in C)>=1-alpha, whence P_0(delta in C)>=1-alpha-TV(P_0,Q). Intersecting with {0 in C} gives probability >=1-2alpha-TV that C contains both numbers. Because C is an interval, its length on that event is at least delta. Thus

$$E_0|C|\ge\delta\{1-2\alpha-\mathrm{TV}(P_0,Q)\}.$$

Also TV(P_0,Q)<=0.5 sqrt(chi^2(Q,P_0)) by Cauchy–Schwarz applied to the likelihood ratio minus one. This step works for intervals depending on the entire observed tensor and for additional independent randomization.

## P7. Proof of T4

For any nontrivial mode bipartition S, set f_i=tensor_(k in S)e_i and g_i=tensor_(k notin S)e_i. Both are orthonormal families. For independent signs s_i in {-1,1}, u=s/sqrt(p), define

$$A_u=\theta\left(\sum_i u_i f_i\right)\otimes\left(\sum_j u_j g_j\right),
\qquad \theta=\min(M,\tau\sqrt p/4).$$

This has rank one in the chosen unfolding, Frobenius norm theta, and diagonal functional psi(A_u)=theta sum_i u_i^2/sqrt(p)=theta/sqrt(p). Let Q average its Gaussian laws. The Gaussian shift likelihood identity is

$$1+\chi^2(Q,P_0)=E_{u,v}\exp\{\langle A_u,A_v\rangle/\tau^2\}
=E\exp\{\theta^2(\sum_i s_i t_i)^2/(\tau^2p^2)\}.$$

To check the identity, the likelihood ratio at mean B is exp(<Z,B>/tau^2-||B||_F^2/(2tau^2)); multiplying two such ratios and integrating the centered Gaussian gives exp(<B,C>/tau^2). The two orthogonal block factors give <A_u,A_v>=theta^2(u^T v)^2.

Write S_p=sum_i s_i t_i and a=theta^2/(tau^2 p)<=1/16. With an independent standard normal H, its moment-generating formula gives exp(a S_p^2/p)=E_H exp(sqrt(2a/p)H S_p). Therefore

$$E\exp(aS_p^2/p)=E_H\cosh(\sqrt{2a/p}H)^p
\le E_H\exp(aH^2)=(1-2a)^{-1/2}\le\sqrt{8/7}.$$

The cosh inequality follows from log cosh(x)<=x^2/2: its derivative tanh(x) is at most x for x>=0, and both functions are even. The Gaussian square moment is obtained by integrating exp[-(1-2a)h^2/2]/sqrt(2pi), valid because a<1/2. All expectations are nonnegative, justifying exchange of integrals.

Apply P6 with delta=theta/sqrt(p) and TV<=0.5 sqrt(sqrt(8/7)-1). This proves the stated lower bound and positivity for alpha<1/4. On the relaxation, |psi(A)|<=M/sqrt(p) follows from its rank-one matrix structure and the loading matrix singular values 1/sqrt(p), giving the matching direct/zero upper order. These alternatives need not satisfy the other tensor rank constraints. That is the point of the comparison, not an embedding into the original joint class.

## P8. Proof of T5

Substitute M=tau sqrt(p), ||w||_infinity=p^(-1/2), q=2/K into b_NL:

$$b_{NL}=\tau J^{1-1/K}p^{1/K-1/2}\{8\log(2p/\alpha)\}^{(K-2)/(2K)}.$$

For fixed K>=3 and J, beta=(K-2)/(2K)>0, so (log(p)/p)^beta tends to zero. T3 with M/sqrt(p)=tau gives h>=z tau/(1+z). T4 with theta=tau sqrt(p)/4 gives E_0 length>=c_alpha tau/4. Dividing the upper bound by either lower bound proves the separation. At K=2, beta=0 and this argument gives no separation. No statistical/computational transition exponent has been borrowed from tensor PCA.

## P9. Proof of T6

Let E_j=e_j^(tensor K), take a=min(M,tau sqrt(log(1+p/4))), and mix uniformly over A_j=aE_j. All are in the rank-one class and have target delta=a/sqrt(p). They are pairwise orthogonal in Frobenius inner product. The same Gaussian likelihood identity gives

$$1+\chi^2(Q,P_0)=p^{-2}\{p\exp(a^2/\tau^2)+p(p-1)\},$$

so chi^2=(exp(a^2/tau^2)-1)/p<=1/4 and TV<=1/4. P6 gives E_0 length>=(3/4-2alpha)a/sqrt(p). The strict positivity is clear for alpha<1/4. This is a standard sparse-mixture lower-bound mechanism, included to expose the remaining gap, not claimed as a new testing technique.

## Proof audit and failure points

- TT path terms are not assumed orthogonal. Prefix squared-weight induction replaces that false shortcut.
- CP rank by itself with a Frobenius bound does not automatically supply a bounded sum of component weights, because cancellation/degeneracy can occur. T1 uses Tucker or TT canonical expansions; an unrestricted CP-rank extension is not asserted.
- The soft threshold is lambda, not 2lambda; its deterministic error envelope is min(|x|,2lambda). Changing either requires recomputing the radius.
- Comparing affine fixed-radius intervals does not prove dominance over all adaptive intervals.
- Unfolding preserves observed information. The T4 lower bound applies to an enlarged honesty class, not to every algorithm that stores a matricized tensor.
- The coordinate-mixture lower bound and nonlinear upper bound do not match. Claiming minimax optimality would be false on the evidence available.
- The Frobenius bound M is supplied, not estimated from the same data. Misspecifying it or the rank cap removes the stated honesty guarantee.

## P2b. Exact rank-one diagonal image — PROVED

The diagonal image of the rank-one Frobenius ball is exactly {a: sum_i |a_i|^(2/K) <= M^(2/K)}. Inclusion follows from T1 with J=1. For the reverse inclusion, set x_1=sum_i sign(a_i)|a_i|^(1/K)v_(1i) and x_k=sum_i |a_i|^(1/K)v_(ki) for k>=2. The product tensor A=x_1 tensor ... tensor x_K has the required diagonal. Each factor has squared norm S=sum_i|a_i|^(2/K), so ||A||_F=S^(K/2)<=M. All ranks are at most one; zero is immediate.

Consequently, inference using only the diagonal is exactly a classical Gaussian sequence problem on an ell_(2/K) ball. This further limits the method's originality. The full tensor contains off-diagonal information, so the experiments are not equivalent when all observations are retained.
