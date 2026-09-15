"""Evaluate corrected event/scalar definitions on every preserved saved draw."""
import hashlib
import json
import sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'empirical/code'))
import common
from numerics import coverage_events,scalar_companion,companion_risk_upper

def eligibility(c):
    if c.get('true_rank',1)==0:return 'OUTSIDE_REGULAR_CLASS: zero signal'
    if 'true_rank' in c and c['rank']!=c['true_rank']:return 'OUTSIDE_SPECIFIED_RANK: rank mismatch'
    if c.get('regime')=='P1':return 'STRONG_SIGNAL_DIAGNOSTIC: initialization/alignment/remainder constants not certified'
    return 'REGULARITY_NOT_CERTIFIED: signal, initialization, alignment and remainder conditions required'

def main():
    source=ROOT.parent/'empirical_study';changes=[];risks=[];checks=[]
    cases=common.load_cases()+json.loads((source/'configs/followup_cases.json').read_text())['cases']
    for c in cases:
        if not c['B']:continue
        path=source/'results'/f"{c['id']}.npz";d=np.load(path)
        if 'endpoints' not in d:continue
        meta=json.loads(path.with_suffix('.json').read_text());ep=d['endpoints'];est=d['estimates'].copy();old=est.copy();target=float(d['target'])
        names=[str(n).replace('split_no_bias','split_unprotected') for n in d['methods']]
        extra=meta['extra'].copy();scope={str(r['method']).replace('split_no_bias','split_unprotected'):r['guarantee'] for r in meta['records']}
        prior=(ep[...,0]<=target+1e-11*max(1.,abs(target)))&(target<=ep[...,1]+1e-11*max(1.,abs(target)))
        corrected=coverage_events(ep,target);strict=coverage_events(ep,target,0)
        for j,n in enumerate(names):
            for ai,a in enumerate(d['alpha']):
                if np.any(prior[:,j,ai]!=corrected[:,j,ai]):
                    changes.append(dict(case=c['id'],method=n,alpha=float(a),old_count=int(prior[:,j,ai].sum()),
                        corrected_count=int(corrected[:,j,ai].sum()),trials=np.flatnonzero(prior[:,j,ai]!=corrected[:,j,ai]).tolist()))
        # Exact power-of-two rescaling preserves normal-range floating-point events.
        for scale in [2.**-100,2.**100]:
            assert np.array_equal(corrected,coverage_events(ep*scale,target*scale)),c['id']
        if 'pointwise' in names:
            j=names.index('pointwise');h=extra['M']*np.sqrt(c['rank']/c['p']);tau=extra['tau']
            est[:,j]=scalar_companion(ep[:,j,1],est[:,names.index('direct')],h,tau)
            risks.append(dict(case=c['id'],repetitions=c['B'],target=target,
                midpoint_mse=float(np.mean((old[:,j]-target)**2)),companion_mse=float(np.mean((est[:,j]-target)**2)),
                midpoint_mse_se=common.mean_se((old[:,j]-target)**2)[1],companion_mse_se=common.mean_se((est[:,j]-target)**2)[1],
                sentinel_count=int(np.sum(np.all(ep[:,j,1]==0,axis=-1))),risk_upper=companion_risk_upper(h,tau),
                estimator_id='interval_companion',estimator_alpha=.05))
            extra['pointwise_estimator']='Risk-controlled scalar companion using 95% interval; R1. Legacy midpoint retained separately.'
        rows=common.save_intervals(c,names,ep,est,target,d['seconds'],scope,extra)
        newpath=common.ROOT/'results'/path.name
        np.savez_compressed(newpath,endpoints=ep,estimates=est,legacy_estimates=old,seconds=d['seconds'],
            target=target,alpha=d['alpha'],methods=np.asarray(names),coverage_strict=strict,coverage_evaluated=corrected)
        newmeta=json.loads(newpath.with_suffix('.json').read_text())
        for r in newmeta['records']:
            j=names.index(r['method']);ai=list(d['alpha']).index(r['alpha'])
            r['strict_covered']=int(strict[:,j,ai].sum())
            r['rounding_only_count']=int(np.sum(corrected[:,j,ai]&~strict[:,j,ai]))
            if r['method'].startswith('xch_'):r['assumption_applicability']=eligibility(c)
            else:r['assumption_applicability']=r['guarantee']
            if r['method']=='pointwise':
                r['legacy_midpoint_mse']=float(np.mean((old[:,j]-target)**2))
                r['legacy_midpoint_estimator_alpha']=.05
        newmeta['revision_provenance']=dict(operation='Deterministic reevaluation of all saved observations; no new noise draws',
            original_npz_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),coverage_policy='four endpoint ULPs',scalar_change='R1 companion only')
        common.write_json(newpath.with_suffix('.json'),newmeta)
        assert np.array_equal(np.load(newpath)['endpoints'],ep)
        checks.append(c['id'])
    common.write_json(ROOT/'results/saved_corrections.json',dict(cases=len(checks),changed_coverage_rows=changes,
        scalar_risk_comparison=risks,power_of_two_scale_checks=2*len(checks),
        scope='All applicable saved raw observations reevaluated, original sources preserved. Unaffected interval endpoints bitwise unchanged.'))
    print('Reevaluated',len(checks),'saved interval cases; changed coverage rows:',changes,flush=True)

if __name__=='__main__':main()
