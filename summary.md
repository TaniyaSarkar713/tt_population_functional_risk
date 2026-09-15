# Project summary

This is a **mathematical statistics project about using tensor structure to learn important quantities more accurately**.

The folder contains two connected research directions:

| Direction | Main question |
|---|---|
| Original tensor-compression project | How accurately can a small tensor-based model reproduce a larger model's behavior? |
| Newer tensor-inference project | How precisely can we estimate a particular quantity from a noisy tensor, with a trustworthy confidence interval? |

Here is the mathematical story, starting from the basics.

A **tensor** is an array with several indices. A vector has one index, a matrix has two, and a three-way tensor has three:

$$
A=(A_{ijk})\in\mathbb R^{p\times p\times p}.
$$

For example, its axes could represent location, time, and measurement type. There are $p^3$ entries, so even moderate $p$ can create a large object.

**Low rank means that these entries have a simpler underlying structure.** The simplest example is

$$
A_{ijk}=u_i v_j w_k.
$$

This is a rank-one tensor. Instead of storing $p^3$ numbers, we store three vectors containing $3p$ numbers.

A tensor train, or **TT**, permits a richer structure by connecting several small arrays, called cores. For three indices,

$$
A_{ijk}=\sum_{a=1}^{r_1}\sum_{b=1}^{r_2}
G_1(i,a)\,G_2(a,j,b)\,G_3(b,k).
$$

The internal sizes $r_1,r_2$ are the TT ranks. Larger ranks allow more complicated tensors but require more parameters.

For $p=10$ and $r_1=r_2=2$, this representation stores

$$
10(2)+2(10)(2)+2(10)=80
$$

numbers, compared with $10^3=1{,}000$ entries in the full tensor.

Tucker decomposition is another structured representation. Both Tucker and TT models impose low matrix ranks when the tensor is rearranged into matrices, though they constrain different rearrangements.

The original project applies this idea to **compressing a model while preserving its behavior**.

Suppose a large teacher model produces response probabilities $q_0(y\mid x)$, and a compressed student produces $p_W(y\mid x)$. Here $x$ is an input, $y$ is a response, and $W$ contains the student's parameters.

The project measures their discrepancy using

$$
D(W)=\mathbb E_X \left[
\sum_y q_0(y\mid X)
\log\frac{q_0(y\mid X)}{p_W(y\mid X)}
\right].
$$

The inner expression is **KL divergence**: it is nonnegative and becomes zero when the two response distributions agree. The expectation averages over the inputs encountered in deployment. This is why the project calls it *population functional risk*: it measures behavior across the input population.

For a candidate TT model $\lambda$, the central tradeoff is schematically

$$
\boxed{
\text{prediction error}
\;\lesssim\;
\underbrace{\text{best error possible within model }\lambda}_{\text{approximation error}}
+
\underbrace{\frac{d_\lambda}{n}}_{\text{estimation error}}.
}
$$

Here:

- $n$ is the number of independent sampled teacher responses.
- $d_\lambda$ is the number of independent model parameters.
- $\lesssim$ means "bounded above up to a constant."

A small rank makes the student easier to learn, but may limit how well it can represent the teacher. A larger rank improves representational capacity, but requires more data.

The paper's full bound includes additional model-selection, geometry, and optimization terms. Under its assumptions, the proposed selection procedure balances these costs almost as well as knowing the best candidate in advance.

There is a subtlety in counting $d_\lambda$: different cores can represent the same tensor. Even in the rank-one example, replacing $u$ by $2u$ and $v$ by $v/2$ leaves $A$ unchanged. These redundancies must be removed. For the 80-parameter TT example above, the exact-rank tensor family has dimension

$$
d=80-2^2-2^2=72.
$$

Turning that tensor dimension into a statistical difficulty also requires that its directions actually affect the model's output probabilities. The original theory explicitly makes that assumption. Its $d/n$ lower bounds concern **sampled teacher responses**; access to exact probabilities or teacher weights changes the problem. See the [original project overview](README.md).

The newer project asks a related question about **uncertainty in a scalar quantity computed from a tensor**.

Its observation model is

$$
\boxed{Z=A+\tau G.}
$$

Here $A$ is the unknown tensor, $Z$ is the observed tensor, and each entry of $G$ is an independent standard normal random variable. The known number $\tau$ controls the noise.

If we average $n$ independent noisy measurements, each with noise standard deviation $\sigma$, then $\tau=\sigma/\sqrt n$.

The target is a **functional**, meaning a rule that turns the entire tensor into one number. The main example is the normalized diagonal sum

$$
\psi(A)=\frac{1}{\sqrt p}\sum_{i=1}^{p}A_{i,\ldots,i}.
$$

This resembles a diagonal average; the normalization $1/\sqrt p$ is chosen to make the noise calculation convenient.

Simply applying the same rule to $Z$ gives

$$
\widehat\psi_{\mathrm{direct}}=\psi(A)+\tau\xi,
\qquad \xi\sim N(0,1).
$$

Consequently, a standard 95% confidence interval is

$$
\widehat\psi_{\mathrm{direct}}\pm1.96\tau.
$$

Its total length is approximately $3.92\tau$.

**Can known tensor structure make this interval shorter?** That is the newer project's central question.

The required confidence interval must be *honest*. Mathematically,

$$
\inf_{A\in\Theta}
\Pr_A\{\psi(A)\in C(Z)\}
\ge 1-\alpha,
$$

where $\Theta$ is the class of tensors satisfying the supplied rank and size bounds.

For 95% confidence, this means the procedure covers the true quantity in at least 95% of repeated experiments **for every tensor allowed by those bounds**. That includes zero tensors, tensors with smaller actual ranks, and tensors with arbitrarily weak components.

This is stronger than working well only when every component is easy to detect. The method knows upper bounds on rank; it does not need to recover the actual rank first.

The key mathematical insight is that **low tensor rank constrains how large many diagonal entries can be simultaneously**.

Consider a rank-one three-way tensor $A=u\otimes v\otimes w$, and write $a_i=A_{iii}$. If its total size satisfies

$$
\|A\|_F = \sqrt{\sum_{ijk}A_{ijk}^{2}}
\le M,
$$

then Hölder's inequality gives

$$
\sum_i |a_i|^{2/3} = \sum_i |u_i v_i w_i|^{2/3}
\le
\bigl(\|u\|_2\|v\|_2\|w\|_2\bigr)^{2/3}
\le M^{2/3}.
$$

This inequality prevents too many diagonal entries from being large. For a $K$-way tensor, the corresponding exponent is $2/K$. Higher rank caps introduce an additional rank-dependent factor.

The practical interval exploits this constraint using **soft thresholding**:

- Small observed diagonal entries are set to zero.
- Larger entries are moved toward zero by a fixed threshold.
- The resulting estimate receives an error bound that accounts for both noise and the bias introduced by shrinking.

For the rank-one three-way example, set

$$
\lambda=\tau\sqrt{2\log(2p/\alpha)}.
$$

With probability at least $1-\alpha$, every diagonal noise entry is at most $\lambda$ in absolute value. Combining that event with the structural inequality gives a valid interval radius

$$
h=\frac{M^{2/3}(2\lambda)^{1/3}}{\sqrt p}.
$$

The implementation compares this radius with the direct Gaussian radius and a radius supplied by the known parameter bounds. It chooses the smallest using only known quantities, which preserves coverage.

The latest development goes further by using **off-diagonal observations too**. Low rank links those observations to the diagonal, so they provide additional information about the target.

Its conceptual construction is to retain every allowed tensor consistent with the observed noise, then report the smallest and largest target values among those possibilities:

$$
C(Z)= \left[
\min_{B\text{ consistent with the data}}\psi(B),
\quad
\max_{B\text{ consistent with the data}}\psi(B)
\right].
$$

The latest manuscript supplies matching upper and lower bounds on the best possible interval length. In the particular regime of fixed tensor order, fixed rank caps, equal dimensions, and $M=\tau\sqrt p$, the optimal worst-case expected length scales as

$$
\boxed{
\begin{cases}
\tau(\log p)^{3/2}/\sqrt p,&K=3,\\
\tau\sqrt{\log p/p},&K\ge4.
\end{cases}
}
$$

"Optimal" here means both that a valid procedure attains this order and that every uniformly valid procedure must incur at least this order in the worst case. Both rates eventually become smaller than the direct interval's order-$\tau$ length.

**Computing an interval with that optimal rate efficiently remains open.** The preserved 2026-09-11 stage implements a global optimizer for the complete continuous rank-one class when each tensor dimension is two. It reports optimization gaps and safe outer confidence bounds, but its cost is exponential. The project also establishes limitations for polynomial estimators of bounded degree, a specific algorithm class; these do not establish impossibility for every efficient algorithm.

The projection interval remains trustworthy even when signals are arbitrarily weak, provided the supplied rank caps are valid. It becomes conservative when the data cannot resolve the retained subspaces. The existing ideal interval already matches the best rate across smaller positive fixed-rank cap classes, without needing to estimate the actual rank.

The 2026-09-12 work makes the growing-rank distinction precise. Once the smallest supplied rank cap reaches order $\sqrt p$, simple structural/direct intervals are minimax at every norm budget. Honesty over those larger classes prevents simultaneous adaptation to the much shorter fixed-rank oracle intervals. At sufficiently strong tensors that fill their supplied Tucker caps, a polynomial projection method does attain the optimal pointwise rate; its required signal strength is conservative. Sharp rates beyond small budgets are also now proved for fixed polynomially decaying loading weights and certain nonorthogonal perturbations. The [preserved 2026-09-12 progress report](honest_tensor_functional_paper/high_dimensional_extension/progress_report.md) gives the precise regimes, 9,100 new trials, and remaining problems.

The original experiments were synthetic. They check coverage, interval lengths, weak components, and failures under incorrect noise assumptions. For example, at $p=8192$, order three, and rank cap one, the implemented selected interval has length about $0.962\tau$, compared with $3.920\tau$ for the direct interval. Its observed coverage is conservative. These experiments concern the implemented interval, while the sharp full-data construction remains a theoretical result with unresolved computational efficiency. A later 122-subject EEG analysis is described below; no LLM application has been established. [Simulation findings](honest_tensor_functional_paper/simulations/results/findings.md).

The **2026-09-13 simulation study** adds 1,084,640 Monte Carlo data sets, paired comparisons with a published regular-signal tensor method, confidence-level and noise/rank sensitivity, intermediate-cap diagnostics, and full numerical records. Its [report](honest_tensor_functional_paper/empirical_study/report.pdf) keeps analytic bounds separate from implemented procedures. The large-cap sample-size rate is supported by the observed RMSE slope. The pointwise dimension slopes have finite-grid discrepancies, so they are not presented as exact confirmation of limiting exponents.

The new experiments also expose practical limits. The conservative pointwise interval can be much wider than regular-signal or oracle intervals. Replacing an empty interval intersection by `{0}` can give its midpoint enormous squared error at a large nonzero signal; the pointwise theorem guarantees coverage and expected length, not this midpoint's risk. At 95% confidence, 94 of 240 binary solver cases still miss endpoint tolerance at 3,000 nodes, with outer bounds and gaps retained. The study preserves an unusually low Gaussian-coverage realization and reports its independent confirmation separately. Those preserved experiments predate the scalar-risk repair, executed EEG analysis, and new results described below. Current open boundaries are recorded in [requirements.md](requirements.md).


The **latest work, dated 2026-09-15**, advances three of those mathematical boundaries. First, if just one rearrangement of the tensor is rank constrained, a singular-value calculation on the known loading now gives an efficient minimax interval for every loading, rank cap and norm budget. This uses the full noisy tensor. Additional rank constraints can make the problem statistically easier, so the theorem does not settle the original simultaneous-cap optimizer.

Second, in tensors of order four or higher, the exact rate is now known for every orthogonal loading profile, including the previously unresolved critical decay. A new rank-one mixture makes many coordinate scales jointly difficult to distinguish from zero. Its lower bound matches the earlier upper bound. The general interval attaining that upper bound remains an ideal optimizer, so knowing the rate and computing a rate-optimal interval are still different achievements.

Third, a rank-one interval now learns its own anchor location. At a signal concentrated in one entry, estimating a coordinate that differs in d indices can have interval length proportional to tau^d / |a|^(d-1) for d at least two. Nearby coordinates with d equal to zero or one retain the ordinary noise scale. This hierarchy has matching lower bounds and an executable method under a sufficient signal-strength condition; coverage remains valid even at weak rank-one signals. Other signal geometries and higher ranks remain open.

The [new report](honest_tensor_functional_paper/minimax_frontier/paper/report.pdf) and [full proofs](honest_tensor_functional_paper/minimax_frontier/paper/technical_supplement.pdf) accompany **320,000 newly generated data sets and 20,489 finite checks**. The spectral method has modest length gains on its tested grid. The rank-one coordinate method fails under a deliberate rank-two violation, which is retained in the report. These results do not close the complete research program.

The preserved **2026-09-14 EEG application** analyzed 122 subjects, treating subjects rather than repeated trials as inferential units. Its mean contrast was 2.222 microvolts, but the primary finite-sample interval was [-77.920, 82.364] and the bias-calibrated tensor interval was [-200, 200]. This defensible bounded-target analysis showed no certified precision gain and did not validate the original Gaussian low-rank model. It was not rerun for the latest theory stage. See the [application report](honest_tensor_functional_paper/scientific_extension/paper/report.pdf).
