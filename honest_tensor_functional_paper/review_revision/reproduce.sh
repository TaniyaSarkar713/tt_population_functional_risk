#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export MPLCONFIGDIR=/private/tmp/tensor_revision_mpl
export XDG_CACHE_HOME=/private/tmp/tensor_revision_cache
if [[ "${1:-}" == "--rerun-new" ]]; then
  for suite in V01 V02 V03 V04 V05; do
    python3 code/run_revision.py --suite "$suite" > "logs/execute_${suite}.log" 2>&1
  done
  python3 code/check_methods.py > logs/check_methods_stdout.log 2>&1
elif [[ -n "${1:-}" ]]; then
  echo 'Usage: bash reproduce.sh [--rerun-new]' >&2
  exit 2
fi
python3 code/recompute_saved.py
python3 empirical/code/analyze_results.py
python3 code/analyze_revision.py
python3 empirical/code/plot_results.py > logs/replot_saved.log 2>&1
python3 code/plot_revision.py > logs/plot_revision.log 2>&1
python3 code/prepare_theory.py
python3 code/build_reports.py
python3 code/finalize_records.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -cd paper/technical_supplement.tex > logs/technical_build.log 2>&1
latexmk -pdf -interaction=nonstopmode -halt-on-error -cd paper/main.tex > logs/main_build.log 2>&1
for report in empirical_report response_to_review revision_summary second_review; do
  pandoc "${report}.md" --resource-path=. -V geometry:margin=0.8in -V fontsize=10pt -V colorlinks=true --pdf-engine=xelatex -o "${report}.pdf" > "logs/${report}_pdf.log" 2>&1
 done
python3 code/validate_revision.py
