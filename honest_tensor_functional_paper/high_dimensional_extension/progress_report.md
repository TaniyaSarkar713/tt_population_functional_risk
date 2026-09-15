# Progress beyond the exponential benchmark

Status: 2026-09-12. This stage gives matching theory and polynomial
procedures in additional regimes, rather than extending the small
exponential optimizer. The general fixed-cap weak-signal computation
problem remains open. All previous-stage files are preserved.

## Main results

| Requested direction | New conclusion | Remaining limit |
|---|---|---|
| Efficient high-dimensional minimax computation | If the smallest cap $r\gtrsim\sqrt p$, a structural/direct interval attains sharp length $\min(M\sqrt{r/p},\tau)$ for every budget | Fixed and intermediate caps with diffuse weak signals remain open |
| Loading rates beyond small budgets | For fixed polynomial decay $\lvert w_i\rvert\le C\lvert w_1\rvert i^{-\beta}$, sharp length is $\lvert w_1\rvert\min(M,\tau)$ at every budget; a class of nonorthogonal perturbations is included | General profiles remain open; the matching block-fit construction is not an efficient optimizer |
| Growing-rank adaptation | Simultaneous minimax adaptation from growing outer caps to positive fixed inner caps is impossible | This is an impossibility for that objective, not a characterization of every adaptation opportunity |
| Pointwise inference | A polynomial cap-valid interval has optimal expected-length rate $\tau\sqrt{r/p}$ at strong diagonal Tucker means saturating their caps | Requires a conservative sufficient amplitude and norm slack; not optimal signal thresholds or leading constants |
| Computational limits | For power exponents $0<\beta<1/K$, a loading-compatible low-degree prior gives a polynomial gap from the new sharp estimation rate | Restricted polynomial-estimator result; no blanket hardness claim for efficient confidence intervals |

The growing-cap conclusion uses a previously proved sparse-diagonal
mixture and supplies its matching upper bound. The pointwise proof uses
the same outer honesty class for both bounds and controls the pilot
failure contribution with a budget shrinking as $r/p$. The loading proof
uses dyadic blocks with explicit error allocations and a summable decay
envelope. Complete supplied derivations are in
[theory/results.md](theory/results.md) and [the supplement](paper/main.pdf).
These results have not undergone independent mathematical review.

## Newly run growing-cap experiments

The interval reads only diagonal observations, so the experiment generates
exactly those independent Gaussian coordinates. It does not materialize the
unused off-diagonal noise. Coverage is proved for the full tensor class;
simulation uses zero and rank-cap boundary means. The largest loading
dimension is 16,384. The table shows its boundary cases; all dimensions and
zero cases are retained in `results/growing_caps.json`.

| $p$ | Cap $r$ | Structural radius / $\tau$ | Covered / trials | Coverage 95% Wilson interval | Mean length |
|---:|---:|---:|---:|---|---:|
| 16384 | 128 | 0.25 | 200/200 | [0.981, 1.000] | 0.500 |
| 16384 | 128 | 2.00 | 189/200 | [0.904, 0.969] | 3.920 |
| 16384 | 128 | 8.00 | 188/200 | [0.898, 0.965] | 3.920 |
| 16384 | 512 | 0.25 | 200/200 | [0.981, 1.000] | 0.500 |
| 16384 | 512 | 2.00 | 195/200 | [0.943, 0.989] | 3.920 |
| 16384 | 512 | 8.00 | 187/200 | [0.892, 0.962] | 3.920 |

There are 36 configurations and 7,200 newly run trials.
The structural/direct choice is deterministic and the theoretical
worst-case squared-risk bound is saved alongside empirical squared error.
Finite Monte Carlo deviations are not used as proof of a uniform guarantee.

## Newly run pointwise experiments

These experiments generate the complete tensor observation, then make a
correctly scaled artificial split. No additional observed replicate is
assumed. The supplied cap is retained. In the strong rows, the signal
amplitude is eight times the theorem's conservative sufficient bound;
it ranges from approximately 60,000 at $p=8$ to 9.4 million at $p=64$,
with $\tau=1$. These are deliberately very strong signals.

| $p$ | Cap $r$ | Covered / trials | Coverage 95% Wilson interval | Mean length | Mean time (ms) |
|---:|---:|---:|---|---:|---:|
| 8 | 1 | 195/200 | [0.943, 0.989] | 2.672 | 0.37 |
| 8 | 3 | 193/200 | [0.930, 0.983] | 3.883 | 0.46 |
| 16 | 1 | 118/120 | [0.941, 0.995] | 1.931 | 0.96 |
| 16 | 4 | 116/120 | [0.917, 0.987] | 3.438 | 1.18 |
| 32 | 1 | 60/60 | [0.940, 1.000] | 1.430 | 6.28 |
| 32 | 6 | 58/60 | [0.886, 0.991] | 3.047 | 8.84 |
| 64 | 1 | 20/20 | [0.839, 1.000] | 1.003 | 74.75 |
| 64 | 8 | 19/20 | [0.764, 0.991] | 2.743 | 88.42 |

At rank one, the mean length decreases with dimension consistently with
the proved $p^{-1/2}$ scale. All strong saturated trials choose the
tangent option. Small sample counts at the largest dimensions produce
wide coverage uncertainty; those rows are runtime/behavior checks, not
high-precision coverage estimates.

The remaining cases test honesty outside the pointwise-optimality family:

| Case | $p$ | Cap | Covered / trials | Mean length | Chosen option |
|---|---:|---:|---:|---:|---|
| weak | 8 | 1 | 484/500 | 1.889 | structural: 500 |
| strong_lower_rank | 8 | 3 | 189/200 | 4.335 | split_direct: 200 |
| strong_plus_weak | 8 | 3 | 193/200 | 4.315 | split_direct: 200 |
| dense_rank_one | 16 | 1 | 197/200 | 2.081 | structural: 200 |

The pointwise suite has 12 configurations and 1,900
new trials. Conservative fallback is retained when actual rank is below
the supplied cap or weak additional components are present. This is
consistent with the limitation in the theorem, not a claim of full
actual-rank adaptation.

Economy SVDs remove an avoidable allocation from the preceding prototype.
For $64^3$ input, the largest returned right singular matrix has 262,144
entries, compared with 16,777,216 for a full right singular matrix: a
factor of 64 reduction in that array. This is an array-size comparison,
not a measured factor-of-64 reduction in total memory or runtime.

## Loading and adaptation calculations

There are 96 new loading-envelope calculations
covering dimensions 64, 1,024 and 16,384, power exponents 0.1, 0.25, 0.5
and 1, orders three/four, and norm budgets from 0.1 to one million.
They evaluate the deterministic diameter of ideal block fits. They do
not numerically solve those fits or claim measured interval coverage.
The fixed-decay proof is uniform over budgets and dimensions; its
constants deteriorate as the decay exponent tends to zero.

Eight saved comparisons evaluate the growing-outer-cap lower bound
against the positive fixed-cap oracle rate. The proved divergence rules
out general simultaneous rate adaptation even for unlimited computation.
The weighted low-degree proof separately explains why a sharp statistical
loading rate need not yield a polynomial estimator.

## Verification and remaining work

Fresh checks passed: 60 exact
hypergeometric likelihood moments, 9
attained structural bounds, 32
dyadic/tail bounds, 60
pointwise bias/allocation cases, 50
independent projection comparisons, 9
weighted low-degree moment comparisons, and
4 signed unknown-support
strong-signal checks. Seeds, actual software versions, source hashes,
coverage intervals, timing, and the previous-stage manifest are saved.

Still open are efficient minimax intervals for the original fixed-cap
diffuse weak-signal class, arbitrary loading geometry, intermediate
growing-cap rates, a full pointwise characterization, and optimal signal
thresholds for computation. The precise audit is in
[theory/audit.md](theory/audit.md); reproduction is in [README.md](README.md).
