# Theory-led empirical study: design frozen before execution

Date: 2026-09-12. This study concerns the honest tensor-functional branch, not the earlier TT compression model. The user's simulation guidelines are the governing protocol. No new theorem is proposed here. EXPECTED statements below are hypotheses, not results.

## Mathematical experiment and estimands

The ideal experiment is Z=A+tau G, G having independent standard normal entries, tau=sigma/sqrt(n), known sigma, supplied Frobenius bound M and supplied Tucker/TT caps. The main loading is L=p^(-1/2) sum_i e_i^(tensor K), with target psi=<L,A>. Rank-r diagonal signals have A=sum_{i in S} a_i e_i^(tensor K), norm ||a||_2, and actual Tucker/TT ranks r. Random supports and signs are independent of noise. Dense rank-one signals are A=M u^(tensor K), u=1_S/sqrt(s). Rotated signals use independent orthogonal mode factors. Zero is in every cap class.

Diagonal-only procedures are simulated using their exact sufficient observations: d_i=A_{i,...,i}+tau g_i. For methods depending only on sum d_i, use its exact scalar Gaussian marginal. This is not a tensor recovery benchmark or an experiment in which off-diagonal entries are absent. Full tensors are generated for projection and solver experiments. n sweeps use the exact Gaussian sample-mean distribution, not additional fictitious observations. Artificial splitting uses Z+tau G' and Z-tau G', with independent G'; both have noise sqrt(2) tau. Paired methods see the same Z, and split ablations share G'.

## Part A: predictions and rates

- Large caps r>=c sqrt(p): length scale min(M sqrt(r/p),tau), squared risk its square. At fixed large structural radius, length and root MSE versus n have slope -1/2. At fixed M and r=sqrt(p), the structural branch has p slope -1/4. Structural-to-noise transitions are deterministic procedure thresholds, not rank recovery thresholds.
- Fixed caps: the implementable threshold interval has radius proportional to M^(2/K) tau^(1-2/K) (log p)^((1-2/K)/2)/sqrt(p). At M=tau sqrt(p), its p exponent is -(K-2)/(2K), with a logarithmic factor. The sharper full-data rate from the residual optimizer is only a theoretical reference at high p.
- Strong saturated diagonal means: P1 gives expected length scale tau sqrt(r/p), when its stated norm and very strong signal conditions hold. For fixed r its p slope is -1/2; for r=ceil(sqrt(p)) it is approximately -1/4. Practical signal sweeps test where shortening begins; they cannot establish an optimal threshold.
- Small-budget loading geometry: for rank one and orthogonal weights, rho(L)=max|w_i|, so structural length is exactly 2M max|w_i|. For fixed power decay beta>0 the all-budget sharp scale is max|w_i| min(M,tau), but the ideal block optimizer is not implemented. Analytic envelopes are reported separately from Monte Carlo performance.
- Joint sub-Gaussian and finite-variance results concern known directional envelopes. Median-of-means full-net feasibility can be checked in a complete binary net. This does not implement the general robust minimax optimizer. No Huber-contamination or dependent-replicate guarantee is claimed.
- Approximate-rank and loading-residual corrections must cover the discarded target contribution. We test implementable conservative threshold/transfer constructions, not the unavailable sharp full-data approximate-rank optimizer.

The theorem map and experiment registry enumerate all main result families, including lower bounds and impossibility statements that finite simulation cannot validate universally.

## Part B: paired comparisons and failures

Baselines are the exact direct Gaussian interval, known-bound structural interval, published sequence-style soft thresholding with the repository's proved calibration, and the Xu–Chen–Han (2025) tensor PCA procedure, Section 4.2 and Algorithm 3. The last is implemented with HOSVD initialization, two simultaneous power iterations, fitted core/right spaces and the exact manifold tangent variance. Known-noise and their residual plug-in noise versions are both retained. It requires regular-signal, initialization and alignment conditions; weak-signal undercoverage is an out-of-domain stress result, not a refutation of its theorem. No truth-assisted initialization is used.

The known-support oracle estimates the true nonzero diagonal coordinates; for dense rank-one signals the known-direction oracle uses an exact jointly Gaussian contraction. Oracles have a smaller honesty class and unavailable information. A bias-omitted split projection and the previous separated rank selector test the need for the new correction/caps. No method is tuned on test outcomes. Solver node budgets and tolerances are fixed in the configuration registry; unresolved endpoints remain outer bounds.

Noise stressors: standardized independent t3 and t5; independent Rademacher; equicorrelated Gaussian coordinates with rho in {0,.2,.5,.8}; centered 1%/5% variance mixtures; 5% mean-shift contamination. Correct known directional proxy and naive iid calibration are distinguished. For finite variance the covariance bound is kept at one by standardizing mixtures. Replicate dependence uses stationary AR(1) correlation .5 and is explicitly outside iid-replicate theory. Approximation allowances and rank/noise bounds are also deliberately understated in labeled violations.

## Precision, failures and reproducibility

Cheap scalar cases use 5,000 independent trials: nominal 95% coverage MCSE .00308. Threshold cases use 1,000 trials: MCSE .00689. Full tensors use 500 trials for most cases, 300 at p=32 and 150 at p=64: MCSE .00975, .01258 and .01780. Solver runs use 30 trials per signal/loading case: MCSE .03979; these measure computation, not precise coverage. Median scans use 500 trials: MCSE .00975. Levels 90%, 95%, 99% reuse the same observations. Wilson 95% intervals remain nondegenerate at 0/100% coverage; interval length, squared error and paired differences include standard errors.

Every trial saves endpoints, error, rejection, timing and relevant solver/selection metadata. Input observations are regenerated by deterministic case/trial seeds. Failures stay in raw records; exceptions fail the run rather than silently drop observations. Simultaneous nominal-coverage screening uses Bonferroni-adjusted one-sided binomial tests over in-scope rows, followed by an explicit diagnostic audit; pointwise Wilson intervals are not simultaneous guarantees. No CLT is asserted for nonlinear interval midpoints. Gaussian direct/oracle and the published regular-signal standardized estimator receive distribution diagnostics; outside their assumptions diagnostics are descriptive.

Timing separates method execution from data generation. A separate repeatable scaling benchmark measures actual diagonal access and full-tensor methods. Report traced Python/NumPy peak allocations separately from input size; these are not total native process-memory peaks. Fixed thread counts prevent BLAS oversubscription. Software, sources, configurations, design and preserved-stage hashes are recorded. Previous saved results are not pooled with this run.

## Real-data scope

The attachment requests real-data work as well. The repository currently has no dataset with a justified repeated-tensor sampling model, known directional noise bound, supplied approximation allowance and independently fixed scientific loading. A dataset preference has been requested while simulations proceed. Without such data, the real-data deliverable is an explicit applicability/missing-input audit; no synthetic tensor or injected-noise image is presented as real-data validation. This empirical requirement remains pending, not completed.
