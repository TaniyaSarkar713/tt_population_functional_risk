# Audit of the norm and loading derivations

This is an internal adversarial check of the supplied proofs. The new numbered statements are in [the manuscript section](../paper/norm_loading_section.tex), with [complete proofs](../paper/norm_loading_proofs.tex). Finite computations do not establish universal correctness or novelty.

| Potential failure | Resolution in the derivation |
|---|---|
| A difference need not have the original rank caps | All difference arguments use doubled unfolding caps and norm at most $2M$; constants $P_2,Q_2$ use $J(2\bar r)$ |
| Taking a minimum after summing may miss the cubic transition | Both bounds apply to the same ordered coordinate; the minimum is taken before the sum |
| The threshold might hide norm/noise dependence | Its bound uses a constant depending only on fixed order/confidence; all $M,\tau$ dependence is displayed through $x$ |
| The harmonic split might fail near one or with floors | The $x\le1$ case is separate; for $x>1$, $\lfloor x^2\rfloor\ge x^2/2$ |
| The cubic hard mixture might violate the norm budget | Choose $m\le x^2$ and retain the original minimum in $b_m$; both constraints are checked separately |
| The large-$p$ lower argument might omit small dimensions | For $p<256$, $\ell_p<7$ and the coordinate bound is sufficient up to a fixed constant |
| An apparent sharp diagonal rate might be transferred to full data | Every lower bound computes full mean-tensor inner products and the full Gaussian likelihood second moment |
| A fixed-confidence midpoint might have huge squared risk outside coverage | The new residual-fit proof integrates a norm-independent Gaussian excess tail and uses the structural bound for small $M$ |
| A minimizer might not be measurable or computable | A fixed countable dense set and positive tolerance define a Borel estimator; no efficient implementation is asserted |
| Dependence among scan directions might invalidate a tail argument | The proof uses a union bound; it never assumes independent contractions |
| Negative loading weights might spoil the common target or likelihood bound | The signed first-mode multipliers cancel the target weights; pairwise inner products contain their squares |
| Rescaling could increase likelihood overlap | The starting factors are nonnegative; multipliers have magnitude at most one, so every relevant inner product decreases |
| Ignoring ambient entries might invalidate a lower bound | Hard alternatives are embedded with all other mean entries zero; extra coordinates are independent pure noise, and full likelihoods are unchanged |
| Flat-support inference might imply a general arbitrary-loading theorem | Only prescribed orthogonal product loadings are covered; unequal-weight envelopes are not asserted sharp in general |
| Constants might imply adaptation to growing or unknown actual rank | Constants depend on supplied fixed caps; neither growing-cap optimality nor actual-rank adaptation is inferred |
| A phase diagram might be mistaken for an exact formula | All rate comparisons are up to fixed constants; transition constants and optimal confidence-level dependence are not claimed |

## Proof dependencies

The diameter uses the earlier diagonal quasi-norm bound, finite-net injective-norm comparison, and measurable compact confidence-set projection. The cubic lower bound uses the earlier sparse harmonic construction and its hypergeometric factorial-moment proof. The all-budget optimization, residual-excess MSE control, and weighted common-target contraction are supplied here in full.

No unverified external theorem is required for the new derivations beyond elementary finite-dimensional inequalities, Gaussian integration, and the previously supplied tensor lemmas. The local literature guide records the classical Gaussian functional and tensor-inference context.

## Verdict and remaining review

The norm-budget and flat-loading claims have complete supplied proofs and passed the saved finite checks. The largest unresolved mathematical risks for the paper remain independent validation of the earlier tensor expansion/scan lemmas and external priority assessment of the evaluated rate. Neither the new proofs nor the existing low-degree result resolves unrestricted efficient computation.
