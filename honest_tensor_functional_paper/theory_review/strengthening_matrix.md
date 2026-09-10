# Final theorem audit and strengthening matrix

S1–S6 are complete supporting propositions in the reviewed appendix. S7 and S8 are revised Theorems 7 and 8. A correct theorem is not automatically a novel theorem.

| Input result | Correct / complete? | Assumptions minimal? | Rate sharp? | Final verified improvement | Status |
|---|---|---|---|---|---|
| T1 diagonal geometry | Yes / yes | Orthogonality sufficient; frame variant possible | Exponent sharp at rank one; cap factor not sharp | S1 replaces J^(1-1/K) by D=min(original,ambient,mode-rank product) | VERIFIED; strengthened |
| T2 honest interval | Yes / yes | Gaussianity/independence too strong for nonlinear component | Diagonal rate sharp, constants conservative | S3 exact/noise-envelope threshold, additive eta, common-event tuning; S4/S5 additional replicate models | VERIFIED; strengthened |
| T3 affine lower | Yes / yes at alpha<1/2 | Class inclusion enough for old bound | Old constant not sharp | S2 exact scalar quantile optimization for entire cap class | VERIFIED; strengthened |
| T4 single unfolding | Yes / yes | Current constant needs alpha<1/4; can relax | Order sharp on enlarged honesty class | S6 retunes constants to every alpha<1/2 | VERIFIED |
| T5 strict separation | Intended domain yes; literal statement omits alpha range | Missing domain corrected | Comparison sharp in affine/relaxed order; diagonal exponent has restricted sharpness | Explicit alpha<1/4; smaller D gives broader sufficient growing-cap condition | VERIFIED after correction |
| T6 coordinate mixture | Yes / yes with equal loading repeated | Isotropy can be compared via covariance floor | Sharp L0 order K>=4; loose K3 | S7 matches it K>=4; S8 improves it K3 | VERIFIED; scope resolved |
| D1 diagonal benchmark | Yes / yes | Restricted observation essential | Both L0,d and Lmax,d sharp for fixed caps | No need to improve a classical matched rate; attribute it | VERIFIED |
| L1 expansion | Yes / yes | Exact finite rank; no spectral gap | Weight identity exact; J may be loose | Also yields \|B\|F<=sqrt(J)rho(B), enabling S7 | VERIFIED |
| L2 image | Yes / yes | Orthogonal product loading | Exact set equality | No full-experiment equivalence claimed | VERIFIED |
| L3 envelope | Yes / yes | $\lvert e\rvert\le\lambda$ | Pointwise sharp; global summation can be loose | Residual one-Lipschitz gives sharp additive eta constant | VERIFIED |
| L4 structural | Yes / yes | Matrix rank bound | Sharp, and tensor structural range attained | S2 gives matching tensor witness | VERIFIED |
| L5 mixture lemma | Yes / yes | Intervals and common target essential to proof | Generic bound; not always optimal constant | S8 uses it with a harder full-data mixture | VERIFIED |
| Q2 proposed rate | No proof in input; explicitly a conjecture | Fixed K>=3 range too broad | False for K3 | S8 counterexample; S7 validates fixed K>=4 | FALSE AS STATED; replaced |
| S7 scan | Yes / full proof supplied | Exhaustive finite nets; known Gaussian scale; fixed caps for rate | Sharp L0 for K>=4; K3 log gap | Full-data rate and preserved worst-case upper bound | PROVED IMPROVEMENT |
| S8 harmonic mixture | Yes / full proof supplied | K3 and equal loading; rank-one class inclusion | Constant conservative; possible sqrt(log p) gap | L0 >=c tau log p/sqrt(p) | PROVED IMPROVEMENT |

## Existing theory → original manuscript → reviewed theory

| Topic | Prior theory | Original manuscript | Final verified statement | Interpretation |
|---|---|---|---|---|
| Diagonal information | Classical ell_q functional rates | tau(log p/p)^((K-2)/(2K)) | Same optimal restricted rate, explicitly attributed | Correct specialization, not the primary novelty |
| Full data, K>=4, at zero | General testing/modulus tools; no equivalent tensor rate found | tau sqrt(log p/p) <= L0 <= tau(log p/p)^beta | L0 ~ tau sqrt(log p/p) | Matching same-experiment upper/lower bounds |
| Full data, K3, at zero | General mixture methods | Polynomial upper/lower gap and smaller-rate conjecture | tau log p/sqrt(p) <= L0 <= tau(log p)^(3/2)/sqrt(p) | Conjecture refuted; only sqrt(log p) gap remains |
| Full-data worst case | Not settled by cited regular-stratum theory | Lmax <=C tau(log p/p)^beta | Same upper bound retained by intersection | Still open; no minimax claim |
| Affine benchmark | Bounded-normal-mean decision theory | Harmonic lower bound | Exact min_t Q_alpha(a0(1-t),tau t) | Exact tensor reduction; classical scalar optimization |
| Rank factor | Canonical tensor geometry | J^(1-1/K) | D<=min(J^(1-1/K),m^(1-1/K),mode-rank product) | Better growing-cap upper guarantee, not sharp rank theory |
| Approximate rank | General deterministic perturbation principles | Exact ranks | Radius plus eta on dist_F class | Complete finite-sample extension |
| Noise | Gaussian calibration; classical robust means | Known iid Gaussian coordinates | Envelope, finite-variance corrupted replicates, or independent residual scale | Explicit changes of assumptions and information |

## Opportunities not promoted to theorems

1. **Cubic sharp rate:** determine r_3(p) between log(p) and log(p)^(3/2) in tau r_3(p)/sqrt(p). Impact 5/5, feasibility 3/5. Improve weighted sign mixtures or entropy-sensitive scans; the missing step is matching the logarithmic factor.
2. **Full-data worst-case length:** determine Lmax separately. Impact 5/5, feasibility 2/5. Need nonzero-base local alternatives or a uniformly short construction; the zero-point scan does not suffice.
3. **Efficient scan substitute:** polynomial-time attainment of S7's rate. Impact 4/5, feasibility 2/5. Need a computable certificate controlling all ordered diagonal magnitudes; no computational lower bound is established.
4. **Actual-rank adaptation:** expected length on smaller strata under honesty on an outer cap. Impact 5/5, feasibility 2/5. Need between-class testing geometry; a deterministic oracle inequality is not an observable adaptive radius.
5. **General loading geometry:** replace orthogonal equal weights by a class of L with a sharp geometry-dependent modulus. Impact 4/5, feasibility 3/5. Frame bounds are only a partial upper result.

The easiest improvements (constants and calibration) are complete. The highest scientific priority is the cubic logarithmic gap or the full-data worst-case problem, not adding unrelated contamination assumptions merely to obtain another theorem.
