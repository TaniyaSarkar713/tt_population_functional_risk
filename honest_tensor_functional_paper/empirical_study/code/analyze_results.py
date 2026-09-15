"""Build checked tables, slope diagnostics and a result audit from saved trials."""
import csv
import hashlib
import json
import warnings
from pathlib import Path

import numpy as np
from scipy.stats import binom, kstest, norm, skew, kurtosis
from scipy.integrate import quad

from common import ROOT, PROJECT, LEVELS, high, load_cases, write_json


def csv_file(path, rows):
    keys=list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
        for row in rows:
            w.writerow({k:json.dumps(v) if isinstance(v,(list,dict)) else v for k,v in row.items()})


def regression(x,y,se=None):
    x,y=np.log(np.asarray(x,float)),np.log(np.asarray(y,float))
    X=np.column_stack((np.ones(len(x)),x))
    if se is None or np.max(se)<1e-10:
        beta=np.linalg.lstsq(X,y,rcond=None)[0]
        return dict(slope=float(beta[1]),slope_se=None,uncertainty='Descriptive fit to deterministic curve')
    sigma=np.maximum(np.asarray(se)/np.exp(y),1e-12)
    WX=X/sigma[:,None];Wy=y/sigma
    beta=np.linalg.lstsq(WX,Wy,rcond=None)[0]
    covariance=np.linalg.inv(np.einsum('ni,nj->ij',WX,WX,optimize=False))
    return dict(slope=float(beta[1]),slope_se=float(np.sqrt(covariance[1,1])),
                uncertainty='Delta-method weighted log regression using independent-case Monte Carlo mean SEs; descriptive finite-grid slope')


def main():
    warnings.simplefilter('error',RuntimeWarning)
    cases=load_cases()+json.loads((ROOT/'configs/followup_cases.json').read_text())['cases'];rows=[];bounds=[];solver=[];diagnostics=[];checks=[]
    def check(label,value):
        if not value:raise AssertionError(label)
        checks.append(label)
    preserved=json.loads((ROOT/'logs/preserved_stage_hashes.json').read_text())
    repo=PROJECT.parent
    check('preserved_stages',all(hashlib.sha256((repo/p).read_bytes()).hexdigest()==h for p,h in preserved.items()))
    for suite in range(1,14):
        manifest=json.loads((ROOT/'logs'/f'run_S{suite:02d}.json').read_text())
        check(f'S{suite:02d}_completed',manifest['status']=='COMPLETED')
        check(f'S{suite:02d}_source_fresh',all(hashlib.sha256((PROJECT/p).read_bytes()).hexdigest()==h
                                             for p,h in manifest['source_hashes'].items()))
    for c in cases:
        path=ROOT/'results'/(c['id']+'.json');meta=json.loads(path.read_text())
        check(c['id']+'_config_match',meta['case']==c)
        if c['B']:
            data=np.load(path.with_suffix('.npz'))
            if 'endpoints' in data:
                ep=data['endpoints'];target=float(data['target']);est=data['estimates']
                check(c['id']+'_raw_finite',np.isfinite(ep).all() and np.isfinite(est).all())
                check(c['id']+'_raw_shape',ep.shape[0]==c['B'] and ep.shape[2:]==(3,2))
                check(c['id']+'_endpoints_ordered',np.all(ep[...,0]<=ep[...,1]))
            else:
                ep=None
                check(c['id']+'_event_shape',data['mom_pass'].shape==(c['B'],3))
            for original in meta['records']:
                row=dict(original)
                row.update({k:v for k,v in c.items() if k not in ['id','suite','B']})
                row['status']='VALIDATED'
                if ep is None:
                    ai=list(LEVELS).index(row['alpha'])
                    values=data['mom_pass'] if row['method']=='directional_mom' else data['mean_pass']
                    check(c['id']+'_'+row['method']+'_'+str(ai)+'_event_count',int(values[:,ai].sum())==row['covered'])
                if ep is not None:
                    j=list(data['methods']).index(row['method']);ai=list(LEVELS).index(row['alpha'])
                    tolerance=1e-11*max(1.,abs(target))
                    hits=((ep[:,j,ai,0]<=target+tolerance)&(target<=ep[:,j,ai,1]+tolerance)).sum()
                    check(c['id']+'_'+row['method']+'_'+str(ai)+'_coverage_recomputed',hits==row['covered'])
                    length=ep[:,j,ai,1]-ep[:,j,ai,0]
                    check(c['id']+'_'+row['method']+'_'+str(ai)+'_length_recomputed',np.isclose(length.mean(),row['length']))
                    row['zero_width_count']=int((length==0).sum())
                    row['zero_sentinel_count']=int(((ep[:,j,ai,0]==0)&(ep[:,j,ai,1]==0)).sum())
                    if c.get('law')=='t3':
                        # Fourth moments are infinite: sample loss SD/sqrt(B)
                        # cannot serve as a finite-variance Monte Carlo SE.
                        row['mse_se']=None;row['paired_mse_se']=None
                        row['mse_uncertainty']='No finite-variance MCSE: t3 has infinite fourth moment; raw sample SD retained only for reproducibility'
                    else:row['mse_uncertainty']='Sample loss SD/sqrt(B)'
                    if c['suite']=='S01':
                        row['rate']=meta['extra']['rate'];row['length_over_rate']=row['length']/row['rate']
                        row['mse_over_rate2']=row['mse']/row['rate']**2
                    if c['suite']=='S03':
                        row['rate']=meta['extra']['pointwise_rate'];row['length_over_rate']=row['length']/row['rate']
                    if c['suite']=='S02':
                        row['ideal_full_data_rate']=meta['extra']['full_data_ideal_rate']
                        row['threshold_rate']=meta['extra']['threshold_rate']
                rows.append(row)
        for b in meta.get('extra',{}).get('bounds',[]):bounds.append(dict(case=c['id'],**c,**b,status='VALIDATED',evidence='Analytic calculation; not fitted interval'))
        for trial in meta.get('extra',{}).get('solver_trials',[]):
            solver.append(dict(case=c['id'],signal=c['signal'],loading=c['loading'],**trial))
        pivot_file=ROOT/'results'/('diagnostics_'+c['id']+'.npz')
        if pivot_file.exists():
            piv=np.load(pivot_file)['pivots']
            for j,name in enumerate(['direct','xch_known','xch_plugin','oracle']):
                v=piv[:,j];ks=kstest(v,'norm',method='asymp')
                diagnostics.append(dict(case=c['id'],suite=c['suite'],method=name,p=c['p'],regime=c['regime'],
                    mean=float(v.mean()),variance=float(v.var(ddof=1)),skewness=float(skew(v,bias=False)),
                    excess_kurtosis=float(kurtosis(v,bias=False)),ks_distance=float(ks.statistic),ks_pvalue=float(ks.pvalue),
                    ks_pvalue_type='Asymptotic, descriptive, not multiple-test adjusted; KS distance is exact for the empirical sample',
                    repetitions=len(v),status='VALIDATED',interpretation='Exact pivot for direct/oracle; asymptotic diagnostic for XCH, not a nonlinear midpoint CLT'))
    finite=[r for r in rows if r['guarantee']=='finite_sample']
    threshold=.05/len(finite)
    contradictions=[]
    for row in rows:
        if row['guarantee']=='finite_sample':
            pvalue=float(binom.cdf(row['covered'],row['repetitions'],1-row['alpha']))
            row['undercoverage_pvalue']=pvalue
            row['bonferroni_screen_threshold']=threshold
            if pvalue<threshold:
                row['status']='CONTRADICTS EXPECTATION';contradictions.append(row)
    # The P1 interval theorem never claimed its {0}-sentinel midpoint is an MSE-optimal estimator.
    sentinels=[r for r in rows if r.get('method')=='pointwise' and r.get('zero_sentinel_count',0)>0 and abs(r['target'])>1e-8 and r['alpha']==.05]
    slopes=[]
    def fit(label,subset,axis,metric,reference):
        ordered=sorted(subset,key=lambda r:r[axis]);x=[r[axis] for r in ordered]
        y=[np.sqrt(r['mse']) if metric=='rmse' else r['length'] for r in ordered]
        se=[r['mse_se']/(2*np.sqrt(r['mse'])) if metric=='rmse' else r['length_se'] for r in ordered]
        slopes.append(dict(label=label,reference_exponent=reference,cases=[r['case'] for r in ordered],
            x=x,y=y,**regression(x,y,se)))
    alpha95=[r for r in rows if r['alpha']==.05]
    fit('G1 fixed-M structural length vs p',[r for r in alpha95 if r['suite']=='S01' and r['method']=='growing' and r['axis']=='structural_p'],'p','length',-.25)
    fit('G1 noise-branch length vs n',[r for r in alpha95 if r['suite']=='S01' and r['method']=='growing' and r['axis']=='n' and r['signal']=='boundary' and r['n']>=4],'n','length',-.5)
    fit('G1 noise-branch RMSE vs n',[r for r in alpha95 if r['suite']=='S01' and r['method']=='growing' and r['axis']=='n' and r['signal']=='boundary' and r['n']>=4],'n','rmse',-.5)
    for fixed in [True,False]:
        subset=[r for r in alpha95 if r['suite']=='S03' and r['method']=='pointwise' and (r['rank']==1)==fixed]
        fit('P1 length vs p: '+('cap 1' if fixed else 'cap ceil(sqrt(p))'),subset,'p','length',-.5 if fixed else -.25)
    for K in [3,4]:
        subset=[r for r in alpha95 if r['suite']=='S02' and r['method']=='threshold_raw' and r['axis']=='p' and r['support']=='threshold' and r['K']==K]
        fit(f'Threshold raw length vs p, K={K} (log factor retained)',subset,'p','length',-(K-2)/(2*K))
    geometry=[]
    for row in [r for r in alpha95 if r['suite']=='S03' and r['method']=='pointwise']:
        meta=json.loads((ROOT/'results'/(row['case']+'.json')).read_text())
        p,r,a=row['p'],row['rank'],row['amplitude'];tau=meta['extra']['tau'];M=meta['extra']['M']
        delta=.05*r/(8*p);eta=high.pilot_bound(p,3,tau,delta)
        angle=min(1.,np.sqrt(3)*(2*eta/(a-eta))**2)
        bias=M*np.sqrt(1-r/p)*angle
        radius=bias+norm.isf((.025-delta)/2)*np.sqrt(2)*tau*np.sqrt(r/p)
        direct=norm.isf(.0125)*tau
        # Freeze fitted subspaces at the true ones and singular values at a.
        # The two Gaussian interval centers then differ by N(0,tau^2).
        A=abs(radius-direct);B=radius+direct
        prediction=2*min(radius,direct)*(2*norm.cdf(A/tau)-1)+2*B*(norm.cdf(B/tau)-norm.cdf(A/tau))-2*tau*(norm.pdf(A/tau)-norm.pdf(B/tau))
        numeric=quad(lambda t:max(0.,min(2*min(radius,direct),B-t))*2*norm.pdf(t/tau)/tau,
                     0.,B,points=[A],epsabs=1e-10)[0]
        check(row['case']+'_frozen_geometry_integral',np.isclose(prediction,numeric,atol=1e-10,rtol=1e-10))
        geometry.append(dict(case=row['case'],p=p,rank=r,observed_length=row['length'],length_se=row['length_se'],
            observed_over_rate=row['length']/row['rate'],frozen_geometry_length=float(prediction),
            prediction_over_rate=float(prediction/row['rate']),
            discrepancy_in_mcse=float((row['length']-prediction)/row['length_se']),
            status='VALIDATED',evidence='Post-hoc analytic approximation with true subspaces; not a simulation or a guarantee for estimated subspaces'))
    counts={s:dict(configurations=sum(c['suite']==s for c in cases),data_sets=sum(c['B'] for c in cases if c['suite']==s),
                   interval_or_event_rows=sum(r['suite']==s for r in rows)) for s in sorted({c['suite'] for c in cases})}
    audit=dict(status='PASSED' if not contradictions else 'CONTRADICTS EXPECTATION',
        registered_cases=len(cases),monte_carlo_cases=sum(c['B']>0 for c in cases),analytic_only_cases=sum(c['B']==0 for c in cases),
        monte_carlo_data_sets=sum(c['B'] for c in cases),summary_rows=len(rows),analytic_bounds=len(bounds),
        solver_solves=len(solver),finite_sample_screen_rows=len(finite),bonferroni_threshold=threshold,
        finite_sample_undercoverage_flags=len(contradictions),contradictions=contradictions,
        pointwise_midpoint_sentinel_cases=sentinels,preserved_files=len(preserved),checks=len(checks),
        counts=counts,interpretation='VALIDATED means results/implementation checked, not proof of uniform coverage or minimax optimality.')
    for name,data in [('summary',rows),('loading_bounds',bounds),('solver',solver),('normal_diagnostics',diagnostics),('slopes',slopes),('pointwise_geometry',geometry)]:
        write_json(ROOT/'tables'/(name+'.json'),data);csv_file(ROOT/'tables'/(name+'.csv'),data)
    write_json(ROOT/'results/analysis_audit.json',audit)
    write_json(ROOT/'logs/analysis_checks.json',dict(status='PASSED',checks=checks))
    print(json.dumps({k:v for k,v in audit.items() if k not in ['contradictions','pointwise_midpoint_sentinel_cases','counts']},indent=2))


if __name__=='__main__':main()
