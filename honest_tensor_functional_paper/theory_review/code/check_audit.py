"""Targeted counterexample and proof-constant checks for the theory audit."""
import itertools
import json
import math
from pathlib import Path
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.stats import norm

ROOT=Path(__file__).resolve().parents[1]
rng=np.random.default_rng(20260910)

def qabs(mu,sd,alpha):
    if sd==0:
        return float(abs(mu))
    return brentq(lambda h:norm.cdf((h-mu)/sd)-norm.cdf((-h-mu)/sd)-(1-alpha),
                  0, abs(mu)+sd*(norm.isf(alpha/2)+10))

def main():
    # Literal Theorem 5 omits the alpha<1/4 condition used in its proof.
    alpha=.9
    h=.1
    t=.6
    coverage=norm.cdf((h-(1-t))/t)-norm.cdf((-h-(1-t))/t)
    old=norm.isf(alpha/2)/(1+norm.isf(alpha/2))
    assert coverage>=1-alpha and h<old
    affine=[]
    for a in (.1,1,2,10):
        obj=lambda t:qabs(a*(1-t),t,.05)
        opt=minimize_scalar(obj,bounds=(1e-9,1),method='bounded')
        candidates=[(a,0.),(norm.isf(.025),1.),(float(opt.fun),float(opt.x))]
        hh,tt=min(candidates)
        if a<=norm.isf(.05):
            assert hh==a and tt==0
        affine.append(dict(a=a,t=tt,radius=hh))
    # Exact cubic-mixture second moments for small p; no Monte Carlo extrapolation.
    mixture=[]
    for p in (1,2,4,6,8,10):
        signs=np.array(list(itertools.product((-1.,1.),repeat=p)))
        weights=np.arange(1,p+1,dtype=float)**(-2/3)
        ss=signs@weights
        third=(signs*weights)@signs.T
        second=float(np.mean(np.exp((ss[:,None]*ss[None,:]*third)/40000)))
        mgf=float(np.mean(np.exp(np.abs(ss)**3/40000)))
        assert second<=mgf+1e-12 and mgf<=20/19+1/100
        norm_ratio=(np.sum(weights)**1.5)/(200*np.sqrt(p))
        assert norm_ratio<=3**1.5/200<1
        mixture.append(dict(p=p,sign_pairs=int(4**p),second_moment=second,
                            cubic_mgf=mgf,norm_divided_by_cap=float(norm_ratio),
                            target_over_tau=float(np.sum(1/np.arange(1,p+1))/(200*np.sqrt(p)))))
    # Independent rank-one check of the ordered-subtensor inequality in S7.
    profiles=[]
    for K in (3,4,5,6):
        for p in (2,4,7):
            for _ in range(10):
                factors=[rng.normal(size=p) for _ in range(K)]
                d=np.prod(factors,axis=0)
                ordered=np.sort(np.abs(d))[::-1]
                for s in range(1,p+1):
                    ids=np.argsort(np.abs(d))[-s:]
                    rho=float(np.prod([np.linalg.norm(x[ids]) for x in factors]))
                    assert ordered[s-1]<=rho*s**(-K/2)+1e-12
                maxrho=[]
                for s in range(1,p+1):
                    maxrho.append(max(np.prod([np.linalg.norm(x[list(S)]) for x in factors])
                                      for S in itertools.combinations(range(p),s)))
                bound=sum(maxrho[s-1]*s**(-K/2) for s in range(1,p+1))/np.sqrt(p)
                assert abs(np.sum(d))/np.sqrt(p)<=bound+1e-12
                profiles.append(K)
    # The residual map, rather than two triangle inequalities, gives approximation cost eta.
    x=rng.normal(size=(10000,5))*3
    noise=rng.uniform(-1,1,size=x.shape)
    residual=rng.normal(size=x.shape)
    w=rng.normal(size=5);w/=np.linalg.norm(w)
    soft=lambda z:np.sign(z)*np.maximum(np.abs(z)-1,0)
    err0=soft(x+noise)-x
    err1=soft(x+residual+noise)-x-residual
    delta=(err1-err0)@w
    excess=float(np.max(np.abs(delta)-np.linalg.norm(residual,axis=1)))
    assert excess<1e-12
    # Sharp support-bound equality under the stated tensor cap, and failure under a false cap.
    p=5;cap=3;w=rng.normal(size=p);w/=np.linalg.norm(w)
    ids=np.argsort(np.abs(w))[-cap:]
    diag=np.zeros(p);diag[ids]=w[ids]/np.linalg.norm(w[ids])
    assert np.isclose(diag@w,np.linalg.norm(w[ids]))
    # Exact max-noise threshold and strict improvement over the Chernoff calibration.
    thresholds=[]
    for m in (1,2,128,8192):
        alpha=.05
        tail=-np.expm1(np.log1p(-alpha)/m)/2
        lam=float(norm.isf(tail))
        conservative=np.sqrt(2*np.log(2*m/alpha))
        coverage=float(np.exp(m*np.log1p(-2*norm.sf(lam))))
        assert abs(coverage-(1-alpha))<1e-10 and lam<conservative
        thresholds.append(dict(m=m,exact=lam,original=float(conservative),event_coverage=coverage))
    # Refined cap coefficient on independent random Tucker and TT constructions.
    geometry=[]
    for case in range(100):
        dims=5;rr=2
        U=[np.linalg.qr(rng.normal(size=(dims,rr)))[0] for _ in range(3)]
        core=rng.normal(size=(rr,rr,rr))
        A=np.einsum('abc,ia,jb,kc->ijk',core,*U)
        M=np.linalg.norm(A)
        lhs=np.sum(np.abs(np.einsum('iii->i',A))**(2/3))
        D=min(4**(2/3),dims**(2/3),2)
        assert lhs<=D*M**(2/3)+1e-10
        G=[rng.normal(size=(1,4,2)),rng.normal(size=(2,4,2)),
           rng.normal(size=(2,4,2)),rng.normal(size=(2,4,1))]
        B=np.einsum('aib,bjc,ckd,dle->ijkl',*G)
        M=np.linalg.norm(B)
        lhs2=np.sum(np.abs(np.einsum('iiii->i',B))**.5)
        D2=min(8**.75,4**.75,(2*4*4*2)**.25)
        assert lhs2<=D2*M**.5+1e-10
        geometry.append([float(lhs/(D*np.linalg.norm(A)**(2/3))),
                         float(lhs2/(D2*M**.5))])
    # Finite-variance counterexample: one outlier forces failure at zero.
    pp=8192;aa=.05
    ll=np.sqrt(2*np.log(2*pp/aa))
    nl=(8*np.log(2*pp/aa)/pp)**(1/6)
    one_probability=2*aa*(1-2*aa/pp)**(pp-1)
    bad_center=(np.sqrt(pp/(2*aa))-ll)/np.sqrt(pp)
    assert one_probability>aa and bad_center>nl
    # Constants in the uniform cubic exponential-moment proof.
    assert 1728/40000<1/20 and 1/192-1/40000>=1/200
    assert 20/19+1/100<5/4 and 18*2**(1/3)<24
    out=dict(status='PASS',seed=20260910,
             alpha_counterexample=dict(alpha=.9,t=.6,h=.1,worst_coverage=float(norm.cdf(-.5)-norm.cdf(-5/6)),
                                       asserted_lower=float(old)),
             affine_optima=affine,cubic_mixture=mixture,rank_one_profiles=len(profiles),
             approximation_cases=len(x),max_approximation_excess=excess,
             gaussian_thresholds=thresholds,geometry_cases=2*len(geometry),
             refined_geometry_max_ratio=float(np.max(geometry)),
             finite_variance_counterexample=dict(single_outlier_probability=one_probability,
                    bad_center=bad_center,selected_radius=nl),
             limits='Finite checks supplement the complete proofs. No full exponential scan benchmark or claim of independent formal verification.')
    (ROOT/'results/audit_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    main()
