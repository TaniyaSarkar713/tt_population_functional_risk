#!/usr/bin/env bash
set -euo pipefail
study_dir="$(cd "$(dirname "$0")" && pwd)"
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export MPLCONFIGDIR=/tmp/tensor-empirical-mpl
export XDG_CACHE_HOME=/tmp/tensor-empirical-cache
python3 "$study_dir/code/run_all.py"
python3 "$study_dir/code/run_followups.py"
python3 "$study_dir/code/analyze_results.py"
python3 "$study_dir/code/plot_results.py"
python3 "$study_dir/code/build_report.py"
python3 "$study_dir/code/validate_artifacts.py"
