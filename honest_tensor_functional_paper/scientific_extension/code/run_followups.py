"""Additional prespecified scope/geometry checks, separate from main MC grid."""
import json,time
from pathlib import Path
import numpy as np
from scipy.linalg import svd
from scipy.stats import norm
from threadpoolctl import threadpool_limits
from methods import *
from methods import _checked_matmul as mm
from run_experiments import summarize
ROOT=Path(__file__).resolve().parents[1]

def main():
    config={'seed':2026091455,'B':2000,'families':['dense_TT_core_loading','diagonal_assumption_violation','bounded_projection_bias'],
            'TT_shape':[4,5,4,3],'TT_caps':[2,3,2],'TT_strengths':['zero','strong'],'bounded_n_each':[100,1000],
            'diagonal_violation_p':4096,'alpha':.05}
    (ROOT/'results/followup_configurations.json').write_text(json.dumps(config,indent=2)+'\n')
    rng=np.random.default_rng(config['seed']);B=config['B'];out=[]
    # General, dense TT cores with an arbitrary loading aligned to one cut.
    cores=[rng.normal(size=(1,4,2)),rng.normal(size=(2,5,3)),rng.normal(size=(3,4,2)),rng.normal(size=(2,3,1))]
    base=cores[0][0]
    for c in cores[1:]:base=np.tensordot(base,c,axes=(-1,0))
    base=base[...,0];U,ss,V=svd(base.reshape(20,12),full_matrices=False)
    H=mm(mm(U[:,:3],rng.normal(size=(3,3))),V[:3]);H/=np.linalg.norm(H)
    R=rng.normal(size=(20,12));R=R-mm(U[:,:3],mm(U[:,:3].T,R));R=R-mm(mm(R,V[:3].T),V[:3]);R/=np.linalg.norm(R)
    gamma=.2;L=(gamma*H+np.sqrt(1-gamma*gamma)*R).reshape(base.shape)
    assert np.isclose(np.linalg.norm(L),1.)
    assert np.isclose(np.linalg.norm(mm(mm(U[:,:3].T,L.reshape(20,12)),V[:3].T)),gamma)
    d=np.sqrt(8*np.log(2/gamma));delta=.05*gamma**4/(64*(1+d)**4)
    eta=2*np.sqrt(2)*np.sqrt(2*(32*np.log(9)+np.log(6/delta)))
    base/=ss[2];a=16*np.linalg.norm(base)*eta**2/gamma
    for signal in ['zero','strong']:
        A=base*a if signal=='strong' else np.zeros_like(base);M=2*np.linalg.norm(A) if signal=='strong' else 5.;target=np.sum(L*A)
        es=[];ds=[];ws=[];cov=[];selections={}
        for _ in range(B):
            z=A+rng.normal(size=A.shape);q=cap_interval(z,L,M,[2,3,2],rng,geometry='tt',kappa=gamma)
            es.append(q['estimate']-target);ds.append(q['direct']-target);ws.append(q['width']);cov.append(q['lo']<=target<=q['hi']);selections[q['candidate']]=selections.get(q['candidate'],0)+1
        out.append({'family':'dense_TT_core_loading','signal':signal,'gamma':gamma,'pointwise_risk_proxy':gamma**2,
                    'method':summarize(es,ws,cov),'direct':summarize(ds,[2*norm.isf(.025)]*B,np.abs(ds)<=norm.isf(.025)),
                    'selected':selections,'bias_condition_ratio':M*(eta/a)**2/gamma if signal=='strong' else None})
        np.savez_compressed(ROOT/f'results/followup_tt_{signal}.npz',error=es,direct_error=ds,width=ws,covered=cov)
    # The observed diagonal of a dense rank-one tensor need not be sparse.
    p=4096;t=np.sqrt(2*np.log1p(p));mu=t/2;M=mu*p**1.5;target=mu*np.sqrt(p)
    es=[];ws=[];cov=[]
    for _ in range(B):
        q=diagonal_sparse(mu+rng.normal(size=p),M,1);es.append(q['estimate']-target);ws.append(q['width']);cov.append(q['lo']<=target<=q['hi'])
    out.append({'family':'diagonal_assumption_violation','scope':'Deliberate use outside exact diagonal-mean submodel; dense rank-one full tensor has all diagonal means t/2.',
                'p':p,'M':M,'method':summarize(es,ws,cov)})
    np.savez_compressed(ROOT/'results/followup_diagonal_violation.npz',error=es,width=ws,covered=cov)
    for n in [100,1000]:
        ce=[];cw=[];cc=[];ne=[];nw=[];nc=[];truth=.4
        for _ in range(B):
            pilot=rng.binomial(1,.7,30)*2-1;shrink=float(np.clip(.3+.2*np.mean(pilot),.2,.6))
            cal=rng.binomial(1,.7,n)*2-1;val=rng.binomial(1,.7,n)*2-1
            q=corrected_projection_interval(cal,shrink*cal,shrink*val,-1,1)
            v=empirical_bernstein(shrink*val,-1,1)
            ce.append(q['mean']-truth);cw.append(q['hi']-q['lo']);cc.append(q['lo']<=truth<=q['hi'])
            ne.append(v['mean']-truth);nw.append(v['hi']-v['lo']);nc.append(v['lo']<=truth<=v['hi'])
        out.append({'family':'bounded_projection_bias','n_calibration':n,'n_validation':n,'target':truth,
                    'corrected':summarize(ce,cw,cc),'uncorrected_DIAGNOSTIC':summarize(ne,nw,nc)})
        np.savez_compressed(ROOT/f'results/followup_bounded_{n}.npz',corrected_error=ce,corrected_width=cw,corrected_covered=cc,
                            naive_error=ne,naive_width=nw,naive_covered=nc)
    (ROOT/'results/followup_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':
    with threadpool_limits(limits=1):main()
