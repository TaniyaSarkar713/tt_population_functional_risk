"""Build the updated manuscript and report, then validate artifacts."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    with (ROOT / 'paper/build_stdout.log').open('w') as output:
        subprocess.run(['latexmk', '-pdf', '-interaction=nonstopmode', '-halt-on-error', 'main.tex'],
                       cwd=ROOT / 'paper', stdout=output, stderr=subprocess.STDOUT, check=True)
    with (ROOT / 'results/report_build.log').open('w') as output:
        subprocess.run(['pandoc', 'progress_report.md', '-o', 'progress_report.pdf',
                        '-f', 'markdown+tex_math_single_backslash+tex_math_dollars',
                        '--pdf-engine=xelatex', '-V', 'geometry:margin=0.85in',
                        '-V', 'fontsize=10pt', '-V', 'colorlinks=true'],
                       cwd=ROOT, stdout=output, stderr=subprocess.STDOUT, check=True)
    subprocess.run([sys.executable, str(ROOT / 'code/validate.py')], check=True)


if __name__ == '__main__':
    main()
