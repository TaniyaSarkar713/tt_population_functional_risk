"""Explicit rounding policy and a scalar companion separate from CI midpoints."""
import numpy as np
from scipy.stats import norm

COVERAGE_ULPS=4

def coverage_events(endpoints,target,ulps=COVERAGE_ULPS):
    """Permit only four representable endpoint steps for evaluation rounding.

    This is a numerical comparison convention, not a statistical slack term.
    Exact structural boundaries can differ by one ULP after different algebra.
    No max(1,abs(target)) floor and no relative statistical tolerance is used.
    Strict counts and every changed event are retained by the revision audit.
    """
    ep=np.asarray(endpoints,float)
    lo,hi=ep[...,0].copy(),ep[...,1].copy()
    for _ in range(ulps):
        lo=np.nextafter(lo,-np.inf);hi=np.nextafter(hi,np.inf)
    return (lo<=target)&(target<=hi)

def scalar_companion(endpoints,direct,structural,tau):
    """95%-CI companion by default; inputs may be any fixed confidence level.

    The CI is unchanged. Use zero on the small structural branch; otherwise
    use its midpoint when nonempty and the clipped direct estimate on the
    legacy {0} empty-section sentinel. A real zero singleton is harmless to
    replace for this separate estimator. Requires every non-sentinel interval
    to lie inside the calibrated direct interval. See Proposition R1.
    """
    ep=np.asarray(endpoints,float);direct=np.asarray(direct,float)
    midpoint=ep.mean(axis=-1)
    sentinel=(ep[...,0]==0)&(ep[...,1]==0)
    out=np.where(sentinel,np.clip(direct,-structural,structural),midpoint)
    return np.zeros_like(out) if structural<=tau else np.clip(out,-structural,structural)

def companion_risk_upper(structural,tau,alpha=.05):
    z=norm.isf(alpha/4)
    return structural**2 if structural<=tau else tau**2*(1+2*z*np.sqrt(2/np.pi)+z*z)
