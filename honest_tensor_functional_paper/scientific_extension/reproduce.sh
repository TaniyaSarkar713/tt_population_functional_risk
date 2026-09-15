#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
export MPLCONFIGDIR=/private/tmp/tensor_science_mpl
export XDG_CACHE_HOME=/private/tmp/tensor_science_cache
export PYTHONPYCACHEPREFIX=/private/tmp/tensor_science_pycache
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
python3 code/check_theory.py > audit/theory_checks.log 2>&1
python3 code/run_experiments.py > audit/simulation.log 2>&1
python3 code/run_followups.py > audit/followups.log 2>&1
python3 code/run_minor.py > audit/minor.log 2>&1
python3 code/analyze_eeg.py > audit/eeg_analysis.log 2>&1
python3 code/runtime_study.py > audit/runtime.log 2>&1
python3 code/plot_results.py
python3 code/build_report.py
pandoc theory/results.md --standalone --pdf-engine=xelatex -o paper/technical_supplement.pdf
(cd paper && pandoc report.md --standalone --lua-filter=../code/figure_pages.lua --pdf-engine=xelatex -o report.pdf)
python3 code/validate.py
