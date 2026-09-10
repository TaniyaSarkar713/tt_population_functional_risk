"""Finite checks of the gap-closing proofs; these are not proof substitutes."""
import itertools,json,math
from pathlib import Path
import numpy as np
from scipy.special import gammaln
from scipy.stats import hypergeom
ROOT=Path(__file__).resolve().parents[1]
rng=np.random.default_rng(20260911)
def main():
    mixture=[]
    for p in [2,4,6,8,10]:
        for m in range(1,min(p,4)+1):
            S=list(itertools.combinations(range(p),m))
            X=np.zeros((len(S),p))
            for j,ids in enumerate(S):X[j,list(ids)]=np.arange(1,m+1)**(-1/3)
            H=(X>0).astype(int)@(X>0).astype(int).T
            dot=X@X.T
            assert np.all(dot**3<=27*H+1e-10)
            b=min(np.sqrt(p/(27*m)),np.sqrt(np.log1p(p/(4*m*m))/27))
            actual=float(np.mean(np.exp(b*b*dot**3)))
            envelope=float(np.mean(np.exp(27*b*b*H)))
            assert actual<=envelope+1e-12 and envelope<=np.exp(.25)+1e-12
            assert np.all(b*np.linalg.norm(X,axis=1)**3<=np.sqrt(p)+1e-10)
            target=b*np.sum(X**3,axis=1)/np.sqrt(p)
            assert np.ptp(target)<1e-12
            mixture.append(dict(p=p,m=m,support_pairs=len(S)**2,
                                second_moment=actual,overlap_envelope=envelope,target=float(target[0])))
    # Low-degree identity checked against explicit full multivariate Hermite coefficients.
    hermite=[]
    p=2;K=3;s=1;lam=.2
    means=[]
    for ids in itertools.combinations(range(p),s):
        x=np.zeros(p);x[list(ids)]=1/np.sqrt(s)
        means.append(lam*np.einsum('i,j,k->ijk',x,x,x).ravel())
    means=np.array(means)
    for degree in range(1,5):
        direct=0.
        for indexes in itertools.combinations_with_replacement(range(p**K),degree):
            counts=np.bincount(indexes,minlength=p**K)
            coefficient=np.mean(np.prod(means**counts,axis=1))/np.sqrt(np.prod([math.factorial(int(j)) for j in counts]))
            direct+=coefficient**2
        pair=float(np.mean((means@means.T)**degree)/math.factorial(degree))
        assert np.isclose(direct,pair,atol=1e-12)
        hermite.append(dict(degree=degree,hermite_coefficient_sum=direct,pair_moment=pair))
    lowdegree=[]
    for p in [20,100,1000]:
        for s in [1,2,3]:
            if s>np.sqrt(p):continue
            for K in [3,4,6]:
                for degree in [1,2,3]:
                    mu=s*s/p
                    lam=.25*s**(K/2)/(K*degree)**(K/2)
                    B=lam**2/s**K*(K*degree)**K
                    H=np.arange(s+1);probs=hypergeom.pmf(H,p,s,s)
                    value=sum(lam**(2*d)*np.dot(probs,H.astype(float)**(K*d))/(math.factorial(d)*s**(K*d))
                              for d in range(1,degree+1))
                    bound=mu*np.exp(mu)*B/(1-B)
                    assert value<=bound+1e-12
                    lowdegree.append(dict(p=p,s=s,K=K,degree=degree,centered_norm_squared=float(value),bound=float(bound)))
    # Ordered-diagonal bound for differences: rank caps must be doubled.
    differences=[]
    for K in [3,4]:
        for p in [3,4,5]:
            for rep in range(20):
                fs=[rng.normal(size=(2,p)) for _ in range(K)]
                terms=[]
                for j in range(2):
                    term=fs[0][j]
                    for k in range(1,K):term=np.multiply.outer(term,fs[k][j])
                    terms.append(term)
                delta=terms[0]-terms[1]
                diag=np.array([delta[(i,)*K] for i in range(p)])
                J2=2**(K-1)
                for size in range(1,p+1):
                    ids=np.argsort(np.abs(diag))[-size:]
                    sub=delta[np.ix_(*([ids]*K))]
                    # A set of tested unit products gives a lower bound on rho.
                    candidate=[]
                    for j in range(2):
                        vv=[fs[k][j,ids]/np.linalg.norm(fs[k][j,ids]) for k in range(K)]
                        v=vv[0]
                        for vec in vv[1:]:v=np.multiply.outer(v,vec)
                        candidate.append(abs(np.sum(sub*v)))
                    rho_lower=max(candidate)
                    # Verify the exact q budget using the Frobenius bound, without treating rho_lower as an upper certificate.
                    q=2/K
                    lhs=np.sum(np.abs(diag[ids])**q)
                    bound=J2**(1-q/2)*np.linalg.norm(sub)**q
                    assert lhs<=bound+1e-10
                differences.append(K)
    # Sparse harmonic lower scale across increasing dimensions.
    rates=[]
    for p in [256,4096,65536,10**6,10**8,10**12]:
        m=int(p**.25)
        b=min(np.sqrt(p/(27*m)),np.sqrt(np.log1p(p/(4*m*m))/27))
        target=b*np.sum(1/np.arange(1,m+1))/np.sqrt(p)
        scale=np.log(p)**1.5/np.sqrt(p)
        assert target>=scale/(16*np.sqrt(27))
        rates.append(dict(p=p,m=m,target=float(target),normalized=float(target/scale)))
    out=dict(status="PASS",seed=20260911,sparse_harmonic_mixtures=mixture,
             hermite_checks=hermite,low_degree_checks=lowdegree,
             doubled_rank_differences=len(differences),cubic_scale_checks=rates,
             note="Exact small cases and deterministic bounds. No inference from simulations to universal proof.")
    (ROOT/"results/theory_checks.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if not isinstance(v,list)},indent=2))
if __name__=="__main__":main()
