# Open questions and claims excluded from the draft

**PARTIAL: unrestricted full-data minimax length.** With fixed caps and M=tau sqrt(p), the proved bracket at zero is

$$c_\alpha\tau\sqrt{\log p/p}\ \lesssim\ \inf_{C\text{ honest}}E_0|C|\ \le\ C_{K,\alpha,J}\tau(\log p/p)^{(K-2)/(2K)}.$$

The upper/lower ratio is of polynomial order (p/log p)^(1/K). The interval uses only diagonal contractions; off-diagonal measurements may close this gap. Both global minimax length and simultaneous subclass adaptation remain unresolved.

**CONJECTURED: lower-scale attainability at zero for rank one.** The coordinate mixture may determine the hardest zero-neighborhood alternative. A test exploiting off-diagonal information might attain its scale. Evidence: large diagonal sums force concentration of rank-one factors; diffuse signal alternatives have smaller target changes. This heuristic does not rule out more difficult multiscale mixtures. No claim of proof or a constructive algorithm is made.

**PARTIAL: sharp rank dependence.** J grows as a product of supplied caps and can be loose. Better diagonal inequalities or a loading-dependent effective budget may improve the bound. Replacing J by actual unknown rank without a uniformly valid upper certificate is not justified.

**PARTIAL: general loadings.** A prescribed orthogonal CP loading is treated. Arbitrary L may have ill-conditioned decompositions, correlated contraction noise, and different lower bounds. Do not extrapolate the present rate.

**PARTIAL: random-design regression.** Mean-tensor denoising is exactly sufficient for replicated Gaussian tensor observations, but not automatically for tensor regression. Establishing uniform scalar remainders and comparable lower bounds would be a further theorem.

**PARTIAL: automatic M and noise calibration.** Known M and tau are restrictive. Independent upper bounds can be combined with coverage allocation, but the effect on expected length must be worked out. A routine plug-in should not be advertised as a new robustness theory.

**Rejected claims.** First rank-agnostic inference; first Tucker/TT cone; first 2/K tensor quasi-norm; full-data minimax-optimal threshold interval; adaptation to actual rank; universal domination of manifold projection; information loss caused by reshaping data; arbitrary CP-rank extension; an LLM-specific theorem.

**Resolved restricted benchmark.** D1 now matches the rate when all procedures observe only the diagonal. This is classified D (substantially solved by classical sequence theory), and is included for comparison rather than as an open or novel rate. The remaining task must exploit or bound the value of the off-diagonal observations.
