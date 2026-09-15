"""Recompute all summaries from retained endpoints, without new draws."""
import json
import numpy as np
from run_experiments import ROOT,summary


def main():
    path=ROOT/'results/simulation_results.json';rows=json.loads(path.read_text());changes=[]
    for c in rows:
        data=np.load(ROOT/'results'/f"{c['id']}.npz");truth=float(data['truth'])
        c['method']=summary(data['lo'],data['hi'],truth,data.get('estimate'))
        c['direct']=summary(data['direct_lo'],data['direct_hi'],truth,data.get('direct_estimate'))
        for name in ['method','direct']:
            if c[name]['rounding_changed']:
                changes.append(dict(id=c['id'],method=name,strict=c[name]['strict_covered'],bounded_ulp=c[name]['covered'],changed=c[name]['rounding_changed']))
    path.write_text(json.dumps(rows,indent=2)+'\n')
    (ROOT/'audit/rounding_audit.json').write_text(json.dumps({'rule':'Four endpoint ULP steps; no target-scaled tolerance.',
        'changes':changes,'new_mc_datasets':0,'recomputed_cases':len(rows),
        'interpretation':'All strict counts are retained. Endpoint rounding is not a coverage guarantee.'},indent=2)+'\n')
    print('Recomputed',len(rows),'saved cases; rounding differences:',changes)


if __name__=='__main__':main()
