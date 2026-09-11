# Norm-budget and loading extensions

**Research update: 2026-09-11.** This stage works on two remaining requirements of the latest tensor-inference paper: the restriction on the norm/noise scaling and the dependence on the prescribed loading. The earlier `gap_development/` stage is preserved.

## Results

- **Resolved within fixed order/caps:** matching full-data confidence-interval length and squared-error rates for every positive norm budget $M$ and noise level $\tau$, for the equal diagonal contrast.
- **Resolved for flat orthogonal loadings:** sharp rates depend on the number $m$ of prescribed orthogonal loading terms, even under dense mode rotations and larger unequal ambient dimensions.
- **Partial for nonuniform orthogonal loadings:** explicit loading-dependent full-data upper and lower bounds; no claim that they always match.
- **Still open:** efficient minimax intervals, unconditional hardness for all efficient intervals, sharp growing-cap dependence, sharp arbitrary-loading geometry, and actual-rank adaptation beyond the supplied-cap guarantees.

Let $\ell_p=\log(ep)$ and $x=M/(\tau\sqrt{\ell_p})$. The new rate is

$$
\mathfrak r_K(p,M,\tau)=\frac{\tau\sqrt{\ell_p}}{\sqrt p}
\begin{cases}
\min\{x,1+\log_+x,\ell_p\},&K=3,\\
\min(x,1),&K\ge4.
\end{cases}
$$

Both minimax expected-length criteria have this order, and minimax squared risk has its square. Constants depend on the fixed order, rank caps, and confidence level, not on $p,M,\tau$. For flat orthogonal loadings replace $p$ by $m$.

## Deliverables and organization

- [Full updated manuscript](paper/main.pdf), [main source](paper/main.tex), [new statements](paper/norm_loading_section.tex), and [complete new proofs](paper/norm_loading_proofs.tex).
- [Progress report](progress_report.md) and [PDF](progress_report.pdf).
- [Proof audit](theory/proof_audit.md) and [remaining requirements](theory/remaining_requirements.md).
- [Literature positioning](literature/update.md).
- [Finite-check code](code/check_theory.py), [check summary](results/theory_checks.json), and detailed grids in `results/`.
- [Rebuild script](code/rebuild.py), [artifact validator](code/validate.py), and [validation record](results/validation.json).
- [Preserved baseline hashes](baseline_manifest.json) and [new deliverable hashes](deliverable_manifest.json).

The new manuscript copies the previous stage's sources and two historical figures, then adds the new section and proof appendix and updates the narrative. Original simulations and their numerical values are reused. The new checks are algebraic and numerical sanity checks, not simulation of the ideal residual optimizer.

## Reproduce

From this directory:

```bash
python3 code/check_theory.py
python3 code/rebuild.py
python3 code/validate.py
```

Dependencies are Python, NumPy, SciPy, pypdf, `latexmk`/pdfLaTeX/BibTeX, and Pandoc/XeLaTeX. No new package installation is required in the recorded environment. The checks use seed 20260911.

“Proved” means a complete supplied derivation with recorded finite checks. It does not mean independent peer review, formal verification, or certified novelty.
