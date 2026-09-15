"""Independent finite identities, inequalities and edge checks; not proofs."""
import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.stats import norm
from methods import *
ROOT=Path(__file__).resolve().parents[1]
rng=np.random.default_rng(2026091401); counts={}
# Independent projector oracle uses direct summation, not the production BLAS path.
def mm(a,b): return np.einsum('ik,kj->ij',a,b,optimize=False)
def check(name,condition):
    if not bool(condition): raise AssertionError(name)
    counts[name]=counts.get(name,0)+1

# Abel identity, all-budget monotonicity, envelope factor and homogeneity.
for K in [3,4,6]:
    for p in [1,2,7,32,257,4096]:
        for M in [0.,1e-5,.5,1.,2.,10.,1e3,1e9]:
            F=flat_prefix_F(p,M,order=K)
            check('prefix_monotonicity',np.all(np.diff(F)>=-1e-10))
            for typ in range(6):
                w=(rng.random(p) if typ==0 else 1/(1+np.log(np.arange(1,p+1)))**[0,.25,.5,1.,2.][typ-1])
                w=np.sort(w)[::-1]
                z=loading_envelope(w,M,order=K); A=np.dot(w-np.r_[w[1:],0],F)
                check('abel_identity',np.isclose(A,z['upper_proxy']))
                check('envelope_comparison',z['lower_proxy']<=A+1e-8 and A<=z['proven_proxy_factor']*z['lower_proxy']+1e-8)
                check('universal_factor',z['proven_proxy_factor']<=z['universal_factor']+1e-10)
                z2=loading_envelope(-3*w,7*M,tau=7,order=K)
                check('homogeneity',np.isclose(z2['upper_proxy'],21*A))

# Scalar clipping identity: dense scalar grid plus extreme randomized cases.
for _ in range(30000):
    theta,Y,c=rng.normal(size=3)*10**rng.uniform(-5,5); D=10**rng.uniform(-6,6)
    lhs=abs(np.clip(c,Y-D,Y+D)-theta); rhs=max(abs(c-theta),max(abs(Y-theta)-D,0))
    check('scalar_projection_lemma',lhs<=rhs+1e-8*max(1,rhs))
for d in np.linspace(2.3,12,30):
    tail=2*quad(lambda x:(x-d)**2*norm.pdf(x),d,max(d+12,20))[0]
    check('normal_overshoot_bound',tail<=4*np.exp(-d*d/2))

# Independent Kronecker projector construction against tensor contractions.
for dims in [(3,4,5),(3,3,3,3)]:
    K=len(dims)
    for _ in range(15):
        bases=[np.linalg.qr(rng.normal(size=(p,2)))[0] for p in dims]
        Ps=[mm(b,b.T) for b in bases]; D=int(np.prod(dims)); T=np.zeros((D,D))
        for mask in range(2**K):
            if bin(mask).count("1")>1: continue
            block=np.array([[1.]])
            for k,p in enumerate(dims):block=np.kron(block,np.eye(p)-Ps[k] if (mask>>k)&1 else Ps[k])
            T+=block
        x=rng.normal(size=dims)
        check('tucker_projector_implementation',np.allclose(tangent_project(x,bases).ravel(),np.einsum('ij,j->i',T,x.ravel(),optimize=False)))
        check('tucker_projector_idempotence',np.allclose(mm(T,T),T) and np.allclose(T,T.T))

# True rank-one and rank-two Tucker tensors: noisily perturbed subspaces and
# independently measured projection bias under a valid deterministic op bound.
for K in [3,4]:
    dims=(4,)*K
    for _ in range(40):
        B=[np.linalg.qr(rng.normal(size=(4,2)))[0] for k in dims]
        C=rng.normal(size=(2,)*K); A=C
        for k,b in enumerate(B): A=np.moveaxis(np.tensordot(b,np.moveaxis(A,k,0),axes=(1,0)),0,k)
        noise=rng.normal(size=dims)*.001; Q=[]; errs=[]
        for k in range(K):
            mat=np.moveaxis(A+noise,k,0).reshape(4,-1); u,ss,v=svd(mat,full_matrices=False)
            eta=np.linalg.norm(np.moveaxis(noise,k,0).reshape(4,-1),2)
            Q.append(u[:,:2]);den=ss[1]-eta;errs.append(min(1,2*eta/den) if den>0 else 1)
        L=rng.normal(size=dims);TL=tangent_project(L,Q)
        cert=np.linalg.norm(A)*np.linalg.norm(L-TL)*min(1,np.sqrt(sum(errs[j]**2*errs[k]**2 for j in range(K) for k in range(j+1,K))))
        check('tucker_bias_certificate',abs(np.sum((L-TL)*A))<=cert+1e-9)

# TT bridge perturbation preserves every cut cap, not just its chosen cut.
for _ in range(60):
    cores=[rng.normal(size=(1,3,2)),rng.normal(size=(2,4,3)),rng.normal(size=(3,3,2)),rng.normal(size=(2,3,1))]
    def contract(cs):
        a=cs[0][0]
        for c in cs[1:]:a=np.tensordot(a,c,axes=(-1,0))
        return a[...,0]
    A=contract(cores)
    for cut,rank in [(1,2),(2,3),(3,2)]:
        mat=A.reshape(int(np.prod(A.shape[:cut])),-1);u,ss,v=svd(mat,full_matrices=False)
        H=mm(mm(u[:,:rank],rng.normal(size=(rank,rank))),v[:rank]).reshape(A.shape)
        A1=A+H
        for j,cap in enumerate([2,3,2],1):
            ss1=svd(A1.reshape(int(np.prod(A.shape[:j])),-1),compute_uv=False)
            check('tt_bridge_all_caps',np.sum(ss1>1e-8*ss1[0])<=cap)
        eps=rng.normal(size=mat.shape)*.0001;uq,sq,vq=svd(mat+eps,full_matrices=False)
        eta=np.linalg.norm(eps,2); e=min(1.,2*eta/(sq[rank-1]-eta)) if sq[rank-1]>eta else 1.
        L=rng.normal(size=mat.shape);U=uq[:,:rank];V=vq[:rank].T
        R=L-mm(U,mm(U.T,L))-mm(mm(L,V),V.T)+mm(mm(U,mm(mm(U.T,L),V)),V.T)
        check('tt_bias_certificate',abs(np.sum(R*mat))<=np.linalg.norm(mat)*np.linalg.norm(R)*e**2+1e-8)

# Sparse-threshold bias/variance checked by numerical Gaussian integration.
for p,r in [(8,1),(256,3),(4096,8),(100,40)]:
    a=diagonal_sparse(np.zeros(p),1e5,r);t=a['threshold']
    for mean in [0.,.5*t,t,2*t,10*t,-t]:
        fun=lambda z:z*norm.pdf(z-mean)
        meanhat=quad(fun,-np.inf,-t)[0]+quad(fun,t,np.inf)[0]
        moment=quad(lambda z:z*z*norm.pdf(z-mean),-np.inf,-t)[0]+quad(lambda z:z*z*norm.pdf(z-mean),t,np.inf)[0]
        # Infinite-interval quadrature can miss distant peaks, so integrate
        # the high-signal tails over a bounded interval enclosing their mass.
        if abs(mean)>8:
            meanhat=quad(fun,min(mean-12,-t-12),-t)[0]+quad(fun,t,max(mean+12,t+12))[0]
            moment=quad(lambda z:z*z*norm.pdf(z-mean),min(mean-12,-t-12),-t)[0]+quad(lambda z:z*z*norm.pdf(z-mean),t,max(mean+12,t+12))[0]
        check('sparse_bias_integral',abs(meanhat-mean)<=t+1e-7)
        check('sparse_variance_integral',moment-meanhat**2<=2*(t*t+1)+1e-7)

# Input, full-space, non-square, zero-budget, and exact replay contracts.
for geom,dims,caps in [('tucker',(3,4,5),[3,4,5]),('tt',(3,4,5),[3,5]),('tucker',(2,3,4),[1,2,2]),('tt',(2,3,4),[1,2])]:
    z=rng.normal(size=dims);L=rng.normal(size=dims)
    a=cap_interval(z,L,10,caps,np.random.default_rng(42),geometry=geom,return_details=True)
    b=cap_interval(z,L,10,caps,np.random.default_rng(42),geometry=geom,return_details=True)
    check('deterministic_replay',a==b)
    check('range_protection',abs(a['estimate'])<=a['structural']+1e-9)
    zero=cap_interval(z,L,0,caps,rng,geometry=geom)
    check('zero_budget',zero['estimate']==zero['width']==0)
for fun in [lambda:loading_envelope([np.nan],1),lambda:cap_interval(np.zeros((2,2,2)),np.zeros((2,2,2)),1,[0,1,1],rng),lambda:empirical_bernstein([0,2],0,1)]:
    try:fun()
    except ValueError:check('invalid_input_rejection',True)
    else:check('invalid_input_rejection',False)

# Rank-one minor: independent corner-range and coverage-on-event checks.
for _ in range(2000):
    factors=rng.normal(size=(3,2)); A=np.einsum('i,j,k->ijk',*factors)
    truth=np.array([A[0,0,0],A[1,0,0],A[0,1,0],A[1,1,0]])
    check('minor_rank_one_identity',np.isclose(truth[0]*truth[3],truth[1]*truth[2]))
    q=norm.isf(.05/12);rd=norm.isf(.05/4)
    error=rng.uniform(-1,1,4)*np.array([q,q,q,rd])
    z=truth+error;ans=rank_one_minor_interval(*z,M=np.linalg.norm(A))
    check('minor_coverage_on_event',ans['lo']-1e-12<=truth[3]<=ans['hi']+1e-12)
    check('minor_direct_width_cap',ans['width']<=2*rd+1e-12)

out={'status':'PASS','seed':2026091401,'checks':sum(counts.values()),'by_family':counts,
     'scope':'Finite checks complement supplied proofs; no general optimizer certification or formal proof verification.'}
(ROOT/'audit/theory_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
