# Theory review of the drafted main.pdf

Review date: September 9, 2026.

**Verdict: B — RIGOROUS BUT CAN BE STRENGTHENED.** The original intended theorems survive after a confidence-domain correction. Original Q2 is false for K=3. The reviewed version proves a matching full-data expected-length-at-zero rate for fixed K>=4 and improves the cubic bracket to a logarithmic gap. Full-data worst-case optimality and efficient scan computation remain open.

## Start here

- [Theory review PDF](report.pdf), eight pages; [editable report](report.md).
- [Reviewed manuscript PDF](revised_paper/main.pdf), 31 pages, including 22 complete numbered-result proofs.
- [Revision changelog](revision_changelog.md).
- [Preserved original manuscript](input_snapshot/main.pdf) and [input hashes](input_manifest.json).

## Mathematical deliverables

- [Framework and identifiability](framework.md).
- [Input theorem inventory](theorem_inventory.md), with CSV/JSON versions.
- [Final numbered-result inventory](final_result_inventory.csv).
- [Assumption audit and relaxation matrix](assumption_audit.md), 26 entries, with CSV/JSON.
- [Dependency table](dependency_audit.md) and [Mermaid graph](dependency_graph.md).
- [Complete original proofs with roadmaps](revised_paper/appendix.tex).
- [New full-data theorem statements](revised_paper/full_data_section.tex) and [complete proofs](revised_paper/full_data_proofs.tex).
- [Supporting propositions and proofs](revised_paper/refinements.tex).
- [Detailed derivations S1–S6](strengthened_results.md) and [S7–S8](new_full_data_results.md).
- [Counterexamples](counterexamples.md).
- [Final theorem audit, strengthening matrix and ranked open problems](strengthening_matrix.md).
- [External theorem/source verification](external_results_audit.md).
- [All 89 requested review checks](instruction_coverage.md).
- [Secondary pre-submission audit](pre_submission_audit.md).
- [Revised result ledger](revised_paper/status.tex).

## Reproduce

Run from this theory_review directory:

    python code/check_audit.py
    python code/validate_artifacts.py
    python code/rebuild.py

The mathematical checks require Python, NumPy and SciPy. Artifact validation also requires pypdf. Rebuilding requires latexmk/pdflatex/BibTeX and Pandoc/XeLaTeX. Existing environment versions are recorded in results/environment.json.

The seed is 20260910. [Numerical outputs](results/audit_checks.json) are finite checks, not proof substitutes. Rebuild uses the original saved simulation figures and tables; it does not run or benchmark the exponential scan.

No original manuscript or simulation file was modified. The revised theory supersedes the old open-question ledger only within this separate reviewed revision. PROVED denotes a complete supplied derivation; it does not mean independent peer review, formal proof verification or certified priority.
