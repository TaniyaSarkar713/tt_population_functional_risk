# Statistical experiment and assumptions

All results concern real tensors. PROVED means a complete derivation is recorded and algebraically checked; it does not mean machine-verified mathematics or independent peer review.

**A1: Gaussian location experiment.** Observe Z=A+tau G in R^(p_1 x ... x p_K), K>=2, tau>0 known, and all entries of G independent N(0,1). Equivalently Z is the sample mean of n independent full tensors W_i=A+sigma G_i, tau=sigma/sqrt(n), with known sigma. No equivalence to random-design tensor regression is asserted. There is no additional latent random parameter: tensor cores are nonunique coordinates of A.

**A2: Known outer class.** ||A||_F<=M, M>0 known. Either every Tucker mode rank is at most its supplied positive cap, or every contiguous TT cut rank is at most its supplied positive cap. Actual ranks can be zero or smaller, and nonzero singular values can be arbitrarily small. Factors need not be incoherent. The norm cap is essential for the nonlinear radius; underestimating it invalidates the guarantee. Cap adaptation is not established.

**A3: Prescribed loading.** L=sum_(i=1)^m w_i v_(1i) tensor ... tensor v_(Ki), where each family (v_(ki))_(i<=m) is orthonormal and w is known with ||w||_2=1. Thus m<=min p_k. A coordinate diagonal is the special case v_(ki)=e_i. This is restrictive relative to arbitrary L, but can be dense after known orthogonal mode rotations. Loading selection from the same data is excluded.

**A4: Coverage.** Fix alpha in (0,1). An interval is honest if inf_(A in Theta) P_A{<L,A> in C(Z)}>=1-alpha at each finite dimension and noise level. Lower bounds use alpha<1/4 for transparent constants. The loss is interval length; compare sup_A E_A length under the same honesty constraint. Estimator squared-error risk is secondary, and empirical coverage is not a proof of honesty.

**A5: Separation regime.** For the principal comparison let p_1=...=p_K=m=p, equal w_i=1/sqrt(p), fixed K>=3, fixed rank caps, and M=tau sqrt(p). A conventional sequence is M=sigma=1, n=p, tau=p^(-1/2), ambient dimension D=p^K=n^K. Signal A may vary arbitrarily inside the class. A5 is needed only for the asymptotic separation, not coverage.

**Pilot/estimator.** No full-tensor pilot is needed. Form d_i=<Z,v_(1i) tensor ... tensor v_(Ki)> and soft threshold it; the final procedure chooses among three intervals using deterministic theoretical radii. In coordinate form this reads m observed entries and costs O(m). For rotated dense loadings the cost of obtaining those contractions is additional and can be large.

**Risk notation.** With observed replicates W_i, squared Frobenius loss has population risk R_A(B)=||B-A||_F^2+D sigma^2 and empirical risk R_n(B)=n^(-1)sum_i||W_i-B||_F^2. The present paper studies a scalar functional, not minimization of these risks.

**Exclusions.** No dependence beyond the tensor coordinates of the unknown mean, no contamination, no missing observations, no distribution shift, and no misspecification. The soft-threshold proof only needs a simultaneous coordinate noise envelope and thus has routine extensions with known tail bounds. Those extensions are not novelty claims. Unknown noise and random-design regression remain outside the proved statements.

**Which restrictions can be weakened?** Equal mode sizes and equal weights are used only for comparison lower bounds. Orthonormal loading factors can perhaps be replaced by frame bounds, but resulting noise dependence and constants must be proved. Fixed rank caps can grow if the displayed rank factor still permits separation. Replacing known M by a validated random upper bound requires a separate coverage argument; a plug-in norm estimate is insufficient.

**Information restriction for D1 only.** Its lower bound allows intervals measurable in d and an independent seed. T3, T4 and T6 allow the full observed tensor. These procedure classes differ even though their honesty classes can be identical. The exact rank-one diagonal image therefore establishes diagonal-information optimality only.
