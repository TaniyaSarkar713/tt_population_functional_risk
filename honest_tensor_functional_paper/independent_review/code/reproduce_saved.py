"""Rebuild saved empirical outputs in an isolated temporary tree, preserving original inputs."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from inventory import ROOT,PROJECT,PACKAGE,dump

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    source=PACKAGE/'empirical_study';stages=[]
    with tempfile.TemporaryDirectory(prefix='tensor-review-repro-') as tmp:
        mirror=Path(tmp);study=mirror/'honest_tensor_functional_paper/empirical_study'
        shutil.copytree(source,study,ignore=shutil.ignore_patterns('__pycache__'))
        preserved=json.loads((source/'logs/preserved_stage_hashes.json').read_text())
        for name in preserved:
            target=mirror/name;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(PROJECT/name,target)
        env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',
            MPLCONFIGDIR=str(mirror/'mpl'),XDG_CACHE_HOME=str(mirror/'cache'))
        for script in ['analyze_results.py','plot_results.py','build_report.py','validate_artifacts.py']:
            t=time.perf_counter()
            with (ROOT/'logs'/('rebuild_'+script+'.log')).open('w') as log:
                result=subprocess.run([sys.executable,str(study/'code'/script)],env=env,stdout=log,stderr=subprocess.STDOUT)
            stages.append(dict(script=script,exit_code=result.returncode,seconds=time.perf_counter()-t))
            print(script,'exit',result.returncode,flush=True)
            if result.returncode:break
        comparisons=[]
        for p in sorted((source/'tables').glob('*')):
            if p.suffix in ['.csv','.json']:
                comparisons.append(dict(file=str(p.relative_to(source)),same_bytes=sha(p)==sha(study/p.relative_to(source))))
        for name in ['report.md','theory_comparison.md','manuscript/empirical_sections.md','figures/captions.md']:
            comparisons.append(dict(file=name,same_bytes=sha(source/name)==sha(study/name)))
        audit=dict(status='PASSED' if all(s['exit_code']==0 for s in stages) and all(c['same_bytes'] for c in comparisons) else 'FAILED',
            stages=stages,comparisons=comparisons,
            scope='New isolated rebuild of analysis, plots, reports and validation from saved observations. Does not rerun the million-draw study or exponential solver.',
            pdf_comparison='PDFs are rebuilt and validated; creation metadata prevents a byte-identity claim.')
        dump(ROOT/'results/reproduction.json',audit)
        if audit['status']!='PASSED':raise AssertionError(audit)
        print('Isolated saved-result reproduction passed.',flush=True)

if __name__=='__main__':main()
