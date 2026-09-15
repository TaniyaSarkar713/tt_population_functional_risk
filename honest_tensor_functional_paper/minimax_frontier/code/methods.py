"""Minimax frontier: precise scopes, no general multi-cap optimizer claim.

spectral_interval is minimax in rate for ONE constrained unfolding, with all
other caps unrestricted. It remains honest on a more restricted tensor class.
Higher-order orthogonal-profile proxies are sharp statistical rates; the ideal
prefix fits attaining them are not implemented here.
"""
import math
import numpy as np
from scipy.linalg import svd
from scipy.special import logsumexp
from scipy.stats import norm


def spectral_clip_solve(singular, l1_budget, l2_budget, iterations=90):
    """Convex scalar problem a*t + v*||(sigma-t)+||_2 and a dual witness.

    Dual: max sigma.b, b>=0, ||b||_1<=a, ||b||_2<=v. Returned upper/lower
    bounds are ordinary floating-point evaluations, not directed-rounding
    interval certificates. The feasible dual vector and residuals are exposed.
    """
    sigma=np.sort(np.asarray(singular,float))[::-1]
    a,v=float(l1_budget),float(l2_budget)
    if sigma.ndim!=1 or not len(sigma) or np.min(sigma)<0 or not np.isfinite(sigma).all() or not np.isfinite([a,v]).all() or a<0 or v<0:
        raise ValueError('Require finite nonnegative spectrum and budgets.')
    if a==0 or v==0 or sigma[0]==0:
        t=sigma[0] if a==0 else 0.
        soft=np.maximum(sigma-t,0.)
        return dict(threshold=float(t),soft=soft,primal=0.,dual=0.,gap=0.,dual_vector=np.zeros_like(sigma),iterations=0)
    lo,hi=0.,float(sigma[0]);niter=0
    if a >= v*np.sum(sigma)/np.linalg.norm(sigma):
        hi=lo=0.
    elif a <= v*np.sqrt(np.count_nonzero(sigma==sigma[0])):
        lo=hi=float(sigma[0])
    else:
        for niter in range(1,iterations+1):
            mid=(lo+hi)/2;soft=np.maximum(sigma-mid,0);sn=np.linalg.norm(soft)
            derivative=a-v*np.sum(soft)/sn
            if derivative>=0:hi=mid
            else:lo=mid
            if hi-lo<=8*np.finfo(float).eps*sigma[0]:break
    candidates=[lo,hi,(lo+hi)/2]
    best=None;lower=0.;witness=np.zeros_like(sigma)
    for t in candidates:
        soft=np.maximum(sigma-t,0);sn=np.linalg.norm(soft);sl=np.sum(soft)
        if sn>0:
            b=soft*min(v/sn,a/sl)
        else:
            active=sigma==sigma[0];k=np.count_nonzero(active);b=active.astype(float)*min(a/k,v/np.sqrt(k))
        # Shrink slightly so that the reported witness has slack against
        # floating evaluation of its norms; this does not certify SVD rounding.
        b*=1-16*np.finfo(float).eps
        dual=float(sigma@b);primal=float(a*t+v*sn)
        if dual>lower:lower,witness=dual,b
        if best is None or primal<best['primal']:best=dict(threshold=float(t),soft=soft,primal=primal)
    best.update(dual=lower,gap=max(0.,best['primal']-lower),dual_vector=witness,iterations=niter,
                dual_l1=float(np.sum(witness)),dual_l2=float(np.linalg.norm(witness)))
    return best


def unfolding(x, mode=None, cut=None):
    if (mode is None)==(cut is None):raise ValueError('Specify exactly one mode or TT cut.')
    x=np.asarray(x,float)
    if mode is not None:
        if int(mode)!=mode or not 0<=mode<x.ndim:raise ValueError('Invalid mode.')
        return np.moveaxis(x,mode,0).reshape(x.shape[mode],-1)
    if int(cut)!=cut or not 1<=cut<x.ndim:raise ValueError('Invalid cut.')
    return x.reshape(int(np.prod(x.shape[:cut])),-1)


def spectral_plan(loading,M,rank,tau=1.,alpha=.05,mode=None,cut=None):
    """Loading-only preprocessing, reusable across observations at fixed bounds."""
    L=np.asarray(loading,float)
    if L.ndim<2 or not np.isfinite(L).all() or not np.isfinite([M,tau,alpha]).all() or M<0 or tau<=0 or not 0<alpha<.25:
        raise ValueError('Invalid loading or model parameters.')
    lm=unfolding(L,mode,cut)
    if int(rank)!=rank or not 1<=rank<=min(lm.shape):raise ValueError('Invalid unfolding cap.')
    rank=int(rank);U,sigma,Vh=svd(lm,full_matrices=False,check_finite=False)
    h=float(M*np.linalg.norm(sigma[:rank]));lnorm=float(np.linalg.norm(sigma));q=norm.isf(alpha/2)
    ci=spectral_clip_solve(sigma,M*np.sqrt(rank),q*tau)
    risk=spectral_clip_solve(sigma,M*np.sqrt(rank),tau)
    if M<=tau:
        rate=h
    else:
        rate=risk['primal']
    def restore(matrix):
        if mode is None:return matrix.reshape(L.shape)
        moved=matrix.reshape((L.shape[mode],)+tuple(n for k,n in enumerate(L.shape) if k!=mode))
        return np.moveaxis(moved,0,mode)
    def make(sol):
        # Non-BLAS sum avoids backend FP-status artifacts in projector products.
        mat=np.einsum('ik,k,kj->ij',U,sol['soft'],Vh,optimize=False)
        residual=sigma-sol['soft'];bias=M*np.linalg.norm(residual[:rank]);sd=tau*np.linalg.norm(sol['soft'])
        return restore(mat),float(bias),float(sd)
    Wc,bc,sc=make(ci);We,be,se=make(risk)
    radius=bc+q*sc;method='spectral_clip'
    if h<=radius:Wc=np.zeros_like(L);radius=h;method='structural'
    mse_bound=be*be+se*se;est_method='spectral_clip'
    if h*h<=mse_bound:We=np.zeros_like(L);mse_bound=h*h;est_method='zero'
    return dict(shape=L.shape,ci_loading=Wc,estimate_loading=We,structural=h,radius=float(radius),
                mse_upper=float(mse_bound),selected=method,estimate_selected=est_method,rate=float(rate),
                spectrum=sigma,rank=rank,ci_optimizer=ci,risk_optimizer=risk,mode=mode,cut=cut,
                loading_norm=lnorm,tau=tau,alpha=alpha,M=M)


def spectral_interval(z,plan):
    z=np.asarray(z,float)
    if z.shape!=plan['shape'] or not np.isfinite(z).all():raise ValueError('Observation/plan mismatch.')
    center=float(np.sum(z*plan['ci_loading']));r=plan['radius'];h=plan['structural']
    lo,hi=max(-h,center-r),min(h,center+r);empty=lo>hi
    if empty:lo=hi=0.
    estimate=float(np.clip(np.sum(z*plan['estimate_loading']),-h,h))
    return dict(lo=float(lo),hi=float(hi),width=float(hi-lo),estimate=estimate,empty=bool(empty),selected=plan['selected'])


def balanced_partition(b,rank):
    """Greedy conditional-expectation partition used in the rank-r lower bound."""
    b=np.asarray(b,float)
    if b.ndim!=1 or not np.isfinite(b).all() or np.min(b)<0 or int(rank)!=rank or rank<1:raise ValueError('Invalid partition inputs.')
    rank=int(rank);loads=np.zeros(rank);groups=[[] for _ in range(rank)]
    for i in np.argsort(-b):
        j=int(np.argmin(loads));groups[j].append(int(i));loads[j]+=b[i]
    return groups,loads


def orthogonal_rate(weights,M,tau=1.,order=4):
    """L3 exact minimax RATE proxy for fixed caps/order>=4, all budgets.

    This does not compute the attaining ideal confidence interval.
    """
    w=np.asarray(weights,float)
    if w.ndim!=1 or not len(w) or not np.isfinite(w).all() or not np.isfinite([M,tau]).all() or M<0 or tau<=0 or int(order)!=order or order<4:
        raise ValueError('Require order>=4, finite weights, M>=0, tau>0.')
    w=np.sort(abs(w))[::-1];p=len(w);F=np.minimum(M,tau*np.sqrt(1+np.log(np.arange(1,p+1))))
    rate=float(np.dot(w,np.diff(F,prepend=0)))
    if M<=tau:return dict(rate=rate,geometric_proxy=float(M*w[0]),ratio=1.,levels=[])
    Q=min(np.log(p),(M/tau)**2);q=1.;levels=[];proxy=tau*w[0]
    while q<=Q:
        N=min(p,int(np.floor(np.exp(q))))
        if N>=2:
            levels.append({'q':q,'N':N,'weight':float(w[N-1])});proxy+=tau*np.sqrt(q)*w[N-1]
        q*=4
    return dict(rate=rate,geometric_proxy=float(proxy),ratio=rate/proxy if proxy else 1.,levels=levels)


def entropy_prior_certificate(order,levels):
    """Upper bound on the full-tensor mixture chi-square via collision states.

    levels is the number of entropy scales q=1,4,... . Actual collision
    probabilities are bounded by min(1,4 exp(-q)); monotonicity makes this
    a conservative analytic bound even when dimensions are only symbolic.
    """
    if order<4 or int(order)!=order or not 0<=levels<=18:raise ValueError('Invalid order/level count.')
    C=1+1/(1-4**(-1/order));eps=1/(16*C**(order/2));qs=4.**np.arange(levels)
    logp=np.minimum(0.,np.log(4)-qs);terms=[]
    for mask in range(1<<levels):
        lp=0.;overlap=1.;valid=True
        for j,q in enumerate(qs):
            if (mask>>j)&1:lp+=logp[j];overlap+=q**(1/order)
            elif logp[j]==0:valid=False;break
            else:lp+=np.log1p(-np.exp(logp[j]))
        if not valid:continue
        x=eps*eps*overlap**order
        logexcess=x+np.log1p(-np.exp(-x)) if x>30 else np.log(np.expm1(x))
        terms.append(lp+logexcess)
    value=float(np.exp(logsumexp(terms)))
    return dict(order=order,levels=levels,epsilon=eps,chi_square_upper=value,
                tv_upper=.5*np.sqrt(value),norm_factor_upper=1/16,
                real_arithmetic_universal_chi_square_bound=.25)


def _ratio_range(numerators,denominator,power):
    lo,hi=1.,1.
    for a,b in numerators:
        corners=[lo*a,lo*b,hi*a,hi*b];lo,hi=min(corners),max(corners)
    dlo,dhi=denominator
    ds=[dlo**power,dhi**power]
    quotients=[x/y for x in [lo,hi] for y in ds]
    return min(quotients),max(quotients)


def adaptive_coordinate_interval(z,target,M,rng,tau=1.,alpha=.05):
    """P5: unseparated rank-one honesty, adaptive axis-pointwise hierarchy.

    The pilot chooses an anchor without knowing its location. Only the
    original direct interval is used for d<=1. For d>=2, independent validation
    calibrates the anchor and d fibers. No estimated-rank substitution is made.
    """
    z=np.asarray(z,float);target=tuple(target)
    if z.ndim<2 or len(target)!=z.ndim or any(int(i)!=i or not 0<=i<n for i,n in zip(target,z.shape)) or not np.isfinite(z).all() or not np.isfinite([M,tau,alpha]).all() or M<0 or tau<=0 or not 0<alpha<.25:
        raise ValueError('Invalid rank-one coordinate inputs.')
    target=tuple(int(i) for i in target)
    if M==0:return dict(lo=0.,hi=0.,width=0.,anchor=target,distance=0,ratio=False,empty=False)
    aux=tau*rng.normal(size=z.shape);pilot=z+aux;validation=z-aux
    anchor=tuple(np.unravel_index(np.argmax(np.abs(pilot)),z.shape));changed=[k for k in range(z.ndim) if anchor[k]!=target[k]];d=len(changed)
    rd=norm.isf(alpha/4)*tau;y=float(z[target]);lo,hi=max(-M,y-rd),min(M,y+rd);used=False
    if d>=2:
        q=norm.isf(alpha/(4*(d+1)))*np.sqrt(2)*tau;x=float(validation[anchor])
        if abs(x)>q:
            fibers=[]
            for k in changed:
                idx=list(anchor);idx[k]=target[k];v=float(validation[tuple(idx)]);fibers.append((v-q,v+q))
            a,b=_ratio_range(fibers,(x-q,x+q),d-1);lo,hi=max(lo,a),min(hi,b);used=True
    empty=lo>hi
    if empty:lo=hi=0.
    return dict(lo=float(lo),hi=float(hi),width=float(hi-lo),anchor=anchor,distance=d,ratio=used,empty=bool(empty))
