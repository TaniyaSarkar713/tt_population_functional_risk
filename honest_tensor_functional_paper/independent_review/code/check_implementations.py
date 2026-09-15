"""Targeted fresh implementation probes, including a reproduced coverage miscount."""
import importlib.util
import itertools
import math
import sys
import numpy as np
from scipy.stats import norm
from inventory import ROOT,PACKAGE,dump

def main():
    study=PACKAGE/'empirical_study';sys.path.insert(0,str(study/'code'))
    from common import rng_for,load_cases
    from run_study import tensor_signal
    c=next(c for c in load_cases() if c['id']=='S03_007');A,M,S,amp=tensor_signal(c)
    d=np.load(study/'results/S03_007.npz');target=float(d['target'])
    j=list(d['methods']).index('oracle');ep=d['endpoints'][:,j,0]
    miss=np.maximum(ep[:,0]-target,target-ep[:,1])
    indices=np.flatnonzero((miss>0)&(miss<=1e-11*abs(target)));records=[]
    for b in indices:
        G=rng_for(c['id'],int(b)).normal(size=A.shape)
        noise=math.fsum(G[i,i,i] for i in S)/np.sqrt(c['p'])
        radius=norm.ppf(.95)*np.sqrt(c['rank']/c['p'])
        records.append(dict(trial=int(b),noise_contraction=float(noise),normal_radius=float(radius),
            exact_noise_miss=bool(abs(noise)>radius),miss_distance=float(abs(noise)-radius),ulp=float(np.spacing(target))))
    assert len(records)==1 and records[0]['exact_noise_miss']
    alpha=.05;p=16;r=1;delta=alpha*r/(8*p)
    ablation=dict(alpha=alpha,p=p,rank=r,full_validation_quantile=float(norm.isf((alpha/2-delta)/2)),
        ablation_validation_quantile=float(norm.isf(alpha/2)),
        changes=['Removes bias','Removes direct/structural fallback and intersections','Changes confidence allocation'])
    sweep=[]
    for c in load_cases():
        if c.get('regime')=='signal_sweep':
            _,M,_,_=tensor_signal(c);sweep.append(dict(case=c['id'],amplitude=c['amplitude'],M=M))
    spec=importlib.util.spec_from_file_location('review_binary',PACKAGE/'certified_weak_signal/code/certified_optimizer.py')
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    rng=np.random.default_rng(2026091308);checks=[]
    def tensor(a,angles):
        u=[np.array([np.cos(x),np.sin(x)]) for x in angles]
        return a*np.einsum('i,j,k->ijk',*u,optimize=False)
    for trial in range(3):
        M=2.;tau=.3;L=rng.normal(size=(2,2,2));L/=np.linalg.norm(L)
        A=tensor(1.,rng.uniform(0,np.pi,3));z=A+.15*rng.normal(size=A.shape)
        fit=module.BinaryRankOneOptimizer(z,L,M,tau)
        directions=fit.directions
        candidates=[tensor(a,angles) for a in np.linspace(-M,M,7)
            for angles in itertools.product(np.linspace(0,np.pi,6),repeat=3)]
        values=[]
        for B in candidates:
            residual=np.abs(np.einsum('id,d->i',directions,(z-B).ravel(),optimize=False))
            if np.all(residual<=fit.thresholds):values.append(float(np.sum(L*B)))
        for budget in [1,25,125]:
            fit=module.BinaryRankOneOptimizer(z,L,M,tau)
            out=fit.project_interval(tolerance=.03,max_nodes=budget)
            passed=bool(values and out['lo']<=min(values) and max(values)<=out['hi'])
            checks.append(dict(trial=trial,budget=budget,grid_feasible=len(values),passed=passed,
                certified=out['certified_to_tolerance'],lo=out['lo'],hi=out['hi']))
    assert all(c['passed'] for c in checks)
    dump(ROOT/'results/implementation_probes.json',dict(status='COMPLETED_WITH_FINDINGS',
        oracle_tolerance=dict(case='S03_007',alpha=.1,records=records,
            conclusion='Genuine miss; strict coverage is 133/150, stored tolerant coverage is 134/150 for oracle and XCH known.'),
        bias_ablation=ablation,signal_budget_sweep=sweep,binary_outer_grid_checks=checks,
        scope='New bounded checks and one full-noise regeneration. Finite grids cannot prove global certificates.'))
    print('Confirmed oracle miscount; recorded ablation changes;',len(checks),'binary outer-grid checks passed.')

if __name__=='__main__':main()
