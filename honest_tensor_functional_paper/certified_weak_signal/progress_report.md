# Progress on the remaining weak-signal problems

Status: 2026-09-11. The work supplies a global computational benchmark and
narrows the loading/adaptation questions. It does **not** solve all three
general open problems. Earlier manuscripts and numerical results are preserved.

## What is established

1. The ideal finite-net residual criterion is implemented on the complete
   continuous binary rank-one tensor ball. A global lower/upper objective
   bracket distinguishes an approximately optimal fit from a local solution.
   Confidence-set projection returns safe outer endpoints and feasible inner
   witnesses, with an explicit gap and budget status. This is an exponential
   benchmark, not a high-dimensional efficient optimizer.
2. For every loading tensor, fixed positive caps, and $M\le\tau$, minimax
   interval length is of order $M\rho(L)$ and squared risk is of order
   $M^2\rho(L)^2$, where $\rho(L)$ is the best unit product overlap.
   Computing that overlap need not be efficient. Unequal orthogonal weights
   additionally have an implemented optimized-prior mixture lower bound.
3. The existing ideal outer interval already adapts in minimax **rate** to
   every smaller positive fixed-cap class, without separation. This follows
   because all those classes share the rank-one lower bound. It does not
   resolve rank-dependent constants, growing caps, or pointwise oracle lengths.
4. A new supplied-cap tangent interval stays honest at zero and arbitrarily
   weak signals. Unresolved singular values receive a worst-case angle bound.
   Correctly calibrated artificial splitting and a simultaneous direct
   interval implement it in the original single-observation experiment.
   Strong signals can shorten it; weak-signal minimax optimality is unproved.

Complete statements and proofs are in [theory/results.md](theory/results.md)
and [the technical supplement](paper/main.pdf). The [audit](theory/audit.md)
separates proved regimes, numerical certificates, and remaining requirements.

## Newly run optimizer experiments

All supports and 1,002 calibrated scan constraints were used for
order three and mode size two. The optimization parameter space is continuous.
The stopping tolerance is $0.2\tau$, with 600 branch expansions per trial.
Intervals reported below always use the outer bounds, including budget stops.

| Signal | Loading | Covered / trials | Coverage 95% Wilson interval | Endpoint gap certified to tolerance | Mean outer length | Mean nodes |
|---|---|---:|---|---:|---:|---:|
| zero | flat | 40/40 | [0.912, 1.000] | 37/40 | 3.148 | 348.5 |
| zero | arbitrary | 40/40 | [0.912, 1.000] | 39/40 | 3.999 | 188.1 |
| weak_dense | flat | 40/40 | [0.912, 1.000] | 40/40 | 3.154 | 326.3 |
| weak_dense | arbitrary | 40/40 | [0.912, 1.000] | 40/40 | 4.000 | 177.4 |
| boundary_atom | flat | 40/40 | [0.912, 1.000] | 37/40 | 3.112 | 349.2 |
| boundary_atom | arbitrary | 40/40 | [0.912, 1.000] | 38/40 | 3.991 | 202.7 |
| strong_dense | flat | 40/40 | [0.912, 1.000] | 0/40 | 2.867 | 600.0 |
| strong_dense | arbitrary | 40/40 | [0.912, 1.000] | 0/40 | 4.547 | 600.0 |

There are 320 new optimizer trials, with 231 meeting the endpoint
tolerance. The strong-signal cases hit the short node budget; their wider
outer intervals remain the reported result. Full coverage in these finite
trials is not a proof of uniform coverage. The small dimensions and conservative
union thresholds do not establish a useful high-dimensional minimax gain.

Independent analytic checks include a one-atom residual minimum with known
exact value, the exact structural support of a flat binary loading, a
certified empty confidence set, and a positive non-rank-one residual optimum.
The latter has global bracket
[8.831631,
8.926524].
An intentional one-node stop verifies that incomplete endpoint optimization
is not silently presented as a completed optimizer.

## Newly run original-model adaptation experiments

Each trial starts with one $4\times4\times4$ Gaussian tensor at $\tau=1$.
Artificial splitting uses noise scale $\sqrt2$ in each half. The reported
interval intersects the cap-valid interval at error $\alpha/2$ with the
original-data direct interval at error $\alpha/2$, for $\alpha=0.05$.
The extra component, when present, lies on an orthogonal product atom.

| Main amplitude | Weak extra | Supplied mode cap | Covered / 1000 | Coverage 95% Wilson interval | Mean length | Tangent chosen | Previous separated method covered / 1000 |
|---:|---:|---:|---:|---|---:|---:|---:|
| 0 | 0 | 1 | 979 | [0.968, 0.986] | 3.438 | 0 | 1000 |
| 0.5 | 0 | 1 | 970 | [0.957, 0.979] | 3.404 | 0 | 0 |
| 2 | 0 | 1 | 976 | [0.965, 0.984] | 3.171 | 0 | 0 |
| 2000 | 0 | 1 | 964 | [0.951, 0.974] | 4.337 | 0 | 958 |
| 2000 | 0.5 | 2 | 962 | [0.948, 0.972] | 4.343 | 0 | 962 |
| 2000 | 0 | 2 | 972 | [0.960, 0.981] | 4.348 | 0 | 959 |
| 200000 | 0 | 1 | 954 | [0.939, 0.965] | 3.018 | 1000 | 968 |
| 200000 | 0 | 2 | 955 | [0.940, 0.966] | 4.349 | 0 | 965 |

There are 8,000 new trials here. The old method is deliberately used
outside its separation assumption in the weak-signal rows; those failures
show why removing the assumption from the statement alone is invalid.
The new interval retains coverage through conservative fallback. At a very
large amplitude and a tight cap it uses the tangent option. A loose cap can
prevent that gain even when the actual signal has rank one: the procedure
does not pretend to have solved actual-rank adaptation. The very large
amplitude also shows how conservative its finite-sample bias bound is.

## Loading calculations and verification

The saved loading calculation has 27 combinations of support size, weight
profile and budget. It evaluates a valid full-data lower bound, not a
simulation or a proof of a matching general rate.

Fresh finite checks passed: 1,000 cosine ranges,
1,800 parameter-box containment points,
5 optimizer contract cases,
120 independent mixture identities,
250 first-order bias certificates,
and 180 cap-valid tangent
certificates including weak, zero, lower-rank, and strong cases.

The bounds are proved in real arithmetic. Implementations use double
precision and conservative guards, not formal directed-rounding arithmetic.
Run manifests record seeds, software versions and source hashes. The
previous stage's tracked files are checked against its baseline hashes.

## What remains open

- Efficient minimax weak-signal intervals at general dimensions and caps.
- Sharp larger-budget geometry for every loading and unequal weight sequence.
- Optimal growing-cap factors and pointwise adaptation where it is possible.
- General-dimensional certified optimization and formal numerical enclosures.

The code, proofs, and new experiments are a concrete advance, with those
general problems still open. Reproduction commands are in [README.md](README.md).
