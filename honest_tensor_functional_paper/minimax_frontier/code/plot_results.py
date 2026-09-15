"""Vector figures from saved calculations and observations; no simulated curves."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
COLORS=['#0072B2','#D55E00','#009E73','#CC79A7','#E69F00','#333333']
plt.rcParams.update({'font.size':10,'axes.labelsize':10,'axes.titlesize':11,
                     'legend.fontsize':9,'pdf.fonttype':42,'svg.fonttype':'none',
                     'axes.spines.top':False,'axes.spines.right':False})


def save(fig,name):
    for ext in ['pdf','svg','png']:fig.savefig(ROOT/'figures'/f'{name}.{ext}',bbox_inches='tight',dpi=140)
    plt.close(fig)


def main():
    sim=json.loads((ROOT/'results/simulation_results.json').read_text())
    prof=json.loads((ROOT/'results/analytic_profiles.json').read_text())
    fig,ax=plt.subplots(1,2,figsize=(6.8,3.4),layout='constrained')
    for j,beta in enumerate([0.,.25,.5,.75]):
        rows=[c for c in prof if c['M']==1000 and c['beta']==beta]
        ax[0].semilogx([c['p'] for c in rows],[c['A_over_B'] for c in rows],'-o',color=COLORS[j],label=fr'$\beta={beta}$')
        ax[0].annotate(fr'$\beta={beta}$',(rows[-1]['p'],rows[-1]['A_over_B']),xytext=(5,0),textcoords='offset points',color=COLORS[j],fontsize=9,va='center')
    ax[0].set(xlabel='Orthogonal loading terms p',ylabel='Exact rate proxy / old prefix proxy',title='A. Information across scales')
    ax[0].set_ylim(bottom=.95);ax[0].set_xlim(12,4e5)
    p=np.array([16,64,256,1024,4096,16384,65536,262144],float)
    ax[1].loglog(p,np.ones_like(p),'-o',color=COLORS[1],label='One rank cap (r = 1)')
    ax[1].loglog(p,np.sqrt((1+np.log(p))/p),'-s',color=COLORS[0],label='All caps fixed, K ≥ 4')
    ax[1].set(xlabel='Loading terms p',ylabel='Length rate / noise scale',title='B. Additional caps matter')
    ax[1].legend(frameon=False,loc='upper right',bbox_to_anchor=(1,.93))
    save(fig,'statistical_frontiers')
    fig,axes=plt.subplots(1,3,figsize=(6.8,3.1),layout='constrained',sharey=True)
    for ax,profile in zip(axes,['flat','spike_tail','log_decay']):
        for j,r in enumerate([1,4,16]):
            rows=[c for c in sim if c['family']=='spectral' and c['profile']==profile and c['rank']==r and c['signal']=='worst_bias']
            ax.errorbar([c['M'] for c in rows],[c['method']['mean_width'] for c in rows],
                        yerr=[1.96*c['method']['width_mcse'] for c in rows],fmt='o-',color=COLORS[j],label=f'r = {r}')
            ax.plot([c['M'] for c in rows],[c['direct']['mean_width'] for c in rows],'--',color=COLORS[j],alpha=.8)
        ax.set(xscale='log',yscale='log',xlabel='Supplied norm budget M',title=profile.replace('_',' '))
    axes[0].set_ylabel('Mean interval length');axes[0].legend(frameon=False)
    fig.suptitle('One-unfolding model: solid spectral; dashed direct + structural',fontsize=10)
    save(fig,'spectral_performance')
    fig,axes=plt.subplots(1,3,figsize=(6.8,3.6),layout='constrained',sharey=True)
    for ax,K in zip(axes,[3,4,5]):
        for d in range(K+1):
            rows=[c for c in sim if c['family']=='coordinate' and c['K']==K and c['distance']==d and c['signal']=='axis' and c['a']>0]
            a=np.array([c['a'] for c in rows]);y=np.array([c['method']['mean_width'] for c in rows]);err=np.array([c['method']['width_mcse'] for c in rows])*1.96
            ax.errorbar(a,y,yerr=err,fmt='o-',color=COLORS[d],label=f'd = {d}',markersize=3)
            if d>=2:
                x=np.array([100.,1000.]);ax.plot(x,y[-1]*(x/a[-1])**(1-d),':',color=COLORS[d])
        ax.set(xscale='log',yscale='log',xlabel=r'Axis amplitude $|a|/\tau$',title=f'Order K = {K}')
        ax.set_ylim(bottom=1e-9,top=10)
    axes[0].set_ylabel('Mean interval length / noise scale')
    handles,labels=axes[-1].get_legend_handles_labels()
    fig.legend(handles,labels,loc='outside lower center',ncol=6,frameon=False,handlelength=1.2,columnspacing=1.)
    save(fig,'coordinate_hierarchy')
    timing=json.loads((ROOT/'results/timing.json').read_text())
    fig,ax=plt.subplots(figsize=(5.4,3.2),layout='constrained')
    x=[c['entries'] for c in timing]
    ax.loglog(x,[c['preprocessing_median_seconds'] for c in timing],'-o',color=COLORS[0],label='Known-loading preprocessing')
    ax.loglog(x,[c['observation_median_seconds'] for c in timing],'-s',color=COLORS[1],label='One subsequent observation')
    ax.set(xlabel='Tensor entries',ylabel='Median seconds (three calls)',title='Reusable spectral computation, one library thread')
    ax.legend(frameon=False)
    save(fig,'computation')


if __name__=='__main__':main()
