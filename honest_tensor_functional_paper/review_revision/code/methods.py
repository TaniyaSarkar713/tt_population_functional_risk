"""Public revised interval API with separate inferential and estimation outputs."""
import sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'empirical/code'))
from common import high
from numerics import scalar_companion,companion_risk_upper

def interval_and_estimate(observation,M,rank,rng,tau=1.,alpha=.05):
    """Supplied-cap Gaussian interval plus the separately analyzed R1 estimator.

    Equal modes/order >=3; common supplied Tucker mode cap. P1's expected-
    length rate additionally requires its strong saturated geometry. R1
    guarantees noise-scale risk, not the ideal weak-signal or pointwise
    minimax squared-risk rate. `midpoint_diagnostic` is not the estimate.
    """
    z=np.asarray(observation,float)
    out=high.pointwise_interval(z,M,rank,rng,tau,alpha)
    p=z.shape[0];ids=np.arange(p)
    direct=float(z[(ids,)*z.ndim].sum()/np.sqrt(p));ep=np.array([out['lo'],out['hi']])
    out.update(estimate=float(scalar_companion(ep,direct,M*np.sqrt(rank/p),tau)),
        estimator_id='interval_companion',estimator_alpha=float(alpha),midpoint_diagnostic=float(ep.mean()),
        empty_or_zero_singleton=bool(np.all(ep==0)),
        squared_risk_upper=companion_risk_upper(M*np.sqrt(rank/p),tau,alpha),
        risk_scope='R1 noise-scale risk on the supplied class; not pointwise minimax MSE')
    return out
