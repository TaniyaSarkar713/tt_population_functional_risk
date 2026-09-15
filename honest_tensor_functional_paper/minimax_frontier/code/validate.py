"""Recheck retained evidence, artifacts, local links and pre-stage preservation."""
import csv
import hashlib
import json
import re
from pathlib import Path
import numpy as np
import fitz
from run_experiments import summary
from numerics import coverage_events

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    nchecks=0
    def check(condition,detail):
        nonlocal nchecks;nchecks+=1
        if not condition:raise AssertionError(detail)
    sim=json.loads((ROOT/'results/simulation_results.json').read_text());cfg=json.loads((ROOT/'results/configurations.json').read_text())
    meta=json.loads((ROOT/'results/run_metadata.json').read_text())
    check(len(sim)==len(cfg)==160,'configuration count')
    check(sum(c['B'] for c in sim)==meta['unique_mc_datasets']==320000,'MC count')
    check(len({c['seed'] for c in cfg})==len(cfg),'unique configuration seeds')
    differences=[]
    for c,frozen in zip(sim,cfg):
        check(all(c[k]==v for k,v in frozen.items()),f"{c['id']} frozen configuration")
        path=ROOT/'results'/f"{c['id']}.npz"
        with np.load(path) as data:
            for key in data.files:check(np.isfinite(data[key]).all(),f'{path.name} finite {key}')
            truth=float(data['truth']);check(truth==c['truth'],'stored target')
            for name,prefix,estkey in [('method','','estimate'),('direct','direct_','direct_estimate')]:
                lo,hi=data[prefix+'lo'],data[prefix+'hi'];check(len(lo)==c['B'] and np.all(lo<=hi),'ordered endpoints')
                metrics=summary(lo,hi,truth,data.get(estkey))
                for k,v in metrics.items():check(np.isclose(v,c[name][k],rtol=1e-12,atol=1e-14),f"{c['id']} {name}.{k}")
                if metrics['rounding_changed']:differences.append((c['id'],name,metrics['rounding_changed']))
            if c['family']=='coordinate':
                check(int(np.sum(data['empty']))==c['empty_count'],'empty sentinel count')
                check(np.isclose(np.mean(data['correct_anchor']),c['correct_anchor_frequency']),'anchor frequency')
    # A bounded comparison cannot hide an actual five-step miss.
    target=1.;endpoint=target
    for _ in range(5):endpoint=np.nextafter(endpoint,-np.inf)
    check(not bool(coverage_events(np.array([0.]),np.array([endpoint]),target)[0]),'five-step miss remains a miss')
    check(differences==[('F037','method',2000),('F037','direct',1890)],'all rounding differences exposed')
    check(sim[-1]['signal']=='rank_two_violation' and sim[-1]['method']['coverage']==0,'negative control preserved')
    check(json.loads((ROOT/'audit/coverage_screen.json').read_text())['holm_rejections']==[],'coverage discrepancy screen')
    checks=json.loads((ROOT/'audit/theory_checks.json').read_text());check(checks['status']=='PASS' and checks['checks']==20489,'finite theorem checks')
    for file,count in [('analytic_profiles.json',120),('analytic_caps.json',265)]:check(len(json.loads((ROOT/'results'/file).read_text()))==count,file)
    with (ROOT/'audit/issue_registry.csv').open() as f:issues=list(csv.DictReader(f))
    check(len(issues)==19,'continued issue count')
    for id in ['T01','T02','T03','T04']:check(next(c for c in issues if c['id']==id)['status']=='PARTIALLY RESOLVED',id+' broad scope retained')
    baseline=json.loads((ROOT/'audit/baseline_hashes.json').read_text());changed=[];missing=[];absent_ignored=[]
    exclusions=set(json.loads((ROOT/'audit/distribution_exclusions.json').read_text())['paths'])
    check(exclusions<=set(baseline),'distribution exclusions belong to baseline')
    for relative,digest in baseline.items():
        file=REPO/relative
        if not file.exists():
            if relative in exclusions:absent_ignored.append(relative)
            else:missing.append(relative)
        elif sha(file)!=digest:changed.append(relative)
    check(not missing,'no previous files missing')
    check(set(changed)<= {'README.md','requirements.md','summary.md'},'only root status docs may change: '+str(changed))
    docs=[REPO/'README.md',REPO/'requirements.md',REPO/'summary.md',ROOT/'README.md',ROOT/'paper/report.md']
    for doc in docs:
        for target in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
            if '://' in target or target.startswith('#'):continue
            target=target.split('#')[0].split(' "')[0]
            # This file is written only after the validation has succeeded.
            if (doc.parent/target).resolve()==ROOT/'audit/validation.json':continue
            check((doc.parent/target).exists(),f'broken local link in {doc}: {target}')
    pdfs=[]
    for path in [ROOT/'paper/report.pdf',ROOT/'paper/technical_supplement.pdf']+sorted((ROOT/'figures').glob('*.pdf')):
        with fitz.open(path) as doc:
            check(len(doc)>0 and all(p.get_text().strip() for p in doc),'PDF text: '+path.name)
            text='\n'.join(p.get_text() for p in doc)
            check('\ufffd' not in text,'PDF replacement glyph: '+path.name)
            if path.parent.name=='paper':
                for page in doc:
                    check(all(r[0]>=25 and r[2]<=page.rect.width-20 and r[3]<=page.rect.height-15 for r in page.get_text('blocks')),'PDF content bounds: '+path.name)
            pdfs.append(dict(path=str(path.relative_to(ROOT)),pages=len(doc),sha256=sha(path)))
    check(len(pdfs)==6,'two reports and four PDF figures')
    for log in ['supplement_build.log','report_build.log']:
        text=(ROOT/'audit'/log).read_text()
        check(not any(s in text for s in ['Error producing PDF','Missing character:','Undefined control sequence']),'PDF build log: '+log)
    manifest={str(p.relative_to(ROOT)):sha(p) for p in sorted(ROOT.rglob('*')) if p.is_file()
              and '__pycache__' not in p.parts and p.suffix!='.pyc' and p.name not in ['.DS_Store','artifact_manifest.json','validation.json']}
    (ROOT/'audit/artifact_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    out=dict(status='PASS',checks=nchecks,baseline_files=len(baseline),unchanged_baseline=len(baseline)-len(changed)-len(absent_ignored),
             changed_baseline=sorted(changed),missing_baseline=missing,artifact_files=len(manifest),pdfs=pdfs,
             absent_ignored_local_files=absent_ignored,
             new_mc_datasets=320000,new_finite_theory_checks=checks['checks'],new_analytic_calculations=385,
             coverage_rounding_changes=differences,
             scope='No new real-data run. Previously saved scientific results preserved. Finite checks are not formal proof verification.')
    (ROOT/'audit/validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
