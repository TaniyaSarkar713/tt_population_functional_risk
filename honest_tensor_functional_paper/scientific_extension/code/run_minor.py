import json
from pathlib import Path
import numpy as np
from methods import rank_one_minor_interval
from run_experiments import summarize
ROOT=Path(__file__).resolve().parents[1]
cfg={'seed':2026091477,'replications':4000,'a_values':[0.,2.,5.,10.,30.,100.,1000.],
     'tau':1.,'M_rule':'max(1, 2*a)','scope':'prespecified rank-one minor; target zero at axis means'}
(ROOT/'results/minor_configurations.json').write_text(json.dumps(cfg,indent=2)+'\n')
rng=np.random.default_rng(cfg['seed']);rows=[]
for a in cfg['a_values']:
    ws=[];cov=[];used=[];errors=[]
    z=rng.normal(size=(cfg['replications'],4));z[:,0]+=a
    for x,b,c,y in z:
        r=rank_one_minor_interval(x,b,c,y,max(1,2*a));ws.append(r['width']);cov.append(r['lo']<=0<=r['hi']);used.append(r['used_ratio']);errors.append(.5*(r['lo']+r['hi']))
    result={'a':a,**summarize(errors,ws,cov),'ratio_fraction':float(np.mean(used)),
            'scaled_length':float(np.mean(ws)*a),'midpoint_MSE_scope':'diagnostic at this zero-target point only; no uniform scalar-risk theorem'}
    rows.append(result);np.savez_compressed(ROOT/f'results/minor_a{a:g}.npz',width=ws,covered=cov,midpoint_error=errors,used_ratio=used)
(ROOT/'results/minor_results.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
