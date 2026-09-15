"""Finite independent checks of new identities and lower-bound constructions.

These checks do not replace the proofs or implement the ideal multi-cap fit.
"""
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar
from methods import (spectral_clip_solve, spectral_plan, spectral_interval,
                     balanced_partition, orthogonal_rate,
                     entropy_prior_certificate, _ratio_range, unfolding,
                     adaptive_coordinate_interval)

ROOT=Path(__file__).resolve().parents[1]


def run():
    rng=np.random.default_rng(9152601);counts={};worst_gap=0.;worst_ratio=0.
    def check(group,condition):
        counts[group]=counts.get(group,0)+1
        if not bool(condition):raise AssertionError((group,counts[group]))
    for n in [1,2,3,8,31,128]:
        for scale in [1e-9,1.,1e9]:
            for family in ['flat','random','spike','ties']:
                s={'flat':np.ones(n),'random':np.sort(rng.uniform(.01,1,n))[::-1],
                   'spike':np.r_[1.,np.zeros(n-1)],'ties':np.ceil(np.arange(n,0,-1)/3)/n}[family]*scale
                for a in [0.,.1,1.,2.,np.sqrt(n),2*np.sqrt(n)]:
                    for v in [0.,.3,1.,3.]:
                        sol=spectral_clip_solve(s,a,v);b=sol['dual_vector']
                        check('dual_feasibility',np.sum(b)<=a*(1+1e-14)+1e-300 and np.linalg.norm(b)<=v*(1+1e-14)+1e-300 and np.min(b)>=0)
                        gap=sol['gap']/max(sol['primal'],1e-300);worst_gap=max(worst_gap,gap)
                        check('primal_dual_gap',gap<1e-10)
                        obj=lambda t:a*t+v*np.linalg.norm(np.maximum(s-t,0))
                        # Independent bounded minimization on normalized spectrum.
                        other=minimize_scalar(lambda u:obj(u*scale),bounds=(0,s[0]/scale),method='bounded',options={'xatol':1e-13})
                        ref=min(obj(0),obj(s[0]),other.fun)
                        check('independent_convex_objective',abs(sol['primal']-ref)<=1e-8*max(ref,scale*1e-12))
    for n in [1,2,5,16,64]:
        for r in range(1,n+1):
            for _ in range(10):
                b=rng.exponential(size=n);groups,loads=balanced_partition(b,r)
                bound=np.sum(b)**2/r+(1-1/r)*np.sum(b*b)
                check('partition_squared_loads',np.sum(loads*loads)<=bound*(1+1e-13))
                check('partition_indices',sorted(sum(groups,[]))==list(range(n)))
    # Exhaustive sign-mixture likelihood calculation for small full matrices.
    for n in [2,3,5,7]:
        signs=np.array(list(itertools.product([-1.,1.],repeat=n)))
        for r in range(1,n+1):
            for M in [1.,2.,10.]:
                s=np.linspace(1,.2,n);sol=spectral_clip_solve(s,M*np.sqrt(r),1);b=sol['dual_vector'];groups,loads=balanced_partition(b,r)
                matrices=[]
                for sign in signs:
                    A=np.zeros((n,n))
                    for g in groups:
                        v=np.zeros(n);v[g]=np.sqrt(b[g])*sign[g];A+=np.outer(v,v)/8
                    matrices.append(A)
                    check('mixture_rank_norm',np.linalg.matrix_rank(A,tol=1e-9)<=r and np.linalg.norm(A)<=M*(1+1e-13))
                    check('mixture_common_target',abs(np.sum(np.diag(A)*s)-sol['dual']/8)<1e-12)
                # Products of two independent signs have the original sign law.
                exponents=np.zeros(len(signs))
                for g in groups:exponents+=np.sum(signs[:,g]*b[g],axis=1)**2/64
                chi=float(np.mean(np.expm1(exponents)))
                check('full_matrix_chi_square',chi<=np.expm1(1/62)*(1+1e-12))
    for p in [1,2,3,8,54,55,100,1000,10000]:
        for M in np.geomspace(.01,1e4,31):
            for family in ['flat','critical','power','step','random']:
                s=np.arange(1,p+1)
                w={'flat':np.ones(p),'critical':(1+np.log(s))**-.5,'power':s**-.3,
                   'step':(s<=max(1,p//3)).astype(float),'random':np.sort(rng.uniform(0,1,p))[::-1]}[family]
                out=orthogonal_rate(w,M);worst_ratio=max(worst_ratio,out['ratio'])
                check('multiscale_profile_comparison',out['ratio']<=np.sqrt(5)*(1+1e-13))
                F=np.minimum(M,np.sqrt(1+np.log(s)))
                abel=float(np.dot(w-np.r_[w[1:],0],F))
                check('abel_identity',abs(out['rate']-abel)<1e-11*max(1,abel))
    for K in [4,5,6,8]:
        for levels in range(9):
            cert=entropy_prior_certificate(K,levels)
            check('entropy_likelihood_certificate',cert['chi_square_upper']<.07 and cert['tv_upper']<.133)
    # Actual rank-one tensors, signed orthogonal weights, one entropy scale.
    for K in [4,5]:
        for _ in range(20):
            w=np.sort(rng.uniform(.1,1,3))[::-1];sign=rng.choice([-1,1],3)
            C=1+1/(1-4**(-1/K));eps=1/(16*C**(K/2));v=np.array([1.,1.,0.]);dv=v*sign
            A=eps*dv
            for _mode in range(K-1):A=np.multiply.outer(A,v)
            theta=sum(w[i]*sign[i]*A[(i,)*K] for i in range(3))
            check('entropy_prior_full_tensor',abs(theta-eps*(w[0]+w[1]))<1e-12 and np.linalg.norm(A)<1/16)
    # Two scales with 52 random positions and nontrivial weight compensation.
    p=55;K=4;w=(1+np.log(np.arange(1,p+1)))**-.5
    C=1+1/(1-4**(-1/K));eps=1/(16*C**(K/2));vs=[];dvs=[]
    for S in range(2,54):
        v=np.zeros(p);v[0]=1;v[1]=1;v[S]=4**(1/(2*K));dv=v.copy();dv[S]*=w[53]/w[S]
        check('multiscale_compensated_target',np.isclose(eps*np.sum(w*dv*v**(K-1)),eps*(w[0]+w[1]+2*w[53])))
        check('multiscale_product_norm',eps*np.linalg.norm(dv)*np.linalg.norm(v)**(K-1)<=2/16)
        vs.append(v);dvs.append(dv)
    inner=np.einsum('bi,ci->bc',vs,vs,optimize=False)**(K-1)*np.einsum('bi,ci->bc',dvs,dvs,optimize=False)*eps**2
    check('multiscale_exact_likelihood',np.mean(np.expm1(inner))<=entropy_prior_certificate(K,2)['chi_square_upper'])
    # Exact finite-group averaging in M2, using a small unrestricted W.
    p=3;W=rng.normal(size=(p,p,p));average=np.zeros_like(W)
    signs=list(itertools.product([-1.,1.],repeat=2*p))
    for sign in signs:
        s=np.array(sign).reshape(2,p)
        average+=W*s[0,:,None,None]*s[1,None,:,None]*(s[0]*s[1])[None,None,:]/len(signs)
    expected=np.zeros_like(W)
    for i in range(p):expected[i,i,i]=W[i,i,i]
    check('affine_sign_symmetrization',np.allclose(average,expected,atol=1e-14))
    perms=list(itertools.permutations(range(p)));perm_average=sum(average[np.ix_(h,h,h)] for h in perms)/len(perms)
    expected=np.zeros_like(W)
    for i in range(p):expected[i,i,i]=sum(W[j,j,j] for j in range(p))/p
    check('affine_permutation_symmetrization',np.allclose(perm_average,expected,atol=1e-14))
    for K in range(2,7):
        for d in range(1,K+1):
            for a in [-100.,-1.,1.,100.]:
                sine=1/(4*d*abs(a));cosine=np.sqrt(1-sine*sine)
                gap=abs(a)*sine**d;distance_sq=2*a*a*(1-cosine**d)
                check('pointwise_rotation_lower',distance_sq<=.25*(1+1e-10) and np.isclose(gap,abs(a)**(1-d)/(4*d)**d))
    for K in [2,3,4,5]:
        for _ in range(100):
            factors=[rng.normal(size=3) for k in range(K)];A=factors[0]
            for f in factors[1:]:A=np.multiply.outer(A,f)
            J=tuple(rng.integers(0,3,K));I=tuple(rng.integers(0,3,K));changed=[k for k in range(K) if I[k]!=J[k]]
            if len(changed)<2:continue
            x=A[J];vals=[]
            for k in changed:
                idx=list(J);idx[k]=I[k];vals.append(A[tuple(idx)])
            check('rank_one_fiber_identity',np.isclose(np.prod(vals)/x**(len(vals)-1),A[I],atol=1e-10))
            delta=abs(x)/4;num=[(b-rng.uniform(0,1),b+rng.uniform(0,1)) for b in vals]
            lo,hi=_ratio_range(num,(x-delta,x+delta),len(vals)-1)
            check('ratio_range_coverage',lo-1e-12<=A[I]<=hi+1e-12)
            for _ in range(10):
                value=np.prod([rng.uniform(a,b) for a,b in num])/rng.uniform(x-delta,x+delta)**(len(vals)-1)
                check('ratio_range_interior',lo-1e-10<=value<=hi+1e-10)
    for shape in [(3,4,5),(2,3,4,2)]:
        L=rng.normal(size=shape)
        for selector in [dict(mode=k) for k in range(len(shape))]+[dict(cut=k) for k in range(1,len(shape))]:
            mat=unfolding(L,**selector);q=min(mat.shape)
            for r in [1,q]:
                for M in [0.,.3,3.,300.]:
                    plan=spectral_plan(L,M,r,**selector)
                    check('spectral_restoration',np.isclose(np.linalg.norm(plan['ci_loading']),np.linalg.norm(np.maximum(plan['spectrum']-plan['ci_optimizer']['threshold'],0))) or plan['selected']=='structural')
                    out=spectral_interval(np.zeros(shape),plan)
                    check('spectral_api',out['lo']<=0<=out['hi'] and out['width']<=2*plan['radius']*(1+1e-14) and out['estimate']==0)
    zero=adaptive_coordinate_interval(np.zeros((2,2)),(0.,0.),0,rng)
    check('degenerate_model',zero['width']==0)
    result={'seed':9152601,'status':'PASS','checks':sum(counts.values()),'by_family':counts,
            'max_relative_optimizer_gap':worst_gap,'max_A_over_geometric_proxy':worst_ratio,
            'interpretation':'Finite checks support identities and implementations; proofs are in theory/results.md.'}
    (ROOT/'audit/theory_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':run()
