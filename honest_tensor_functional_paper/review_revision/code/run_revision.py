"""Execute preregistered review-response experiments without outcome tuning."""
import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path
import numpy as np
from scipy.stats import norm,chi2
from threadpoolctl import threadpool_limits

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'empirical/code'))
from common import high,global_fit,write_json,mean_se,wilson
from tensor_methods import pointwise_levels,xch_pca
from numerics import coverage_events,scalar_companion,companion_risk_upper

SEED=2026091309
LEVELS=np.array([.10,.05,.01])

def rng(case,trial=0,stream=0):
    h=int.from_bytes(hashlib.sha256(case.encode()).digest()[:4],'little')
    return np.random.default_rng(np.random.SeedSequence([SEED,h,trial,stream]))

def interval(center,radius):return [center-radius,center+radius]

def from_geometry(details,p,r,M,tau=1.,variant='full'):
    out=[]
    for a,d in zip(LEVELS,details):
        h=M*np.sqrt(r/p);bias=M*np.sqrt(max(0.,1-d['tangent_norm']**2))*d['angle']
        # The loading is unit norm and the cap projection is orthogonal.
        q=d['q'];tn=d['tangent_norm'];noise=q*np.sqrt(2)*tau
        radii=[bias+noise*tn,noise,h];choice=int(np.argmin(radii))
        centers=[d['center_t'],d['center_s'],0.]
        rad=radii[choice];center=centers[choice]
        if variant=='no_bias_fixed_choice' and choice==0:rad-=bias
        if variant=='quantile_only':
            noise=norm.isf(a/2)*np.sqrt(2)*tau
            rad=[bias+noise*tn,noise,h][choice]
        if variant=='tangent_without_fallback':center=centers[0];rad=radii[0]
        if variant=='unprotected':center=centers[0];rad=norm.isf(a/2)*np.sqrt(2)*tau*tn
        lo,hi=interval(center,rad)
        if variant not in ['no_intersection','tangent_without_fallback','unprotected']:
            rd=norm.isf(a/4)*tau
            lo=max(lo,d['center_d']-rd,-h);hi=min(hi,d['center_d']+rd,h)
            if lo>hi:lo=hi=0.
        out.append([lo,hi])
    return np.asarray(out)

def save(c,names,ep,est,target,extra=None,alpha=LEVELS,aux=None):
    ep=np.asarray(ep);est=np.asarray(est);alpha=np.asarray(alpha);B=len(ep)
    covered=coverage_events(ep,target);rows=[]
    for j,name in enumerate(names):
        errors=est[:,j]-target
        for ai,a in enumerate(alpha):
            hits=int(covered[:,j,ai].sum());width=ep[:,j,ai,1]-ep[:,j,ai,0]
            row=dict(case=c['id'],suite=c['suite'],method=name,alpha=float(a),repetitions=B,target=float(target),
                coverage=hits/B,covered=hits,coverage_wilson_95=wilson(hits,B),coverage_mcse=float(np.sqrt(hits/B*(1-hits/B)/B)),
                length=mean_se(width)[0],length_se=mean_se(width)[1],mse=mean_se(errors**2)[0],mse_se=mean_se(errors**2)[1],
                bias=mean_se(errors)[0],bias_se=mean_se(errors)[1],
                paired_length=mean_se(width-(ep[:,0,ai,1]-ep[:,0,ai,0]))[0],
                paired_length_se=mean_se(width-(ep[:,0,ai,1]-ep[:,0,ai,0]))[1],
                paired_coverage=mean_se(covered[:,j,ai].astype(float)-covered[:,0,ai])[0],
                paired_coverage_se=mean_se(covered[:,j,ai].astype(float)-covered[:,0,ai])[1],
                estimator_id='interval_companion' if name.startswith('cap_') else name+'_scalar',
                estimator_alpha=.05 if name.startswith('cap_') else None,
                coverage_policy='four endpoint ULPs',status='COMPLETED')
            rows.append(row)
    np.savez_compressed(ROOT/'results'/f"{c['id']}.npz",endpoints=ep,estimates=est,target=target,alpha=alpha,
        methods=np.asarray(names),**(aux or {}))
    write_json(ROOT/'results'/f"{c['id']}.json",dict(case=c,records=rows,extra=extra or {},seed=SEED))
    return rows

def tensor_case(c):
    p,r,B=c['p'],c['rank'],c['B'];a=c['amplitude'];tau=1.
    A=np.zeros((p,p,p));support=rng(c['id'],stream=5).choice(p,r,replace=False)
    for i in support:A[i,i,i]=a
    L=high.flat_loading(p,3);target=float(np.sum(L*A))
    Mmatch=max(np.sqrt(p),1.1*np.linalg.norm(A),np.linalg.norm(A)+1)
    Mfixed=c.get('M_fixed',Mmatch);hfixed=Mfixed*np.sqrt(r/p)
    names=['direct','cap_fixed','cap_matched','no_bias_fixed_choice','no_intersection','quantile_only',
           'tangent_without_fallback','split_unprotected','xch_known','xch_plugin','oracle']
    ep=np.empty((B,len(names),3,2));est=np.empty((B,len(names)));legacy=np.empty((B,2));times=[];equiv=0
    for b in range(B):
        z=A+rng(c['id'],b).normal(size=A.shape);aux=rng(c['id'],b,1).normal(size=A.shape)
        start=time.perf_counter();base,_,details,_=pointwise_levels(z,Mfixed,r,aux,tau)
        times.append(time.perf_counter()-start)
        direct=details[0]['center_d'];ep[b,0]=np.array([interval(direct,norm.isf(x/2)) for x in LEVELS]);est[b,0]=direct
        ep[b,1]=from_geometry(details,p,r,Mfixed);ep[b,2]=from_geometry(details,p,r,Mmatch)
        assert np.allclose(ep[b,1],base,rtol=1e-12,atol=1e-8)
        equiv+=1
        for j,M in [(1,Mfixed),(2,Mmatch)]:
            est[b,j]=scalar_companion(ep[b,j,1],direct,M*np.sqrt(r/p),tau)
            legacy[b,j-1]=ep[b,j,1].mean()
        for j,v in enumerate(['no_bias_fixed_choice','no_intersection','quantile_only','tangent_without_fallback','unprotected'],3):
            ep[b,j]=from_geometry(details,p,r,Mfixed,variant=v);est[b,j]=ep[b,j,1].mean()
        comp=xch_pca(z,L,r,tau)
        for j,sd in [(8,comp['sd']),(9,comp['sd_plugin'])]:
            ep[b,j]=np.array([interval(comp['estimate'],norm.isf(x/2)*sd) for x in LEVELS]);est[b,j]=comp['estimate']
        oracle=float(z[support,support,support].sum()/np.sqrt(p));est[b,10]=oracle
        ep[b,10]=np.array([interval(oracle,norm.isf(x/2)*np.sqrt(r/p)) for x in LEVELS])
        if p>=32 and (b+1)%100==0:print(c['id'],b+1,'/',B,flush=True)
    save(c,names,ep,est,target,extra=dict(M_fixed=Mfixed,M_matched=Mmatch,tau=tau,
        pointwise_rate=np.sqrt(r/p),P1_sufficient_bound=high.pointwise_amplitude_bound(p,r),
        geometry_equivalence_checks=equiv,mean_cap_seconds=mean_se(times)[0],input_entries=p**3,input_bytes=A.nbytes,
        companion_risk_bound=companion_risk_upper(hfixed,tau),
        comparator_applicability='OUTSIDE_REGULAR_CLASS: zero' if a==0 else 'Regularity constants not certified; rank correct; strong-signal diagnostics only',
        ablation_contract='Same data, pilot projectors, supplied M and original full-choice index. Bias-only removes B; quantile-only changes q; no-intersection removes intersections. Tangent-without-fallback separately removes candidate fallback and intersections. Historical unprotected removes all three protections.',
        legacy_midpoint_mse=[float(np.mean((legacy[:,j]-target)**2)) for j in range(2)]),aux={'legacy_midpoints':legacy})

def solver_case(c):
    B=c['B'];K=3;M=c['M'];tau=c['tau'];budgets=c['budgets'];a=c['amplitude'];alpha=.05
    # The loading AND signal direction are held fixed across all amplitudes.
    L=rng('V02_fixed_loading').normal(size=(2,2,2));L/=np.linalg.norm(L)
    angles=rng('V02_fixed_direction').uniform(0,np.pi,3)
    u=[np.array([np.cos(x),np.sin(x)]) for x in angles];U=np.einsum('i,j,k->ijk',*u,optimize=False)
    A=a*U;target=float(np.sum(A*L));names=['direct']+[f'global_{n}' for n in budgets]
    ep=np.empty((B,len(names),1,2));est=np.empty((B,len(names)));records=[]
    for b in range(B):
        z=A+tau*rng(c['id'],b).normal(size=A.shape);direct=float(np.sum(z*L))
        ep[b,0,0]=interval(direct,norm.isf(alpha/2)*tau);est[b,0]=direct
        for j,budget in enumerate(budgets,1):
            fit=global_fit.BinaryRankOneOptimizer(z,L,M,tau,alpha=alpha)
            start=time.perf_counter();out=fit.project_interval(tolerance=c['tolerance']*tau,max_nodes=budget)
            ep[b,j,0]=[out['lo'],out['hi']];est[b,j]=np.mean(ep[b,j,0])
            records.append(dict(trial=b,budget=budget,seconds=time.perf_counter()-start,**out))
        if (b+1)%10==0:print(c['id'],b+1,'/',B,flush=True)
    save(c,names,ep,est,target,alpha=[alpha],extra=dict(solver_records=records,loading=L.tolist(),direction=U.tolist(),
        input_entries=8,input_bytes=64,scope='Numerical float64 global bounds; fixed loading, class and tolerance across budgets/signals.'))

def calibration_case(c):
    B=c['B'];m=c['m'];n=c['n'];alpha=.05;M=c['M'];q=2/3
    a=np.zeros(m);a[0]=M if c.get('signal','boundary')=='boundary' else 0.;target=float(a.sum()/np.sqrt(m))
    if c['suite']=='V03':names=['naive_gaussian','bounded_row_median']
    else:names=['known_sigma','independent_upper_sigma','naive_plugin_sigma']
    ep=np.empty((B,len(names),1,2));est=np.empty((B,len(names)));scales=[];events=[]
    if c['suite']=='V03':
        bcount=int(max(8*c['supplied_c'],32*np.log(m/alpha)))+1
        if bcount%2==0:bcount+=1
        assert n>=2*bcount
        k=n//bcount;lam=2/np.sqrt(k);hNL=M**q*(2*lam)**(1-q)/np.sqrt(m)
    for trial in range(B):
        generator=rng(c['id'],trial)
        if c['suite']=='V03':
            if c['law']=='t3':noise=generator.standard_t(3,size=(n,m))/np.sqrt(3)
            elif c['law']=='correlated':noise=np.sqrt(.5)*generator.normal(size=(n,m))+np.sqrt(.5)*generator.normal(size=(n,1))
            else:noise=generator.normal(size=(n,m))
            W=a+noise
            for j in range(c['actual_c']):W[j*k,:]=a+1e4
            med=np.median(W[:bcount*k].reshape(bcount,k,m).mean(axis=1),axis=0)
            center=float(np.sum(np.sign(med)*np.maximum(abs(med)-lam,0))/np.sqrt(m))
            h0=M/np.sqrt(m);radius=min(hNL,h0);center=center if hNL<h0 else 0.
            mean=float(W.mean(axis=0).sum()/np.sqrt(m));ep[trial,0,0]=interval(mean,norm.isf(alpha/2)/np.sqrt(n));est[trial,0]=mean
            ep[trial,1,0]=interval(center,radius);est[trial,1]=center
            events.append(bool(np.max(abs(med-a))<=lam));scales.append(lam)
        else:
            sigma=c['sigma'];W=a+sigma*generator.normal(size=(n,m));means=W.mean(axis=0)
            nu=m*(n-1);S=np.sqrt(np.sum((W-means)**2)/nu);delta=.01
            SU=S*np.sqrt(nu/chi2.ppf(delta,nu));events.append(bool(SU>=sigma));scales.append(SU/sigma)
            for j,scale,level in [(0,sigma,alpha),(1,SU,alpha-delta),(2,S,alpha)]:
                tau=scale/np.sqrt(n);lam=tau*np.sqrt(2*np.log(2*m/level))
                radii=[M**q*(2*lam)**(1-q)/np.sqrt(m),norm.isf(level/2)*tau,M/np.sqrt(m)]
                centers=[np.sum(np.sign(means)*np.maximum(abs(means)-lam,0))/np.sqrt(m),means.sum()/np.sqrt(m),0.]
                choice=int(np.argmin(radii));ep[trial,j,0]=interval(centers[choice],radii[choice]);est[trial,j]=centers[choice]
    extra=dict(event_coverage=float(np.mean(events)),event_wilson=wilson(int(sum(events)),B),mean_scale=float(np.mean(scales)),
        conditions_satisfied=c['actual_c']<=c['supplied_c'] if c['suite']=='V03' else True,
        scope='Coordinate-envelope/selected-interval calibration, not general robust minimax computation.')
    if c['suite']=='V03':extra.update(blocks=bcount,block_size=k,threshold=lam)
    save(c,names,ep,est,target,alpha=[alpha],extra=extra,aux={'calibration_events':events,'calibration_scales':scales})

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--suite',required=True);args=parser.parse_args()
    config=json.loads((ROOT/'configs/revision_cases.json').read_text());cases=[c for c in config['cases'] if c['suite']==args.suite]
    assert cases
    start=time.perf_counter();source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
        list((ROOT/'code').glob('*.py'))+list((ROOT/'empirical/code').glob('*.py'))+[ROOT/'configs/revision_cases.json']}
    with threadpool_limits(limits=1):
        for c in cases:
            if args.suite in ['V01','V05']:tensor_case(c)
            elif args.suite=='V02':solver_case(c)
            else:calibration_case(c)
            print('Completed',c['id'],flush=True)
    write_json(ROOT/'logs'/f'run_{args.suite}.json',dict(status='COMPLETED',cases=len(cases),datasets=sum(c['B'] for c in cases),
        seconds=time.perf_counter()-start,seed=SEED,source_hashes=source_hashes,threads=1))

if __name__=='__main__':main()
