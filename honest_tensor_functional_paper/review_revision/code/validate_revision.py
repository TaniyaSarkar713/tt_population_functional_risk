"""Final raw-data, source, theorem, document and preservation validation."""
import hashlib,json,re,sys
from pathlib import Path
import numpy as np
import fitz
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[1]
sys.path.insert(0,str(ROOT/'empirical/code'))
from numerics import coverage_events,scalar_companion
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    checks=[]
    def check(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    baseline=json.loads((ROOT/'logs/baseline_hashes.json').read_text());changes=[]
    for rel,digest in baseline.items():
        p=REPO/rel
        if not p.exists() or sha(p)!=digest:changes.append(rel)
    check('preserved_preexisting_files',set(changes)<= {'README.md','requirements.md'},dict(total=len(baseline),unchanged=len(baseline)-len(changes),changed=changes))
    config=json.loads((ROOT/'configs/revision_cases.json').read_text());check('registered_55_cases',len(config['cases'])==55)
    check('new_independent_dataset_count',sum(c['B'] for c in config['cases'])==87200)
    deps=['code/run_revision.py','empirical/code/common.py','empirical/code/tensor_methods.py','empirical/code/numerics.py','configs/revision_cases.json']
    non_generation_changes=[]
    for suite in ['V01','V02','V03','V04','V05']:
        run=json.loads((ROOT/'logs'/f'run_{suite}.json').read_text());cs=[c for c in config['cases'] if c['suite']==suite]
        check(suite+'_completed',run['status']=='COMPLETED' and run['datasets']==sum(c['B'] for c in cs))
        for rel in deps:check(suite+'_generation_source_'+rel,run['source_hashes'][rel]==sha(ROOT/rel))
        for rel,digest in run['source_hashes'].items():
            if rel not in deps and (not (ROOT/rel).exists() or sha(ROOT/rel)!=digest):non_generation_changes.append(dict(suite=suite,file=rel,role='Post-generation plot/report/theory tooling; not imported by the simulation runner'))
    summaries=json.loads((ROOT/'tables/revision_summary.json').read_text())
    for c in config['cases']:
        d=np.load(ROOT/'results'/f"evaluated_{c['id']}.npz");ep=d['endpoints'];target=float(d['target']);hit=coverage_events(ep,target)
        check(c['id']+'_all_draws',len(ep)==c['B'])
        check(c['id']+'_finite_ordered',np.isfinite(ep).all() and np.all(ep[...,0]<=ep[...,1]))
        check(c['id']+'_coverage_saved',np.array_equal(hit,d['coverage']))
        for r in [x for x in summaries if x['case']==c['id']]:
            j=list(d['methods']).index(r['method']);ai=list(d['alpha']).index(r['alpha']);width=np.diff(ep[:,j,ai],axis=-1).ravel()
            check(c['id']+'_'+r['method']+f'_{ai}_coverage',int(hit[:,j,ai].sum())==r['covered'])
            check(c['id']+'_'+r['method']+f'_{ai}_width',np.isclose(width.mean(),r['length'],rtol=1e-12,atol=1e-12))
            check(c['id']+'_'+r['method']+f'_{ai}_risk',np.isclose(np.mean((d['estimates'][:,j]-target)**2),r['mse'],rtol=1e-12,atol=1e-12))
            check(c['id']+'_'+r['method']+f'_{ai}_identity',bool(r['estimator_id']) and 'estimator_alpha' in r and bool(r['assumption_applicability']))
        if c['suite'] in ['V01','V05']:
            raw=np.load(ROOT/'results'/f"{c['id']}.npz");j=list(d['methods']).index('cap_fixed');check(c['id']+'_full_endpoints_unchanged',np.array_equal(ep[:,j],raw['endpoints'][:,j]))
            meta=json.loads((ROOT/'results'/f"{c['id']}.json").read_text());check(c['id']+'_all_pilot_geometry_equivalence',meta['extra']['geometry_equivalence_checks']==c['B'])
            for name,key in [('cap_fixed','M_fixed'),('cap_matched','M_matched')]:
                j=list(d['methods']).index(name);h=meta['extra'][key]*np.sqrt(c['rank']/c['p']);direct=d['estimates'][:,0]
                check(c['id']+'_'+name+'_companion',np.array_equal(scalar_companion(ep[:,j,1],direct,h,1.),d['estimates'][:,j]))
    corrections=json.loads((ROOT/'results/saved_corrections.json').read_text())
    check('303_saved_interval_cases',corrections['cases']==303)
    check('two_corrected_rows_one_observation',len(corrections['changed_coverage_rows'])==2 and all(r['case']=='S03_007' and r['old_count']==134 and r['corrected_count']==133 and r['trials']==[41] for r in corrections['changed_coverage_rows']))
    check('606_saved_scale_checks',corrections['power_of_two_scale_checks']==606)
    n=0
    for p in sorted((ROOT/'empirical/results').glob('S*.npz')):
        d=np.load(p)
        if 'endpoints' not in d:continue
        orig=ROOT.parent/'empirical_study/results'/p.name;o=np.load(orig);n+=1
        check(p.stem+'_original_endpoints_unchanged',np.array_equal(d['endpoints'],o['endpoints']))
        check(p.stem+'_original_estimates_preserved',np.array_equal(d['legacy_estimates'],o['estimates']))
        check(p.stem+'_recomputed_coverage',np.array_equal(d['coverage_evaluated'],coverage_events(d['endpoints'],float(d['target']))))
        meta=json.loads(p.with_suffix('.json').read_text());check(p.stem+'_original_provenance',meta['revision_provenance']['original_npz_sha256']==sha(orig))
    check('saved_interval_files_count',n==303)
    risk=next(x for x in json.loads((ROOT/'tables/scalar_risk_saved.json').read_text()) if x['case']=='S03_002')
    check('R1_exposed_case_fixed',risk['bound_applicable'] and risk['midpoint_mse']>1e7 and .14<risk['companion_mse']<.16 and risk['sentinel_count']==1)
    solves=json.loads((ROOT/'tables/solver_trials.json').read_text());check('600_solver_calls_retained',len(solves)==600)
    check('all_failures_and_gaps_retained',sum(s['certified_to_tolerance'] for s in solves)==7 and all(s['endpoint_gap'] is not None for s in solves))
    loads=[json.loads((ROOT/'results'/f'V02_{i:03d}.json').read_text())['extra'] for i in range(4)]
    check('solver_loading_and_direction_fixed',all(x['loading']==loads[0]['loading'] and x['direction']==loads[0]['direction'] for x in loads))
    for name in ['method_checks','new_analysis']:
        check(name+'_pass',json.loads((ROOT/'logs'/f'{name}.json').read_text())['status']=='PASS')
    statuses=json.loads((ROOT/'theory/theorem_status.json').read_text());check('60_proved_results',len(statuses)==60 and all(x['status']=='PROVED' for x in statuses))
    tex='\n'.join(p.read_text() for p in (ROOT/'paper').glob('*.tex'));aux=(ROOT/'paper/technical_supplement.aux').read_text()
    for r in statuses:
        label=r['label'];expected='sup:'+label if re.fullmatch(r'[A-Z]\d+',label) else label
        check('proof_result_'+label,(r'\newlabel{'+expected+'}') in aux)
    registry=json.loads((ROOT/'tables/issue_registry.json').read_text());check('all_19_issues_responded',len(registry)==19 and all(r['action_taken'] and r['remaining_issue'] for r in registry))
    check('P0_P1_resolved',all(r['status']=='RESOLVED' for r in registry if r['severity'] in ['P0','P1']))
    check('four_general_theory_problems_open',all(next(r for r in registry if r['id']==id)['status']=='NOT RESOLVED' for id in ['T01','T02','T03','T04']))
    cross=(ROOT/'guideline_coverage.md').read_text();check('40_revision_instructions',len(re.findall(r'^\| \d+ \|',cross,re.M))==40)
    for name in ['main','technical_supplement']:
        log=(ROOT/'paper'/f'{name}.log').read_text();check(name+'_clean_latex',not any(s in log for s in ['undefined references','undefined on input line','! LaTeX Error','Fatal error']))
    for name in ['empirical_report.md','response_to_review.md']:
        check(name+'_table_syntax','|\n\n|' not in (ROOT/name).read_text())
    pdfs=[];outside=[]
    for rel in ['paper/main.pdf','paper/technical_supplement.pdf','empirical_report.pdf','response_to_review.pdf','revision_summary.pdf','second_review.pdf']:
        p=ROOT/rel;check(rel+'_exists',p.exists())
        if not p.exists():continue
        doc=fitz.open(p);texts=[]
        for i,page in enumerate(doc):
            texts.append(page.get_text())
            for word in page.get_text('words'):
                if word[0]<-1 or word[1]<-1 or word[2]>page.rect.width+1 or word[3]>page.rect.height+1:outside.append(dict(file=rel,page=i+1,text=word[4]))
        check(rel+'_readable',all(len(t)>30 for t in texts));pdfs.append(dict(file=rel,pages=len(doc),sha256=sha(p)))
    check('no_text_clipped_at_page_boundaries',not outside,outside[:10])
    for folder,count in [(ROOT/'figures',6),(ROOT/'empirical/figures',10)]:
        captions=json.loads((folder/'captions.json').read_text());check(str(folder.relative_to(ROOT))+'_figure_count',len(captions)==count)
        for name in captions:
            check(name+'_vector_and_preview',all((folder/f'{name}.{e}').exists() for e in ['pdf','svg','png']))
    result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',checks=len(checks),failures=[c for c in checks if not c['passed']],
        baseline=dict(files=len(baseline),unchanged=len(baseline)-len(changes),changed=changes),new_datasets=87200,new_summary_rows=len(summaries),
        pdfs=pdfs,non_generation_tooling_changes=non_generation_changes,scope='New validations of current artifacts. Prior 59-result mathematical review retained; no formal proof or interval arithmetic claim.',details=checks)
    (ROOT/'logs/final_validation.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k not in ['details','non_generation_tooling_changes','pdfs']})
    if result['status']!='PASS':raise SystemExit(1)

if __name__=='__main__':main()
