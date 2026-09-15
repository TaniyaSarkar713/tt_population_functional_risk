"""Lock configurations before drawing MC data; retain per-replicate outcomes."""
import csv,hashlib,json,time
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.linalg import svd
from scipy.stats import norm
from threadpoolctl import threadpool_limits
from methods import *
ROOT=Path(__file__).resolve().parents[1]

def summarize(errors,widths,covered):
    errors=np.asarray(errors); widths=np.asarray(widths);covered=np.asarray(covered);B=len(errors);ph=float(covered.mean())
    z=norm.isf(.025);den=1+z*z/B;mid=(ph+z*z/(2*B))/den
    half=z*np.sqrt(ph*(1-ph)/B+z*z/(4*B*B))/den
    losses=errors**2
    return dict(replications=B,coverage=ph,coverage_lo=mid-half,coverage_hi=mid+half,
                mean_width=float(widths.mean()),width_mcse=float(widths.std(ddof=1)/np.sqrt(B)),
                mse=float(losses.mean()),mse_mcse=float(losses.std(ddof=1)/np.sqrt(B)),
                error_mean=float(errors.mean()),max_squared_error=float(losses.max()))

def config_list():
    cs=[]
    for geometry,order,ps in [('tucker',3,[8,16,32]),('tt',4,[4,8,12])]:
        for p in ps:
            for r in [1,2]:
                for signal in ['zero','weak','strong']:
                    cs.append(dict(family='tensor',geometry=geometry,order=order,p=p,rank=r,signal=signal,
                                   B=500 if p>=12 else 1000))
    # A strong undersaturated mean: cap-valid construction must retain cap.
    for geom,K,p in [('tucker',3,16),('tt',4,8)]:
        cs.append(dict(family='tensor',geometry=geom,order=K,p=p,rank=2,signal='undersaturated',B=1000))
    for p in [256,4096,65536]:
        for r in sorted(set([1,4,int(p**.25),int(np.sqrt(p)),min(p,4*int(np.sqrt(p)))])):
            for budget in [.2,2.,20.]:
                cs.append(dict(family='diagonal',p=p,rank=r,budget=budget,B=1000))
    return cs

def tensor_case(c,idx):
    p,K,r=c['p'],c['order'],c['rank'];geom=c['geometry'];B=c['B'];rng=np.random.default_rng(202609140000+idx)
    gamma=np.sqrt(r/p);kappa=gamma;d=np.sqrt(8*np.log(2/kappa));delta=.05*kappa**4/(64*(1+d)**4)
    shapes=[(p,p**(K-1))]*K if geom=='tucker' else [(p**j,p**(K-j)) for j in range(1,K)]
    eta=max(2*np.sqrt(2)*np.sqrt(2*((a+b)*np.log(9)+np.log(2*len(shapes)/delta))) for a,b in shapes)
    a=8*eta**2*np.sqrt(p)
    # Dense Tucker core, rotated together with a prescribed orthogonal loading.
    # TT examples use a rotated diagonal core and can be bounded at every cut.
    C=np.zeros((r,)*K);C[(np.arange(r),)*K]=1
    if geom=='tucker' and r>1:C+=.15*rng.normal(size=C.shape)
    base=np.zeros((p,)*K);base[tuple(slice(r) for _ in range(K))]=C
    L=np.zeros_like(base);L[(np.arange(p),)*K]=1/np.sqrt(p)
    rotations=[np.linalg.qr(rng.normal(size=(p,p)))[0] for _ in range(K)]
    for j,Q in enumerate(rotations):
        base=np.moveaxis(np.tensordot(Q,np.moveaxis(base,j,0),axes=(1,0)),0,j)
        L=np.moveaxis(np.tensordot(Q,np.moveaxis(L,j,0),axes=(1,0)),0,j)
    singular=[]
    for j in range(len(shapes)):
        mat=np.moveaxis(base,j,0).reshape(p,-1) if geom=='tucker' else base.reshape(shapes[j])
        singular.append(svd(mat,compute_uv=False)[r-1])
    base=base/min(singular)
    if c['signal']=='strong':A=a*base;M=2*np.linalg.norm(A)
    elif c['signal']=='weak':A=base*(np.sqrt(p)/np.linalg.norm(base));M=2*np.sqrt(p)
    elif c['signal']=='zero':A=np.zeros_like(base);M=np.sqrt(p)
    else:
        A=rotations[0][:,0]
        for j in range(1,K):A=np.multiply.outer(A,rotations[j][:,0])
        A=a*A;M=2*np.linalg.norm(A)
    target=float(np.sum(L*A)); rec={n:[] for n in ['safe','direct','same_interval_midpoint','legacy_direct_fallback']}; widths=[];covers=[];selected=Counter();empty=0;details=None;start=time.perf_counter()
    for b in range(B):
        z=A+rng.normal(size=A.shape)
        ans=cap_interval(z,L,M,[r]*len(shapes),rng,geometry=geom,kappa=kappa,return_details=b==0)
        if b==0:details=ans
        mid=.5*(ans['lo']+ans['hi']);legacy=np.clip(ans['direct'],-ans['structural'],ans['structural']) if ans['empty'] or (ans['lo']==ans['hi']==0) else mid
        for n,val in [('safe',ans['estimate']),('direct',ans['direct']),('same_interval_midpoint',mid),('legacy_direct_fallback',legacy)]:rec[n].append(val-target)
        widths.append(ans['width']);covers.append(ans['lo']<=target<=ans['hi']);selected[ans['candidate']]+=1;empty+=ans['empty']
    out={**c,'id':f'E{idx:03d}','M':float(M),'target':target,'gamma':gamma,'eta':eta,'a_design':a,'selected':dict(selected),'empty_count':empty,'seconds':time.perf_counter()-start,
         'methods':{n:summarize(x,[2*norm.isf(.025)]*B,[abs(v)<=norm.isf(.025) for v in x]) if n=='direct' else summarize(x,widths,covers) for n,x in rec.items()},'pointwise_risk_proxy':r/p,
         'strong_conditions':dict(a_over_eta=a/eta,bias_condition_ratio=(M*(eta/a)**2/gamma)) if c['signal']=='strong' else None,
         'first_call_details':details}
    np.savez_compressed(ROOT/f'results/E{idx:03d}_replicates.npz',**{f'error_{n}':v for n,v in rec.items()},width=widths,covered=covers)
    return out

def diagonal_case(c,idx):
    p,r,B=c['p'],c['rank'],c['B'];rng=np.random.default_rng(202609140000+idx)
    stochastic=r/np.sqrt(p)*np.sqrt(np.log1p(p/r**2));M=c['budget']*stochastic*np.sqrt(p/r)
    # Equal positive entries at min(norm limit, threshold) stress truncation bias.
    template=diagonal_sparse(np.zeros(p),M,r);amp=min(M/np.sqrt(r),template['threshold'])
    mu=np.zeros(p);mu[:r]=amp;target=r*amp/np.sqrt(p); errors=[];widths=[];covers=[];direct_errors=[];sels=Counter();start=time.perf_counter()
    for b in range(B):
        z=mu+rng.normal(size=p);d=diagonal_sparse(z,M,r);errors.append(d['estimate']-target);widths.append(d['width']);covers.append(d['lo']<=target<=d['hi']);direct_errors.append(z.sum()/np.sqrt(p)-target);sels[d['selected']]+=1
    out={**c,'id':f'E{idx:03d}','M':float(M),'target':target,'seconds':time.perf_counter()-start,'selected':dict(sels),'rate':template['rate'],
         'methods':{'sparse':summarize(errors,widths,covers),'direct':summarize(direct_errors,[2*norm.isf(.025)]*B,[abs(x)<=norm.isf(.025) for x in direct_errors])}}
    np.savez_compressed(ROOT/f'results/E{idx:03d}_replicates.npz',error_sparse=errors,error_direct=direct_errors,width=widths,covered=covers)
    return out

def loading_grid():
    rng=np.random.default_rng(2026091499);rows=[]
    for K in [3,4]:
        for p in [16,256,4096,65536]:
            for M in [.1,1.,3.,10.,100.,1e4,1e8]:
                t=1+np.log(np.arange(1,p+1))
                profiles={'flat':np.ones(p),'random':rng.lognormal(0,2,p),'step':np.r_[np.ones(max(1,p//10)),np.full(p-max(1,p//10),.05)]}
                for beta in [.25,.5,.75,1.25,1.5,2.]:profiles['log_'+str(beta)]=t**(-beta)
                for name,w in profiles.items():
                    w=w/np.linalg.norm(w);d=loading_envelope(w,M,order=K);d.update(order=K,p=p,M=M,profile=name)
                    if name.startswith('log_') and float(name[4:]) not in ([.5,1.5] if K==3 else [.5]):
                        d['sharp_proxy']=log_profile_rate(p,M,float(name[4:]),order=K,scale=1/np.linalg.norm(t**(-float(name[4:]))))
                    rows.append(d)
    (ROOT/'results/loading_grid.json').write_text(json.dumps(rows,indent=2)+'\n')

if __name__=='__main__':
    cs=config_list();payload=json.dumps(cs,indent=2)+'\n';(ROOT/'results/configurations.json').write_text(payload)
    (ROOT/'results/configuration_lock.json').write_text(json.dumps({'sha256':hashlib.sha256(payload.encode()).hexdigest(),'seed_rule':'202609140000 + configuration index; loading grid seed 2026091499','registered_before_MC':True},indent=2)+'\n')
    rows=[]
    with threadpool_limits(limits=1):
        loading_grid()
        for idx,c in enumerate(cs):
            out=tensor_case(c,idx) if c['family']=='tensor' else diagonal_case(c,idx);rows.append(out)
            (ROOT/'results/simulation_results.json').write_text(json.dumps(rows,indent=2)+'\n')
            print(out['id'],c['family'],c['p'],c.get('signal',c.get('budget')),round(out['seconds'],2),flush=True)
    print('Complete:',len(rows),'configurations',sum(r['B'] for r in rows),'independent MC datasets',flush=True)
