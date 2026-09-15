"""Actual access timings and traced allocations, separately from MC simulation."""
import json
import platform
import time
import tracemalloc
import numpy as np
from threadpoolctl import threadpool_limits
from common import ROOT,high,global_fit,write_json,hashes,rng_for
from tensor_methods import pointwise_levels,xch_pca


def measure(fn,reps):
    fn()  # One warmup, fixed before measurement.
    times=[]
    for _ in range(reps):
        t=time.perf_counter();fn();times.append(time.perf_counter()-t)
    tracemalloc.start();fn();current,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    return dict(repeats=reps,mean_seconds=float(np.mean(times)),seconds_se=float(np.std(times,ddof=1)/np.sqrt(reps)),
                median_seconds=float(np.median(times)),peak_traced_bytes=peak,
                memory_scope='Python and NumPy traced allocations during one call; excludes untraced native workspace and preallocated input.')


def main():
    cfg=json.loads((ROOT/'configs/runtime.json').read_text());rows=[];started=time.time();source=hashes()
    with threadpool_limits(limits=1):
        for p in cfg['diagonal_p']:
            d=rng_for('runtime',p).normal(size=p);r=int(np.ceil(np.sqrt(p)))
            rows.append(dict(method='growing_actual_diagonal',p=p,input_bytes=d.nbytes,
                **measure(lambda:high.growing_cap_interval(d,8.,r),cfg['diagonal_repeats'])))
        for p in cfg['tensor_p']:
            a=8*high.pointwise_amplitude_bound(p,1);z=rng_for('runtime_tensor',p).normal(size=(p,)*3);z[0,0,0]+=a
            L=high.flat_loading(p,3);aux=rng_for('runtime_aux',p).normal(size=z.shape);M=1.1*a
            for name,fn in [('pointwise',lambda:pointwise_levels(z,M,1,aux)),('xch',lambda:xch_pca(z,L,1))]:
                rows.append(dict(method=name,p=p,input_bytes=z.nbytes,**measure(fn,cfg['tensor_repeats'])))
                print(name,p,rows[-1]['mean_seconds'],flush=True)
        for K in cfg['solver_K']:
            z=rng_for('runtime_solver',K).normal(size=(2,)*K);L=high.flat_loading(2,K)
            for budget in cfg['solver_budgets']:
                def fn():
                    return global_fit.BinaryRankOneOptimizer(z,L,2.).project_interval(tolerance=.1,max_nodes=budget)
                rows.append(dict(method='global',K=K,p=2,budget=budget,input_bytes=z.nbytes,
                                 **measure(fn,cfg['solver_repeats']),result=fn()))
                print('global',K,budget,rows[-1]['mean_seconds'],flush=True)
    write_json(ROOT/'results/runtime.json',dict(status='NEEDS CHECK',rows=rows))
    write_json(ROOT/'logs/run_S11.json',dict(status='COMPLETED',seconds=time.time()-started,source_hashes=source,
                                           platform=platform.platform(),python=platform.python_version()))


if __name__=='__main__':main()
