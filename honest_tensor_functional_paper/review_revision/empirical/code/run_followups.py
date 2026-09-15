"""Explicitly registered diagnostic additions; never overwrite primary data."""
import hashlib
import json
import time
import numpy as np
from scipy.stats import norm,binom,kstest
from common import ROOT,PROJECT,LEVELS,SEED,high,rng_for,save_intervals,symmetric,write_json,load_cases
from run_study import tensor_signal


def main():
    cases=json.loads((ROOT/'configs/followup_cases.json').read_text())['cases']
    started=time.time();sources=[ROOT/'code/run_followups.py',ROOT/'code/common.py',ROOT/'code/run_study.py',
         ROOT/'code/tensor_methods.py',ROOT/'configs/followup_cases.json',PROJECT/'high_dimensional_extension/code/methods.py']
    hs={str(p.relative_to(PROJECT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    for c in cases:
        B,p=c['B'],c['p'];rng=rng_for(c['id']);rd=norm.isf(LEVELS/2)
        if c['suite']=='S12':
            r,M=c['rank'],c['M'];h=M*np.sqrt(r/p)
            b=min(M/np.sqrt(r),np.sqrt(np.log1p(p/(4*r*r))))
            target=r*b/np.sqrt(p)
            g1,g2=rng.normal(size=(2,B))
            observed=target+np.sqrt(r/p)*g1+np.sqrt(1-r/p)*g2
            oracle=target+np.sqrt(r/p)*g1
            ep=np.empty((B,4,3,2));est=np.empty((B,4))
            ep[:,0]=symmetric(observed[:,None],rd)
            ep[:,1]=symmetric(np.where(h<=rd,0.,observed[:,None]),np.minimum(h,rd))
            ep[:,2]=symmetric(oracle[:,None],rd*np.sqrt(r/p))
            ep[:,3]=symmetric(np.zeros((B,3)),h)
            est[:,0]=observed;est[:,1]=0. if h<=1 else observed;est[:,2]=oracle;est[:,3]=0.
            lower=high.growing_lower(p,r,M)
            save_intervals(c,['direct','cap_upper','support_oracle','structural'],ep,est,target,
                scope={'support_oracle':'oracle'},extra=dict(length_lower=lower['length_lower'],
                minimax_claim='Only r >= c sqrt(p); intermediate rows are unmatched upper/lower diagnostics',
                amplitude=b,rank_over_sqrt_p=r/np.sqrt(p),observation='Exact joint Gaussian diagonal-sum and support-sum marginals'))
        else:
            d=rng.normal(size=(B,p));y=d.sum(axis=1)/np.sqrt(p)
            ep=symmetric(y[:,None,None],rd[None,None,:])
            save_intervals(c,['direct_confirmation'],ep,y[:,None],0.,extra=dict(
                post_hoc=True,primary_case='S03_007',source='New fixed seed, exact diagonal observations; does not replace primary outcomes'))
        print(c['id'],'complete',flush=True)
    original=next(c for c in load_cases() if c['id']=='S03_007')
    A,M,_,_=tensor_signal(original);p=original['p'];ids=np.arange(p);target=A[ids,ids,ids].sum()/np.sqrt(p)
    expected=[];pivots=[]
    for b in range(original['B']):
        G=rng_for(original['id'],b).normal(size=A.shape)
        noise=G[ids,ids,ids].sum()/np.sqrt(p)
        expected.append(target+noise);pivots.append(noise)
    saved=np.load(ROOT/'results/S03_007.npz')['estimates'][:,0]
    difference=float(np.max(np.abs(np.asarray(expected)-saved)))
    assert difference<1e-8
    k=int((np.abs(pivots)<=norm.isf(.025)).sum());N=len(pivots)
    reference=json.loads((ROOT/'results/S03_007.json').read_text())
    reference=next(r for r in reference['records'] if r['method']=='direct' and r['alpha']==.05)
    assert k==reference['covered']
    check=dict(status='VALIDATED',original_case='S03_007',full_noise_regenerated=True,
               maximum_center_discrepancy=difference,covered95=k,repetitions=N,
               original_one_sided_binomial_pvalue=float(binom.cdf(k,N,.95)),
               original_pivot_mean=float(np.mean(pivots)),original_pivot_variance=float(np.var(pivots,ddof=1)),
               original_pivot_ks_distance=float(kstest(pivots,'norm').statistic),
               confirmation_case='S13_000',interpretation='Original low coverage is retained. Independent confirmation is a separate post-hoc diagnostic, not a replacement.')
    write_json(ROOT/'results/gaussian_diagnostic.json',check)
    for s in ['S12','S13']:
        write_json(ROOT/'logs'/('run_'+s+'.json'),dict(status='COMPLETED',seed=SEED,source_hashes=hs,
                 registered_cases=[c['id'] for c in cases if c['suite']==s],seconds=time.time()-started,
                 timing_scope='Combined follow-up wall time; do not sum twice',post_hoc_registered=True))


if __name__=='__main__':main()
