# Real-data applicability and missing-input audit

**Status: PENDING DATA/MODEL (R01).** No real-data result, real-data coverage claim or LLM application has been run. The user's attached guidelines request an application, but the current request prioritizes simulations and the repository contains no justified repeated-tensor dataset. A data preference was requested while the simulation work continued.

The suitable experiment would consist of independent calibrated repetitions of the same K-way mean tensor, or a defensible extension with known directional concentration/variance bounds. A scientific loading must be fixed independently of the inference observations. Exact low rank requires a substantive justification; approximate low rank needs an externally supplied allowance. These cannot be asserted because an observed tensor has a good low-rank fit.

## Required data description and preprocessing contract

| Field | Required before analysis | Present status |
|---|---|---|
| Scientific population and target | Define <L,A> in domain terms; justify any orthogonal diagonal matching across modes | Not supplied |
| Tensor modes | Native measurement axes, dimensions, units and calibration | Not supplied |
| Independent sampling unit | Identify specimen/session/subject; preserve complete clusters in splits | Not supplied |
| Replications and dependence | Count genuinely independent repeated tensors; analyze temporal/within-unit dependence | Not supplied |
| Noise envelope | Known sigma or joint proxy; additional calibration theory if estimated | Not supplied |
| Rank/norm/approximation bounds | Externally justified supplied bounds, or explicit sensitivity analysis without honesty claims | Not supplied |
| Missingness | Complete-observation model or new sampling theory; no unacknowledged imputation | Not supplied |
| Loading and preprocessing | Prespecify target; estimate scaling/projections only on training or independent pilot data | Not supplied |
| Evaluation | Paired target stability/precision, cluster-level uncertainty; no coverage without known truth | Not supplied |
| Provenance | Primary data source, license, immutable raw checksum, exact download/preprocessing script | Not supplied |

An ordinary RGB/hyperspectral image supplies a native tensor but usually not independent repetitions, known noise or a scientific orthogonal-diagonal contrast. Fluorescence arrays can have meaningful modes and low-rank mechanisms, but stacking different specimens as independent repetitions of one fixed mean is not justified automatically. LLM layers/tokens/prompts introduce additional dependence and data-derived loadings. These are model-fit concerns, not claims that such applications are impossible.

Raw observational data should remain immutable under `data/raw/`; preprocessing, split indices, code, results, tables, figures and logs should be added only once a dataset is chosen. No empty result files or artificial application section are created. This document is an applicability audit and does **not** satisfy the requested real-data execution deliverable. It keeps that limitation reviewable while completing the authorized simulation study.
