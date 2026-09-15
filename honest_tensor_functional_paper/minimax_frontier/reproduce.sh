#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
export MPLCONFIGDIR=/private/tmp/tensor_frontier_mpl
export XDG_CACHE_HOME=/private/tmp/tensor_frontier_cache
export PYTHONPYCACHEPREFIX=/private/tmp/tensor_frontier_pycache
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
python3 code/check_theory.py > audit/theory_checks.log 2>&1
if [[ "${1:-}" == "--rerun-mc" ]]; then
    python3 code/run_experiments.py > audit/simulation.log 2>&1
elif [[ -n "${1:-}" ]]; then
    echo "Usage: reproduce.sh [--rerun-mc]" >&2
    exit 2
fi
python3 code/reanalyze.py > audit/reanalysis.log 2>&1
python3 code/plot_results.py
python3 code/build_report.py
pandoc theory/results.md --standalone --pdf-engine=xelatex -o paper/technical_supplement.pdf > audit/supplement_build.log 2>&1
(cd paper && pandoc report.md --standalone --lua-filter=../code/figure_pages.lua --pdf-engine=xelatex -o report.pdf) > audit/report_build.log 2>&1
python3 code/pdf_audit.py
python3 code/validate.py
