# Counterexample appendix and boundary checks

These examples separate false proposed extensions from valid results under the stated model. C1 concerns a missing confidence-level domain in the input. C2 refutes an explicitly labeled conjecture, not a proved theorem. Finite computations are supplementary to the analytic arguments.

## C1. Theorem 5 needs its confidence-level restriction

Input Theorem 5, PDF page 7, does not state alpha<1/4, although its proof invokes lower bounds requiring that domain. Interpreted literally for all alpha in the model's (0,1), its affine conclusion is false.

Take any K>=3, rank cap one, equal diagonal loading, M=tau sqrt(p), and alpha=.9. The functional range is [-tau,tau]. The interval centered at .6<L,Z> with radius .1tau has worst-case coverage

$$\Phi(-1/2)-\Phi(-5/6)=0.1062091577>1-\alpha.$$

The minimum occurs at either endpoint of the functional range because normal interval probability decreases with absolute bias. Its radius .1tau is smaller than the claimed z_(.55)tau/(1+z_(.55))=0.1116333498tau. It is therefore an honest affine counterexample to the unqualified statement. The repair is to write 0<alpha<1/4 explicitly in Theorem 5. No counterexample is asserted in that intended range. This is a domain correction, not a failure of the main 95% inference argument.

## C2. The conjectured cubic full-data zero-point rate is false

Input Appendix B, PDF page 19, suggests order min(M,tau sqrt(log p))/sqrt(p) at zero for the full rank-one class. S8 constructs tensors
A_(u,v)=(tau/200)x_u tensor x_v tensor x_(uv), x_(u,i)=u_i i^(-1/3).
They have norm <=M=tau sqrt(p), a common harmonic diagonal and full-mixture chi-square <1/4. Hence
E0 length >=(3/4-2alpha)tau H_p/(200sqrt(p)).
At K=3 this contradicts the proposed order by a factor sqrt(log p). The complete uniform cubic-moment proof is in new_full_data_results.md. For K>=4, S7 and T6 instead prove that order. The dimensional distinction must replace the blanket conjecture.

## C3. Marginal finite variance does not justify the original Gaussian threshold

At A=0 let independent coordinate errors equal +/-sqrt(m/(2alpha)) with probability alpha/m each, and zero otherwise. Each has mean zero and variance one. Take tau=1, K=3, m=p=8192, M=sqrt(p), alpha=.05 and equal weights. The original selected interval is the nonlinear one, with radius approximately .481116. On exactly one nonzero error its center has absolute value
(sqrt(p/(2alpha))-sqrt(2log(2p/alpha)))/sqrt(p)>3,
so it misses zero. That event has probability
2alpha(1-2alpha/p)^(p-1)>0.09>alpha.
Thus finite variance alone does not validate the original calibration or raw-mean procedure. S4 changes the estimator and requires independent replicates.

## C4. Coordinate independence is unnecessary for thresholding but matters for the direct variance

If every diagonal error equals tau g for a single standard normal g, each marginal is Gaussian with the stated variance. The nonlinear union-bound proof still applies. The direct normalized diagonal has variance p tau^2, however. Using radius z tau gives coverage 2Phi(z/sqrt(p))-1, which tends to zero. With sufficiently large M the original radius selection chooses that incorrectly calibrated direct interval. Known-covariance recalibration fixes this example.

## C5. No orthogonality or frame bound destroys the stated diagonal budget

Set every v_(ki)=e_1 for i=1,...,m. For A=M e_1^(tensor K), the left side of T1 is m M^(2/K), while its rank-one right side is M^(2/K). The stated bound fails for m>1. A Bessel/frame factor repairs the contraction inequality; orthogonality is sufficient, not indispensable in itself. The loading normalization and direct variance must also be recalculated.

## C6. A false supplied norm or rank cap can give zero coverage

For p=1, K=3, assumed M=1 and tau=1, the selected structural interval is [-1,1]. If the true mean is 2, its coverage is zero. This shows failure of the procedure under an invalid norm certificate, not impossibility of all inference without a bound.

For p=2, K=3, M=tau=1 and supplied cap one, take true A=(E_1+E_2)/sqrt(2). Its norm is one but its mode/cut ranks are two. The selected structural interval has radius 1/sqrt(2), while its true normalized diagonal functional is one. Coverage is zero. Exact rank recovery is unnecessary, but the outer cap must be valid.

If the norm bound is removed entirely and only diagonal observations are used, the rank-one diagonal image becomes all of R^p. For mean vectors a=delta w, the target changes by delta and the Gaussian shift norm is delta. A small fixed delta/tau has bounded total variation, so the common-target lemma forces expected length at zero of order tau. This excludes a uniform diagonal-only o(tau) claim without a size constraint.

## C7. Data-selected loadings and intervals require new coverage arguments

Choose the loading after observing data to be E_j for j maximizing |Z_(j,...,j)|. At A=0 the target is still zero, but the direct nominal Gaussian interval has coverage (1-alpha)^p, tending to zero.

For interval selection alone, fix alpha<1/2 and epsilon=alpha/4. Put a=z_(1-alpha+epsilon), b=z_(1-epsilon). In the scalar N(theta,1) model both
C1=[Z-a,Z+b] and C2=[Z-b,Z+a]
have coverage 1-alpha for every theta. Select C1 for Z>=0 and C2 otherwise. At theta=0 the failure probability is 2(alpha-epsilon)=3alpha/2. Both intervals have the same finite deterministic length. Therefore marginal validity does not justify arbitrary data-dependent selection. The original selection is deterministic and is valid.

## C8. Lower covariance bounds are needed for positive Gaussian information lower bounds

Let the full Gaussian noise covariance be Sigma=tau^2(I-LL^T), where ||L||_F=1. Then <L,Z>=psi(A) exactly. A zero-length interval is honest for every mean. Upper marginal variance bounds alone therefore cannot preserve T3, T4 or T6's positive lower bounds. No lower covariance bound is needed for a separately calibrated upper-confidence procedure.

## C9. The nonlinear center has no uniform nondegenerate Gaussian limit

For m=1, A=0 and lambda=c tau, tau^(-1)soft_lambda(tau g)=soft_c(g). This distribution has an atom at zero of size 2Phi(c)-1, independent of n, and is not Gaussian. At a fixed positive signal with tau tending to zero, the scaled error instead tends to g-c, with nonzero bias. Thus the current threshold center is not uniformly efficient or centered asymptotically normal. The direct estimator already has an exact normal distribution in the original model.

## C10. Factor identifiability is not tensor-mean identifiability

For nonzero c, x tensor y tensor z=(cx) tensor (y/c) tensor z. TT cores similarly admit invertible bond transformations and their inverses. Factor coordinates are not identifiable. The Gaussian mean A is identifiable because equal probability laws have equal expectations; psi(A) is therefore identifiable. All losses and confidence statements concern A or psi, so the gauge ambiguities do not invalidate them.

## C11. Order and regime boundaries are substantive

At K=2 a Tucker/TT rank-one class is exactly a single matrix rank class. Original T4 therefore rules out the claimed polynomial joint-versus-single-unfolding advantage. K>=3 is needed for that separation. The new scan has a summability boundary at K=4, while S8 proves a distinct logarithmic obstruction at K=3.

The equality M=tau sqrt(p) is not needed for finite-sample coverage. Writing u=M/(tau sqrt(p)), the original separation holds whenever
D u^(2/K)(log p/p)^((K-2)/(2K))/min(u,1) tends to zero.
This follows by dividing its length upper bound by the affine/relaxed-class lower order tau min(u,1). No claim is made when this ratio fails to vanish.

## C12. The diagonal exponent and approximation constant cannot simply be improved

For rank one with uniform unit factors, a_i=M p^(-K/2). A dimension-free bound sum_i|a_i|^q<=M^q fails for q<2/K because its left side is M^q p^(1-Kq/2). Thus 2/K is the smallest such exponent in the rank-one geometry.

In the scalar deterministic envelope, take B=0, A=eta, noise zero and lambda>=eta. Soft thresholding gives center zero and error eta. The additive approximation constant one in S3 is attained; replacing it by a universal smaller constant is impossible for that pathwise statement.
