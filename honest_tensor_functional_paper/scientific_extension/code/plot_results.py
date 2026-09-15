import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'serif','font.size':9,'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8,
                     'legend.fontsize':8,'pdf.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
COL=['#0072B2','#D55E00','#009E73','#CC79A7'];MARK=['o','s','^','D'];STYLE=['-','--','-.',':']

def save(fig,name):
    fig.tight_layout(pad=.8)
    for ext in ['pdf','svg']:fig.savefig(ROOT/f'figures/{name}.{ext}',bbox_inches='tight')
    fig.savefig(ROOT/f'figures/{name}.png',dpi=150,bbox_inches='tight');plt.close(fig)

def main():
    grid=json.loads((ROOT/'results/loading_grid.json').read_text());sim=json.loads((ROOT/'results/simulation_results.json').read_text());minor=json.loads((ROOT/'results/minor_results.json').read_text())
    fig,axs=plt.subplots(1,2,figsize=(6.4,2.7))
    for j,beta in enumerate([.25,.75,1.5,2.]):
        a=[r for r in grid if r['order']==3 and r['M']==1e8 and r['profile']==f'log_{beta}'];a.sort(key=lambda r:r['p']);x=[r['p'] for r in a]
        axs[0].loglog(x,[r['lower_proxy'] for r in a],color=COL[j],marker=MARK[j],ls=STYLE[j],label=f'beta={beta}')
        axs[0].fill_between(x,[r['lower_proxy'] for r in a],[r['upper_proxy'] for r in a],color=COL[j],alpha=.12)
        a=[r for r in grid if r['order']==3 and r['p']==65536 and r['profile']==f'log_{beta}'];a.sort(key=lambda r:r['M'])
        axs[1].semilogx([r['M'] for r in a],[r['proxy_ratio'] for r in a],color=COL[j],marker=MARK[j],ls=STYLE[j])
    axs[0].set(xlabel='Number of loading terms (log)',ylabel='Rate proxy (log)',title='Cubic, M/tau = 10^8');axs[0].legend(frameon=False)
    axs[1].set(xlabel='Norm budget M/tau (log)',ylabel='Abel upper / prefix lower',title='Cubic, 65,536 terms');axs[1].set_ylim(1,5)
    save(fig,'loading_envelopes')
    fig,axs=plt.subplots(1,2,figsize=(6.4,2.7))
    for ax,geom in zip(axs,['tucker','tt']):
        for j,r in enumerate([1,2]):
            a=sorted([c for c in sim if c['family']=='tensor' and c['geometry']==geom and c['signal']=='strong' and c['rank']==r],key=lambda c:c['p'])
            x=np.array([c['p'] for c in a]);y=np.sqrt([c['methods']['safe']['mse'] for c in a]);se=np.array([c['methods']['safe']['mse_mcse'] for c in a])/(2*y)
            ax.errorbar(x,y,yerr=1.96*se,color=COL[j],marker=MARK[j],ls=STYLE[j],label=f'cap {r}: measured')
            ax.plot(x,np.sqrt(2*r/x),color=COL[j],ls=':',alpha=.65,label=f'cap {r}: sqrt(2r/p)')
        ax.set(xscale='log',yscale='log',xlabel='Mode dimension p (log)',ylabel='Root MSE / tau (log)',title=geom.upper());ax.legend(frameon=False,fontsize=7.5)
    save(fig,'pointwise_risk')
    fig,axs=plt.subplots(1,2,figsize=(6.4,2.7))
    for j,p in enumerate([256,4096,65536]):
        a=sorted([c for c in sim if c['family']=='diagonal' and c['p']==p and c['budget']==20],key=lambda c:c['rank']);x=[c['rank'] for c in a]
        axs[0].semilogx(x,[c['methods']['sparse']['mean_width']/c['rate'] for c in a],marker=MARK[j],ls=STYLE[j],color=COL[j],label=f'p={p:,}')
        yy=np.array([np.sqrt(c['methods']['sparse']['mse'])/c['rate'] for c in a]);ee=np.array([c['methods']['sparse']['mse_mcse']/(2*np.sqrt(c['methods']['sparse']['mse'])*c['rate']) if c['methods']['sparse']['mse'] else 0 for c in a])
        axs[1].errorbar(x,yy,yerr=1.96*ee,color=COL[j],marker=MARK[j],ls=STYLE[j]);axs[1].set_xscale('log')
    axs[0].set(xlabel='Sparsity cap r (log)',ylabel='Mean width / rate proxy');axs[0].legend(frameon=False)
    axs[1].set(xlabel='Sparsity cap r (log)',ylabel='Root MSE / rate proxy');save(fig,'diagonal_caps')
    fig,axs=plt.subplots(1,2,figsize=(6.4,2.7));a=[r for r in minor if r['a']>=10];x=np.array([r['a'] for r in a]);y=np.array([r['mean_width'] for r in a]);se=np.array([r['width_mcse'] for r in a])
    axs[0].errorbar(x,y,yerr=1.96*se,color=COL[0],marker='o',label='Measured width');axs[0].plot(x,y[0]*x[0]/x,color='0.4',ls='--',label='Slope -1 reference');axs[0].set(xscale='log',yscale='log',xlabel='Anchor a/tau (log)',ylabel='Mean width / tau (log)');axs[0].legend(frameon=False)
    axs[1].errorbar(x,y*x,yerr=1.96*se*x,color=COL[0],marker='o');axs[1].set(xscale='log',xlabel='Anchor a/tau (log)',ylabel='Mean width x a / tau^2');save(fig,'minor_pointwise')
    import csv
    data=list(csv.DictReader((ROOT/'real_data/subject_contrasts.csv').open()));primary=[d for d in data if float(d['clip_microvolts'])==100]
    analysis=json.loads((ROOT/'real_data/analysis_results.json').read_text())['analyses'][1]
    fig,axs=plt.subplots(1,2,figsize=(6.4,2.7));rng=np.random.default_rng(1)
    for j,g in enumerate(['a','c']):
        vals=[float(d['direct_contrast']) for d in primary if d['group']==g]
        axs[0].scatter(j+rng.uniform(-.12,.12,len(vals)),vals,s=9,color=COL[j],marker=MARK[j],alpha=.7)
        axs[0].plot([j-.2,j+.2],[np.mean(vals)]*2,color='black',lw=1.5)
    axs[0].axhline(0,color='.6',ls=':',lw=.8);axs[0].set(xticks=[0,1],xticklabels=['Group a (77)','Group c (45)'],ylabel='Subject contrast (microvolts)')
    rows=[('Direct EB',analysis['primary_stratified_EB']),('Approximate t',analysis['approximate_stratified_t']),('Bias calibrated',analysis['corrected_projection'])]
    for j,(name,r) in enumerate(rows):
        axs[1].plot([r['lo'],r['hi']],[j,j],color=COL[j],lw=2);axs[1].plot(r['mean'],j,color=COL[j],marker=MARK[j],ms=4)
    axs[1].axvline(0,color='.6',ls=':',lw=.8);axs[1].set(yticks=range(3),yticklabels=[a[0] for a in rows],xlabel='Population contrast (microvolts)',xlim=(-210,210));axs[1].invert_yaxis();save(fig,'eeg_intervals')
    print('Generated five vector figures and previews.')
if __name__=='__main__':main()
