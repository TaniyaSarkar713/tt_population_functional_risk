# Closest references and reading guide

Selection checked on **2026-09-10** against primary sources and the project's latest [gap-development manuscript](../honest_tensor_functional_paper/gap_development/paper/main.pdf). This is a focused comparison, not an exhaustive priority review.

**Start with Collier, Comminges, and Tsybakov (2017) for the mathematical precursor.** For the closest direct tensor-functional inference comparison, read **Xu, Chen, and Han (2025)**. For the original compression/model-selection branch, start with **Michel and Nouy (2022)**. These judgments compare the observation model, target, assumptions, and guarantee; no single paper covers both project branches.

## The eight selected papers

| Paper | Connection to this project | Local PDF |
|---|---|---|
| Collier, Comminges, and Tsybakov (2017), *Minimax estimation of linear and quadratic functionals on sparsity classes* | Diagonal functional and Gaussian support-mixture bounds | [PDF](closest_papers/collier_comminges_tsybakov_2017.pdf) |
| Xu, Chen, and Han (2025), *Statistical Inference for Low-Rank Tensor Models* | Confidence intervals for tensor linear functionals | [PDF](closest_papers/xu_chen_han_2025.pdf) |
| Cai and Low (2004), *An adaptation theory for nonparametric confidence intervals* | Honest coverage, expected length, and adaptation | [PDF](closest_papers/cai_low_2004_adaptation.pdf) |
| Cai and Low (2004), *Minimax estimation of linear functionals over nonconvex parameter spaces* | Nonlinear inference and limits of affine procedures | [PDF](closest_papers/cai_low_2004_nonconvex.pdf) |
| Agterberg and Zhang (2026; preprint 2024), *Statistical Inference for Low-Rank Tensors: Heteroskedasticity, Subgaussianity, and Applications* | Additive-noise Tucker tensor inference | [PDF](closest_papers/agterberg_zhang_2026.pdf) |
| Choo and d'Orsi (2021), *The Complexity of Sparse Tensor PCA* | Search-cost tradeoffs and low-degree likelihood bounds | [PDF](closest_papers/choo_dorsi_2021.pdf) |
| Fu and Sohn (2026), *Low-degree estimation thresholds in planted hypergraphs and tensor PCA* | Recent low-degree estimation thresholds | [PDF](closest_papers/fu_sohn_2026.pdf) |
| Michel and Nouy (2022), *Learning with tree tensor networks: complexity estimates and model selection* | Oracle/model-selection comparison for the original TT work | [PDF](closest_papers/michel_nouy_2022.pdf) |

## What is shared, and what remains different

### 1. Collier, Comminges, and Tsybakov: the mathematical starting point

They estimate scalar functionals of a Gaussian sequence under sparsity and $\ell_q$ constraints. Our diagonal observations have exactly that form:

$$
d_i=a_i+\tau g_i,\qquad
\psi(A)=p^{-1/2}\sum_i a_i,\qquad q=2/K.
$$

At rank one, the possible diagonal vectors form an $\ell_{2/K}$ ball. The diagonal-only minimax benchmark is therefore a specialization of established sequence theory. The current full-tensor rate also uses off-diagonal information and requires separate lower bounds. Inspect **Theorems 2–3 and Lemma 1**. [arXiv](https://arxiv.org/abs/1502.00665), [journal DOI](https://doi.org/10.1214/15-AOS1432).

### 2. Xu, Chen, and Han: the direct tensor-inference comparison

They infer linear functionals in low-Tucker-rank regression and tensor PCA through debiasing and tangent-space projection. Their scope includes more general loadings than ours. Inspect **Theorem 3.1** for regression signal and pilot conditions, and **Theorem 4.1** for PCA signal conditions. Our distinction is finite-sample coverage over a supplied rank-cap class, including zero and arbitrarily weak components, for a restricted loading and known norm/noise bounds. The project does not dominate their efficient regular-signal inference. [arXiv](https://arxiv.org/abs/2501.16223).

### 3. Cai and Low: honest confidence intervals

Their between-class modulus connects coverage over a larger parameter class to expected interval length on a smaller class. Inspect **Theorem 1** and the following adaptive constructions. This explains why uncertainty about additional weak components can obstruct adaptation. Our work evaluates geometry for a specific joint tensor rank-cap class; it does not establish a new general principle of interval adaptation. [arXiv](https://arxiv.org/abs/math/0503662), [journal DOI](https://doi.org/10.1214/009053604000000049).

### 4. Cai and Low: nonconvex functional estimation

Their Gaussian functional theory shows how nonlinear procedures can outperform affine ones over nonconvex parameter spaces. Inspect **Theorems 4–5** for finite convex unions and affine risk. Tensor rank-cap classes are also nonconvex, so nonlinear advantage by itself is not a new tensor discovery. The joint-rank versus single-unfolding comparison and evaluated full-data rates are our narrower questions. [arXiv](https://arxiv.org/abs/math/0406427), [journal DOI](https://doi.org/10.1214/009053604000000094).

### 5. Agterberg and Zhang: the additive-noise tensor model

They analyze HOOI-based inference for tensor singular vectors and entries under heteroskedastic sub-Gaussian noise. This shares our additive-noise setting but permits broader noise models. Their signal-strength conditions, including **Theorem 1** of the saved preprint, differ from coverage at arbitrarily weak signals. Our scalar target and known bounds also narrow the setting. The paper is now published in **The Annals of Statistics 54(3), 1178–1204 (2026)**; older project files retain its 2024 preprint label. [arXiv](https://arxiv.org/abs/2410.06381), [publication record](https://scholars.duke.edu/publication/1910297), [DOI](https://doi.org/10.1214/25-AOS2589).

### 6. Choo and d'Orsi: computation versus information

They study sparse tensor PCA recovery, algorithms interpolating between limited and exhaustive search, and low-degree likelihood bounds. Inspect **Theorem 26** for the single-spike argument. Their Hermite/overlap machinery is directly relevant to our computational analysis. Our target is a scalar contrast and an honest interval, rather than recovery of a sparse factor. A low-degree limitation alone does not rule out every polynomial-time confidence interval. [arXiv](https://arxiv.org/abs/2106.06308).

### 7. Fu and Sohn: the recent estimation comparison

They derive low-degree estimation thresholds for planted hypergraphs and tensor PCA. Inspect **Theorems 2.5–2.6** for sparse and general tensor PCA. Their estimation results are relevant to our scalar polynomial-estimator obstruction, but their latent-coordinate/product targets and priors must be compared explicitly with our contrast. Their theorems do not automatically establish hardness for honest intervals on our rank-cap class. [arXiv](https://arxiv.org/abs/2605.30113).

### 8. Michel and Nouy: the original compression branch

They analyze complexity-penalized learning with tree tensor networks, with risk bounds and fast-rate results. Inspect **Section 4**, including **Theorem 4.6** and the subsequent least-squares analysis. Our original setup studies sampled teacher responses and conditional KL after propagating TT-compressed weights through a frozen nonlinear model, with an explicitly qualified quotient dimension. Tensor-network oracle inequalities themselves are established prior work. [arXiv](https://arxiv.org/abs/2007.01165), [journal DOI](https://doi.org/10.3150/21-BEJ1371).

## Versions, verification, and organization

All eight PDFs were downloaded from version-pinned arXiv URLs. These are arXiv versions, including for papers subsequently published in journals. The Collier PDF is the 2015 preprint of the 2017 article; the Agterberg PDF is the 2024 preprint of the 2026 article. Cai and Low's adaptation article was published in 2004 and uploaded to arXiv in 2005. The theorem pointers above refer to the saved versions.

- [download_manifest.json](download_manifest.json): exact source/version, publication metadata, download timestamp, local path, page count, byte count, and SHA-256 checksum for every PDF.
- [references.bib](references.bib): eight bibliographic entries distinguishing publication years from saved preprint versions.
- [closest_papers/](closest_papers/): the eight PDFs, with descriptive filenames.

PDF signatures, parsability, page counts, and title matches on the opening pages were checked. Selected theorem statements and assumptions were inspected; this is not an independent proof audit. Older literature libraries remain in their original project-stage folders. This curated collection is the convenient entry point for the closest comparisons.

The current internal result ledger identifies the sharp full-data contrast rates as the project's main statistical advance. Efficient minimax intervals and actual-rank adaptation remain open. This selection does not establish novelty or priority.
