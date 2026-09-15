"""Common publication-sized vector figure style."""
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/tensor-empirical-mpl')
os.environ.setdefault('XDG_CACHE_HOME','/tmp/tensor-empirical-cache')
os.makedirs(os.environ['XDG_CACHE_HOME'],exist_ok=True)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import NullFormatter,LogLocator

COLORS=['#0072B2','#D55E00','#009E73','#CC79A7','#E69F00','#000000']
MARKERS=['o','s','^','D','v','x']
LINES=['-','--','-.',':','--',':']
plt.rcParams.update({'font.family':'serif','font.size':10,'axes.labelsize':10,'xtick.labelsize':9,
    'ytick.labelsize':9,'legend.fontsize':9,'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none',
    'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.18,
    'lines.linewidth':1.4,'lines.markersize':4.5,'savefig.bbox':'tight'})


def style(i):
    return dict(color=COLORS[i%len(COLORS)],marker=MARKERS[i%len(MARKERS)],linestyle=LINES[i%len(LINES)])


def pair(height=3.8):
    fig,ax=plt.subplots(1,2,figsize=(6.8,height),layout='constrained')
    return fig,ax


def save(fig,root,name):
    for ax in fig.axes:
        if ax.get_xscale()=='log':
            values=[]
            for line in ax.lines:
                values.extend(np.asarray(line.get_xdata(),float).ravel())
            values=sorted({float(v) for v in values if np.isfinite(v) and v>0})
            if 1<len(values)<=6:
                ax.set_xticks(values,labels=[f'{v:g}' for v in values])
            else:ax.xaxis.set_major_locator(LogLocator(base=10,numticks=4))
            ax.xaxis.set_minor_formatter(NullFormatter())
        legend=ax.get_legend()
        if legend is not None:
            handles,labels=ax.get_legend_handles_labels();legend.remove()
            labels=[label.replace('xch known','XCH known').replace('xch_known','XCH known') for label in labels]
            ax.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,-.24),ncol=2,
                      frameon=False,fontsize=8)
    for ext in ['pdf','svg','png']:
        fig.savefig(root/(name+'.'+ext),dpi=150)
    plt.close(fig)
