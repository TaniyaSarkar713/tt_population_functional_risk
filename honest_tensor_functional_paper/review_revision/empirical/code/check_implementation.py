"""Known-answer and independent numerical checks before Monte Carlo runs."""
import json
import warnings
import numpy as np
from scipy.stats import norm
from common import ROOT, LEVELS, high, old, global_fit, rng_for, write_json, load_cases
from tensor_methods import mode_multiply, reduce, xch_pca, pointwise_levels
from run_study import tensor_signal, weights


def main():
    warnings.simplefilter('error',RuntimeWarning)
    rng=np.random.default_rng(614209);passed=[]
    def check(name,condition):
        if not condition:raise AssertionError(name)
        passed.append(name)
    for j in range(12):
        p=4;r=1+j%3;tau=.4+.2*(j%3);M=20.
        z=rng.normal(size=(p,)*3)*(1 if j<6 else 100)
        seed=314+j
        aux=tau*np.random.default_rng(seed).normal(size=z.shape)
        calculated=pointwise_levels(z,M,r,aux,tau)[0]
        for ai,a in enumerate(LEVELS):
            exact=high.pointwise_interval(z,M,r,np.random.default_rng(seed),tau,float(a))
            check(f'cached_pointwise_{j}_{a}',np.allclose(calculated[ai],[exact['lo'],exact['hi']],atol=2e-12,rtol=2e-12))
    for r in [1,2,3]:
        p=4;bases=[np.linalg.qr(rng.normal(size=(p,r)))[0] for _ in range(3)]
        core=rng.normal(size=(r,)*3);A=core
        for k,U in enumerate(bases):A=mode_multiply(A,U,k)
        L=rng.normal(size=A.shape);L/=np.linalg.norm(L)
        out=xch_pca(A,L,r)
        check(f'xch_noiseless_reconstruction_r{r}',abs(out['estimate']-np.sum(A*L))<1e-11)
        # Independent Jacobian basis for the exact fixed-rank Tucker manifold.
        fitted_bases=out['bases'];fitted_core=reduce(A,fitted_bases);vectors=[]
        for ind in np.ndindex(fitted_core.shape):
            C=np.zeros_like(fitted_core);C[ind]=1.
            for k,U in enumerate(fitted_bases):C=mode_multiply(C,U,k)
            vectors.append(C.ravel())
        for k,U in enumerate(fitted_bases):
            complement=np.linalg.svd(U.T,full_matrices=True)[2][r:].T
            for i in range(p-r):
                for col in range(r):
                    derivative=np.zeros_like(U);derivative[:,col]=complement[:,i]
                    C=fitted_core.copy()
                    for l,V in enumerate(fitted_bases):C=mode_multiply(C,derivative if l==k else V,l)
                    vectors.append(C.ravel())
        Q=np.linalg.qr(np.stack(vectors,axis=1),mode='reduced')[0]
        check(f'exact_manifold_variance_r{r}',np.isclose(out['variance'],np.linalg.norm(np.einsum('ij,i->j',Q,L.ravel(),optimize=False))**2,rtol=1e-10,atol=1e-10))
    for j in range(20):
        p=4+j;r=min(p,1+j//3);M=.1+2*j;tau=.5
        d=rng.normal(size=p);out=high.growing_cap_interval(d,M,r,tau)
        h=M*np.sqrt(r/p);q=norm.isf(.025)*tau
        center=0. if h<=q else d.sum()/np.sqrt(p)
        check(f'growing_formula_{j}',np.allclose([out['lo'],out['hi']],[center-min(h,q),center+min(h,q)]))
    for c in load_cases():
        if c['suite'] in ['S03','S04','S10']:
            A,M,S,amps=tensor_signal(c)
            check(c['id']+'_norm',np.linalg.norm(A)<=M)
            rank=np.linalg.matrix_rank(A.reshape(c['p'],-1))
            check(c['id']+'_actual_rank',rank==c['true_rank'])
        if c['suite']=='S07':
            w=weights(c['p'],c['profile'])
            check(c['id']+'_loading_norm',np.isclose(np.linalg.norm(w),1.))
    template=global_fit.BinaryRankOneOptimizer(np.zeros((2,2,2)),high.flat_loading(2,3),1.)
    check('complete_projective_net_size',len(template.directions)==1002)
    check('unit_net_directions',np.allclose(np.linalg.norm(template.directions,axis=1),1.))
    for alpha in LEVELS:
        params=old.mom_parameters({1:2,2:1000},64,beta=alpha)
        check(f'mom_union_bound_{alpha}',sum(N*2.**(-params[s]['b']) for s,N in [(1,2),(2,1000)])<=alpha)
        check(f'mom_replication_{alpha}',all(v['b']%2==1 and v['k']>=2 for v in params.values()))
    for j in range(3):
        pars=np.r_[.3+j,[.2,.7,1.1]];A=global_fit.rank_one(pars);L=high.flat_loading(2,3)
        fit=global_fit.BinaryRankOneOptimizer(A,L,4.)
        out=fit.project_interval(tolerance=.5,max_nodes=15)
        target=np.sum(A*L)
        check(f'global_noiseless_outer_{j}',out['lo']<=target<=out['hi'])
        check(f'global_true_feasible_{j}',fit.objective(pars)==0.)
    # Exact Gaussian artificial-split covariance and scalar oracle covariance.
    G=rng.normal(size=(60000,2));P=G[:,0]+G[:,1];V=G[:,0]-G[:,1]
    check('artificial_split_variance',abs(P.var()-2)<.06 and abs(V.var()-2)<.06)
    check('artificial_split_independence_covariance',abs(np.cov(P,V)[0,1])<.04)
    check('case_ids_unique',len({c['id'] for c in load_cases()})==len(load_cases()))
    write_json(ROOT/'logs/implementation_checks.json',dict(status='PASSED',checks=len(passed),passed=passed,
        limitations='Finite numerical checks, not proofs or independent review. No Monte Carlo result was used to tune methods.'))
    print('Passed',len(passed),'known-answer checks.')


if __name__=='__main__':main()
