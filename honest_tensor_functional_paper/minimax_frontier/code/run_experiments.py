"""New full-observation experiments. Configurations are saved before draws."""
import json
import time
import platform
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import qr
from scipy.stats import norm
from threadpoolctl import threadpool_limits
from methods import spectral_plan, spectral_interval, adaptive_coordinate_interval, orthogonal_rate
from numerics import coverage_events

ROOT=Path(__file__).resolve().parents[1]
B=2000


def summary(lo,hi,truth,estimate=None):
    strict=(lo<=truth)&(truth<=hi);covered=coverage_events(lo,hi,truth);n=len(lo);p=float(np.mean(covered));z=norm.isf(.025)
    den=1+z*z/n;mid=(p+z*z/(2*n))/den;half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    width=hi-lo
    out=dict(replications=n,coverage=p,covered=int(np.sum(covered)),strict_covered=int(np.sum(strict)),
             rounding_changed=int(np.sum(covered!=strict)),wilson_low=mid-half,wilson_high=mid+half,
             mean_width=float(np.mean(width)),width_mcse=float(np.std(width,ddof=1)/np.sqrt(n)),
             min_width=float(np.min(width)),max_width=float(np.max(width)))
    if estimate is not None:
        loss=(estimate-truth)**2
        out.update(mse=float(np.mean(loss)),mse_mcse=float(np.std(loss,ddof=1)/np.sqrt(n)),max_squared_loss=float(np.max(loss)))
    return out


def make_loading(p,profile,seed):
    rng=np.random.default_rng(seed);U=qr(rng.normal(size=(p,p)),mode='economic')[0]
    V=qr(rng.normal(size=(p*p,p)),mode='economic')[0]
    s={'flat':np.ones(p),'spike_tail':np.r_[1.,np.full(p-1,.12)],
       'log_decay':(1+np.log(np.arange(1,p+1)))**-.7}[profile]
    s/=np.linalg.norm(s)
    # Dense singular vectors: this loading is not an orthogonal CP loading.
    L=np.einsum('ik,k,jk->ij',U,s,V,optimize=False).reshape(p,p,p)
    return L,U,s,V


def spectral_run(c):
    rng=np.random.default_rng(c['seed']);p,r,M=c['p'],c['rank'],c['M']
    L,U,s,V=make_loading(p,c['profile'],9152620+p)
    plan=spectral_plan(L,M,r,mode=0);mu=np.zeros_like(L)
    if c['signal']=='worst_bias':
        if plan['selected']=='structural':residual=s.copy()
        else:residual=np.minimum(s,plan['ci_optimizer']['threshold'])
        if np.linalg.norm(residual[:r])<1e-12:residual=s.copy()
        values=np.r_[M*residual[:r]/np.linalg.norm(residual[:r]),np.zeros(p-r)]
        mu=np.einsum('ik,k,jk->ij',U,values,V,optimize=False).reshape(L.shape)
    elif c['signal']=='dense_random':
        X=qr(rng.normal(size=(p,r)),mode='economic')[0];Y=qr(rng.normal(size=(p*p,r)),mode='economic')[0]
        values=rng.uniform(.1,1,r);values*=M/np.linalg.norm(values)
        mu=np.einsum('ik,k,jk->ij',X,values,Y,optimize=False).reshape(L.shape)
    truth=float(np.sum(L*mu));z=rng.normal(size=(c['B'],)+L.shape)+mu
    # Batch the same fixed linear contractions as the public API; verify
    # independent scalar API calls against five observations in each case.
    center=np.einsum('bijk,ijk->b',z,plan['ci_loading'],optimize=False)
    h=plan['structural'];lo=np.maximum(-h,center-plan['radius']);hi=np.minimum(h,center+plan['radius']);empty=lo>hi
    lo[empty]=0;hi[empty]=0
    estimate=np.clip(np.einsum('bijk,ijk->b',z,plan['estimate_loading'],optimize=False),-h,h)
    direct_center=np.einsum('bijk,ijk->b',z,L,optimize=False);rd=norm.isf(.025)
    dl=np.maximum(-h,direct_center-rd);dh=np.minimum(h,direct_center+rd);de=dl>dh;dl[de]=0;dh[de]=0
    direct_estimate=np.clip(direct_center,-h,h)
    for j in range(5):
        api=spectral_interval(z[j],plan)
        assert np.allclose([api['lo'],api['hi'],api['estimate']],[lo[j],hi[j],estimate[j]],rtol=1e-11,atol=1e-11)
    np.savez_compressed(ROOT/'results'/f"{c['id']}.npz",lo=lo,hi=hi,estimate=estimate,direct_lo=dl,direct_hi=dh,direct_estimate=direct_estimate,truth=truth)
    return {**c,'truth':truth,'mean_norm':float(np.linalg.norm(mu)),'method':summary(lo,hi,truth,estimate),
            'direct':summary(dl,dh,truth,direct_estimate),'empty_count':int(np.sum(empty)),
            'rate_proxy':plan['rate'],'radius':plan['radius'],'mse_upper':plan['mse_upper'],
            'selected':plan['selected'],'optimizer_relative_gap':plan['risk_optimizer']['gap']/max(1e-300,plan['risk_optimizer']['primal'])}


def point_run(c):
    rng=np.random.default_rng(c['seed']);K,p,a,d=c['K'],c['p'],c['a'],c['distance'];shape=(p,)*K
    anchor=tuple(rng.integers(0,p,K));target=tuple((j+1)%p if k<d else j for k,j in enumerate(anchor))
    mu=np.zeros(shape);mu[anchor]=a
    if c['signal']=='dense_rank_one':
        factors=[]
        for k in range(K):
            v=rng.normal(size=p);v[anchor[k]]+=2;v/=np.linalg.norm(v);factors.append(v)
        mu=a*factors[0]
        for v in factors[1:]:mu=np.multiply.outer(mu,v)
    if c['signal']=='rank_two_violation':mu[target]=5.
    M=c['M'];truth=float(mu[target]);lo=np.empty(c['B']);hi=lo.copy();dl=lo.copy();dh=lo.copy()
    chosen=np.zeros(c['B'],bool);ratio=chosen.copy();empty=chosen.copy();selected_distance=np.zeros(c['B'],int)
    for i in range(c['B']):
        z=mu+rng.normal(size=shape);out=adaptive_coordinate_interval(z,target,M,rng)
        lo[i],hi[i]=out['lo'],out['hi'];chosen[i]=out['anchor']==anchor;ratio[i]=out['ratio'];empty[i]=out['empty'];selected_distance[i]=out['distance']
        dl[i],dh[i]=max(-M,z[target]-norm.isf(.025)),min(M,z[target]+norm.isf(.025))
        if dl[i]>dh[i]:dl[i]=dh[i]=0
    np.savez_compressed(ROOT/'results'/f"{c['id']}.npz",lo=lo,hi=hi,direct_lo=dl,direct_hi=dh,truth=truth,correct_anchor=chosen,ratio=ratio,empty=empty,selected_distance=selected_distance)
    return {**c,'truth':truth,'anchor':anchor,'target':target,'mean_norm':float(np.linalg.norm(mu)),
            'method':summary(lo,hi,truth),'direct':summary(dl,dh,truth),
            'correct_anchor_frequency':float(np.mean(chosen)),'ratio_frequency':float(np.mean(ratio)),
            'empty_count':int(np.sum(empty)),'pointwise_proxy':1. if d<=1 or a==0 else abs(a)**(1-d)}


def analytic_run():
    rows=[]
    for p in [16,256,4096,65536]:
        for M in [.3,1.,3.,10.,100.,1000.]:
            for beta in [0.,.25,.5,.75,1.5]:
                w=(1+np.log(np.arange(1,p+1)))**(-beta);w/=np.linalg.norm(w)
                rate=orthogonal_rate(w,M);F=np.minimum(M,np.sqrt(1+np.log(np.arange(1,p+1))));prefix=float(np.max(w*F))
                rows.append(dict(p=p,M=M,beta=beta,rate=rate['rate'],old_prefix_lower_proxy=prefix,
                                 A_over_B=rate['rate']/prefix,geometric_proxy=rate['geometric_proxy']))
    (ROOT/'results/analytic_profiles.json').write_text(json.dumps(rows,indent=2)+'\n')
    # This is a symbolic rate calculation, not high-dimensional fitting.
    rows=[]
    for p in [16,64,256,1024,4096,16384,65536,262144]:
        for r in sorted(set([1,2,4,8,int(np.sqrt(p)),p//4,p])):
            if r>p:continue
            for M in [.3,1.,3.,np.sqrt(p),10*np.sqrt(p)]:
                rows.append(dict(p=p,rank=r,M=float(M),one_cap_rate=float(min(M*np.sqrt(r/p),1.)),
                                 fixed_cap_order4_rate=float(min(M,np.sqrt(1+np.log(p)))/np.sqrt(p)),
                                 comparison_valid_as_same_rank_class=(r==1)))
    (ROOT/'results/analytic_caps.json').write_text(json.dumps(rows,indent=2)+'\n')


def timing_run():
    rows=[]
    for shape in [(16,16,16),(32,32,32),(64,64,64),(32,64,1024)]:
        rng=np.random.default_rng(9152699+sum(shape));L=rng.normal(size=shape);L/=np.linalg.norm(L);z=rng.normal(size=shape)
        prep=[];obs=[]
        for _ in range(3):
            start=time.perf_counter();plan=spectral_plan(L,3.,1,mode=0);prep.append(time.perf_counter()-start)
            start=time.perf_counter();spectral_interval(z,plan);obs.append(time.perf_counter()-start)
        rows.append(dict(shape=shape,entries=int(np.prod(shape)),input_mebibytes=8*np.prod(shape)/2**20,
                         preprocessing_median_seconds=float(np.median(prep)),observation_median_seconds=float(np.median(obs)),repeats=3,
                         optimizer_relative_gap=plan['risk_optimizer']['gap']/max(plan['risk_optimizer']['primal'],1e-300)))
    (ROOT/'results/timing.json').write_text(json.dumps(rows,indent=2)+'\n')


def main():
    configs=[]
    for profile in ['flat','spike_tail','log_decay']:
        for r in [1,4,16]:
            for M in [.3,3.,30.]:
                for signal in ['zero','worst_bias','dense_random']:
                    configs.append(dict(family='spectral',p=16,rank=r,M=M,profile=profile,signal=signal,B=B))
    for K,p in [(3,4),(4,4),(5,3)]:
        for d in range(K+1):
            for a in [3.,10.,30.,100.,1000.]:
                configs.append(dict(family='coordinate',K=K,p=p,a=a,distance=d,M=1000.,signal='axis',B=B))
    for a,signal in [(0.,'axis'),(-100.,'axis'),(30.,'dense_rank_one'),(1000.,'rank_two_violation')]:
        configs.append(dict(family='coordinate',K=4,p=4,a=a,distance=4,M=1001.,signal=signal,B=B))
    for j,c in enumerate(configs):c.update(id=f'F{j:03d}',seed=9152700+j)
    (ROOT/'results/configurations.json').write_text(json.dumps(configs,indent=2)+'\n')
    results=[];start=time.perf_counter()
    with threadpool_limits(limits=1):
        for j,c in enumerate(configs):
            results.append(spectral_run(c) if c['family']=='spectral' else point_run(c))
            if j%10==0:print(f"Completed {j+1}/{len(configs)} configurations",flush=True)
        analytic_run();timing_run()
    (ROOT/'results/simulation_results.json').write_text(json.dumps(results,indent=2,default=lambda x:int(x) if isinstance(x,np.integer) else str(x))+'\n')
    meta=dict(date='2026-09-15',python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,
              platform=platform.platform(),seconds=time.perf_counter()-start,configurations=len(configs),
              unique_mc_datasets=sum(c['B'] for c in configs),seed_rule='9152700 + configuration index',
              threads=1,noise='iid N(0,1), full observation arrays generated',
              saved='All interval endpoints and scalar losses recoverable; deterministic seeds regenerate observations.',
              real_data='No new application run; scientific_extension EEG results preserved.')
    (ROOT/'results/run_metadata.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta,indent=2),flush=True)


if __name__=='__main__':main()
