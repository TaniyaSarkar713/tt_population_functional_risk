"""New bounded falsification checks; formulas are reconstructed independently."""
import itertools
import math
import numpy as np
from scipy.stats import norm
from inventory import ROOT,dump

def product(vectors):
    out=np.array(1.)
    for x in vectors:out=np.multiply.outer(out,x)
    return out

def main():
    rng=np.random.default_rng(2026091307);checks=[];failures=[];examples={}
    def check(label,condition):
        checks.append(label)
        if not condition:failures.append(label)
    # Exact diagonal image, including signs and zero coordinates.
    for K in [3,4,5]:
        for p in [2,3,5]:
            for trial in range(5):
                d=rng.normal(size=p);d[0]=0.;q=2/K
                factors=[np.abs(d)**(1/K) for _ in range(K)]
                factors[0]=np.sign(d)*factors[0]
                A=product(factors);ids=np.arange(p)
                check(f'diagonal_image_{K}_{p}_{trial}',np.allclose(A[(ids,)*K],d))
                check(f'diagonal_norm_{K}_{p}_{trial}',np.isclose(np.linalg.norm(A),np.sum(abs(d)**q)**(1/q)))
    # The TT path identity must work even when individual paths are not orthogonal.
    nonorthogonal=False
    for trial in range(12):
        ranks=[1,2,2,2,1];cores=[]
        for k in range(4):
            C=rng.normal(size=(ranks[k]*3,ranks[k+1]))
            if k<3:C=np.linalg.qr(C)[0]
            cores.append(C.reshape(ranks[k],3,ranks[k+1]))
        A=np.ones(1)
        for C in cores:A=np.einsum('...a,aib->...ib',A,C,optimize=False)
        A=A[...,0];terms=[]
        for path in itertools.product(range(2),repeat=3):
            ids=(0,)+path+(0,)
            terms.append(product([cores[k][ids[k],:,ids[k+1]] for k in range(4)]))
        check(f'TT_reconstruction_{trial}',np.allclose(sum(terms),A))
        check(f'TT_squared_path_weights_{trial}',np.isclose(sum(np.sum(T*T) for T in terms),np.sum(A*A)))
        nonorthogonal|=any(abs(np.sum(U*V))>1e-8 for i,U in enumerate(terms) for V in terms[i+1:])
    check('TT_nonorthogonal_paths_present',nonorthogonal)
    # Full-data harmonic likelihoods: enumerate actual tensors, not diagonal-only likelihoods.
    for p,m in [(5,1),(5,2),(7,3),(8,4)]:
        supports=list(itertools.combinations(range(p),m))
        for M in [.1,1.,10.]:
            b=min(M/np.sqrt(27*m),np.sqrt(np.log1p(p/(4*m*m))/27))
            tensors=[]
            for S in supports:
                x=np.zeros(p);x[list(S)]=np.arange(1,m+1)**(-1/3)
                tensors.append(b*product([x,x,x]))
            flat=np.stack([A.ravel() for A in tensors]);gram=np.einsum('id,jd->ij',flat,flat,optimize=False)
            delta=b*sum(1/j for j in range(1,m+1))/np.sqrt(p)
            check(f'harmonic_norm_{p}_{m}_{M}',max(np.linalg.norm(A) for A in tensors)<=M+1e-12)
            check(f'harmonic_target_{p}_{m}_{M}',all(np.isclose(np.einsum('iii->',A)/np.sqrt(p),delta) for A in tensors))
            check(f'harmonic_full_likelihood_{p}_{m}_{M}',np.exp(gram).mean()<=np.exp(.25)+1e-12)
            w=np.linspace(1.,.1,p)*np.where(np.arange(p)%2,1.,-1.)
            changed=[A*(abs(w).min()/w)[:,None,None] for A in tensors]
            W=np.stack([A.ravel() for A in changed]);new=np.einsum('id,jd->ij',W,W,optimize=False)
            check(f'weighted_overlap_contraction_{p}_{m}_{M}',np.all(new<=gram+1e-12))
            check(f'weighted_equal_target_{p}_{m}_{M}',all(np.isclose(np.sum(w*A[np.arange(p),np.arange(p),np.arange(p)]),abs(w).min()*np.sqrt(p)*delta) for A in changed))
    # All support sizes, including dense/saturated ranks, by exact hypergeometric probabilities.
    for p in range(1,41):
        for r in range(1,p+1):
            probabilities=[math.comb(r,h)*math.comb(p-r,r-h)/math.comb(p,r)
                if 0<=r-h<=p-r else 0. for h in range(r+1)]
            b2=np.log1p(p/(4*r*r))
            moment=sum(prob*np.exp(b2*h) for h,prob in enumerate(probabilities))
            check(f'G1_full_mixture_{p}_{r}',moment<=np.exp(.25)+2e-12)
            if r<=np.sqrt(p):
                for degree in [1,2]:
                    K=3;lam2=.04*r**K/(K*degree)**K;mu=r*r/p;BD=.04
                    exact=sum(lam2**d*sum(prob*h**(K*d) for h,prob in enumerate(probabilities))/
                        (math.factorial(d)*r**(K*d)) for d in range(1,degree+1))
                    check(f'low_degree_moment_{p}_{r}_{degree}',exact<=mu*np.exp(mu)*BD/(1-BD)+1e-12)
    # Product-space bias certificate tested with arbitrary loadings and unsaturated true ranks.
    dimensions=(3,4,3);D=math.prod(dimensions)
    for cap in [1,2,3]:
        for actual in range(cap+1):
            for amplitude in [0.,1.,100.,1e5]:
                if actual==0:A=np.zeros(dimensions)
                else:
                    factors=[np.linalg.qr(rng.normal(size=(p,actual)))[0] for p in dimensions]
                    A=rng.normal(size=(actual,)*3)*amplitude
                    for k,U in enumerate(factors):
                        A=np.moveaxis(np.einsum('ij,j...->i...',U,np.moveaxis(A,k,0),optimize=False),0,k)
                E=rng.normal(size=dimensions);pilot=A+E;Q=[];errors=[]
                for k,p in enumerate(dimensions):
                    mat=np.moveaxis(pilot,k,0).reshape(p,-1)
                    U,s,_=np.linalg.svd(mat,full_matrices=False)
                    eta=np.linalg.svd(np.moveaxis(E,k,0).reshape(p,-1),compute_uv=False)[0]+1e-10
                    Q.append(np.einsum('ir,jr->ij',U[:,:cap],U[:,:cap],optimize=False))
                    den=s[cap-1]-eta
                    errors.append(0. if cap==p else min(1.,2*eta/den) if den>0 else 1.)
                T=np.kron(np.kron(Q[0],Q[1]),Q[2])
                for k in range(3):
                    factors=[np.eye(dimensions[l])-Q[l] if k==l else Q[l] for l in range(3)]
                    T+=np.kron(np.kron(factors[0],factors[1]),factors[2])
                L=rng.normal(size=D);L/=np.linalg.norm(L)
                R=L-np.einsum('ij,j->i',T,L,optimize=False)
                bound=np.linalg.norm(A)*np.linalg.norm(R)*min(1.,np.sqrt(sum(errors[k]**2*errors[l]**2 for k in range(3) for l in range(k+1,3))))
                bias=abs(np.sum(R*A.ravel()))
                check(f'A4_bias_{cap}_{actual}_{amplitude}',bias<=bound+1e-8*max(1.,np.linalg.norm(A)))
                check(f'A4_projector_{cap}_{actual}_{amplitude}',np.allclose(np.einsum('ij,jk->ik',T,T,optimize=False),T,atol=1e-10))
    # Outside-assumption examples are not counterexamples to the stated theorems.
    p=256;rho=.8;q=norm.ppf(.975)
    examples['correlated_gaussian_naive_exact_coverage']=float(2*norm.cdf(q/np.sqrt(1+(p-1)*rho))-1)
    examples['understated_cap']=dict(p=4,true_rank=2,supplied_cap=1,amplitude=1.,
        true_target=1.,claimed_structural_radius=1/np.sqrt(2),conclusion='The supplied-cap structural range excludes the target deterministically.')
    examples['P1_threshold_exponent']=dict(K3=2.5,K4=3.5,
        explanation='The sufficient minimum amplitude grows as tau p^(K-1/2); this is not an optimal threshold claim.')
    dump(ROOT/'results/proof_checks.json',dict(status='PASSED' if not failures else 'FAILED',checks=len(checks),
        passed=checks,failures=failures,examples=examples,seed=2026091307,
        scope='New exact finite enumerations and bounded numerical falsification attempts; not formal verification.'))
    print('Proof checks:',len(checks),'Failures:',len(failures))
    if failures:raise AssertionError(failures[:5])

if __name__=='__main__':main()
