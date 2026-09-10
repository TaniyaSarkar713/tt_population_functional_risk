"""Runtime/calibration prototype; it does not benchmark minimax projection."""
import csv,json,time,platform
from pathlib import Path
import numpy as np
from scipy.stats import beta
from truncated_scan import TruncatedScan,sphere_net
ROOT=Path(__file__).resolve().parents[1]
rng=np.random.default_rng(20260912)
def main():
    # Angular coverage and product-vector normalization.
    net=sphere_net(2,3)
    grid=2*np.pi*np.arange(20000)/20000
    points=np.column_stack([np.cos(grid),np.sin(grid)])
    nearest=np.sqrt(np.maximum(0,2-2*np.max(points@net.T,axis=1)))
    assert nearest.max()<=1/6
    reference=TruncatedScan(3)
    Z=rng.normal(size=(3,3,3))
    got=reference.evaluate(Z)
    for t,level in reference.levels.items():
        explicit=max(abs(float(Z.ravel()[ix]@v)) for ix in level['indices'] for v in level['products'])
        assert abs(explicit-got['history'][t-1]['max_contraction'])<1e-12
        assert np.allclose(np.linalg.norm(level['products'],axis=1),1)
    rows=[]
    reps=100
    for p in [8,16,32]:
        scan=TruncatedScan(p)
        for signal in ['zero','coordinate','diffuse_support']:
            A=np.zeros((p,p,p))
            if signal=='coordinate':A[0,0,0]=np.sqrt(p)
            if signal=='diffuse_support':
                s=max(1,int(p**(1/3)))
                x=np.zeros(p);x[:s]=1/np.sqrt(s)
                A=np.sqrt(p)*np.einsum('i,j,k->ijk',x,x,x)
            truth=sum(A[(i,i,i)] for i in range(p))/np.sqrt(p)
            covered=[];length=[];seconds=[];accept=[]
            for _ in range(reps):
                Z=A+rng.normal(size=A.shape)
                start=time.perf_counter()
                out=scan.evaluate(Z)
                seconds.append(time.perf_counter()-start)
                assert 0<=out['length']<=out['base_length']+1e-12
                covered.append(out['lo']<=truth<=out['hi'])
                length.append(out['length']);accept.append(out['history'][-1]['accepted'])
            count=sum(covered)
            lo=0 if count==0 else beta.ppf(.025,count,reps-count+1)
            hi=1 if count==reps else beta.ppf(.975,count+1,reps-count)
            rows.append(dict(p=p,order=3,signal=signal,replications=reps,
                             contractions=sum(x['contractions'] for x in scan.levels.values()),
                             coverage=np.mean(covered),coverage_mcse=np.std(covered,ddof=1)/np.sqrt(reps),
                             coverage_lower=lo,coverage_upper=hi,mean_length=np.mean(length),
                             length_mcse=np.std(length,ddof=1)/np.sqrt(reps),
                             mean_seconds=np.mean(seconds),median_seconds=np.median(seconds),
                             runtime_mcse=np.std(seconds,ddof=1)/np.sqrt(reps),
                             acceptance=np.mean(accept),baseline_length=out['base_length']))
    with (ROOT/'results/scan_benchmark.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)
    summary=dict(status='PASS',seed=20260912,replications_per_configuration=reps,
                 configurations=len(rows),platform=platform.platform(),
                 max_sphere_distance=float(nearest.max()),
                 limitation='Complete levels 1 and 2 only. These small dimensions validate implementation and costs; no sharp-rate or practical interval improvement is claimed.',
                 results=rows)
    (ROOT/'results/scan_benchmark.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2))
if __name__=='__main__':main()
