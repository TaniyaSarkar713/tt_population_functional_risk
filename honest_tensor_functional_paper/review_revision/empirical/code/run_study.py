"""Execute registered cases. No tuning or deletion based on observed outcomes."""
import argparse
from collections import Counter
import platform
import time

import numpy as np
import scipy
from scipy.stats import norm
from threadpoolctl import threadpool_limits, threadpool_info

from common import (ROOT, LEVELS, SEED, high, old, diag, global_fit, rng_for,
                    save_intervals, symmetric, write_json, load_cases, hashes, wilson)
from tensor_methods import pointwise_levels, xch_pca
from numerics import scalar_companion


def scalar_growing(c):
    B,p,r=c['B'],c['p'],c['rank'];M=c['M'];tau=1/np.sqrt(c['n'])
    h=M*np.sqrt(r/p)
    target=0. if c['signal']=='zero' else h
    observed=target+tau*rng_for(c['id']).normal(size=B)
    rd=tau*norm.isf(LEVELS/2)
    ep=np.empty((B,3,3,2));est=np.empty((B,3))
    ep[:,0]=symmetric(observed[:,None],rd)
    ep[:,1]=symmetric(np.where(h<=rd,0.,observed[:,None]),np.minimum(h,rd))
    ep[:,2]=symmetric(np.zeros((B,3)),h)
    est[:,0]=observed;est[:,1]=0. if h<=tau else observed;est[:,2]=0.
    lower=high.growing_lower(p,r,M,tau)
    return save_intervals(c,['direct','growing','structural'],ep,est,target,
        extra=dict(rate=min(h,tau),mse_upper=min(h*h,tau*tau),length_lower=lower['length_lower'],
                   observation='Exact scalar sufficient statistic; actual O(p) access measured in S11.'))


def threshold(c):
    B,p,K,M=c['B'],c['p'],c['K'],c['M'];tau=1/np.sqrt(c['n'])
    lam=tau*np.sqrt(2*np.log(2*p/.05))
    s={'atom':1,'eight':8,'threshold':max(1,int((M/lam)**(2/K)))}[c['support']]
    s=min(p,s)
    dval=M*s**(-K/2); target=s*dval/np.sqrt(p)
    unit_diagonal=s**(-K/2)
    coeff=s*unit_diagonal/np.sqrt(p)
    names=['direct','threshold_selected','threshold_raw','structural','oracle_direction']
    ep=np.empty((B,5,3,2));est=np.empty((B,5));secs=np.zeros((B,5))
    rng=rng_for(c['id'])
    configs=[diag.radii(K,p,tau,M,1,float(a)) for a in LEVELS]
    for start in range(0,B,32):
        stop=min(B,start+32);b=stop-start
        noise=rng.normal(size=(b,p));d=tau*noise;d[:,:s]+=dval
        t=time.perf_counter();direct=d.sum(axis=1)/np.sqrt(p);dt=time.perf_counter()-t
        oracle=target+tau*coeff*(noise[:,:s].sum(axis=1)*unit_diagonal+
                           np.sqrt(max(0.,1-s*unit_diagonal**2))*rng.normal(size=b))
        est[start:stop,0]=direct;est[start:stop,3]=0;est[start:stop,4]=oracle
        for ai,a in enumerate(LEVELS):
            cfg=configs[ai]
            t=time.perf_counter()
            soft=(np.sign(d)*np.maximum(np.abs(d)-cfg.threshold,0)).sum(axis=1)/np.sqrt(p)
            cost=time.perf_counter()-t
            selected={'nonlinear':soft,'gaussian':direct,'structural':np.zeros(b)}[cfg.selected]
            rad={'nonlinear':cfg.nonlinear,'gaussian':cfg.gaussian,'structural':cfg.structural}[cfg.selected]
            ep[start:stop,0,ai]=symmetric(direct,cfg.gaussian)
            ep[start:stop,1,ai]=symmetric(selected,rad)
            ep[start:stop,2,ai]=symmetric(soft,cfg.nonlinear)
            ep[start:stop,3,ai]=symmetric(np.zeros(b),cfg.structural)
            ep[start:stop,4,ai]=symmetric(oracle,cfg.gaussian*abs(coeff))
            if ai==1:
                est[start:stop,1]=selected;est[start:stop,2]=soft
                secs[start:stop,0]=dt/b;secs[start:stop,1:3]=cost/b
    ideal=high.fixed_cap_rate(p,M,tau,K)
    q=2/K
    raw_rate=M**q*tau**(1-q)*np.log(np.e*p)**((1-q)/2)/np.sqrt(p)
    return save_intervals(c,names,ep,est,target,secs,scope={'oracle_direction':'oracle'},
        extra=dict(support=s,full_data_ideal_rate=ideal,threshold_rate=raw_rate,
                   selected95=configs[1].selected,timing='Batch-amortized component timings; use S11 for wall-cost comparisons.'))


def tensor_signal(c):
    p,r,a=c['p'],c['true_rank'],c['amplitude'];tau=1/np.sqrt(c['n'])
    A=np.zeros((p,)*3);rng=rng_for(c['id'],stream=5)
    support=rng.choice(p,size=max(1,r),replace=False)
    amps=np.full(r,a)
    if c['signal']=='strong_plus_weak':amps[-1]=.5*tau
    if c['signal']=='opposite':
        amps[1]=-a+c['shift']*tau*np.sqrt(r)
    if c['signal']=='rotated':
        bases=[np.linalg.qr(rng.normal(size=(p,r)))[0] for _ in range(3)]
        A=np.einsum('ir,jr,kr,r->ijk',*bases,amps,optimize=False)
    elif r:
        for i,amp in zip(support,amps):A[i,i,i]=amp
    M=max(np.sqrt(p)*tau,1.1*np.linalg.norm(A),np.linalg.norm(A)+tau)
    return A,float(M),support,amps


def tensors(c):
    B,p,r=c['B'],c['p'],c['rank'];tau=1/np.sqrt(c['n'])
    A,M,support,amps=tensor_signal(c);L=high.flat_loading(p,3)
    target=float(np.sum(A*L));ids=np.arange(p)
    names=['direct','pointwise','xch_known','xch_plugin','oracle','split_unprotected']
    if c['suite']=='S04':names+=['separated_selector']
    ep=np.empty((B,len(names),3,2));est=np.empty((B,len(names)));seconds=np.zeros((B,len(names)))
    choices=Counter();ranks=Counter();biases=[];tangent_norms=[]
    pivots=np.empty((B,4))
    oracle_loading=np.zeros_like(A)
    if c['signal']=='rotated':
        # Known full direction, a strictly smaller class than unknown rotations.
        unit=A/np.linalg.norm(A)
        oracle_loading=float(np.sum(L*unit))*unit
    elif c['true_rank']:
        oracle_loading[(support[:c['true_rank']],)*3]=1/np.sqrt(p)
    else:
        oracle_loading[support[0],support[0],support[0]]=1/np.sqrt(p)
    oracle_sd=tau*np.linalg.norm(oracle_loading)
    for b in range(B):
        z=A+tau*rng_for(c['id'],b).normal(size=A.shape)
        auxiliary=tau*rng_for(c['id'],b,1).normal(size=A.shape)
        t=time.perf_counter();direct=float(z[ids,ids,ids].sum()/np.sqrt(p));seconds[b,0]=time.perf_counter()-t
        ep[b,0]=symmetric(direct,tau*norm.isf(LEVELS/2));est[b,0]=direct
        t=time.perf_counter();safe,uncorrected,detail,center_t=pointwise_levels(z,M,r,auxiliary,tau)
        seconds[b,1]=time.perf_counter()-t
        ep[b,1]=safe;est[b,1]=scalar_companion(safe[1],direct,M*np.sqrt(r/p),tau)
        choices[detail[1]['selected']]+=1;biases.append(detail[1]['bias']);tangent_norms.append(detail[1]['tangent_norm'])
        ep[b,5]=uncorrected;est[b,5]=center_t
        t=time.perf_counter();comp=xch_pca(z,L,r,tau);seconds[b,2]=time.perf_counter()-t;seconds[b,3]=seconds[b,2]
        for j,sd in [(2,comp['sd']),(3,comp['sd_plugin'])]:
            ep[b,j]=symmetric(comp['estimate'],norm.isf(LEVELS/2)*sd);est[b,j]=comp['estimate']
        oracle=float(np.sum(oracle_loading*z));est[b,4]=oracle
        ep[b,4]=symmetric(oracle,norm.isf(LEVELS/2)*oracle_sd)
        pivots[b]=[(direct-target)/tau,(comp['estimate']-target)/max(comp['sd'],1e-300),
                   (comp['estimate']-target)/max(comp['sd_plugin'],1e-300),(oracle-target)/oracle_sd]
        if len(names)>6:
            for ai,alpha in enumerate(LEVELS):
                t=time.perf_counter()
                out=old.adaptive_interval(z+auxiliary,z-auxiliary,L,M,v1=np.sqrt(2)*tau,v2=np.sqrt(2)*tau,
                                          alpha=float(alpha),delta=float(alpha/5))
                seconds[b,6]+=time.perf_counter()-t
                ep[b,6,ai]=[out['lo'],out['hi']]
                if ai==1:est[b,6]=out['center'];ranks[str(out['ranks'])]+=1
    scope={'xch_known':'asymptotic_regular_signal','xch_plugin':'asymptotic_regular_signal',
           'oracle':'oracle','split_unprotected':'ablation_no_guarantee'}
    if r<c['true_rank']:scope['pointwise']='outside_supplied_rank'
    # A separated-class guarantee is only assigned if the minimum singular
    # value passes the strongest of the three prescribed pilot thresholds.
    eta=old.pilot_envelope(A.shape,np.sqrt(2)*tau,min(LEVELS)/5).max()
    min_signal=min((np.linalg.svd(np.moveaxis(A,k,0).reshape(p,-1),compute_uv=False)[c['true_rank']-1]
                    for k in range(3)),default=0.) if c['true_rank'] else np.inf
    scope['separated_selector']='finite_sample' if min_signal>2*eta else 'outside_separation'
    np.savez_compressed(ROOT/'results'/('diagnostics_'+c['id']+'.npz'),pivots=pivots,biases=biases,tangent_norms=tangent_norms)
    return save_intervals(c,names,ep,est,target,seconds,scope,extra=dict(M=M,tau=tau,
        actual_rank=c['true_rank'],supplied_rank=r,choices95=dict(choices),selected_ranks95=dict(ranks),
        mean_bias=float(np.mean(biases)),mean_tangent_norm=float(np.mean(tangent_norms)),
        pointwise_rate=tau*np.sqrt(r/p) if c['regime']=='P1' else None,
        P1_signal_bound=high.pointwise_amplitude_bound(p,r,tau),min_nonzero_singular=float(min_signal) if np.isfinite(min_signal) else None,
        oracle='Known support with unknown amplitudes, or known complete direction for rotated signals.',
        pointwise_estimator='Risk-controlled scalar companion using the 95% interval; Proposition R1. No pointwise-minimax MSE claim.',
        input_bytes=A.nbytes,timing='All three levels share factor decompositions; xch_known/plugin share computation.'))


def noise_sample(rng,shape,law):
    if law in ['t3','t5']:
        df=int(law[-1]);return rng.standard_t(df,size=shape)*np.sqrt((df-2)/df)
    if law=='rademacher':return rng.choice([-1.,1.],size=shape)
    if law in ['rare_variance','variance_01','variance_05']:
        prob=.01 if law in ['rare_variance','variance_01'] else .05
        scale=50. if law=='rare_variance' else 10.
        return rng.normal(size=shape)*np.where(rng.random(size=shape)<prob,scale,1.)/np.sqrt(1+prob*(scale**2-1))
    if law=='mean_shift':
        return rng.normal(size=shape)+10*(rng.random(size=shape)<.05)
    return rng.normal(size=shape)


def noise_stress(c):
    p,B,law,rho=c['p'],c['B'],c['law'],c['rho'];rng=rng_for(c['id'])
    x=noise_sample(rng,(B,p),law)
    if rho:x=np.sqrt(1-rho)*x+np.sqrt(rho)*rng.normal(size=(B,1))
    y=x.sum(axis=1)/np.sqrt(p)
    ep=np.empty((B,2,3,2));est=np.column_stack((y,y))
    ep[:,0]=symmetric(y[:,None],norm.isf(LEVELS/2))
    scope={}
    if law=='gaussian':
        rad=norm.isf(LEVELS/2)*np.sqrt(1+(p-1)*rho)
        calibration='Exact known Gaussian covariance'
    elif law in ['t3','t5']:
        rad=1/np.sqrt(LEVELS);calibration='Known variance Chebyshev baseline; not a Gaussian or sub-Gaussian claim'
    elif law in ['variance_01','variance_05']:
        prob=.01 if law=='variance_01' else .05
        proxy=10/np.sqrt(1+prob*99)
        rad=proxy*np.sqrt(2*np.log(2/LEVELS));calibration='Known joint sub-Gaussian proxy from maximum mixture scale'
    elif law=='rademacher':
        rad=np.sqrt(2*np.log(2/LEVELS));calibration='Known joint sub-Gaussian proxy one'
    else:
        rad=np.sqrt(1+100*.05*.95)*norm.isf(LEVELS/2)
        calibration='Variance corrected but mean shift ignored: deliberately invalid'
        scope['calibrated']='outside_centered_noise'
    if law!='gaussian' or rho:scope['iid_gaussian']='outside_iid_gaussian'
    ep[:,1]=symmetric(y[:,None],rad)
    return save_intervals(c,['iid_gaussian','calibrated'],ep,est,0.,scope=scope,extra=dict(calibration=calibration))


def median_scans(c):
    B,n=c['B'],c['n'];law=c['law']
    template=global_fit.BinaryRankOneOptimizer(np.zeros((2,2,2)),np.zeros((2,2,2)),1.)
    nets={s:template.directions[template.levels==s] for s in [1,2]}
    counts={s:len(d) for s,d in nets.items()}
    params=[old.mom_parameters(counts,n,beta=float(a)) for a in LEVELS]
    passed=np.ones((B,3),bool);mean_pass=np.ones((B,3),bool);ratio=np.zeros((B,3));timing=[]
    for b in range(B):
        rng=rng_for(c['id'],b);x=noise_sample(rng,(n,8),law)
        if law=='ar1':
            for j in range(1,n):x[j]=.5*x[j-1]+np.sqrt(.75)*x[j]
        started=time.perf_counter()
        for ai,alpha in enumerate(LEVELS):
            for s,directions in nets.items():
                cfg=params[ai][s]
                blocks=x[:cfg['b']*cfg['k']].reshape(cfg['b'],cfg['k'],8).mean(axis=1)
                med=np.median(np.einsum('bd,ud->bu',blocks,directions,optimize=False),axis=0)
                r=float(np.max(np.abs(med))/cfg['threshold'])
                ratio[b,ai]=max(ratio[b,ai],r);passed[b,ai]&=r<=1
                bound=np.sqrt(2*np.log(4*len(directions)/alpha)/n)
                mean_pass[b,ai]&=np.max(np.abs(np.einsum('d,ud->u',x.mean(axis=0),directions,optimize=False)))<=bound
        timing.append(time.perf_counter()-started)
    rows=[]
    for name,values in [('directional_mom',passed),('gaussian_mean_scan',mean_pass)]:
        for ai,alpha in enumerate(LEVELS):
            k=int(values[:,ai].sum())
            valid=(name=='directional_mom' and law!='ar1') or (name=='gaussian_mean_scan' and law=='gaussian')
            rows.append(dict(case=c['id'],suite='S06',method=name,alpha=float(alpha),repetitions=B,covered=k,
                coverage=k/B,coverage_wilson_95=wilson(k,B),coverage_mcse=float(np.sqrt(k/B*(1-k/B)/B)),
                metric='Simultaneous full-net feasibility',guarantee='finite_sample' if valid else 'outside_tail_or_replication_assumption',status='NEEDS CHECK'))
    np.savez_compressed(ROOT/'results'/(c['id']+'.npz'),mom_pass=passed,mean_pass=mean_pass,ratio=ratio,seconds=timing)
    write_json(ROOT/'results'/(c['id']+'.json'),dict(case=c,records=rows,extra=dict(scan_directions=sum(counts.values()),
        params=params,mean_seconds=float(np.mean(timing)),max_threshold_ratio=float(ratio.max()),
        scope='Full-net event component only; general robust interval optimizer remains unimplemented.')))
    return rows


def weights(p,profile):
    i=np.arange(1,p+1,dtype=float)
    if profile.startswith('power_'):w=i**(-int(profile[-3:])/100)
    elif profile=='spike':w=np.r_[1.,np.full(p-1,.01)]
    elif profile=='log':w=1/np.log(np.e*i)
    elif profile=='plateau':w=np.where(i<=np.sqrt(p),1.,.1)
    else:w=np.ones(p)
    w*=np.where(np.arange(p)%2, -1.,1.)
    return w/np.linalg.norm(w)


def loadings(c):
    p,M=c['p'],c['M'];w=weights(p,c['profile']);largest=float(np.max(np.abs(w)))
    bounds=[]
    for K in [3,4]:
        value=high.dyadic_envelope(w,M,order=K)
        bounds.append(dict(K=K,upper_diameter=value['upper_diameter'],block_diameter=value['block_diameter'],
            direct_diameter=value['direct_diameter'],structural_diameter=value['structural_diameter'],
            H=value['profile_H'],largest=largest,two_point_scale=largest*min(M,1.),
            sharp_scale_claim=c['profile'].startswith('power_') or M<=1,
            analytic_only=True))
    if c['B']:
        B=c['B'];target=M*largest;y=target+rng_for(c['id']).normal(size=B)
        ep=np.empty((B,2,3,2));ep[:,0]=symmetric(y[:,None],norm.isf(LEVELS/2))
        ep[:,1]=symmetric(np.zeros((B,3)),target)
        return save_intervals(c,['direct','loading_structural'],ep,np.column_stack((y,np.zeros(B))),target,
            extra=dict(bounds=bounds,rho=largest,rate=M*largest,loading='Prescribed alternating signed orthogonal weights'))
    write_json(ROOT/'results'/(c['id']+'.json'),dict(case=c,records=[],extra=dict(bounds=bounds,
        status='NEEDS CHECK',interpretation='Analytic envelopes only; no fitted interval or empirical rate attainment.')))
    return []


def optimizer(c):
    K,B=c['K'],c['B'];rng=rng_for(c['id'],stream=5)
    L=high.flat_loading(2,K) if c['loading']=='flat' else rng.normal(size=(2,)*K)
    L=L/np.linalg.norm(L)
    signal=c['signal'];M=20. if signal=='strong' else .2 if signal=='zero' else 2.
    tau=.3 if signal=='strong' else 1.
    amp={'zero':0.,'weak':.8,'boundary':2.,'strong':15.}[signal]
    pars=np.r_[amp,[0.,0.,0.] if signal=='boundary' else [.4,.9,1.2]]
    A=global_fit.rank_one(pars);target=float(np.sum(A*L))
    names=['direct']+[f'global_{n}' for n in c['budgets']]+['norm_structural']
    ep=np.empty((B,len(names),3,2));est=np.empty((B,len(names)));secs=np.zeros((B,len(names)))
    records=[]
    for b in range(B):
        z=A+tau*rng_for(c['id'],b).normal(size=A.shape);direct=float(np.sum(z*L))
        ep[b,0]=symmetric(direct,norm.isf(LEVELS/2)*tau);est[b,0]=direct
        ep[b,-1]=symmetric(np.zeros(3),M);est[b,-1]=0.
        # Each confidence level is actually solved; observations are paired.
        for ai,alpha in enumerate(LEVELS):
            for j,(nodes,tol) in enumerate(zip(c['budgets'],c['tolerances']),start=1):
                t=time.perf_counter();fit=global_fit.BinaryRankOneOptimizer(z,L,M,tau,float(alpha))
                result=fit.project_interval(tolerance=tol*tau,max_nodes=nodes)
                secs[b,j]+=time.perf_counter()-t
                ep[b,j,ai]=[result['lo'],result['hi']]
                if ai==1:est[b,j]=(result['lo']+result['hi'])/2
                records.append(dict(trial=b,alpha=float(alpha),budget=nodes,tolerance=tol*tau,**result))
    return save_intervals(c,names,ep,est,target,secs,extra=dict(M=M,tau=tau,solver_trials=records,
        arithmetic='Existing float64 conservative guards; no formal interval arithmetic.',
        estimator='Interval midpoint, not the all-budget MSE residual estimator.'))


def corrections(c):
    B,p,M,K=c['B'],c['p'],c['M'],c['K'];rng=rng_for(c['id'])
    names=['direct','corrected','omitted_correction'];ep=np.empty((B,3,3,2));est=np.empty((B,3))
    if c['kind']=='loading':
        eps=c['epsilon'];a=np.sqrt(1-eps**2)
        # A=M e_0 x e_1 x e_2 x e_3: rank one, off-diagonal target eps*M.
        d=rng.normal(size=(B,p));off=M+rng.normal(size=B);target=eps*M
        direct=a*d.sum(axis=1)/np.sqrt(p)+eps*off
        for ai,alpha in enumerate(LEVELS):
            lam=np.sqrt(2*np.log(4*p/alpha));q_res=norm.isf(alpha/4);q_dir=norm.isf(alpha/2)
            hnl=M**(2/K)*(2*lam)**(1-2/K)/np.sqrt(p)
            cnl=(np.sign(d)*np.maximum(np.abs(d)-lam,0)).sum(axis=1)/np.sqrt(p)
            radii=[a*hnl+eps*q_res,q_dir,min(M,M*(a/np.sqrt(p)+eps))]
            j=int(np.argmin(radii));center=[a*cnl+eps*off,direct,np.zeros(B)][j]
            ep[:,0,ai]=symmetric(direct,q_dir);ep[:,1,ai]=symmetric(center,radii[j])
            ep[:,2,ai]=symmetric(a*cnl,a*hnl)
            if ai==1:est[:,0]=direct;est[:,1]=center;est[:,2]=a*cnl
    else:
        eta=c['eta'];d=rng.normal(size=(B,p))+eta/np.sqrt(p);d[:,0]+=M
        target=M/np.sqrt(p)+eta;direct=d.sum(axis=1)/np.sqrt(p)
        for ai,alpha in enumerate(LEVELS):
            q=norm.isf(alpha/2);lam=np.sqrt(2*np.log(2*p/alpha))
            for j,allow in [(1,eta),(2,0.)]:
                threshold=lam+allow
                cnl=(np.sign(d)*np.maximum(np.abs(d)-threshold,0)).sum(axis=1)/np.sqrt(p)
                radii=[M**(2/K)*(2*threshold)**(1-2/K)/np.sqrt(p)+allow,q,M/np.sqrt(p)+allow]
                choice=int(np.argmin(radii));center=[cnl,direct,np.zeros(B)][choice]
                ep[:,j,ai]=symmetric(center,radii[choice])
                if ai==1:est[:,j]=center
            ep[:,0,ai]=symmetric(direct,q)
            if ai==1:est[:,0]=direct
    return save_intervals(c,names,ep,est,target,scope={'omitted_correction':'ablation_no_guarantee'},
        extra=dict(construction='Conservative executable transfer/threshold construction; not the sharp ideal full-data fit.'))


DISPATCH={'S01':scalar_growing,'S02':threshold,'S03':tensors,'S04':tensors,'S05':noise_stress,
          'S06':median_scans,'S07':loadings,'S08':optimizer,'S09':corrections,'S10':tensors}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--suite',required=True,choices=list(DISPATCH));args=parser.parse_args()
    cases=load_cases(args.suite);started=time.time()
    manifest=dict(seed=SEED,suite=args.suite,started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
                  source_hashes=hashes(),python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,
                  registered_cases=[c['id'] for c in cases],status='RUNNING')
    write_json(ROOT/'logs'/f'run_{args.suite}.json',manifest)
    with threadpool_limits(limits=1):
        manifest['threadpools']=threadpool_info()
        try:
            for c in cases:
                t=time.perf_counter();rows=DISPATCH[args.suite](c)
                print(c['id'],'B',c['B'],'rows',len(rows),'seconds',round(time.perf_counter()-t,3),flush=True)
        except Exception as exc:
            manifest.update(status='FAILED',exception=repr(exc),failed_case=c['id'],seconds=time.time()-started)
            write_json(ROOT/'logs'/f'run_{args.suite}.json',manifest)
            raise
    manifest.update(status='COMPLETED',seconds=time.time()-started)
    write_json(ROOT/'logs'/f'run_{args.suite}.json',manifest)


if __name__=='__main__':main()
