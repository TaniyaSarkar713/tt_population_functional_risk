"""Rebuild the separate reviewed manuscript and review report."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]
def run(args,cwd):
    subprocess.run(args,cwd=cwd,check=True)
run(["latexmk","-pdf","-interaction=nonstopmode","-halt-on-error","main.tex"],
    ROOT/"revised_paper")
run(["pandoc","report.md","-f","markdown+tex_math_single_backslash+tex_math_dollars",
     "--pdf-engine=xelatex","-V","geometry:margin=0.8in","-V","fontsize=10pt",
     "-V","colorlinks=true","--toc","-o","report.pdf"],ROOT)
run(["python","code/validate_artifacts.py"],ROOT)
