"""Public-API timing only, not additional statistical Monte Carlo evidence."""
import json,time
from pathlib import Path
import numpy as np
from threadpoolctl import threadpool_limits
from methods import cap_interval
ROOT=Path(__file__).resolve().parents[1]
rng=np.random.default_rng(2026091498);rows=[]
with threadpool_limits(limits=1):
    for geom,K,ps in [('tucker',3,[32,64,128]),('tt',4,[8,16,24])]:
        for p in ps:
            L=np.zeros((p,)*K);L[(np.arange(p),)*K]=1/np.sqrt(p);z=rng.normal(size=L.shape)
            for r in [1,4]:
                durations=[]
                for rep in range(3):
                    start=time.perf_counter();a=cap_interval(z,L,np.sqrt(p),[r]*(K if geom=='tucker' else K-1),rng,geometry=geom,kappa=np.sqrt(r/p));durations.append(time.perf_counter()-start)
                row={'geometry':geom,'order':K,'p':p,'rank':r,'entries':int(z.size),'input_tensor_mebibytes':z.nbytes/2**20,
                     'seconds':durations,'median_seconds':float(np.median(durations)),'selected':a['candidate'],
                     'scope':'Full public API including loading SVDs and artificial splitting; fixed observation per shape, one library thread; not a weak-minimax benchmark.'}
                rows.append(row);print(geom,p,r,round(row['median_seconds'],4),flush=True)
(ROOT/'results/runtime_results.json').write_text(json.dumps({'seed':2026091498,'calls':36,'warmups':0,'results':rows},indent=2)+'\n')
