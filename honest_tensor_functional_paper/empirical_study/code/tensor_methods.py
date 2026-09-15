"""Cached cap-valid calculation and published PCA comparator, with tests."""
import time
import numpy as np
from scipy.linalg import svd
from scipy.stats import norm
from common import high, LEVELS


def mode_multiply(a, matrix, mode):
    moved=np.moveaxis(a,mode,0)
    return np.moveaxis(np.einsum('ij,j...->i...',matrix,moved,optimize=False),0,mode)


def reduce(a, bases, omit=None):
    for k,U in enumerate(bases):
        if k!=omit:
            a=mode_multiply(a,U.T,k)
    return a


def leading(a,k,r):
    mat=np.moveaxis(a,k,0).reshape(a.shape[k],-1)
    U,s,_=svd(mat,full_matrices=False,check_finite=False)
    return U[:,:r],s


def xch_pca(z, loading, rank, tau=1., iterations=2):
    """Xu/Chen/Han arXiv v1 Section 4.2, Algorithm 3, Eqs.16/24.

    Two *simultaneous* factor updates from HOSVD. Known-noise version gives
    the comparator the same supplied scale as the cap-valid procedure.
    Core row-space projections implement the exact manifold tangent variance,
    not the larger first-order product-space projector used by our certificate.
    """
    bases=[leading(z,k,rank)[0] for k in range(3)]
    for _ in range(iterations):
        previous=bases
        bases=[leading(reduce(z,previous,omit=k),k,rank)[0] for k in range(3)]
    core=reduce(z,bases)
    fitted=high.project_modes(z,bases)
    estimate=float(np.sum(fitted*loading))
    core_loading=reduce(loading,bases)
    variance=float(np.sum(core_loading**2))
    for k,U in enumerate(bases):
        core_mat=np.moveaxis(core,k,0).reshape(rank,-1)
        W=np.linalg.qr(core_mat.T,mode='reduced')[0]
        contracted=reduce(loading,bases,omit=k)
        mat=np.moveaxis(contracted,k,0).reshape(z.shape[k],-1)
        mat=np.einsum('ij,jk->ik',mat,W,optimize=False)
        reduced=np.einsum('ir,ij->rj',U,mat,optimize=False)
        perpendicular=mat-np.einsum('ir,rj->ij',U,reduced,optimize=False)
        variance+=float(np.sum(perpendicular**2))
    sigma_hat=float(np.linalg.norm(z-fitted)/np.sqrt(z.size))
    return dict(estimate=estimate,sd=tau*np.sqrt(variance),sd_plugin=sigma_hat*np.sqrt(variance),
                sigma_hat=sigma_hat,variance=variance,iterations=iterations,bases=bases)


def pointwise_levels(z,M,rank,auxiliary,tau=1.):
    """Algebraically identical to high.pointwise_interval, caching its SVDs.

    Independent auxiliary has iid N(0,tau^2) entries. This returns all three
    predeclared levels and the shared-pilot bias-omission ablation.
    """
    p,K=z.shape[0],z.ndim
    pilot,second=z+auxiliary,z-auxiliary
    bases=[];singulars=[]
    for k in range(K):
        U,s=leading(pilot,k,rank)
        bases.append(U if rank<p else None);singulars.append(s)
    L=high.flat_loading(p,K)
    joint=high.project_modes(L,bases)
    tangent=-(K-1)*joint
    for k in range(K):
        tangent+=high.project_modes(L,bases,omit=k)
    residual_norm=np.linalg.norm(L-tangent)
    tn=float(np.linalg.norm(tangent))
    center_t=float(np.sum(tangent*second))
    ids=np.arange(p)
    center_s=float(second[(ids,)*K].sum()/np.sqrt(p))
    center_d=float(z[(ids,)*K].sum()/np.sqrt(p))
    structural=M*np.sqrt(rank/p)
    endpoints=[];ablation=[];details=[]
    for alpha in LEVELS:
        delta=alpha*rank/(8*p)
        eta=high.pilot_bound(p,K,tau,delta)
        errors=[]
        for s in singulars:
            denom=s[rank-1]-eta
            errors.append(0. if rank==p else min(1.,2*eta/denom) if denom>0 else 1.)
        angle=min(1.,np.sqrt(sum(errors[k]**2*errors[l]**2 for k in range(K) for l in range(k+1,K))))
        bias=float(M*residual_norm*angle)
        q=norm.isf((alpha/2-delta)/2)
        radii=[bias+q*np.sqrt(2)*tau*tn,q*np.sqrt(2)*tau,structural]
        choice=int(np.argmin(radii))
        center=[center_t,center_s,0.][choice]
        rd=norm.isf(alpha/4)*tau
        lo=max(center-radii[choice],center_d-rd,-structural)
        hi=min(center+radii[choice],center_d+rd,structural)
        if lo>hi:lo=hi=0.
        endpoints.append([lo,hi])
        # Omit only bias and fallback: useful diagnostic, no honest guarantee.
        qa=norm.isf(alpha/2)
        ablation.append([center_t-qa*np.sqrt(2)*tau*tn,center_t+qa*np.sqrt(2)*tau*tn])
        details.append(dict(bias=bias,tangent_norm=tn,selected=['tangent','split_direct','structural'][choice],
                            eta=eta,angle=angle,delta=delta))
    return np.array(endpoints),np.array(ablation),details,center_t
