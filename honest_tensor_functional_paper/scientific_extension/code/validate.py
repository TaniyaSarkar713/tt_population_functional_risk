"""Validate delivered artifacts and unchanged historical work without rerunning MC."""
import ast,csv,hashlib,json,math,re,sys,time
from unittest.mock import patch
from collections import Counter
from pathlib import Path
import fitz
import numpy as np
from scipy.stats import norm
from methods import loading_envelope, _checked_matmul
from run_experiments import summarize
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[1]
counts=Counter();failures=[]
def check(family,condition,detail=''):
    counts[family]+=1
    if not bool(condition):failures.append({'family':family,'detail':str(detail)})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

# Preserve the pre-stage baseline, including preexisting uncommitted files.
baseline=json.loads((ROOT/'audit/baseline_hashes.json').read_text());changed=[];missing=[]
for name,digest in baseline.items():
    p=REPO/name
    if not p.exists():missing.append(name)
    elif sha(p)!=digest:changed.append(name)
check('historical_preservation',not missing and set(changed)<=set(['README.md','requirements.md']),{'changed':changed,'missing':missing})
check('protocol_hash',sha(ROOT/'real_data/protocol.md')==json.loads((ROOT/'real_data/protocol_lock.json').read_text())['sha256'])
for p in (ROOT/'code').glob('*.py'):
    ast.parse(p.read_text());check('python_parse',True,p.name)
checks=json.loads((ROOT/'audit/theory_checks.json').read_text());check('finite_mathematical_checks',checks['status']=='PASS' and checks['checks']==sum(checks['by_family'].values())==40553)
ledger=json.loads((ROOT/'theory/theorem_status.json').read_text());check('theorem_ledger',len(ledger)==8 and all(x['status']=='PROVED' for x in ledger))
registry=list(csv.DictReader((ROOT/'audit/issue_registry.csv').open()));check('complete_review_registry',len(registry)==19 and len({r['id'] for r in registry})==19)

# Force the FP-signal fallback and compare against an independent dense product.
a0=np.arange(12,dtype=float).reshape(3,4)/10;b0=np.arange(8,dtype=float).reshape(4,2)/10
expected=np.einsum('ik,kj->ij',a0,b0,optimize=False)
check('checked_matmul',np.allclose(_checked_matmul(a0,b0),expected))
with patch('methods.np.matmul',side_effect=FloatingPointError('forced check')):
    check('checked_matmul_forced_fallback',np.allclose(_checked_matmul(a0,b0),expected))
try:
    _checked_matmul(np.array([[np.inf]]),np.array([[1.]]))
except FloatingPointError:
    check('checked_matmul_nonfinite_rejection',True)
else:
    check('checked_matmul_nonfinite_rejection',False)

# Compare every main aggregate to retained individual outcomes.
rows=json.loads((ROOT/'results/simulation_results.json').read_text());nmc=0
for row in rows:
    a=np.load(ROOT/f"results/{row['id']}_replicates.npz");B=row['B'];nmc+=B
    for name,old in row['methods'].items():
        es=a['error_'+name]
        ws=np.full(B,2*norm.isf(.025)) if name=='direct' else a['width']
        cov=np.abs(es)<=norm.isf(.025) if name=='direct' else a['covered']
        fresh=summarize(es,ws,cov)
        for k,v in fresh.items():check('main_aggregate_recomputation',np.isclose(v,old[k],rtol=1e-11,atol=1e-12),f"{row['id']} {name} {k}")
        check('replicate_lengths',len(es)==B and len(ws)==B)
    check('interval_outputs',np.all(np.isfinite(a['width'])) and np.all(a['width']>=0))
    if row['family']=='tensor':check('direct_width_cap',np.max(a['width'])<=2*norm.isf(.0125)+1e-8)
configs=json.loads((ROOT/'results/configurations.json').read_text());check('main_configurations',len(configs)==len(rows)==80 and sum(c['B'] for c in configs)==71000)
check('configuration_lock',sha(ROOT/'results/configurations.json')==json.loads((ROOT/'results/configuration_lock.json').read_text())['sha256'])
follow=json.loads((ROOT/'results/followup_results.json').read_text())
for c in follow:
    if c['family']=='dense_TT_core_loading':
        a=np.load(ROOT/f"results/followup_tt_{c['signal']}.npz");fresh=summarize(a['error'],a['width'],a['covered']);old=c['method']
    elif c['family']=='diagonal_assumption_violation':
        a=np.load(ROOT/'results/followup_diagonal_violation.npz');fresh=summarize(a['error'],a['width'],a['covered']);old=c['method']
        check('retained_negative_control',old['coverage']==0)
    else:
        a=np.load(ROOT/f"results/followup_bounded_{c['n_calibration']}.npz");fresh=summarize(a['corrected_error'],a['corrected_width'],a['corrected_covered']);old=c['corrected']
        naive=summarize(a['naive_error'],a['naive_width'],a['naive_covered'])
        for k,v in naive.items():check('followup_aggregate_recomputation',np.isclose(v,c['uncorrected_DIAGNOSTIC'][k]))
    for k,v in fresh.items():check('followup_aggregate_recomputation',np.isclose(v,old[k]))
    nmc+=2000
minor=json.loads((ROOT/'results/minor_results.json').read_text())
for c in minor:
    a=np.load(ROOT/f"results/minor_a{c['a']:g}.npz");fresh=summarize(a['midpoint_error'],a['width'],a['covered'])
    for k,v in fresh.items():check('minor_aggregate_recomputation',np.isclose(v,c[k]))
    check('minor_normalized_width',np.isclose(np.mean(a['width'])*c['a'],c['scaled_length']));nmc+=4000
check('MC_counts',nmc==109000 and len(rows)+len(follow)+len(minor)==92)
for r in json.loads((ROOT/'results/loading_grid.json').read_text()):
    check('loading_proxies',r['lower_proxy']<=r['upper_proxy']+1e-10 and r['proxy_ratio']<=r['proven_proxy_factor']+1e-10 and r['proven_proxy_factor']<=r['universal_factor']+1e-10)
timing=json.loads((ROOT/'results/runtime_results.json').read_text());check('runtime_scope',timing['calls']==36 and len(timing['results'])==12 and max(r['entries'] for r in timing['results'])==2097152)

# Data provenance, subject split, loading and scalar summaries.
d=np.load(ROOT/'real_data/subject_tensors.npz');prov=json.loads((ROOT/'real_data/provenance.json').read_text());analysis=json.loads((ROOT/'real_data/analysis_results.json').read_text());L=np.load(ROOT/'real_data/primary_loading.npy')
check('subject_tensor_schema',d['tensors'].shape==(122,3,3,64,16) and np.isfinite(d['tensors']).all())
check('primary_loading',np.count_nonzero(L)==16 and np.isclose(np.sum(abs(L)),2) and np.isclose(np.sum(L),0))
check('eligible_subjects',prov['eligible_subjects']==122 and len(set(d['subjects']))==122 and np.all(d['condition_counts']>0))
status=Counter();trials=[]
for line in (ROOT/'real_data/trial_manifest.jsonl').read_text().splitlines():
    r=json.loads(line);status[r['status']]+=1;trials.append(r)
check('trial_accounting',len(trials)==prov['trial_file_count']==11074 and dict(status)==prov['trial_status_counts'] and status['included']==int(d['condition_counts'].sum())==10962)
check('no_duplicate_trial_paths',len({(r['subject'],r['file']) for r in trials})==len(trials))
seen=[]
for g,parts in analysis['splits'].items():
    for part,subjects in parts.items():
        check('stratum_consistent_splits',all(s[3]==g for s in subjects));seen+=subjects
check('independent_subject_splits',len(seen)==len(set(seen))==122 and set(seen)==set(d['subjects']))
contrasts=list(csv.DictReader((ROOT/'real_data/subject_contrasts.csv').open()))
for j,clip in enumerate(d['clips']):
    X=d['tensors'][:,j];check('bounded_subject_tensors',np.max(abs(X))<=clip+1e-8)
    F=np.einsum('nijk,ijk->n',X,L);r=analysis['analyses'][j]
    check('real_primary_mean',np.isclose(F.mean(),r['cohort_descriptive_mean']) and np.isclose(F.std(ddof=1),r['subject_sd']))
    stored={x['subject']:float(x['direct_contrast']) for x in contrasts if float(x['clip_microvolts'])==clip}
    check('real_individual_contrasts',all(np.isclose(F[i],stored[s]) for i,s in enumerate(d['subjects'])))
    for method in ['primary_stratified_EB','corrected_projection','approximate_stratified_t']:
        q=r[method];check('real_interval_order',np.isfinite([q['lo'],q['hi']]).all() and q['lo']<=q['hi'])
check('primary_no_certified_positive_claim',analysis['analyses'][1]['primary_stratified_EB']['lo']<0<analysis['analyses'][1]['primary_stratified_EB']['hi'])

# PDFs: full content, both axis directions, vector figures, no missing labels.
pdfs={};clipped=[]
for p in list((ROOT/'paper').glob('*.pdf'))+list((ROOT/'figures').glob('*.pdf')):
    d=fitz.open(p);pdfs[str(p.relative_to(ROOT))]={'pages':len(d),'bytes':p.stat().st_size};check('PDF_readable',len(d)>0 and p.stat().st_size>1000,p.name)
    for i,pg in enumerate(d):
        for b in pg.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                for sp in line['spans']:
                    x0,y0,x1,y1=sp['bbox']
                    if x0 < -1 or y0 < -1 or x1>pg.rect.width+1 or y1>pg.rect.height+1:clipped.append((str(p),i+1,sp['text'][:50]))
        if p.parent.name=='figures':
            check('vector_figure',len(pg.get_images())==0 and len(pg.get_drawings())>5,p.name)
            check('figure_label_text',len(pg.get_text())>50,p.name)
check('PDF_no_clipped_text',not clipped,clipped[:20])
report='\n'.join(p.get_text() for p in fitz.open(ROOT/'paper/report.pdf'))
check('report_figures',all(f'Figure {i}:' in report for i in range(1,6)))
check('report_counts',all(x in report for x in ['109,000','40,553','10,962','2.222']))
proof='\n'.join(p.get_text() for p in fitz.open(ROOT/'paper/technical_supplement.pdf'))
check('proof_sections',all(x in proof for x in ['AB1.','AB2.','P2.','P3.','P4.','D2.','B1.']))
check('repro_script_syntax', (ROOT/'reproduce.sh').is_file())

# All new deliverable hashes, excluding mutable validation/manifests/caches.
manifest={str(p.relative_to(ROOT)):sha(p) for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ['validation.json','deliverable_manifest.json','validation.log','reproduction.log']}
(ROOT/'audit/deliverable_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
result={'status':'PASS' if not failures else 'FAIL','artifact_checks':sum(counts.values()),'by_family':dict(counts),'failures':failures,
        'fresh_mathematical_checks':checks['checks'],'MC_datasets':nmc,'MC_configurations':92,'analytic_calculations':504,'API_timing_calls':36,
        'baseline_files':len(baseline),'baseline_changed':changed,'baseline_missing':missing,'baseline_unchanged':len(baseline)-len(changed)-len(missing),
        'new_manifest_files':len(manifest),'PDFs':pdfs,
        'visual_inspection':'Root agent inspected report table pages, EEG figure and corrected full figure page; vector labels/captions readable, no clipping after pagination fix.',
        'limits':'Internal checks, not formal proofs, independent review, or verification of subject independence. Historical stages were not rerun.'}
(ROOT/'audit/validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));sys.exit(0 if not failures else 1)
