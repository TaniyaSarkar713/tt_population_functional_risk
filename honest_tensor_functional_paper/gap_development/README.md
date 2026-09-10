# Further development of the remaining theory gaps

The earlier reviewed manuscript is preserved. This directory contains the subsequent results.

**Resolved:** the cubic logarithmic factor, full-data worst-case expected length, and the corresponding squared-error minimax rate, under fixed order/caps, equal diagonal loading, and M=tau sqrt(p).

**Computational progress:** a proved truncated-scan search/precision tradeoff; a complete level-one/two implementation; a self-contained low-degree polynomial estimation obstruction; and an interval-to-detection reduction.

**Still open:** a polynomial-time minimax confidence interval or an unconditional lower bound ruling one out.

## Deliverables

- [Progress report PDF](progress_report.pdf) and [editable report](progress_report.md).
- [Updated full manuscript](paper/main.pdf).
- [New theorem statements](paper/gap_section.tex) and [complete proofs](paper/gap_proofs.tex).
- [Detailed derivations and scope limits](theory/proved_results.md).
- [Literature update](literature/update.md).
- [Final mathematical audit](theory/final_audit.md).
- [Document validation](results/validation.json) and [deliverable hashes](deliverable_manifest.json).
- [Initial candidate ledger](theory/candidate_results.md), retained as research history.
- [Theoretical checks](results/theory_checks.json).
- [Prototype results](results/scan_benchmark.csv) and [metadata](results/scan_benchmark.json).
- [Baseline manuscript hashes](baseline_manifest.json).

## Reproduce

Run from this gap_development directory:

    python code/check_theory.py
    OPENBLAS_NUM_THREADS=1 python code/benchmark_scan.py
    python code/rebuild.py
    python code/validate.py

Python dependencies: NumPy, SciPy and pypdf. Building needs latexmk, BibTeX, pdflatex and Pandoc/XeLaTeX. Seeds are fixed and are identifiers, not execution dates.

The scan prototype implements complete levels one and two; it does not silently approximate higher complete levels. The exact minimax confidence-set projection is an existence construction, not the prototype.

PROVED means a complete supplied derivation with finite checks. It does not mean independent peer review, machine-checked mathematics, or certified novelty.
