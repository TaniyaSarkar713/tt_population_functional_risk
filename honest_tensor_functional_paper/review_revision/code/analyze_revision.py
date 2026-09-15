"""Independently summarize every new draw; retain raw generator outputs."""
import csv,json,sys
from pathlib import Path
import numpy as np
from scipy.stats import norm
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'empirical/code'))
from numerics import coverage_events
from common import mean_se,wilson

def dump(name,rows):
    (ROOT/'tables'/f'{name}.json').write_text(json.dumps(rows,indent=2,default=lambda x:x.item())+'\n')
    if rows:
        keys=list(dict.fromkeys(k for r in rows for k in r))
        with (ROOT/'tables'/f'{name}.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)

def main():
    config=json.loads((ROOT/'configs/revision_cases.json').read_text());rows=[];solves=[];cal=[];risks=[];checks=0
    for c in config['cases']:
        meta=json.loads((ROOT/'results'/f"{c['id']}.json").read_text());d=np.load(ROOT/'results'/f"{c['id']}.npz")
        ep=d['endpoints'];est=d['estimates'];target=float(d['target']);levels=d['alpha'];names=list(d['methods']);B=c['B']
        assert len(ep)==B and np.isfinite(ep).all() and np.all(ep[...,0]<=ep[...,1]);checks+=3
        # Pure fallback ablation, evaluated on the same saved pilot candidate:
        # force tangent choice, retaining BOTH calibrated intersections.
        if c['suite'] in ['V01','V05']:
            candidate=ep[:,names.index('tangent_without_fallback')].copy()
            center=est[:,names.index('direct')];h=meta['extra']['M_fixed']*np.sqrt(c['rank']/c['p'])
            radius=norm.isf(levels/4)
            candidate[...,0]=np.maximum(np.maximum(candidate[...,0],center[:,None]-radius),-h)
            candidate[...,1]=np.minimum(np.minimum(candidate[...,1],center[:,None]+radius),h)
            candidate[candidate[...,0]>candidate[...,1]]=0
            ep=np.concatenate([ep,candidate[:,None]],axis=1);est=np.column_stack([est,candidate[:,1].mean(axis=1)])
            names.append('no_fallback_only')
        hit=coverage_events(ep,target);strict=coverage_events(ep,target,0)
        for scale in [2.**-100,2.**100]:
            assert np.array_equal(hit,coverage_events(ep*scale,target*scale));checks+=1
        # Keep this derivation separate from immutable simulation output.
        np.savez_compressed(ROOT/'results'/f"evaluated_{c['id']}.npz",endpoints=ep,estimates=est,target=target,
                            alpha=levels,methods=np.array(names),coverage=hit,coverage_strict=strict)
        for j,name in enumerate(names):
            err=est[:,j]-target;loss=err**2
            for ai,a in enumerate(levels):
                width=np.diff(ep[:,j,ai],axis=-1).ravel();k=int(hit[:,j,ai].sum())
                r=dict(case=c['id'],suite=c['suite'],method=name,alpha=float(a),repetitions=B,target=target,
                    covered=k,coverage=k/B,coverage_wilson_95=wilson(k,B),coverage_mcse=float(np.sqrt(k/B*(1-k/B)/B)),
                    strict_covered=int(strict[:,j,ai].sum()),rounding_only_count=int(np.sum(hit[:,j,ai]&~strict[:,j,ai])),
                    length=mean_se(width)[0],length_se=mean_se(width)[1],mse=mean_se(loss)[0],mse_se=mean_se(loss)[1],
                    bias=mean_se(err)[0],bias_se=mean_se(err)[1],estimator_id=name+'_scalar',estimator_alpha=None,
                    guarantee='NO_GENERAL_COVERAGE_THEOREM',assumption_applicability='DIAGNOSTIC',coverage_policy='four endpoint ULPs')
                for key,value in c.items():
                    if key not in ['id','B','suite']:r[key]=value
                if name in ['cap_fixed','cap_matched']:
                    r.update(estimator_id='interval_companion',estimator_alpha=.05,guarantee='FINITE_SAMPLE_CAP_HONEST',assumption_applicability='SATISFIED')
                elif name in ['direct','oracle','known_sigma']:
                    r.update(guarantee='FINITE_SAMPLE_GAUSSIAN',assumption_applicability='SATISFIED' if name!='oracle' else 'ORACLE_INFORMATION')
                elif name.startswith('xch'):
                    r.update(guarantee='REGULAR_STRATUM_ASYMPTOTIC',assumption_applicability=meta['extra']['comparator_applicability'])
                elif name.startswith('global'):
                    r.update(estimator_id=name+'_midpoint',estimator_alpha=.05,guarantee='FINITE_MODEL_OUTER_PROJECTION',assumption_applicability='MODEL_SATISFIED; FLOAT64_BOUNDS_NOT_FORMAL')
                elif name=='bounded_row_median':
                    r.update(estimator_alpha=.05,guarantee='FINITE_SAMPLE_ROW_BOUND',assumption_applicability='SATISFIED' if meta['extra']['conditions_satisfied'] else 'VIOLATED: actual corruption exceeds supplied cap')
                elif name=='independent_upper_sigma':
                    r.update(estimator_alpha=.05,guarantee='FINITE_SAMPLE_ALPHA0_PLUS_DELTA',assumption_applicability='SATISFIED')
                elif name=='naive_gaussian':
                    r.update(guarantee='GAUSSIAN_ISOTROPIC_UNCORRUPTED_ONLY',assumption_applicability='SATISFIED' if c['law']=='gaussian' and c['actual_c']==0 else 'OUTSIDE_GUARANTEE')
                else:r.update(estimator_id=name+'_95pct_midpoint',estimator_alpha=.05)
                if c['suite']=='V03' and c['law']=='t3':
                    r['mse_se_sample_diagnostic']=r['mse_se'];r['mse_se']=None
                    r['mse_uncertainty_note']='Fourth-moment based MSE error bars not asserted for this heavy-tail experiment; raw sample diagnostic retained.'
                for refname,prefix in [(names[0],'paired_direct'),('cap_fixed','paired_full')]:
                    if refname not in names:continue
                    ref=names.index(refname)
                    for key,value in [('length',width-np.diff(ep[:,ref,ai],axis=-1).ravel()),('coverage',hit[:,j,ai].astype(float)-hit[:,ref,ai])]:
                        r[prefix+'_'+key],r[prefix+'_'+key+'_se']=mean_se(value)
                if c['suite'] in ['V01','V05']:
                    r['length_over_pointwise_rate']=r['length']/meta['extra']['pointwise_rate']
                    r['P1_sufficient_conditions']=c['amplitude']>=meta['extra']['P1_sufficient_bound']
                prior=[x for x in meta['records'] if x['method']==name and x['alpha']==a]
                if prior:
                    for key in ['coverage','length','length_se','mse','bias']:
                        assert np.isclose(r[key],prior[0][key],rtol=1e-12,atol=1e-12),(c['id'],name,key);checks+=1
                rows.append(r)
        if 'calibration_events' in d:
            k=int(d['calibration_events'].sum());cal.append(dict(**c,event_covered=k,event_wilson_95=wilson(k,B),**meta['extra']))
        if c['suite']=='V02':
            for s in meta['extra']['solver_records']:solves.append(dict(case=c['id'],amplitude=c['amplitude'],**s))
        if 'legacy_midpoints' in d:
            for j,name in enumerate(['cap_fixed','cap_matched']):
                oldloss=(d['legacy_midpoints'][:,j]-target)**2;newloss=(est[:,names.index(name)]-target)**2
                risks.append(dict(case=c['id'],suite=c['suite'],p=c['p'],rank=c['rank'],method=name,amplitude=c['amplitude'],
                    midpoint_mse=mean_se(oldloss)[0],midpoint_mse_se=mean_se(oldloss)[1],companion_mse=mean_se(newloss)[0],companion_mse_se=mean_se(newloss)[1],
                    paired_mse_change=mean_se(newloss-oldloss)[0],paired_mse_change_se=mean_se(newloss-oldloss)[1],
                    sentinel_count=int(np.all(ep[:,names.index(name),1]==0,axis=1).sum()),bound_applicable=True))
    agg=[]
    for case in sorted({s['case'] for s in solves}):
        for budget in [100,600,3000]:
            v=[s for s in solves if s['case']==case and s['budget']==budget];finite=[s['endpoint_gap'] for s in v if s['endpoint_gap'] is not None and np.isfinite(s['endpoint_gap'])]
            k=sum(s['certified_to_tolerance'] for s in v)
            agg.append(dict(case=case,amplitude=v[0]['amplitude'],budget=budget,solves=len(v),certified=k,certificate_fraction=k/len(v),certificate_wilson=wilson(k,len(v)),
                missing_finite_gap=len(v)-len(finite),mean_gap=mean_se(finite)[0],gap_se=mean_se(finite)[1],mean_seconds=mean_se([s['seconds'] for s in v])[0]))
    old=json.loads((ROOT/'results/saved_corrections.json').read_text())['scalar_risk_comparison']
    for r in old:
        meta=json.loads((ROOT/'empirical/results'/f"{r['case']}.json").read_text());c=meta['case'];ex=meta['extra']
        r['bound_applicable']=c.get('true_rank',c.get('rank',1))<=c.get('rank',1) and abs(r['target'])<=ex['M']*np.sqrt(c['rank']/c['p'])*(1+1e-14)
    dump('revision_summary',rows);dump('solver_trials',solves);dump('solver_summary',agg);dump('calibration',cal);dump('scalar_risk_new',risks);dump('scalar_risk_saved',old)
    summary=dict(status='PASS',cases=len(config['cases']),datasets=sum(c['B'] for c in config['cases']),summary_rows=len(rows),solver_calls=len(solves),checks=checks,
        pure_fallback_ablation='Exact postprocessing of every saved tangent candidate; same observations, pilot and intersections, no extra draws')
    (ROOT/'logs/new_analysis.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary)

if __name__=='__main__':main()
