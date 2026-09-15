"""Publication figures from checked summaries; formulas explicitly analytic."""
import json,os
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/tensor_revision_mpl')
os.environ.setdefault('XDG_CACHE_HOME','/private/tmp/tensor_revision_cache')
os.makedirs(os.environ['XDG_CACHE_HOME'],exist_ok=True)
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'serif','font.size':9.5,'axes.labelsize':9.5,'legend.fontsize':8,'axes.spines.top':False,'axes.spines.right':False,'savefig.bbox':'tight','pdf.fonttype':42,'svg.fonttype':'none'})
COLORS=['#0072B2','#D55E00','#009E73','#CC79A7','#333333','#E69F00'];MARKERS=['o','s','^','D','v','x'];STYLES=['-','--','-.',':','--','-.']
rows=json.loads((ROOT/'tables/revision_summary.json').read_text());captions={}
def select(**kw):return [r for r in rows if r['alpha']==.05 and all(r.get(k)==v for k,v in kw.items())]
def pair():return plt.subplots(1,2,figsize=(6.4,2.55),layout='constrained')
def save(fig,name,caption):
    if name in ['02_fixed_budget','03_controlled_ablations']:
        handles,labels=fig.axes[0].get_legend_handles_labels()
        for ax in fig.axes:
            if ax.get_legend() is not None:ax.get_legend().remove()
        fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,-.01),ncol=2 if name=='02_fixed_budget' else 3,frameon=False,fontsize=8)
    else:
        for ax in fig.axes:
            legend=ax.get_legend()
            if legend is not None:
                handles,labels=ax.get_legend_handles_labels();legend.remove()
                ax.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,-.27),ncol=1 if name=='05_calibration' else 2,frameon=False,fontsize=8)
    for ext in ['pdf','svg','png']:fig.savefig(ROOT/'figures'/f'{name}.{ext}',dpi=160)
    plt.close(fig);captions[name]=caption
def curve(ax,v,x,y,i,label):
    v=sorted(v,key=lambda r:r[x]);xs=np.array([r[x] for r in v]);ys=np.array([r[y] for r in v]);err=None
    if y=='coverage':
        ci=np.array([r['coverage_wilson_95'] for r in v]).T;err=np.maximum(0,np.array([ys-ci[0],ci[1]-ys]))
    elif y+'_se' in v[0]:err=1.96*np.array([r[y+'_se'] for r in v])
    ax.errorbar(xs,ys,yerr=err,capsize=2,color=COLORS[i],marker=MARKERS[i],ls=STYLES[i],ms=3.5,lw=1.1,label=label)

def main():
    fig,ax=pair();p=4096;ell=np.log(np.e*p);x=np.geomspace(.01,1e4,300)
    for i,K in enumerate([3,4]):
        rate=np.sqrt(ell/p)*(np.minimum.reduce([x,1+np.maximum(0,np.log(x)),np.full_like(x,ell)]) if K==3 else np.minimum(x,1))
        ax[0].plot(x,rate,color=COLORS[i],ls=STYLES[i],label=f'Order {K}'+(' and above' if K==4 else ''))
    ax[0].set(xscale='log',yscale='log',xlabel=r'$M/(\tau\sqrt{\log(ep)})$',ylabel=r'Rate scale / $\tau$',title=r'All budgets, fixed $p=4096$');ax[0].legend()
    p=np.geomspace(16,1e6,300);ell=np.log(np.e*p)
    for i,(label,y) in enumerate([('Full, order 3',ell**1.5/np.sqrt(p)),('Full, order 4',np.sqrt(ell/p)),('Diagonal, order 3',(ell/p)**(1/6)),('Direct',np.ones_like(p))]):
        ax[1].plot(p,y,color=COLORS[i],ls=STYLES[i],label=label)
    ax[1].set(xscale='log',yscale='log',xlabel='Mode size p',ylabel=r'Rate scale / $\tau$',title=r'$M=\tau\sqrt{p}$, fixed caps');ax[1].legend()
    save(fig,'01_final_rates','Analytic minimax rate scales for the normalized flat loading, with unspecified multiplicative constants set to one. Left: all-budget dependence at p=4096. Right: full-data and diagonal-information scales at M=tau sqrt(p); the direct line is a noise-scale benchmark. These curves show theorem orders, not attained experimental performance or leading-constant comparisons.')
    fig,ax=pair()
    for i,(m,label) in enumerate([('cap_fixed','Cap, fixed M'),('cap_matched','Cap, norm-comparable M'),('direct','Direct'),('xch_known','XCH, known noise')]):
        for j,y in enumerate(['coverage','length']):curve(ax[j],select(suite='V01',method=m),'amplitude',y,i,label)
    for a in ax:a.set_xscale('symlog',linthresh=2);a.set_xlabel('Signal amplitude (symlog)');a.legend()
    ax[0].axhline(.95,color='black',ls=':',lw=.8);ax[0].set(ylim=(-.03,1.04),ylabel='Coverage (Wilson 95% bars)')
    ax[1].set(ylabel='Mean length',ylim=(0,4.8))
    save(fig,'02_fixed_budget','Paired signal sweep at p=16, rank cap one and tau=1, with 1,000 new datasets per amplitude. Fixed-M inference uses the same M=342023.69 throughout; the norm-comparable branch changes M while retaining the same observations and pilot. Bars show Wilson 95% coverage intervals or 1.96 standard errors for mean length. XCH is a regular-stratum comparator whose weak-signal conditions are not certified; it is not cap-uniform.')
    fig,ax=pair()
    for i,(m,label) in enumerate([('cap_fixed','Full'),('no_bias_fixed_choice','Remove bias only'),('no_fallback_only','Remove fallback only'),('quantile_only','Change quantile only'),('split_unprotected','Combined diagnostic')]):
        for j,y in enumerate(['coverage','length']):curve(ax[j],select(suite='V01',method=m),'amplitude',y,i,label)
    for a in ax:a.set_xscale('symlog',linthresh=2);a.set_xlabel('Signal amplitude (symlog)')
    ax[0].axhline(.95,color='black',ls=':',lw=.8);ax[0].set(ylim=(-.03,1.04),ylabel='Coverage');ax[0].legend(fontsize=8)
    ax[1].set(ylabel='Mean length',ylim=(0,4.8));ax[1].legend(fontsize=8)
    save(fig,'03_controlled_ablations','Isolated ablations use the same data, pilot projectors, supplied M and other calibration as the full procedure (1,000 datasets per amplitude). Removing bias freezes the original candidate choice; removing fallback forces the tangent candidate but preserves both intersections. Changing the validation quantile preserves the candidate choice, bias and intersections. The historical combined diagnostic removes multiple protections, so its weak-signal failure cannot identify the effect of bias alone; all paired differences and uncertainties are retained in the tables.')
    fig,ax=pair();rs=json.loads((ROOT/'tables/scalar_risk_new.json').read_text());v=[r for r in rs if r['suite']=='V05' and r['method']=='cap_fixed'];labels=[f"{r['p']}/{r['rank']}" for r in v];xx=np.arange(len(v))
    for i,(key,label) in enumerate([('midpoint_mse','Original midpoint'),('companion_mse','R1 companion')]):
        ax[0].plot(xx,[r[key] for r in v],color=COLORS[i],marker=MARKERS[i],ls=STYLES[i],label=label)
    ax[0].set(yscale='log',xticks=xx,xticklabels=labels,xlabel='Mode size / supplied cap',ylabel='Unconditional empirical MSE');ax[0].legend()
    for i,(m,label) in enumerate([('cap_fixed','Cap-valid'),('xch_known','XCH'),('oracle','Support oracle')]):
        data=select(suite='V05',method=m)
        data=sorted(data,key=lambda r:(r['p'],r['rank']));y=np.array([r['length_over_pointwise_rate'] for r in data]);se=np.array([r['length_se']/np.sqrt(r['rank']/r['p']) for r in data])
        ax[1].errorbar(xx,y,yerr=1.96*se,color=COLORS[i],marker=MARKERS[i],ls=STYLES[i],capsize=2,label=label)
    ax[1].set(xticks=xx,xticklabels=labels,xlabel='Mode size / supplied cap',ylabel=r'Mean length / $\{\tau\sqrt{r/p}\}$');ax[1].legend()
    save(fig,'04_scalar_and_pointwise','Four new strong saturated cases use 1,000 datasets each, increasing precision at p=32 and p=64. Left: raw, unconditional losses retain all empty-intersection events; the R1 companion changes only the scalar estimate. Full MSE standard errors, sentinel counts and paired losses are in the table; a logarithmic axis displays their extreme scale difference without treating the rare-loss mean as precisely estimated. Right: finite-grid lengths normalized by the P1 rate, with 1.96 standard errors; constants and rounded growing caps preclude reading this as an exact slope claim.')
    fig,ax=pair()
    for i,(m,label) in enumerate([('known_sigma','Known noise'),('independent_upper_sigma','Independent upper bound'),('naive_plugin_sigma','Naive plug-in')]):curve(ax[0],select(suite='V04',method=m,m=1,sigma=1.),'n','coverage',i,label)
    ax[0].set(xlabel='Independent replicates n',ylabel='Coverage',ylim=(.6,1.025));ax[0].legend()
    for i,(m,law,label) in enumerate([('bounded_row_median','gaussian','Median, Gaussian'),('bounded_row_median','t3','Median, t3'),('naive_gaussian','gaussian','Mean, Gaussian'),('naive_gaussian','correlated','Mean, correlated')]):
        v=[r for r in select(suite='V03',method=m,law=law,n=512) if r['actual_c']<=20];curve(ax[1],v,'actual_c','coverage',i,label)
    ax[1].plot([120],[0],marker='x',ms=7,color='black',ls='none',label='Median, cap violation');ax[1].set(xlabel='Corrupted whole replicates',ylabel='Coverage',ylim=(-.04,1.04));ax[1].legend(fontsize=8)
    for a in ax:a.axhline(.95,color='black',ls=':',lw=.8)
    save(fig,'05_calibration','Independent variance calibration uses Gaussian replicate residuals, chi-square error delta=.01 and inference error alpha0=.04; the displayed m=1, sigma=1 cases have 3,000 datasets each. Whole-replicate corruption uses the finite-variance median envelope with 1,000 datasets per case, m=16 and n=512. The separately marked 120-row case supplies a zero corruption cap and deliberately violates the theorem. All coverage bars are Wilson 95% intervals; the full m/n/noise grids and conservative lengths appear in the accompanying tables.')
    fig,ax=pair();solver=json.loads((ROOT/'tables/solver_summary.json').read_text())
    for i,a in enumerate([0.,.2,1.,2.5]):
        v=[r for r in solver if r['amplitude']==a];x=[r['budget'] for r in v]
        ax[0].errorbar(x,[r['mean_gap'] for r in v],yerr=[1.96*r['gap_se'] for r in v],color=COLORS[i],marker=MARKERS[i],ls=STYLES[i],capsize=2,label=f'Amplitude {a:g}')
        ax[1].plot(x,[r['mean_seconds'] for r in v],color=COLORS[i],marker=MARKERS[i],ls=STYLES[i],label=f'Amplitude {a:g}')
    for a in ax:a.set_xscale('log');a.set_xlabel('Search node budget');a.legend()
    ax[0].axhline(.05,color='black',ls=':',lw=.8);ax[0].set(ylabel='Mean endpoint gap',yscale='log')
    ax[1].set(ylabel='Mean solve time (seconds)',yscale='log')
    save(fig,'06_fixed_solver','All budgets use the same normalized arbitrary loading, signal direction, M=3, tau=.5 and endpoint tolerance .05 in a 2 by 2 by 2 rank-one model. Each amplitude uses 50 new observations shared across the three budgets, giving 600 solves. Every unresolved global gap is retained; mean-gap bars are 1.96 standard errors, while timing is descriptive. Seven of 600 solves meet the requested tolerance, all at the strongest signal and largest budget; guarded float64 outer bounds are not formal interval arithmetic or a general high-dimensional minimax implementation.')
    (ROOT/'figures/captions.json').write_text(json.dumps(captions,indent=2)+'\n')
    (ROOT/'figures/captions.md').write_text('# Revised figure captions\n\n'+'\n\n'.join(f'**{k}.** {v}' for k,v in captions.items())+'\n')
    print('Generated',len(captions),'PDF/SVG/PNG figures.')

if __name__=='__main__':main()
