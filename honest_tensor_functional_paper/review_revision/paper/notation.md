# Canonical notation dictionary

| Symbol | Meaning | Dimension / first definition |
|---|---|---|
| K, p_k, p | Tensor order, mode sizes, common mode size | Positive integers; model |
| D_amb | Product of mode sizes | Ambient number of real observations; model |
| A, Z, G | Fixed mean, observed tensor, standard Gaussian error | Product tensor space; model |
| tau, sigma, n | Mean noise scale, replicate scale, independent replicates | Scalars; model |
| M, r-bar, r | Supplied Frobenius bound, cap vector, common/minimum cap | Scalars/vector; model |
| L, psi | Prescribed loading, its tensor contraction | Tensor / scalar; model |
| q_K=2/K | Diagonal compressibility exponent | Scalar; mechanism |
| J | Canonical component-complexity bound | Integer bound; mechanism |
| H | Random support overlap | Integer random variable; lower bounds |
| ell_p, x, mathfrak r_K | log(ep), normalized budget, minimax rate scale | Scalars; central theorem |
| lambda_s, N_S, T | Scan threshold, finite scan seminorm, residual excess | Scalar-valued functions; construction |
| h, h_0 | Supplied structural radius | Scalar; intervals |
| z_u, z_val | Standard normal quantile / validation critical value | Scalar; calibration |
| eta_k | Pilot unfolding noise bound | Scalar; pointwise construction |
| delta | Pilot/auxiliary failure allocation in its stated experiment | Probability; calibration |
| epsilon_A | Frobenius approximation allowance | Scalar; robustness |
| epsilon_TV | Total variation slack in confidence-level refinement | Scalar; technical supplement |
| mathsf d | Polynomial degree cutoff | Integer; computational separation |
| C_diag | Refined diagonal-envelope coefficient | Scalar; technical supplement |
| mathcal D_L | Orthogonal contraction map, distinct from D_amb | Linear tensor-to-vector map; supplement |

The technical supplement preserves locally defined aliases in complete proofs: q for q_K in threshold bounds; z_val for validation critical values in A4/P1; eta for the local pilot or total-variation bound where explicitly defined. These scopes are separate, not an assertion that the quantities coincide. Main-text symbols are global. Coefficient D, ambient D and degree D have been separated throughout the active supplement; approximation allowances no longer share the pilot symbol. Supplied cap and actual rank are never interchanged.
