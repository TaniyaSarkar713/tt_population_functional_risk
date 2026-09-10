# Reconstructed mathematical framework and identifiability

The input is the 22-page PDF preserved in input_snapshot. This reconstruction does not rely on its PROVED labels.

## Experiment

Let K>=2, p_k>=1 and D=product_k p_k. On the Borel sample space R^D, augmented by an independent uniform random seed when randomized intervals are allowed, observe
Z=A+tau G, vec(G)~N(0,I_D), tau>0.
The statistical parameter is a fixed real tensor A, not its factor coordinates. The equivalent replicate experiment has W_j=A+sigma G_j, j=1,...,n, with independent standard Gaussian arrays and tau=sigma/sqrt(n). With known sigma, the mean is sufficient: an orthogonal transformation in the replicate index separates it from independent parameter-free residuals. With unknown sigma, those residuals contain variance information and cannot be discarded in S5.

There are no random latent factors, missing entries, random design matrices, contamination, serial dependence or estimated loadings in the original experiment. M, tau, alpha, rank caps and loading vectors are supplied. Smoothness, eigengaps, incoherence and optimization initialization are absent.

## Parameter spaces and ordering

Theta_Tu consists of tensors with ||A||_F<=M and rank(A_(k))<=rbar_k for every mode. Theta_TT instead constrains rank(A_<k>)<=rbar_k for contiguous prefix/suffix cuts k=1,...,K-1, in the fixed given mode order. Caps are positive integers. Infeasible nominal rank combinations cause no inconsistency: the classes still contain zero and every rank-one tensor, and inequalities use valid upper caps. Caps can be truncated to corresponding unfolding dimensions if desired.

The classes are compact: each rank condition is the zero set of all minors of the next order, hence closed, and the norm ball is closed and bounded in finite dimension. Compactness is useful for attained ranges and approximation classes, but the original confidence proof does not require solving an optimization over the class.

## Loading, target and procedure

For 1<=m<=min_k p_k choose fixed orthonormal mode families v_(ki) and fixed weights with ||w||_2=1. Let V_i=product_k v_(ki), L=sum_i w_i V_i, and psi(A)=<L,A>. Then V_i are orthonormal, ||L||_F=1, and the contractions d_i=<Z,V_i>=a_i+tau g_i have independent normal errors.

Write q=2/K, J_Tu=min_k product_(l!=k)rbar_l and J_TT=product_(k<K)rbar_k. The original procedure thresholds d at lambda=tau sqrt(2log(2m/alpha)), uses center sum_i w_i soft_lambda(d_i), and bounds its error by h_NL=||w||_infinity J^(1-q/2)M^q(2lambda)^(1-q). Two alternatives are the exact Gaussian interval of radius z_(1-alpha/2)tau and the structural interval [-h0,h0], h0=M sqrt(sum_top_s w_i^2), s=min(m,smallest cap). The selected radius is the deterministic minimum. The strengthened procedures and information requirements are stated separately in S1–S8.

## Coverage and losses

An honest interval satisfies inf_(A in Theta) P_A{psi(A) in C}>=1-alpha at every finite dimension. This is the original primary guarantee. The loss is length |C|, and
L0=inf_honest_C E0|C|, Lmax=inf_honest_C sup_A E_A|C|.
The diagonal-restricted versions require C to be measurable in d and independent randomization. The full-data versions allow all of Z. These classes are not interchangeable. Intersections used in S7 are closed intervals, with an empty intersection replaced by {0}; this convention preserves the coverage proof and zero length in the empty case.

Squared Frobenius estimation risk for replicates is ||B-A||_F^2+D sigma^2. It is not the objective minimized by the functional interval and plays no role in the rate claims. No unproved consistency or optimization guarantee for a full-tensor estimator is needed.

## Identification

If P_A=P_B in the Gaussian location model, their finite expectations agree, so A=B and psi(A)=psi(B). The entire tensor mean and prescribed functional are identifiable. Factors and cores are not: scalar rescaling, signs and invertible TT bond gauges leave A unchanged. All statements are in ambient tensor coordinates or scalar functional loss, so no gauge-identification theorem is required. At zero, factor directions are unidentified and tangent spaces can change with rank; the interval arguments avoid those coordinates.

## Asymptotics

The principal sequence is fixed K>=3, equal mode dimension p, fixed positive caps, equal diagonal weights p^(-1/2), and M=tau sqrt(p). A concrete version has M=sigma=1, n=p and D=n^K. All coverage theorems are finite-sample. The asymptotic notation concerns deterministic interval bounds or explicitly bounded expectations, not an unjustified conversion from O_p to expectation.

The audit proves a sharper full-data result at zero for K>=4 and a stronger lower bound for K=3. It does not prove a sharp full-data worst-case expected length, a uniform Gaussian limit for the threshold center, actual-rank adaptation, or a polynomial-time optimal procedure.
