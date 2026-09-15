# Mathematical positioning and comparator contract

The revised claim is the full-data tensor minimax argument and its all-budget phase diagram. No exhaustive priority or “first” claim is made. Primary sources and version-pinned copies in the project were used; the earlier full literature comparison remains preserved.

| Closest precedent | What transfers | What requires a different argument here |
|---|---|---|
| Cai–Low, nonconvex linear-functional estimation and confidence-interval adaptation | Moduli, testing, nonlinear procedures and honest-adaptation obstructions | Specific tensor diagonal geometry, full tensor likelihood and cubic harmonic mixture. General nonlinear inference is not novel here. |
| Collier–Comminges–Tsybakov, Gaussian sparse/ell-q functionals | The exact rank-one diagonal image reduces the marginal experiment to q=2/K sparse functional theory | Off-diagonal observations change likelihood overlap; diagonal lower bounds do not establish full-data lower bounds. |
| Juditsky–Nemirovski, inference over finite unions of convex sets | Aggregation and nonconvex-model inference principles | The tensor cap class and scan/ordered-coordinate geometry needed for the all-budget rate. |
| Xu–Chen–Han, tensor functional inference | Full-data tangent variance and a relevant regular-signal benchmark | Finite-sample honesty on the whole cap union at zero and weak signals; narrower loadings, known budgets and conservative length are real costs. |
| Choo–d'Orsi, sparse tensor PCA | Low-degree likelihood methodology | The scalar target, prior and risk reduction must be specified. Low-degree separation is not all-algorithm interval hardness. |
| Canonical Tucker/TT and tensor norm literature | Orthonormal core gauges, TT prefix identities and product exponent 2/K | The inference construction and full-likelihood rate proof; the exponent itself is not a new general geometric principle. |

For the flat contrast at M=tau sqrt(p), compare full-data cubic length tau(log(ep))^(3/2)/sqrt(p) with diagonal-only length tau(log(ep)/p)^(1/6). These are different observation restrictions under the same rank-one class. The order-tau single-unfolding lower bound instead changes the honesty class while retaining all data. Fixed-radius affine intervals impose a procedure restriction. The revised manuscript never conflates those three comparisons.

For sparse support overlap H, the diagonal Gaussian mixture likelihood has an exponent proportional to H, whereas product tensor alternatives can have one proportional to H^K. The cubic harmonic construction is designed for the latter full experiment. The norm cap is imposed before summing ordered coordinates; taking a minimum only after summation can discard the intermediate logarithmic budget regime. These are the substantive mathematical distinctions that support the focused contribution.

## XCH implementation-to-source map

Source: Xu, Chen and Han, *Statistical Inference for Low-Rank Tensor Models*, [arXiv:2501.16223](https://arxiv.org/abs/2501.16223), tensor-PCA Section 4.2 Algorithm 3 and Section 4.3 inference results. The available local primary PDF/text was read for the algorithm and theorem assumptions. The compared observation model is the tensor-PCA/Gaussian tensor setting, not the scalar-response regression theorem.

`empirical/code/tensor_methods.py::xch_pca` uses HOSVD initialization and two simultaneous subspace projection updates. Each update uses the previous collection of mode factors. It fits the core after projection, evaluates the same prescribed functional, and reports tangent-loading variance with either supplied tau or the residual plug-in scale. The public implementation in the source and this local numerical implementation are not claimed byte-identical.

Information access: all observed entries, supplied rank, fixed loading, known-noise variant using the same tau as our procedure. The support oracle additionally receives true support and is labeled as such. Our cap-valid artificial split uses independent auxiliary noise; it is not extra observed data. All methods in a case share the same observed tensor; paired ablations share the same pilot. No target-based tuning is performed.

Guarantee type and case eligibility are distinct fields. Exact zero and supplied-rank mismatch are flagged outside the specified regular model. In other cases, correct rank or a large observed signal does not certify the theorem's initialization, alignment and remainder conditions. They remain explicitly unverified per case. Strong-signal agreement is useful empirical evidence, not a finite-sample cap-honesty guarantee for XCH. Its smaller lengths at strong signals are reported without attempting to manufacture leading-constant dominance for the cap-valid interval.

Primary methodological pages: [Cai–Low adaptation](https://doi.org/10.1214/009053604000000049), [Collier–Comminges–Tsybakov](https://arxiv.org/abs/1502.00665), [Juditsky–Nemirovski](https://arxiv.org/abs/1804.00355), and [Choo–d'Orsi](https://arxiv.org/abs/2106.06308). Final submission should still receive a targeted priority and bibliography check against the then-current versions. This internal revision is not an independent priority certification.
