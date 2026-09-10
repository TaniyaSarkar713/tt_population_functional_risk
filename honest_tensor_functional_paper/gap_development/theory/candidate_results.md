# Initial candidate ledger (preserved research history)

Baseline is the separate theory-reviewed manuscript; it is preserved unchanged. These candidates were recorded before the derivations were completed. Current status: G1/G2 proved; computational progress and precise limits are in proved_results.md and the updated manuscript.

## G1. Sparse harmonic cubic lower bound

For m<=p, let x_S have nonzero values j^(-1/3), j=1,...,m, assigned in increasing coordinate order on a uniform size-m support S. Set A_S=b x_S^(tensor 3), where
b=min{M/sqrt(27m), tau/sqrt(27) sqrt(log(1+p/(4m^2)))}.
Then all targets equal b H_m/sqrt(p). For overlap h=|S cap T|, Cauchy–Schwarz and the decreasing profile give
<x_S,x_T><=sum_(j<=h)j^(-2/3)<=3h^(1/3).
Thus <A_S,A_T>/tau²<=27b²h/tau². Hypergeometric factorial moments bound the full likelihood second moment by e^(1/4). The interval lemma gives E0 length >=c_alpha,d b H_m/sqrt(p).
For M=tau sqrt(p), m=floor(p^(1/4)), this is order tau(log p)^(3/2)/sqrt(p), matching the prior upper bound.

## G2. Residual-scan projection and worst-case length

Let F(Z)={B in Theta(M,rbar): N_S(Z-B)<=lambda_s(alpha) for every nonempty S}.
The true A is feasible with probability >=1-alpha. Define C_F=[min_(B in F)psi(B),max_(B in F)psi(B)], using {0} for empty F.
For B,B' in F, Delta=B-B' has doubled rank caps; N_S(Delta)<=2lambda_s. The previous ordered-diagonal argument gives
|psi(Delta)|<=4J(2rbar)^(K/2)/sqrt(p) sum_s lambda_s s^(-K/2).
Therefore C_F is uniformly honest and has a deterministic full-data length bound of that order.
Together with G1 and T6:
L0 ~ Lmax ~ tau(log p)^(3/2)/sqrt(p), K=3;
L0 ~ Lmax ~ tau sqrt(log p/p), fixed K>=4.
Measurability, compactness and empty-feasible-set handling need to be made explicit in the complete proof.

## G3. Computation

The exact confidence-set projection is an existence theorem; do not label it efficient.
Investigate a truncated finite-net scan with explicit operation/error tradeoff, and a conditional interval-to-detection reduction.
A low-degree lower bound for symmetric sparse tensor PCA can be relevant for even order because the equal diagonal target is deterministic positive despite factor signs. A low-degree barrier is not a proof against all polynomial-time confidence intervals.
