"""Execute the locked EEG protocol and pre-outcome sampling amendment."""
import csv,json
from pathlib import Path
import numpy as np
from scipy.linalg import svd
from scipy.stats import norm,t as student_t
from threadpoolctl import threadpool_limits
from methods import empirical_bernstein,corrected_projection_interval,product_project
ROOT=Path(__file__).resolve().parents[1]

def main():
    d=np.load(ROOT/'real_data/subject_tensors.npz'); W=d['tensors']; ids=d['subjects']; channels=d['channels'].tolist()
    groups=np.array([s[3] for s in ids]); weights={g:float(np.mean(groups==g)) for g in ['a','c']}
    rng=np.random.default_rng(20260914); splits={}; pilot=[]
    for g in ['a','c']:
        ix=rng.permutation(np.flatnonzero(groups==g));n=len(ix);npilot=n//4; remain=ix[npilot:];nbias=len(remain)//2
        splits[g]={'pilot':ix[:npilot].tolist(),'calibration':remain[:nbias].tolist(),'validation':remain[nbias:].tolist()};pilot.extend(ix[:npilot])
    L=np.zeros(W.shape[2:]);ch=[channels.index('CZ'),channels.index('PZ')]
    for k in ch:
        L[2,k,4:8]=1/8;L[1,k,4:8]=-1/8
    # Each scalar averages 2 channels x 4 bins (64 samples) per condition.
    out={'seed':20260914,'alpha':.05,'group_weights':weights,'loading_nonzeros':int(np.count_nonzero(L)),
         'sampling_assumption':'independent subjects, iid within each recorded group; fixed archive group mixture, not population prevalence',
         'splits':{g:{k:[str(ids[i]) for i in ix] for k,ix in v.items()} for g,v in splits.items()},'analyses':[]}
    records=[]
    for j,clip in enumerate(d['clips']):
        X=W[:,j];F=np.einsum('nijk,ijk->n',X,L);bound=2*float(clip);R=2*bound;alpha=.05
        pooled=empirical_bernstein(F,-bound,bound,alpha)
        se=float(np.std(F,ddof=1)/np.sqrt(len(F)));qt=float(student_t.isf(alpha/2,len(F)-1))
        strata={}; rad=0.;mean=0.;hoeff=0.;vapprox=0.;vdf=0.
        for g in ['a','c']:
            ix=np.flatnonzero(groups==g);a=empirical_bernstein(F[ix],-bound,bound,alpha/2);strata[g]=a
            rad+=weights[g]*a['radius'];mean+=weights[g]*a['mean'];hoeff+=weights[g]*R*np.sqrt(np.log(4/alpha)/(2*len(ix)))
            vi=weights[g]**2*np.var(F[ix],ddof=1)/len(ix);vapprox+=vi;vdf+=vi**2/(len(ix)-1)
        df=vapprox*vapprox/vdf;approx_radius=float(student_t.isf(alpha/2,df)*np.sqrt(vapprox))
        primary={'mean':mean,'lo':max(-bound,mean-rad),'hi':min(bound,mean+rad),'radius':rad,'n':len(F),'strata':strata}
        pilotmean=np.mean(X[pilot],axis=0); candidate=[]
        for caps in [(1,2,2),(2,4,4),(3,8,8)]:
            bases=[]
            for k,r in enumerate(caps):
                u,ss,v=svd(np.moveaxis(pilotmean,k,0).reshape(X.shape[k+1],-1),full_matrices=False)
                bases.append(u[:,:r])
            projected=product_project(L,bases);res=float(np.linalg.norm(L-projected))
            candidate.append({'caps':list(caps),'loading_residual_norm':res,'projected':projected,
                              'pilot_reconstruction_relative_error':float(np.linalg.norm(pilotmean-product_project(pilotmean,bases))/np.linalg.norm(pilotmean))})
        chosen=min(candidate,key=lambda x:(x['loading_residual_norm'],sum(x['caps'])))
        Graw=np.einsum('nijk,ijk->n',X,chosen['projected']);G=np.clip(Graw,-bound,bound)
        corrected={};cm=0.;cr=0.;naivem=0.;naiver=0.;direct_holdout={};hm=0.;hr=0.
        for g in ['a','c']:
            cal,val=splits[g]['calibration'],splits[g]['validation'];
            a=corrected_projection_interval(F[cal],G[cal],G[val],-bound,bound,alpha/2);corrected[g]=a
            cm+=weights[g]*a['mean'];cr+=weights[g]*a['radius'];naivem+=weights[g]*a['projected']['mean'];naiver+=weights[g]*a['projected']['radius']
            h=empirical_bernstein(F[cal+val],-bound,bound,alpha/2);direct_holdout[g]=h;hm+=weights[g]*h['mean'];hr+=weights[g]*h['radius']
        analysis={'clip_microvolts':float(clip),'cohort_descriptive_mean':float(F.mean()),'subject_sd':float(F.std(ddof=1)),
                  'subject_quantiles':dict(zip(['min','q25','median','q75','max'],np.quantile(F,[0,.25,.5,.75,1]).tolist())),
                  'primary_stratified_EB':primary,'stratified_Hoeffding':{'lo':max(-bound,mean-hoeff),'hi':min(bound,mean+hoeff)},
                  'approximate_stratified_t':{'mean':mean,'lo':mean-approx_radius,'hi':mean+approx_radius,'df':float(df)},
                  'pooled_iid_EB_sensitivity':pooled,
                  'projection_caps':chosen['caps'],'pilot_reconstruction_relative_error':chosen['pilot_reconstruction_relative_error'],
                  'projection_candidates':[{k:v for k,v in a.items() if k!='projected'} for a in candidate],
                  'corrected_projection':{'mean':cm,'lo':max(-bound,cm-cr),'hi':min(bound,cm+cr),'unclipped_radius':cr,'strata':corrected},
                  'uncorrected_projection_DIAGNOSTIC_ONLY':{'mean':naivem,'lo':max(-bound,naivem-naiver),'hi':min(bound,naivem+naiver)},
                  'direct_nonpilot_EB':{'mean':hm,'lo':max(-bound,hm-hr),'hi':min(bound,hm+hr),'strata':direct_holdout},
                  'projected_scalar_clip_count':int(np.count_nonzero(Graw!=G)),'n_pilot':len(pilot),
                  'n_calibration':sum(len(splits[g]['calibration']) for g in splits),'n_validation':sum(len(splits[g]['validation']) for g in splits)}
        out['analyses'].append(analysis)
        for i,s in enumerate(ids):
            records.append({'subject':str(s),'group':str(groups[i]),'clip_microvolts':float(clip),'direct_contrast':float(F[i]),'projected_contrast':float(G[i]),
                            'residual_contrast':float(F[i]-G[i]),'split':next(k for k,ix in splits[groups[i]].items() if i in ix)})
    np.save(ROOT/'real_data/primary_loading.npy',L)
    (ROOT/'real_data/analysis_results.json').write_text(json.dumps(out,indent=2)+'\n')
    with (ROOT/'real_data/subject_contrasts.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    for a in out['analyses']:
        print('clip',a['clip_microvolts'],'mean',a['cohort_descriptive_mean'],'EB',a['primary_stratified_EB']['lo'],a['primary_stratified_EB']['hi'],'approx t',a['approximate_stratified_t'],'corrected',a['corrected_projection']['lo'],a['corrected_projection']['hi'])
if __name__=='__main__':
    with threadpool_limits(limits=1):main()
