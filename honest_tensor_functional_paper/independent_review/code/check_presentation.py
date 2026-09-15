"""Inspect active PDF/source structure and compile the integrated paper in a copy."""
import collections
import importlib.metadata
import json
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import fitz
from inventory import ROOT, PROJECT, PACKAGE, dump

def main():
    paths=json.loads((ROOT/'logs/active_sources.json').read_text())
    integrated=[PROJECT/p for p in paths if '/robust_adaptive_extension/paper/' in p]
    source='\n'.join(p.read_text() for p in integrated)
    labels=re.findall(r'\\label\{([^}]+)\}',source)
    refs=re.findall(r'\\(?:eqref|ref|autoref)\{([^}]+)\}',source)
    cites=set()
    for match in re.finditer(r'\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}',source):
        cites.update(x.strip() for x in match.group(1).split(','))
    bib=(PACKAGE/'robust_adaptive_extension/paper/references.bib').read_text()
    keys=set(re.findall(r'@\w+\s*\{\s*([^,]+),',bib))
    report=dict(active_source_count=len(paths), integrated_label_count=len(labels),
        duplicate_labels=[x for x,n in collections.Counter(labels).items() if n>1],
        missing_reference_labels=sorted(set(refs)-set(labels)),
        cited_keys=len(cites),missing_bib_keys=sorted(cites-keys),
        bibliography_scope='Key resolution only; not a full accuracy/priority audit.',pdfs=[],figures=[])
    pdfpaths=[PACKAGE/'robust_adaptive_extension/paper/main.pdf',PACKAGE/'certified_weak_signal/paper/main.pdf',
              PACKAGE/'high_dimensional_extension/paper/main.pdf',PACKAGE/'empirical_study/report.pdf',
              PACKAGE/'empirical_study/manuscript/empirical_sections.pdf']
    for p in pdfpaths:
        d=fitz.open(p);bad=[]
        for i,page in enumerate(d):
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    for span in line['spans']:
                        r=fitz.Rect(span['bbox'])
                        if r.x0<0 or r.y0<0 or r.x1>page.rect.width+1 or r.y1>page.rect.height+1:
                            bad.append(dict(page=i+1,text=span['text'],bbox=list(r)))
        report['pdfs'].append(dict(file=str(p.relative_to(PROJECT)),pages=len(d),outside_page_spans=bad,
                                  replacement_characters=sum(page.get_text().count('\ufffd') for page in d)))
    figs=[PACKAGE/'robust_adaptive_extension/paper/figures/theoretical_comparison.pdf',
          PACKAGE/'robust_adaptive_extension/paper/figures/weak_rank_coverage.pdf',
          PACKAGE/'robust_adaptive_extension/figures/adaptive_intervals.pdf',
          PACKAGE/'robust_adaptive_extension/figures/robustness_and_loadings.pdf']
    figs+=sorted((PACKAGE/'empirical_study/figures').glob('*.pdf'))
    for p in figs:
        d=fitz.open(p)
        report['figures'].append(dict(file=str(p.relative_to(PROJECT)),pages=len(d),
                                      embedded_raster_images=sum(len(page.get_images()) for page in d)))
    with tempfile.TemporaryDirectory(prefix='tensor-review-latex-') as tmp:
        mirror=__import__('pathlib').Path(tmp)/'robust_adaptive_extension'
        shutil.copytree(PACKAGE/'robust_adaptive_extension',mirror,ignore=shutil.ignore_patterns('__pycache__'))
        start=time.perf_counter()
        with (ROOT/'logs/integrated_latex_build.log').open('w') as log:
            r=subprocess.run(['latexmk','-g','-pdf','-interaction=nonstopmode','-halt-on-error','main.tex'],
                             cwd=mirror/'paper',stdout=log,stderr=subprocess.STDOUT)
        log=(ROOT/'logs/integrated_latex_build.log').read_text()
        report['isolated_latex_build']=dict(exit_code=r.returncode,seconds=time.perf_counter()-start,
            final_pages=len(fitz.open(mirror/'paper/main.pdf')) if r.returncode==0 else None,
            warning_lines=[line for line in log.splitlines() if any(x in line for x in ['Warning:','Overfull','Underfull'])])
    dump(ROOT/'results/presentation_checks.json',report)
    dump(ROOT/'logs/review_environment.json',dict(python=sys.version,executable=sys.executable,
        platform=platform.platform(),packages={p:importlib.metadata.version(p) for p in
        ['numpy','scipy','matplotlib','PyMuPDF','threadpoolctl']},
        pandoc=subprocess.run(['pandoc','--version'],capture_output=True,text=True).stdout.splitlines()[0]))
    print(json.dumps({k:v for k,v in report.items() if k not in ['pdfs','figures']},indent=2))
    assert not report['duplicate_labels'] and not report['missing_reference_labels'] and not report['missing_bib_keys']
    assert report['isolated_latex_build']['exit_code']==0

if __name__=='__main__':main()
