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
A_{ijk}
=
\sum_{a=1}^{r_1}\sum_{b=1}^{r_2}
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
D(W)
=
\mathbb E_X\!\left[
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
\widehat\psi_{\mathrm{direct}}
=
\psi(A)+\tau\xi,
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
\|A\|_F
=
\sqrt{\sum_{ijk}A_{ijk}^{2}}
\le M,
$$

then Hölder's inequality gives

$$
\sum_i |a_i|^{2/3}
=
\sum_i |u_i v_i w_i|^{2/3}
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
C(Z)=
\left[
\min_{B\text{ consistent with the data}}\psi(B),
\quad
\max_{B\text{ consistent with the data}}\psi(B)
\right].
$$

The latest manuscript supplies matching upper and lower bounds on the best possible interval length. In the particular regime of fixed tensor order, fixed rank caps, equal dimensions, and $M=\tau\sqrt p$, the optimal worst-case expected length scales as

$$
\boxed{
\begin{cases}
\tau(\log p)^{3/2}/\sqrt p,&K=3,\\[2mm]
\tau\sqrt{\log p/p},&K\ge4.
\end{cases}
}
$$

"Optimal" here means both that a valid procedure attains this order and that every uniformly valid procedure must incur at least this order in the worst case. Both rates eventually become smaller than the direct interval's order-$\tau$ length.

**Computing an interval with that optimal rate efficiently remains open.** The project implements limited scans and proves a computation-versus-precision tradeoff. It also establishes limitations for polynomial estimators of bounded degree, a specific algorithm class. These results do not establish impossibility for every efficient algorithm. The [latest progress report](honest_tensor_functional_paper/gap_development/progress_report.md) records these distinctions and supersedes several older open-question statements.

The existing experiments are synthetic. They check coverage, interval lengths, weak components, and failures under incorrect noise assumptions. For example, at $p=8192$, order three, and rank cap one, the implemented selected interval has length about $0.962\tau$, compared with $3.920\tau$ for the direct interval. Its observed coverage is conservative. These experiments concern the implemented interval, while the sharp full-data construction remains a theoretical result with unresolved computational efficiency. No real-data or LLM application has yet been established. [Simulation findings](honest_tensor_functional_paper/simulations/results/findings.md).
