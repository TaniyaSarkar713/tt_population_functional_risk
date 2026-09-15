"""Every plotted value comes from checked trial summaries or labeled bounds."""
import json
import numpy as np
from scipy.stats import norm
from matplotlib.ticker import NullFormatter
from common import ROOT,write_json,wilson
from plot_utils import plt,style,pair,save


def main():
    rows=json.loads((ROOT/'tables/summary.json').read_text())
    records=[r for r in rows if r['alpha']==.05]
    captions={};root=ROOT/'figures'
    def select(**kw):return [r for r in records if all(r.get(k)==v for k,v in kw.items())]
    def curve(ax,data,x,y,index,label,uncertainty=True,connect=True):
        data=sorted(data,key=lambda r:r[x]);xs=[r[x] for r in data];ys=[r[y] for r in data]
        appearance=style(index)
        if not connect:appearance['linestyle']='none'
        if y=='coverage':
            ci=np.array([r['coverage_wilson_95'] for r in data]).T
            ax.errorbar(xs,ys,yerr=np.maximum(0,np.stack((np.array(ys)-ci[0],ci[1]-np.array(ys)))),capsize=2,label=label,**appearance)
        elif uncertainty and y+'_se' in data[0]:
            ax.errorbar(xs,ys,yerr=[1.96*r[y+'_se'] for r in data],capsize=2,label=label,**appearance)
        else:ax.plot(xs,ys,label=label,**appearance)
    fig,ax=pair()
    for i,m in enumerate(['direct','growing']):
        curve(ax[0],select(suite='S01',axis='structural_p',method=m),'p','length',i,m)
        curve(ax[1],[r for r in select(suite='S01',axis='n',signal='boundary',method=m) if r['n']>=4],'n','length',i,m)
    for a,label in zip(ax,['Mode size p (log scale)','Replicates n (log scale)']):
        a.set(xscale='log',yscale='log',xlabel=label,ylabel='Mean interval length (log scale)');a.legend()
        a.set_yticks([.125,.25,.5,1,2,4],labels=['0.125','0.25','0.5','1','2','4'])
        a.set_ylim(.105,4.6);a.yaxis.set_minor_formatter(NullFormatter())
    save(fig,root,'01_growing_rates')
    captions['01_growing_rates']='The executable large-cap interval follows its structural and noise branches. Left: M=1, tau=1, r=sqrt(p), boundary diagonal signals. Right: p=1024, r=32, M=8, tau=n^(-1/2), n>=4. Each point uses 5,000 data sets; interval lengths are deterministic, so mean-length error bars vanish. The tested exponents are -1/4 in p and -1/2 in n.'
    fig,ax=pair()
    for k,a in zip([3,4],ax):
        for i,m in enumerate(['direct','threshold_selected','threshold_raw']):
            curve(a,select(suite='S02',axis='p',support='threshold',K=k,method=m),'p','length',i,m.replace('_',' '))
        a.set(xscale='log',yscale='log',xlabel='Mode size p (log scale)',ylabel=f'Length, order K={k} (log scale)');a.legend()
    save(fig,root,'02_weak_threshold')
    captions['02_weak_threshold']='The fast diagonal interval becomes shorter as dimension grows, with conservative coverage in the tested signals. M=sqrt(p), tau=1, rank-one support near the threshold boundary; 1,000 data sets per configuration. The raw threshold curve differs from deterministic selection when structural or direct intervals are shorter. This evaluates the diagonal procedure, not attainment of the sharper full-data ideal rate.'
    fig,ax=pair()
    for fixed,a in zip([True,False],ax):
        for i,m in enumerate(['direct','pointwise','xch_known','oracle']):
            data=[r for r in select(suite='S03',method=m) if (r['rank']==1)==fixed]
            curve(a,data,'p','length',i,m.replace('_',' '))
        a.set(xscale='log',yscale='log',xlabel='Mode size p (log scale)',ylabel='Mean length (log scale)',title='Cap 1' if fixed else r'Cap $\lceil\sqrt{p}\rceil$');a.legend()
    save(fig,root,'03_pointwise_rates')
    captions['03_pointwise_rates']='Strong saturated signals allow substantial shortening, while the regular-signal comparator and support oracle can be shorter than the finite-sample certificate; their curves nearly coincide here. Signal amplitudes equal eight times the P1 sufficient bound. Replications are 500 at p=8/16, 300 at p=32, and 150 at p=64; bars are 1.96 mean-length standard errors. XCH denotes the locally reimplemented Xu–Chen–Han PCA procedure with known noise. Pointwise optimality is a rate claim, not leading-constant dominance.'
    fig,ax=pair()
    for i,m in enumerate(['direct','pointwise','xch_known','separated_selector']):
        data=select(suite='S04',regime='signal_sweep',method=m)
        curve(ax[0],data,'amplitude','coverage',i,m.replace('_',' '))
        curve(ax[1],data,'amplitude','length',i,m.replace('_',' '))
    ax[0].axhline(.95,color='black',lw=.8,ls=':');ax[0].set(ylim=(-.03,1.04),ylabel='Coverage (Wilson 95% bars)')
    ax[1].set_yscale('symlog',linthresh=.1);ax[1].set_ylabel('Mean length (symlog scale)')
    for a in ax:
        a.set_xscale('symlog',linthresh=.5)
        a.set_xlim(-.1,max(r['amplitude'] for r in data)*1.2)
        a.set_xticks([0,1,100,1e4,3e5],labels=['0','1','100',r'$10^4$',r'$3\times10^5$'])
        a.set_xlabel('Signal amplitude (symlog scale)');a.legend(fontsize=8)
    save(fig,root,'04_signal_sweep')
    captions['04_signal_sweep']='The separated rank selector fails for weak nonzero components, and the cap-valid correction can remain wider than direct inference well into the signal sweep. p=16, supplied cap one, supplied M changes with the signal norm, 500 paired data sets per amplitude; confidence level 95%. Coverage bars are Wilson intervals and length bars are 1.96 mean standard errors. Weak-signal results are outside the regular/separated comparators\' guarantees. Symlog axes retain zero amplitudes and zero reported widths.'
    fig,ax=pair()
    for i,m in enumerate(['iid_gaussian','calibrated']):
        data=select(suite='S05',law='gaussian',method=m)
        curve(ax[0],data,'rho','coverage',i,m.replace('_',' '))
        subset=[r for r in select(suite='S05',method=m) if r['law']!='gaussian']
        order=['rademacher','t5','t3','variance_01','variance_05','mean_shift']
        subset=sorted(subset,key=lambda r:order.index(r['law']))
        temp=[dict(r,position=j+(i-.5)*.12) for j,r in enumerate(subset)]
        curve(ax[1],temp,'position','coverage',i,m.replace('_',' '),connect=False)
    ax[0].set(xlabel='Coordinate correlation',ylabel='Coverage (Wilson 95% bars)')
    ax[1].set(xticks=range(6),xticklabels=['sign','t5','t3','mix1%','mix5%','shift'],xlabel='Noise law',ylabel='Coverage (Wilson 95% bars)')
    for a in ax:a.axhline(.95,color='black',lw=.8,ls=':');a.set_ylim(-.03,1.04);a.legend()
    save(fig,root,'05_noise')
    captions['05_noise']='Correct covariance calibration restores coverage under correlated Gaussian coordinates; a mean shift is not repaired by variance correction. p=256 and 5,000 data sets per noise law. The calibrated method uses exact Gaussian covariance, a known sub-Gaussian proxy for bounded/mixture laws, or a Chebyshev variance bound for t3/t5. Both mean-shift curves deliberately ignore the nonzero noise mean and have no centered-noise guarantee. Mixtures are variance-standardized.'
    fig,ax=pair()
    solver=json.loads((ROOT/'tables/solver.json').read_text())
    for i,signal in enumerate(['zero','weak','boundary','strong']):
        values=[r for r in solver if r['signal']==signal and r['loading']=='arbitrary' and r['alpha']==.05]
        points=[];bootstrap=np.random.default_rng(20260913+i)
        for budget in sorted({r['budget'] for r in values}):
            v=[r for r in values if r['budget']==budget];g=[r['endpoint_gap'] for r in v if r['endpoint_gap'] is not None]
            k=sum(r['certified_to_tolerance'] for r in v)
            gap_ci=np.quantile(bootstrap.choice(g,size=(2000,len(g))).mean(axis=1),[.025,.975]).tolist() if g else [np.nan,np.nan]
            points.append(dict(budget=budget,gap=float(np.mean(g)) if g else np.nan,gap_ci=gap_ci,
                               certificate=k/len(v),certificate_ci=wilson(k,len(v))))
        for a,key in zip(ax,['gap','certificate']):
            y=np.array([r[key] for r in points]);ci=np.array([r[key+'_ci'] for r in points]).T
            a.errorbar([r['budget'] for r in points],y,yerr=np.maximum(0,np.stack((y-ci[0],ci[1]-y))),capsize=2,label=signal,**style(i))
    ax[0].set(xscale='log',yscale='log',xlabel='Node budget (log scale)',ylabel='Mean endpoint gap (log scale)')
    ax[1].set(xscale='log',xlabel='Node budget (log scale)',ylabel='Fraction certified to tolerance',ylim=(-.03,1.03))
    for a in ax:a.legend()
    save(fig,root,'06_solver')
    captions['06_solver']='Finite search budgets can leave large endpoint gaps for arbitrary binary loadings. K=3, mode size two, 30 shared observations per signal/loading case; gap bars use 2,000 fixed-seed bootstrap resamples and certification bars are Wilson 95% intervals. Gap averages condition on a finite feasible-witness gap; missing-witness counts are in the table. Each signal case has its own independently fixed arbitrary loading. The budget-100 tolerance is .5 tau; budgets 600 and 3000 use .1 tau, so the first certification point uses a looser tolerance. Gaps are numerical float64 bounds with guards, not formal interval arithmetic.'
    fig,ax=pair()
    for i,m in enumerate(['direct','corrected','omitted_correction']):
        curve(ax[0],select(suite='S09',kind='loading',method=m),'epsilon','coverage',i,m.replace('_',' '))
        curve(ax[1],select(suite='S09',kind='approximation',method=m),'eta','coverage',i,m.replace('_',' '))
    ax[0].set(xlabel='Loading residual norm',ylabel='Coverage (Wilson 95% bars)')
    ax[1].set_xscale('symlog',linthresh=.01);ax[1].set(xlabel='Frobenius allowance (symlog scale)',ylabel='Coverage (Wilson 95% bars)')
    ax[1].set_xlim(-.002,4.5);ax[1].set_xticks([0,.01,.1,1,4],labels=['0','0.01','0.1','1','4'])
    for a in ax:a.axhline(.95,color='black',lw=.8,ls=':');a.set_ylim(-.03,1.04);a.legend(fontsize=8)
    save(fig,root,'07_corrections')
    captions['07_corrections']='Omitting known loading or approximation contributions can destroy coverage. p=4096, K=4, 1,000 paired data sets per point. Left: rank-one off-diagonal mean, M=64, loading a flat diagonal plus a known off-diagonal product atom. Right: a rank-one core of norm one plus eta times the unit flat loading. These are executable conservative corrections, not the unavailable sharp full-data optimizer. Bars are Wilson 95% intervals.'
    fig,ax=pair()
    for i,m in enumerate(['direct','pointwise','xch_known','oracle']):
        data=sorted(select(suite='S10',method=m),key=lambda r:r['shift'])
        y=np.array([r['rejection'] for r in data]);ci=np.array([r['rejection_wilson_95'] for r in data]).T
        ax[0].errorbar([r['shift'] for r in data],y,yerr=np.maximum(0,np.stack((y-ci[0],ci[1]-y))),capsize=2,label=m,**style(i))
    x=np.linspace(0,8,100);delta=x*np.sqrt(2/16);q=norm.isf(.025)
    ax[0].plot(x,norm.cdf(-q-delta)+norm.sf(q-delta),color='black',ls=':',label='Exact direct power')
    ax[0].set(xlabel='Target shift / (tau sqrt(r/p))',ylabel='Rejection probability',ylim=(-.03,1.03));ax[0].legend(fontsize=8)
    piv=np.load(ROOT/'results/diagnostics_S03_002.npz')['pivots']
    theoretical=norm.ppf((np.arange(len(piv))+.5)/len(piv))
    for i,j in enumerate([0,1,3]):ax[1].plot(theoretical,np.sort(piv[:,j]),label=['Direct','XCH','Oracle'][i],**{**style(i),'markersize':2,'linewidth':.8})
    ax[1].plot([-3.2,3.2],[-3.2,3.2],color='black',ls=':',lw=.8)
    ax[1].set(xlabel='Standard-normal quantile',ylabel='Observed standardized quantile');ax[1].legend()
    save(fig,root,'08_power_and_pivots')
    captions['08_power_and_pivots']='Regular-signal intervals and the support oracle can resolve smaller target shifts than the direct interval. Left: p=16, cap two, opposite large diagonal amplitudes, 1,000 draws per local alternative; bars are Wilson 95% intervals and the dotted curve is exact direct-Gaussian power. Right: the strong p=16 cap-one case, 500 draws, with exact direct/oracle pivots and the XCH regular-signal diagnostic. No normality claim is made for the cap-valid interval midpoint.'
    fig,ax=pair()
    rt=json.loads((ROOT/'results/runtime.json').read_text())['rows']
    for i,m in enumerate(['pointwise','xch']):
        data=sorted([r for r in rt if r['method']==m],key=lambda r:r['p'])
        ax[0].errorbar([r['p'] for r in data],[r['mean_seconds'] for r in data],yerr=[r['seconds_se'] for r in data],capsize=2,label=m,**style(i))
        ax[1].plot([r['p'] for r in data],[r['peak_traced_bytes']/2**20 for r in data],label=m,**style(i))
    for a in ax:a.set_xscale('log');a.set_yscale('log');a.set_xlabel('Mode size p (log scale)');a.legend()
    ax[0].set_ylabel('Seconds per call (log scale)');ax[1].set_ylabel('Peak traced MiB (log scale)')
    save(fig,root,'09_runtime')
    captions['09_runtime']='Full-tensor projection costs grow with the explicit input size. Fixed thread count, one warmup and ten measured calls per point; runtime bars are descriptive plus/minus one standard error, not 95% confidence intervals. The wider symmetric 1.96-SE interval crosses zero in one case and cannot be displayed fully on a log axis; all mean/SE values remain in the table. Memory counts traced Python/NumPy allocations during a call, excluding preallocated input and untraced native workspace; it is not total process memory. XCH and cap-valid calls both reuse factors across confidence levels. Separate tables report actual O(p) diagonal access and binary K=3/4 optimizer costs.'
    fig,ax=pair()
    for p,i in [(256,0),(4096,1),(65536,2)]:
        data=select(suite='S12',p=p,M=float(np.sqrt(p)),method='cap_upper')
        curve(ax[0],data,'rank','length',i,f'p={p}')
        lowers=[]
        for r in sorted(data,key=lambda r:r['rank']):
            meta=json.loads((ROOT/'results'/(r['case']+'.json')).read_text())
            lowers.append((r['rank'],r['length']/meta['extra']['length_lower']))
        ax[1].plot(*zip(*lowers),label=f'p={p}',**style(i))
    for a in ax:a.set(xscale='log',yscale='log',xlabel='Supplied cap (log scale)');a.legend()
    ax[0].set_ylabel('Upper interval length (log scale)');ax[1].set_ylabel('Length / analytic lower bound (log scale)')
    ax[0].set_yticks([2,3,4],labels=['2','3','4']);ax[0].yaxis.set_minor_formatter(NullFormatter())
    ax[1].set_yticks([2,10,100,500],labels=['2','10','100','500']);ax[1].yaxis.set_minor_formatter(NullFormatter())
    save(fig,root,'10_intermediate_caps')
    captions['10_intermediate_caps']='The valid cap-based upper interval leaves a substantial upper/lower gap at small and intermediate caps. This follow-up was registered separately after a requirements audit: 5,000 draws per configuration, sparse common-target diagonal means, M=sqrt(p), tau=1. The lower curve is an analytic testing bound, not an empirically attained benchmark. Matching intermediate-cap rates remain open. Interval lengths here are deterministic.'
    write_json(root/'captions.json',captions)
    (root/'captions.md').write_text('# Figure captions\n\n'+'\n\n'.join(f'**{name}.** {caption}' for name,caption in captions.items())+'\n')
    print('Generated',len(captions),'figures in PDF, SVG and inspection PNG formats.')


if __name__=='__main__':main()
