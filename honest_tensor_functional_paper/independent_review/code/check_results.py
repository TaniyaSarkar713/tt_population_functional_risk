"""Independently recompute saved scalar losses and interval summaries, without writes to the study."""
import collections
import json
from pathlib import Path
import numpy as np
from scipy.stats import norm,binom
from inventory import ROOT,PACKAGE,dump

def main():
    study=PACKAGE/'empirical_study'
    rows=json.loads((study/'tables/summary.json').read_text())
    grouped=collections.defaultdict(list)
    for r in rows:grouped[r['case']].append(r)
    checks=[];failures=[];strict_changes=[];midpoints=[]
    def check(name,actual,expected):
        good=bool(np.allclose(actual,expected,rtol=2e-10,atol=2e-12))
        checks.append(name)
        if not good:failures.append(dict(check=name,actual=np.asarray(actual).tolist(),expected=expected))
    def se(x):return float(np.std(x,ddof=1)/np.sqrt(len(x)))
    z=norm.ppf(.975)
    for case,records in grouped.items():
        d=np.load(study/'results'/(case+'.npz'))
        if 'endpoints' not in d:
            for r in records:
                ai=[.1,.05,.01].index(r['alpha'])
                hits=d['mom_pass'][:,ai] if r['method']=='directional_mom' else d['mean_pass'][:,ai]
                check(case+'_'+r['method']+str(ai)+'_event',int(hits.sum()),r['covered'])
            continue
        ep=d['endpoints'];target=float(d['target']);est=d['estimates'];B=len(est)
        strict=(ep[...,0]<=target)&(target<=ep[...,1])
        tol=1e-11*max(1.,abs(target))
        covered=(ep[...,0]<=target+tol)&(target<=ep[...,1]+tol)
        widths=np.diff(ep,axis=-1)[...,0]
        for r in records:
            j=list(d['methods']).index(r['method']);ai=list(d['alpha']).index(r['alpha'])
            key=case+'_'+r['method']+'_'+str(ai)
            errors=est[:,j]-target;loss=errors**2
            hit=covered[:,j,ai];k=int(hit.sum());phat=k/B
            center=(phat+z*z/(2*B))/(1+z*z/B)
            half=z*np.sqrt(phat*(1-phat)/B+z*z/(4*B*B))/(1+z*z/B)
            expected=dict(covered=k,coverage=phat,coverage_mcse=np.sqrt(phat*(1-phat)/B),
                coverage_wilson_95=[center-half,center+half],length=widths[:,j,ai].mean(),
                length_se=se(widths[:,j,ai]),mse=loss.mean(),bias=errors.mean(),bias_se=se(errors),
                paired_length=(widths[:,j,ai]-widths[:,0,ai]).mean(),
                paired_length_se=se(widths[:,j,ai]-widths[:,0,ai]),
                paired_coverage=(hit.astype(float)-covered[:,0,ai]).mean(),
                paired_coverage_se=se(hit.astype(float)-covered[:,0,ai]),
                paired_mse=(loss-(est[:,0]-target)**2).mean())
            if r['mse_se'] is not None:expected.update(mse_se=se(loss),paired_mse_se=se(loss-(est[:,0]-target)**2))
            rejected=(ep[:,j,ai,0]>0)|(ep[:,j,ai,1]<0)
            expected.update(reject_count=int(rejected.sum()),rejection=rejected.mean())
            for field,value in expected.items():check(key+'_'+field,value,r[field])
            if strict[:,j,ai].sum()!=k:
                strict_changes.append(dict(case=case,method=r['method'],alpha=r['alpha'],target=target,
                    strict=int(strict[:,j,ai].sum()),tolerant=k,tolerance=tol,
                    maximum_extra_miss=float(np.maximum(ep[:,j,ai,0]-target,target-ep[:,j,ai,1])[hit&~strict[:,j,ai]].max())))
            if r['method']=='pointwise' and r['alpha']==.05:
                check(key+'_midpoint',ep[:,j,ai].mean(axis=-1),est[:,j])
                sent=(ep[:,j,ai,0]==0)&(ep[:,j,ai,1]==0)
                midpoints.append(dict(case=case,target=target,sentinels=int(sent.sum()),
                    mse=float(loss.mean()),sentinel_loss_share=float(loss[sent].sum()/loss.sum()) if loss.sum() else 0.,
                    nonsentinel_mse=float(loss[~sent].mean()) if (~sent).any() else None))
    finite=[r for r in rows if r['guarantee']=='finite_sample']
    flagged=[r['case']+'_'+r['method']+'_'+str(r['alpha']) for r in finite
             if binom.cdf(r['covered'],r['repetitions'],1-r['alpha'])<.05/len(finite)]
    solver=json.loads((study/'tables/solver.json').read_text())
    selected=[r for r in solver if r['alpha']==.05 and r['budget']==3000]
    check('solver_count',len(solver),2160);check('solver_independent_datasets',len(selected),240)
    check('solver_certified95',sum(r['certified_to_tolerance'] for r in selected),146)
    configs=json.loads((study/'configs/cases.json').read_text())['cases']+json.loads((study/'configs/followup_cases.json').read_text())['cases']
    check('registered_cases',len(configs),402);check('data_sets',sum(c['B'] for c in configs),1084640)
    result=dict(status='PASSED' if not failures else 'FAILED',checks=len(checks),failures=failures,
        summary_rows=len(rows),stochastic_cases=len(grouped),finite_sample_screen_rows=len(finite),flags=flagged,
        strict_coverage_differences=strict_changes,pointwise_midpoint_decomposition=midpoints,
        solver_certified95=sum(r['certified_to_tolerance'] for r in selected),solver_total95=len(selected),
        scope='Recomputed existing raw arrays and scalar losses. No new Monte Carlo draws; not proof of honesty.')
    dump(ROOT/'results/raw_results_audit.json',result)
    print(result['status'],len(checks),'raw-result checks;',len(strict_changes),'strict/tolerant coverage differences;',len(failures),'failures')
    if failures:raise AssertionError(failures[:3])

if __name__=='__main__':main()
