# Proof dependency audit

Every dependency below was recalculated in the audit. Full proofs, including roadmaps, are in the revised PDF's appendices. No unproved conjecture is an ancestor of a theorem. S1–S8 are review identifiers; S7/S8 are revised Theorems 7/8, S1–S6 are revised Propositions 2–7.

| Result | Direct dependencies | Check and external assumptions |
|---|---|---|
| L1 canonical expansion | Orthonormal mode bases; sequential column-space factorization | Exact finite-dimensional linear algebra; actual rank can vanish; no bounded inverse. TT prefix recursion, not path orthogonality. |
| T1 diagonal budget | L1; q-subadditivity; Holder; Bessel; finite power mean | q=2/K in (0,1]; zero term handled; loading orthonormal mode by mode. |
| L2 exact image | T1 at rank one; signed product construction | Both inclusions; norm equals the q-budget to power 1/q; every sign allowed. |
| L3 scalar envelope | Sign cases; min interpolation | lambda>=0, \|e\|<=lambda; q=1 endpoint valid by continuous convention. |
| L4 structural matrix inequality | Column projection; Cauchy–Schwarz; ordered eigenvalue trace | Projection rank <=r; eigenvalues nonnegative; includes zero matrix. |
| T2 coverage | T1, L3, L4; Gaussian Chernoff and union bound | Uniform event; known scale; exact direct variance; deterministic index. |
| T3 affine bound | Normal interval probability maximized at zero bias; median; coordinate alternatives | Confidence >1/2; both signs and zero included; all full-data affine W allowed. |
| L5 common-target CI bound | Coverage; TV; Cauchy–Schwarz | Interval length, not disconnected-set volume; independent random seed harmless. |
| Gaussian LR identity | Gaussian mgf | Positive isotropic variance; complete full tensor inner product. |
| T4 unfolding lower | L5; LR; independent signs; auxiliary Gaussian; log cosh <=x^2/2 | Mixture belongs to enlarged class; theta <=tau sqrt(p)/4; quadratic mgf finite. |
| T5 separations | T2/T3/T4; scale substitution | Explicit alpha<1/4 inserted; fixed caps/order or tracked growing-cap coefficient. |
| T6 coordinate lower | LR; L5; orthogonal coordinate shifts | Alternatives rank one, norm<=M, common target; chi-square <=1/4. |
| D1 diagonal minimax | L2; diagonal LR; hypergeometric factorial moments; L5; T2 | Restricted experiment throughout; floor support asymptotics verified; full LR has overlap power K. |
| S1 budget refinement | T1; ambient Bessel; mode projectors; TT mode-rank bound | Trace and Holder verified; no rank-estimation assertion. |
| S2 affine optimum | L4; sparse diagonal witnesses; Gaussian quantile monotonicity | h>=absolute mean follows from confidence>1/2; variance monotonicity used only on that domain. |
| S3 envelope and approximation | L3; S1; residual one-Lipschitz; Bessel | Same event for all Lambda>=lambda0; additive eta; unknown oracle term not a usable radius. |
| S4 robust replicate calibration | Chebyshev; independent clean block indicators; tilted Bernoulli mgf; S3 | At most c altered blocks; adaptive replacements allowed; explicit b,n requirements. |
| S5 residual scale | Orthogonal Gaussian transformation; chi-square; conditional selection; T2 | Residual/mean independence verified; n>=2; error split alpha0+delta. |
| S6 levels/covariance | Original mixture second moments; L5; Gaussian noise addition | Constants retuned; PSD noise addition valid even if added covariance is singular. |
| New L6 finite nets | Volume packing; telescoping; L1 and Cauchy–Schwarz | Unit product contractions; K epsilon=1/2; finite sets and measurable tests. |
| S7 full-data scan | New L6; T1; rank preserved under coordinate restriction; Gaussian union; T2/T6 | All subsets and sizes counted; no independence of contractions assumed; expected rejection cost controlled. |
| New L7 cubic mgf | Head/tail decomposition; weighted-sign Chernoff; Tonelli | Uniform tail for x>=12; head m floor handled; cubic mgf constant verified. |
| S8 cubic obstruction | New L7; coupled rank-one signs; full LR; Holder; L5 | Three weighted sums dependent; Holder needs only marginal mgfs; norm and common target verified. |

The finite proof graph is acyclic. The only external structural construction is standard orthogonal tensor factorization, restated algebraically in L1. Classical sparse-sequence, bounded-normal-mean and median-of-means papers provide attribution, not missing proof steps.
