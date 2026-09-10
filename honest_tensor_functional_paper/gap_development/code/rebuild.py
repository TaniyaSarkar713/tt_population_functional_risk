"""Build both deliverables, then check their structural integrity.

Run from any working directory. This does not rerun the simulations or
alter the preserved earlier manuscript.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    paper = ROOT / "paper"
    with (paper / "build_stdout.log").open("w") as log:
        subprocess.run(
            ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
            cwd=paper, stdout=log, stderr=subprocess.STDOUT, check=True,
        )
    subprocess.run(
        ["pandoc", "progress_report.md", "-o", "progress_report.pdf",
         "-f", "markdown+tex_math_single_backslash+tex_math_dollars",
         "--pdf-engine=xelatex", "-V", "geometry:margin=0.85in",
         "-V", "fontsize=10pt", "-V", "colorlinks=true"],
        cwd=ROOT, check=True,
    )
    subprocess.run([sys.executable, str(ROOT / "code/validate.py")], check=True)


if __name__ == "__main__":
    main()
