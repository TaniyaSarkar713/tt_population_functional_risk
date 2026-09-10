# Result ledger

Use q=2/K and J_Tu=min_k product_(l!=k) rbar_l or J_TT=product_(k=1)^(K-1) rbar_k. All caps are positive integers. Put B=J^(1-q/2) M^q, lambda=tau sqrt(2 log(2m/alpha)), b_NL=||w||_infinity B (2lambda)^(1-q), b_G=z_(1-alpha/2) tau, and b_0=M sqrt(sum_(i=1)^s w_(i)^2), where |w_(i)| are sorted and s=min(m, smallest rank cap). The b_0 formula follows from any one constrained unfolding.

## T1 — Orthogonal diagonal compressibility — PROVED

Under A2–A3,

$$\sum_{i=1}^m |\langle A,v_{1i}\otimes\cdots\otimes v_{Ki}\rangle|^{2/K}
\le J^{1-1/K}M^{2/K}.$$

No minimum signal or identifiable factor-coordinate assumption is used. J is an explicit sufficient factor, not a claimed optimal dependence on ranks.

## T2 — Finite-sample honest interval — PROVED

Let soft_lambda(x)=sign(x)(|x|-lambda)_+ and psi_hat_NL=sum_i w_i soft_lambda(d_i). Then [psi_hat_NL +/- b_NL] has coverage at least 1-alpha uniformly on either rank-cap class. Choose the smallest-radius interval among it, [<L,Z> +/- b_G], and [-b_0,b_0], breaking ties deterministically. This choice is deterministic in (M,tau,rank caps,L,alpha), so there is no selection coverage penalty. Its length is exactly 2 min(b_NL,b_G,b_0).

This is adaptation to known experimental quantities, not adaptation to the unknown actual rank or spectrum. A data-dependent choice using observed centers would need its own proof.

## T3 — Necessary radius for fixed-radius affine intervals — PROVED

Let p_k=p, L=p^(-1/2)sum_i e_i^(tensor K), and suppose the honesty class contains all tensors +/-M e_i^(tensor K) and zero. If C(Z)=[<W,Z>+b +/- h], with deterministic W,b,h, is honest at level 1-alpha, alpha<1/2, then, writing z=z_(1-alpha/2),

$$h\ge \frac{(M/\sqrt p)z\tau}{M/\sqrt p+z\tau}.$$

For the rank-one tensor norm ball, the best fixed-radius affine interval therefore has radius of order min(M/sqrt(p),tau), since the direct interval and the zero-centered structural interval give a matching upper bound up to alpha-dependent constants. This does not cover data-dependent widths with affine centers.

## T4 — Cost of retaining only one unfolding constraint — PROVED

For any nontrivial bipartition S of the K modes, let Theta_S={A: rank(A_[S])<=1, ||A||_F<=M}. Let L be the equal diagonal loading. For alpha<1/4, every interval honest on Theta_S satisfies

$$E_0|C|\ge c_\alpha\min\{M/\sqrt p,\tau/4\},\quad
c_\alpha=1-2\alpha-\tfrac12\sqrt{\sqrt{8/7}-1}>0.$$

The pointwise-at-zero lower rate min(M/sqrt(p),tau) is attained up to constants by a deterministic choice between direct and zero-centered intervals on Theta_S. The same lower bound applies to a larger unfolding-rank cap. Matricization is a bijection and does not lose information; relaxing the parameter class loses the joint restriction.

## T5 — Strict nonlinear and joint-constraint separation — PROVED

Under A5, the interval in T2 obeys

$$|C|\le2\tau J^{1-1/K}\left\{\frac{8\log(2p/\alpha)}p\right\}^{(K-2)/(2K)}=o(\tau)$$

for fixed K>=3 and J. In contrast, T3 forces every honest fixed-radius affine interval on the same tensor class to have length at least 2z tau/(1+z), and T4 forces every interval honest on a single-unfolding relaxation to have E_0 length at least c_alpha tau/4. Hence two specific comparisons improve by a polynomial dimension factor, up to logs. This is not unrestricted minimax optimality, and does not dominate strong-signal oracle projection intervals pointwise.

For growing rank caps, the same separation follows if J^(1-1/K){log(p)/p}^((K-2)/(2K))->0. This condition may be restrictive because J is not sharp.

## T6 — Lower bound inside the joint tensor class — PROVED

For alpha<1/4, any interval honest on a class containing all rank-one tensors of norm <=M satisfies

$$E_0|C|\ge(3/4-2\alpha)\frac{\min\{M,\tau\sqrt{\log(1+p/4)}\}}{\sqrt p}.$$

At M=tau sqrt(p), the lower scale is tau sqrt(log(p)/p), whereas T2 has the larger scale tau{log(p)/p}^((K-2)/(2K)) for fixed ranks. This polynomial gap is unresolved.

## D1 — Classical diagonal-information benchmark — PROVED

Manuscript Proposition 1; complete derivation in [diagonal_minimax.md](diagonal_minimax.md). Restrict C to d and independent randomization, with honesty on the full rank-at-most-one tensor Frobenius ball. For 1<=s<=p,

$$b_s=\min\{M s^{-K/2},\tau\sqrt{\log(1+p/(4s^2))}\},\quad
E_0|C(d)|\ge\left(1-2\alpha-\tfrac12\sqrt{e^{1/4}-1}\right)\frac{s b_s}{\sqrt p}.$$

At fixed K>=3 and M=tau sqrt(p), this and T2 match:

$$\mathcal L_{0,d}\asymp\mathcal L_{\max,d}\asymp
\tau(\log p/p)^{(K-2)/(2K)}.$$

The same order holds for fixed positive Tucker/TT caps. This is a confidence-interval specialization of classical Gaussian sparse-sequence theory, not a new minimax rate. It does not apply to procedures using the full tensor; their likelihood second moment involves overlap raised to K instead of overlap.

## Q1 — Sharp full-data minimax expected length — PARTIAL

T2 and T6 give a bracket, not a matching rate. No theorem asserts that thresholding is minimax among full-data procedures, that the two-point modulus is sufficient, or that the coordinate mixture is the hardest alternative.

## Q2 — Possible zero-point rate — CONJECTURED

For the rank-one class, it is plausible that a procedure using off-diagonal information attains E_0 length of order min(M,tau sqrt(log p))/sqrt(p), under honesty on the whole class. This is a conjecture about expected length at zero, not a uniform fixed-radius claim. It may be false; more complicated mixtures may increase the lower bound. No manuscript theorem relies on it.

## Q3 — Unknown actual rank/spectrum adaptation and general L — PARTIAL

The previous broad target survives as an open program. T2 uses supplied rank caps and M, and exploits a prescribed orthogonal loading. It does not estimate or adapt the radius to the actual rank, singular values, or arbitrary loading geometry.
