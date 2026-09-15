"""Scientific extensions. General cap intervals are honest, not weak-minimax solvers.

All Gaussian routines assume an explicitly observed tensor with iid known-scale
noise. diagonal_sparse requires an ADDITIONAL exact diagonal-mean restriction.
loading_envelope evaluates rate proxies, not confidence interval endpoints.
"""
import numpy as np
from scipy.linalg import svd
from scipy.stats import norm



def _checked_matmul(a, b):
    """Check BLAS results; recompute in a non-BLAS contraction on an FP signal.

    Apple Accelerate/NumPy can signal an FP exception for bounded projector
    products. This fallback does not assume every warning is spurious: both
    paths must return finite values, or execution fails explicitly.
    """
    try:
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            out = np.matmul(a, b)
    except FloatingPointError:
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            out = np.einsum('ik,kj->ij', a, b, optimize=False)
    if not np.isfinite(out).all():
        raise FloatingPointError('Nonfinite matrix product in projection.')
    return out

def flat_prefix_F(p, M, tau=1., order=3):
    if int(p) != p or p < 1 or M < 0 or tau <= 0 or int(order) != order or order < 3:
        raise ValueError('Require p>=1, M>=0, tau>0, integer order>=3.')
    if not np.isfinite([p, M, tau]).all():
        raise ValueError('Nonfinite parameter.')
    t = 1 + np.log(np.arange(1, p + 1, dtype=float))
    if M == 0:
        return np.zeros(p)
    if order >= 4:
        return np.minimum(M, tau * np.sqrt(t))
    return np.minimum(np.minimum(M, tau * np.sqrt(t) *
                      (1 + np.maximum(0, np.log(M / tau) - .5 * np.log(t)))),
                      tau * t ** 1.5)


def loading_envelope(weights, M, tau=1., order=3):
    w = np.asarray(weights, float)
    if w.ndim != 1 or len(w) == 0 or not np.isfinite(w).all():
        raise ValueError('Finite nonempty vector required.')
    w = np.sort(np.abs(w))[::-1]
    F = flat_prefix_F(len(w), M, tau, order)
    lower = float(np.max(w * F))
    upper = float(np.dot(w, np.diff(F, prepend=0)))
    factor = 1 + np.log(F[-1] / F[0]) if F[0] > 0 else 1.
    return dict(lower_proxy=lower, upper_proxy=upper,
                proxy_ratio=upper/lower if lower > 0 else 1.,
                proven_proxy_factor=float(factor),
                universal_factor=float(1 + (1.5 if order == 3 else .5) * np.log(1 + np.log(len(w)))))


def log_profile_rate(p, M, beta, tau=1., order=3, scale=1.):
    """AB2 rate proxy; constants depend on fixed beta, not p,M,tau,scale."""
    if beta <= 0 or beta in ((.5, 1.5) if order == 3 else (.5,)):
        raise ValueError('Positive noncritical beta required.')
    flat_prefix_F(1, M, tau, order)
    if M <= tau:
        return scale * M
    m, ell = M / tau, 1 + np.log(p)
    T, U = min(ell, m*m), min(ell, 1 + np.log(m))
    if order >= 4:
        return scale * tau * (T ** (.5-beta) if beta < .5 else 1.)
    if beta < .5:
        return scale * tau * min(T**(1.5-beta), T**(.5-beta)*(1+np.log(m/np.sqrt(T))))
    return scale * tau * (U**(1.5-beta) if beta < 1.5 else 1.)


def mode_project(x, basis, mode):
    if basis is None:
        return x
    a = np.moveaxis(x, mode, 0)
    return np.moveaxis(np.tensordot(basis, np.tensordot(basis.T, a, axes=(1,0)), axes=(1,0)), 0, mode)


def product_project(x, bases, omit=None):
    out = x
    for k, b in enumerate(bases):
        if k != omit:
            out = mode_project(out, b, k)
    return out


def tangent_project(x, bases):
    out = -(x.ndim-1) * product_project(x, bases)
    for k in range(x.ndim):
        out = out + product_project(x, bases, omit=k)
    return out


def safe_scalar(candidate_center, direct, structural, noise_scale, kappa):
    if not 0 < kappa <= 1:
        raise ValueError('kappa must be in (0,1].')
    D = noise_scale * np.sqrt(8 * np.log(2/kappa))
    return float(np.clip(np.clip(candidate_center, direct-D, direct+D), -structural, structural))


def cap_interval(z, loading, M, caps, rng, tau=1., alpha=.05,
                 geometry='tucker', kappa=.1, return_details=False):
    """Polynomial SVD algorithm, arbitrary loading and unequal dimensions.

    Supplied caps are retained at weak or undersaturated means. The scalar uses
    the PRE-intersection center; it never switches to a zero sentinel midpoint.
    kappa is deterministic performance tuning, not an estimated population rank.
    """
    z, L = np.asarray(z, float), np.asarray(loading, float)
    if z.shape != L.shape or z.ndim < 3 or not np.isfinite(z).all() or not np.isfinite(L).all():
        raise ValueError('Matching finite tensors of order at least three required.')
    if not np.isfinite([M,tau,alpha,kappa]).all() or M < 0 or tau <= 0 or not 0 < alpha < .25 or not 0 < kappa <= 1:
        raise ValueError('Invalid Gaussian parameters.')
    ncuts = z.ndim if geometry == 'tucker' else z.ndim-1 if geometry == 'tt' else 0
    if ncuts == 0 or len(caps) != ncuts:
        raise ValueError('Incorrect geometry or caps.')
    matrices = []
    for j, rank in enumerate(caps):
        m = np.moveaxis(z,j,0).reshape(z.shape[j],-1) if geometry == 'tucker' else z.reshape(int(np.prod(z.shape[:j+1])),-1)
        if int(rank) != rank or not 1 <= rank <= min(m.shape):
            raise ValueError('Cap must be an integer within its unfolding dimensions.')
        matrices.append(m.shape)
    lnorm = float(np.linalg.norm(L))
    if lnorm == 0 or M == 0:
        return dict(lo=0., hi=0., width=0., estimate=0., candidate='structural', candidate_center=0., delta=0., empty=False,
                    direct=float(np.sum(L*z)), structural=0., candidates=[])
    s = tau * lnorm
    d0 = np.sqrt(8*np.log(2/kappa))
    delta = alpha*kappa**4 / (64*(1+d0)**4)
    v = np.sqrt(2)*tau
    q = norm.isf((alpha/2-delta)/2)
    aux = tau*rng.normal(size=z.shape)
    pilot, validation = z+aux, z-aux
    h = M*lnorm
    bases, errors, candidates, etas = [], [], [], []
    for j, (rank, shape) in enumerate(zip(caps, matrices)):
        rank = int(rank)
        if geometry == 'tucker':
            pm = np.moveaxis(pilot,j,0).reshape(shape)
            lm = np.moveaxis(L,j,0).reshape(shape)
        else:
            pm, lm = pilot.reshape(shape), L.reshape(shape)
        sl = svd(lm, full_matrices=False, compute_uv=False, check_finite=False)
        h = min(h, M*float(np.linalg.norm(sl[:rank])))
        eta = float(2*v*np.sqrt(2*((sum(shape))*np.log(9)+np.log(2*ncuts/delta))))
        etas.append(eta)
        if geometry == 'tucker' and rank == shape[0]:
            bases.append(None); errors.append(0.)
            continue
        if geometry == 'tt' and rank == min(shape):
            TL, error = L.copy(), 0.
        else:
            u, ss, vh = svd(pm, full_matrices=False, check_finite=False)
            den = ss[rank-1]-eta
            error = min(1., 2*eta/den) if den > 0 else 1.
            if geometry == 'tucker':
                bases.append(u[:,:rank].copy()); errors.append(error)
                continue
            U, V = u[:,:rank], vh[:rank].T
            left = _checked_matmul(U, _checked_matmul(U.T, lm))
            right = _checked_matmul(_checked_matmul(lm, V), V.T)
            TL = (left+right-_checked_matmul(_checked_matmul(left, V), V.T)).reshape(z.shape)
        residual = L-TL
        bias = M*float(np.linalg.norm(residual))*error**2
        candidates.append(dict(name=f'tt_cut_{j+1}', radius=bias+q*v*np.linalg.norm(TL),
                               center=float(np.sum(TL*validation)), bias=bias, loading_norm=float(np.linalg.norm(TL))))
        errors.append(error)
    if geometry == 'tucker':
        TL = tangent_project(L,bases)
        angle = min(1., np.sqrt(sum(errors[j]**2*errors[k]**2 for j in range(z.ndim) for k in range(j+1,z.ndim))))
        bias = M*float(np.linalg.norm(L-TL))*angle
        candidates.append(dict(name='tucker_tangent',radius=bias+q*v*np.linalg.norm(TL),
                               center=float(np.sum(TL*validation)),bias=bias,loading_norm=float(np.linalg.norm(TL))))
    candidates.extend([dict(name='split_direct',radius=q*v*lnorm,center=float(np.sum(L*validation)),bias=0.,loading_norm=lnorm),
                       dict(name='structural',radius=h,center=0.,bias=h,loading_norm=0.)])
    choice = min(candidates, key=lambda c:c['radius'])
    direct = float(np.sum(L*z))
    c, r = float(choice['center']), float(choice['radius'])
    rd = norm.isf(alpha/4)*s
    lo, hi = max(c-r,direct-rd,-h), min(c+r,direct+rd,h)
    empty = lo > hi
    if empty:
        lo = hi = 0.
    est = safe_scalar(c,direct,h,s,kappa)
    out = dict(lo=float(lo),hi=float(hi),width=float(hi-lo),estimate=est,candidate=choice['name'],
               candidate_center=c,candidate_radius=r,delta=float(delta),empty=bool(empty),direct=direct,structural=h,
               candidates=[{k:float(v) if isinstance(v,np.floating) else v for k,v in c.items()} for c in candidates])
    if return_details:
        out.update(errors=errors,etas=etas)
    return out


def diagonal_sparse(z, M, rank, tau=1., alpha=.05):
    """Exact diagonal-mean submodel ONLY: sharp all caps/budgets, O(p)."""
    z = np.asarray(z,float)
    if z.ndim != 1 or len(z) == 0 or not np.isfinite(z).all():
        raise ValueError('Finite diagonal vector required.')
    p = len(z)
    if int(rank) != rank or not 1 <= rank <= p or not np.isfinite([M,tau,alpha]).all() or M < 0 or tau <= 0 or not 0 < alpha < .25:
        raise ValueError('Invalid sparse parameters.')
    u = np.sqrt(2*np.log1p(p/rank**2))
    t = tau*u
    nu = 2*(u*norm.pdf(u)+norm.sf(u))
    bias = rank*t/np.sqrt(p)
    variance = (2*rank*(t*t+tau*tau)+(p-rank)*tau*tau*nu)/p
    h = M*np.sqrt(rank/p)
    hard = float(np.sum(z*(np.abs(z)>t))/np.sqrt(p))
    direct = float(np.sum(z)/np.sqrt(p))
    cs = [('structural',0.,h),('direct',direct,norm.isf(alpha/2)*tau),('threshold',hard,bias+np.sqrt(variance/alpha))]
    name,c,r = min(cs,key=lambda x:x[2])
    risks = [h*h,tau*tau,bias*bias+variance]
    est = [0.,direct,hard][int(np.argmin(risks))]
    return dict(lo=c-r,hi=c+r,width=2*r,estimate=est,selected=name,mse_upper=min(risks),
                rate=min(h,tau*rank/np.sqrt(p)*np.sqrt(np.log1p(p/rank**2))),threshold=t,
                threshold_center=hard,bias_bound=bias,variance_bound=variance)


def empirical_bernstein(x, lower, upper, alpha=.05):
    x = np.asarray(x,float)
    if x.ndim != 1 or len(x)<2 or not np.isfinite(x).all() or not np.isfinite([lower,upper,alpha]).all() or upper < lower or not 0 < alpha < 1:
        raise ValueError('Invalid bounded-mean inputs.')
    if np.min(x) < lower-1e-9 or np.max(x)>upper+1e-9:
        raise ValueError('Observations outside prespecified range.')
    radius = np.sqrt(2*np.var(x,ddof=1)*np.log(4/alpha)/len(x)) + 7*(upper-lower)*np.log(4/alpha)/(3*(len(x)-1))
    center = float(np.mean(x))
    return dict(mean=center,radius=float(radius),lo=max(lower,center-radius),hi=min(upper,center+radius),n=len(x))


def corrected_projection_interval(f_cal, g_cal, g_val, lower, upper, alpha=.05):
    """Independent pilot chooses g; separate subjects calibrate its mean bias."""
    R = upper-lower
    b = empirical_bernstein(np.asarray(f_cal)-np.asarray(g_cal),-R,R,alpha/2)
    g = empirical_bernstein(g_val,lower,upper,alpha/2)
    center, radius = b['mean']+g['mean'],b['radius']+g['radius']
    lo, hi = max(lower,center-radius),min(upper,center+radius)
    if lo > hi:
        lo = hi = float(np.clip(center,lower,upper))
    return dict(mean=center,radius=radius,lo=lo,hi=hi,bias=b,projected=g)


def rank_one_minor_interval(anchor, row_entry, column_entry, target_entry,
                            M, tau=1., alpha=.05):
    """P4: rank-one minor target = row*column/anchor, whenever anchor != 0.

    Four entries must refer to one prescribed 2x2 matrix minor of a rank-one
    slice/unfolding, with target diagonally opposite the anchor. Valid uniformly
    at zero and vanishing anchors; pointwise rate tau^2/a at mean (a,0,0,0).
    Constant coordinate-access cost, no fitted rank or denominator assumption.
    """
    if not np.isfinite([anchor,row_entry,column_entry,target_entry,M,tau,alpha]).all() or M<0 or tau<=0 or not 0<alpha<.25:
        raise ValueError('Invalid minor inputs.')
    if M==0:
        return dict(lo=0.,hi=0.,width=0.,used_ratio=False,empty=False)
    q=norm.isf(alpha/12)*tau  # Three intervals, each failure alpha/6.
    lower,upper=-M,M
    used=abs(anchor)>q
    if used:
        products=[b*c for b in [row_entry-q,row_entry+q] for c in [column_entry-q,column_entry+q]]
        ratios=[z/a for z in products for a in [anchor-q,anchor+q]]
        lower,upper=max(lower,min(ratios)),min(upper,max(ratios))
    rd=norm.isf(alpha/4)*tau
    lower,upper=max(lower,target_entry-rd),min(upper,target_entry+rd)
    empty=lower>upper
    if empty:lower=upper=0.
    return dict(lo=float(lower),hi=float(upper),width=float(upper-lower),used_ratio=bool(used),empty=bool(empty))
