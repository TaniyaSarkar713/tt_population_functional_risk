"""Materialize the predeclared registry before validation and execution."""
import numpy as np
from common import ROOT, SEED, high, write_json


def main():
    cases = []
    def add(suite, **kw):
        count = sum(c['suite'] == suite for c in cases)
        cases.append(dict(id=f'{suite}_{count:03d}', suite=suite, **kw))
    for p in [64, 256, 1024, 4096, 16384, 65536]:
        r = int(np.ceil(np.sqrt(p)))
        for h in [.25, 1., 4.]:
            for signal in ['zero', 'boundary']:
                add('S01', p=p, rank=r, M=h*np.sqrt(p/r), n=1, signal=signal, B=5000, axis='p', h=h)
    for n in [1,4,16,64,256,1024]:
        for signal in ['zero', 'boundary']:
            add('S01',p=1024,rank=32,M=8.,n=n,signal=signal,B=5000,axis='n',h=8/np.sqrt(32)*np.sqrt(n))
    # Fixed-M structural p sweep isolates the predicted p^(-1/4) slope.
    for p in [64,256,1024,4096,16384,65536]:
        add('S01',p=p,rank=int(np.sqrt(p)),M=1.,n=1,signal='boundary',B=5000,axis='structural_p',h=p**(-.25))
    for K in [3,4]:
        for p in [256,1024,4096,16384,65536]:
            for support in ['atom','eight','threshold']:
                add('S02',p=p,K=K,M=float(np.sqrt(p)),n=1,support=support,B=1000,axis='p')
        for n in [16,64,256,1024,4096,16384,65536]:
            add('S02',p=4096,K=K,M=1.,n=n,support='threshold',B=1000,axis='n')
    for p,B in [(8,500),(16,500),(32,300),(64,150)]:
        for rank in [1,int(np.ceil(np.sqrt(p)))]:
            add('S03',p=p,rank=rank,true_rank=rank,amplitude=8*high.pointwise_amplitude_bound(p,rank),
                signal='diagonal',n=1,B=B,regime='P1',shift=None)
    threshold=high.pointwise_amplitude_bound(16,1)
    for a in [0.,.5,2.,8.,32.,128.,512.,2048.,8192.,threshold,8*threshold]:
        add('S04',p=16,rank=1,true_rank=int(a>0),amplitude=a,signal='diagonal',n=1,B=500,regime='signal_sweep',shift=None)
    for rank in [1,2,4]:
        for signal in ['saturated_two','strong_plus_weak','one_strong']:
            add('S04',p=16,rank=rank,true_rank=1 if signal=='one_strong' else 2,
                amplitude=8*high.pointwise_amplitude_bound(16,2),signal=signal,n=1,B=500,
                regime='rank_sensitivity',shift=None)
    for a in [2.,128.,8*threshold]:
        add('S04',p=16,rank=2,true_rank=2,amplitude=a,signal='rotated',n=1,B=500,regime='rotation',shift=None)
    for n in [1,4,16,64,256]:
        add('S04',p=16,rank=1,true_rank=1,amplitude=8*threshold,signal='diagonal',n=n,B=500,
            regime='sample_size',shift=None)
    for law in ['gaussian','t3','t5','rademacher','variance_01','variance_05','mean_shift']:
        add('S05',p=256,law=law,rho=0.,B=5000)
    for rho in [.2,.5,.8]:
        add('S05',p=256,law='gaussian',rho=rho,B=5000)
    for n in [64,256,1024]:
        for law in ['gaussian','t3','t5','rare_variance','ar1']:
            add('S06',n=n,law=law,B=500)
    for p in [64,256,1024,4096,16384,65536]:
        for profile in ['flat','power_025','power_075','power_125','spike','log','plateau']:
            for M in [.1,1.,float(np.sqrt(p)),1000.]:
                add('S07',p=p,profile=profile,M=M,B=5000 if M<=1 else 0)
    for signal in ['zero','weak','boundary','strong']:
        for loading in ['flat','arbitrary']:
            add('S08',K=3,signal=signal,loading=loading,B=30,
                budgets=[100,600,3000],tolerances=[.5,.1,.1])
    for eps in [0.,.01,.05,.2,.5]:
        add('S09',kind='loading',p=4096,K=4,M=64.,epsilon=eps,B=1000)
    for eta in [0.,.01,.05,.2,1.,4.]:
        add('S09',kind='approximation',p=4096,K=4,M=1.,eta=eta,B=1000)
    for shift in [0.,1.,2.,4.,8.]:
        add('S10',p=16,rank=2,true_rank=2,amplitude=8*high.pointwise_amplitude_bound(16,2),
            signal='opposite',n=1,B=1000,regime='local_power',shift=shift)
    write_json(ROOT/'configs/cases.json',dict(seed=SEED,alpha=[.1,.05,.01],cases=cases))
    write_json(ROOT/'configs/runtime.json',dict(diagonal_p=[1024,4096,16384,65536,262144,1048576],
        diagonal_repeats=100, tensor_p=[8,16,32,64],tensor_repeats=10,solver_K=[3,4],solver_budgets=[25,100],solver_repeats=3))
    print('Registered',len(cases),'cases before execution.')


if __name__=='__main__':
    main()
