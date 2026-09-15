"""Meaningful regression checks for the scientific correction, plus fresh timing."""
import json,platform,sys,time,tracemalloc
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import norm
from threadpoolctl import threadpool_limits,threadpool_info
from methods import interval_and_estimate,high,scalar_companion
from numerics import coverage_events
ROOT=Path(__file__).resolve().parents[1]

def main():
    checks=0;gen=np.random.default_rng(2026091317)
    # A true miss survives the rounding convention; one representable step does not.
    target=9371115.579480572/8;ep=np.array([target-2,target-6e-5])
    assert not coverage_events(ep,target);checks+=1
    x=1.;ep=np.array([0.,np.nextafter(x,-np.inf)])
    assert not coverage_events(ep,x,0) and coverage_events(ep,x);checks+=1
    for h in [.1,1.,10.,1e9]:
        for psi in [-h,0.,h]:
            tau=1.;g=gen.normal(size=10000);Y=psi+g;rad=norm.isf(.05/4)
            centers=Y+gen.normal(size=len(Y))*10;rr=gen.exponential(size=len(Y))
            lo=np.maximum(np.maximum(centers-rr,Y-rad),-h);hi=np.minimum(np.minimum(centers+rr,Y+rad),h)
            empty=lo>hi;ep=np.column_stack([lo,hi]);ep[empty]=0
            estimate=scalar_companion(ep,Y,h,tau)
            assert np.all(abs(estimate-psi)<=((h if h<=tau else abs(g)+rad)+1e-6));checks+=len(Y)
            assert np.all(abs(estimate)<=h);checks+=1
    # Same original RNG stream: the public method must preserve interval endpoints.
    for p,r,a,M in [(4,1,0.,2.),(8,2,200000.,400000.)]:
        z=gen.normal(size=(p,)*3)
        for i in range(r):z[i,i,i]+=a
        for alpha in [.1,.05,.01]:
            old=high.pointwise_interval(z,M,r,np.random.default_rng(11),1.,alpha)
            new=interval_and_estimate(z,M,r,np.random.default_rng(11),1.,alpha)
            assert (old['lo'],old['hi'])==(new['lo'],new['hi']);checks+=1
            assert new['estimator_alpha']==alpha and np.isfinite(new['estimate']);checks+=1
    timings=[]
    with threadpool_limits(limits=1):
        for p in [8,16,32,64]:
            z=gen.normal(size=(p,)*3);M=2.;r=1
            interval_and_estimate(z,M,r,gen)
            times=[]
            for _ in range(10):
                start=time.perf_counter();interval_and_estimate(z,M,r,gen);times.append(time.perf_counter()-start)
            tracemalloc.start();interval_and_estimate(z,M,r,gen);current,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
            timings.append(dict(p=p,order=3,rank=r,calls=10,mean_seconds=float(np.mean(times)),seconds_se=float(np.std(times,ddof=1)/np.sqrt(10)),
                input_entries=p**3,input_bytes=z.nbytes,diagonal_access_entries=p,diagonal_access_bytes=p*8,peak_traced_call_bytes=peak,
                memory_scope='Preallocated input excluded from trace; native BLAS/LAPACK workspace not guaranteed traced. Trace is not RSS.',
                theoretical_full_input_storage='O(p^K)',theoretical_economy_SVD_work='O(K p^(K+1))'))
    (ROOT/'tables/runtime_revision.json').write_text(json.dumps(timings,indent=2)+'\n')
    result=dict(status='PASS',checks=checks,runtime_calls=40,seed=2026091317,python=sys.version,numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform(),threadpools=threadpool_info())
    (ROOT/'logs/method_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

if __name__=='__main__':main()
