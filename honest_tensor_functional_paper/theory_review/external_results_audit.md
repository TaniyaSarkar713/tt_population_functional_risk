# External results and theoretical comparison

The mathematical proofs in the reviewed manuscript are self-contained apart from elementary finite-dimensional linear algebra and probability identities, whose applications are recorded below. Contextual citations are not silently imported as theorems. The original project's 20-paper matrix remains available at ../literature/novelty_matrix.md.

## Load-bearing identities

| Result used | Conditions here | Verification |
|---|---|---|
| Orthonormal Tucker/TT representation | Finite real tensor; actual unfolding ranks below supplied caps | Tucker mode bases preserve norm; sequential orthogonal TT factors preserve final-core norm. Exact existence matches Oseledets Theorem 2.1. L1 supplies the needed squared-path identity. |
| Holder and Bessel | Positive exponents K; orthonormal mode families; finite sums | Applied to absolute contractions with powers 2/K; finite sums remove integrability concerns. |
| Cauchy–Schwarz and projection trace | Matching Euclidean spaces; orthogonal projection | Used for scalar target, rank-r matrix bound and component weights; no stochastic dependence condition. |
| Gaussian mgf and Chernoff | Centered N(0,tau²), tau>0 | MGF exp(t²tau²/2); exponential optimization is explicit. |
| Gaussian likelihood second moment | Entire mean experiment with covariance tau²I | Completing the Gaussian exponential gives exp(<B,C>/tau²); applied to full arrays except explicitly diagonal D1. |
| Total variation / chi-square | Q absolutely continuous w.r.t. P0 | TV=E0\|LR-1\|/2 <=sqrt(chi-square)/2; proof included. |
| Tonelli | Nonnegative integrands | Auxiliary Gaussian calculation and cubic exponential moment integration; no unjustified signed exchange. |
| Hypergeometric moments | Independent uniform size-s supports, 1<=s<=p | Count j-subsets: E binom(H,j)=binom(s,j)(s)_j/(p)_j; checked factor by factor, including j=0. |
| Sphere net volume | Finite Euclidean unit sphere | Disjoint epsilon/2 balls inside radius 1+epsilon/2 give (1+2/epsilon)^s; net telescoping costs K epsilon. |
| Chebyshev and Bernoulli concentration | Finite marginal variances; independent clean blocks | Clean error <=1/4; log tilted Bernoulli mgf second derivative <=1/4 gives explicit exp(-b/32). |
| Chi-square residual law | iid Gaussian replicates, orthogonal prescribed contractions | Orthogonal replicate-index transform yields independent mean and residual coordinates; degrees of freedom m(n-1). |

No generic empirical-process theorem, differentiability theorem, Berry–Esseen inequality, tensor perturbation expansion, semiparametric efficiency theorem, or optimization convergence theorem is invoked.

## Closest external results inspected

| Source | What was checked | Implication for this project |
|---|---|---|
| [Collier, Comminges and Tsybakov (2017)](https://arxiv.org/pdf/1502.00665), Theorems 2–3 and sparse-mixture argument | Full-text Gaussian sequence formulation and sparse-zone linear-functional rate. With q=2/K, radius M=tau sqrt(p) and normalization by sqrt(p), the rate equals the manuscript's diagonal benchmark. | D1 is a classical specialization. The audit does not claim a new diagonal minimax principle. Its proof is supplied separately, so no estimation-risk-to-interval conversion is assumed. |
| [Oseledets (2011)](https://users.math.msu.edu/users/iwenmark/Teaching/CMSE890/TENSOR_oseledets2011.pdf), Theorems 2.1–2.2 | Exact TT representation from unfolding ranks and the TT-SVD approximation statement; full mathematical pages inspected. | Only exact finite-rank representation is needed. The new approximation extension is stated as a distance class; it does not import an unverified sharper TT-tail formula. |
| [Devroye, Lerasle, Lugosi and Oliveira (2016)](https://arxiv.org/pdf/1509.05845), Section 4.1 | Full-text median-of-means construction for independent finite-variance data. | S4 uses a classical robust-mean mechanism with a separately proved simultaneous contraction bound and bounded-row-corruption calculation. No general minimax robustness novelty is claimed. |
| [Stark (1992), publisher record](https://www.sciencedirect.com/science/article/abs/pii/016771529290234V); [Berkeley author manuscript record](https://digicoll.lib.berkeley.edu/record/86105) | Bibliographic metadata and bounded-normal-mean scope verified. The manuscript PDF endpoint returned 403; its full proof was not read in this audit. | This is background attribution only. S2's exact tensor-to-scalar reduction and scalar minimization are proved in full here; no inaccessible theorem is a dependency. |
| [Ma, Du, Xia and Yuan (2026), arXiv v3](https://arxiv.org/pdf/2312.00305), Appendix E, Theorem 10, pp. 83–84 | Full-text tensor-completion CI lower-bound statement, class and SNR condition. The model samples canonical entries; the class imposes incoherence, a positive minimum signal, bounded condition number and tangent-loading norm at least s0. The lower bound is c sigma sqrt(d*/n) s0. | A serious neighboring inference result, but its experiment and strong-signal class exclude our zero-point rank-boundary question. It is not a proof of S7/S8, and its title alone would conceal the tensor appendix. |
| [Cai and Low (2004), adaptive intervals](https://arxiv.org/abs/math/0503662); [nonconvex functionals](https://arxiv.org/abs/math/0406427) | The prior project retained the full texts and theorem-level inspection notes; those notes and their relationship to the present definitions were reviewed. | Testing/modulus methods and nonlinear advantages over affine procedures are established foundations. The proposed novelty must be the evaluated tensor geometry and rates, not generic honest adaptation. |
| [Xu, Chen and Han (2025)](https://arxiv.org/abs/2501.16223); [Ke et al. (2026)](https://www3.stat.sinica.edu.tw/statistica/fp/SS-2026-0222.html) | Prior full-text notes record functional inference on regular low-rank strata, pilot/projection conditions and a positive minimum unfolding signal in principal theorems. | A tangent-normal interval on a regular stratum is not uniform coverage on the whole cap union. Our loading is narrower and no efficient regular-stratum dominance is proved. |

## Novelty attack

Additional searches used combinations of tensor linear functional confidence interval, minimax expected length at zero, tensor spectral/injective norm scan, subtensor tests, harmonic diagonal rank-one sign mixture, weighted Rademacher series cubic exponential moment, affine bounded normal mean, and tensor-completion CI lower bounds. Classical nonconvex sequence and testing constructions were treated as competitors, not ignored because they lack tensor terminology.

No substantially equivalent statement of the S7/S8 pair was identified in the material inspected. This is **apparent mathematical novelty, not certified priority**. Both techniques use classical tools; a sharp tensor specialization can still be substantial, but its relation to broader nonconvex functional-testing theory deserves an independent expert literature check before submission. The present audit is not a claim to have exhaustively read every relevant 2026 paper.

The strongest defensible difference is:
\[
\begin{array}{ll}
K\ge4:& \mathcal L_0(\Theta)\asymp\tau\sqrt{\log p/p},\\
K=3:& c\tau\log p/\sqrt p\le\mathcal L_0(\Theta)
        \le C\tau(\log p)^{3/2}/\sqrt p,
\end{array}
\]
for full Gaussian tensor observations, fixed positive Tucker/TT caps, equal diagonal loading and M=tau sqrt(p). This is distinct from the already established diagonal Gaussian-sequence rate and the regular-stratum tangent variance.
