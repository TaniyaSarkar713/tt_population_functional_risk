"""Exact finite-net scans at completed levels one and two.

This prototype is a certified truncated zero test, not an optimizer of the
full residual confidence set. Known iid Gaussian noise and supplied rank/norm
caps are required. No partial enumeration is silently treated as complete.
"""
import itertools,math
import numpy as np
from scipy.special import gammaln
from scipy.stats import norm

def sphere_net(size,order):
    if size==1:return np.array([[-1.],[1.]])
    if size==2:
        count=math.ceil(2*math.pi*order)
        theta=2*math.pi*np.arange(count)/count
        return np.column_stack([np.cos(theta),np.sin(theta)])
    raise ValueError("Prototype implements complete levels 1 and 2 only.")

class TruncatedScan:
    def __init__(self,p,order=3,max_level=2,tau=1.,M=None,J=1.,min_cap=1,alpha=.05):
        if order<3 or p<1 or not (0<alpha<1):
            raise ValueError("Require order>=3, p>=1 and 0<alpha<1.")
        if max_level not in (1,2) or max_level>p:
            raise ValueError("Complete levels must be 1 or 2, no greater than p.")
        self.p,self.K,self.t=p,order,max_level
        self.tau,self.M,self.J=tau,(tau*np.sqrt(p) if M is None else M),J
        if tau<=0 or self.M<=0 or J<1 or min_cap<1:raise ValueError("Invalid supplied bounds.")
        self.alpha0=alpha/2
        self.gamma=alpha/(2*p)
        self.h0=self.M*np.sqrt(min(p,min_cap)/p)
        self.levels={}
        for size in range(1,max_level+1):
            net=sphere_net(size,order)
            product=net
            for _ in range(order-1):
                product=np.einsum('ai,bj->abij',product,net).reshape(len(product)*len(net),-1)
            ids=[]
            for S in itertools.combinations(range(p),size):
                coords=list(itertools.product(S,repeat=order))
                ids.append(np.ravel_multi_index(np.array(coords).T,(p,)*order))
            ids=np.array(ids,dtype=np.int64)
            log_count=gammaln(p+1)-gammaln(size+1)-gammaln(p-size+1)
            threshold=tau*np.sqrt(2*(log_count+order*np.log(len(net))+np.log(2*p/self.gamma)))
            self.levels[size]=dict(indices=ids,products=product,threshold=threshold,
                                   contractions=len(ids)*len(product),net_points=len(net))
        self.lam0=tau*np.sqrt(2*np.log(2*p/self.alpha0))
        q=2/order
        self.Bq=J**(1-1/order)*self.M**q
        radii=[self.Bq*(2*self.lam0)**(1-q)/np.sqrt(p),
               norm.isf(self.alpha0/2)*tau,self.h0]
        self.base_index=int(np.argmin(radii))
        self.base_radius=float(radii[self.base_index])
        self.R={}
        for t in range(1,max_level+1):
            head=4*J**(order/2)/np.sqrt(p)*sum(self.levels[s]['threshold']*s**(-order/2) for s in range(1,t+1))
            at=4*J**(order/2)*self.levels[t]['threshold']*t**(-order/2)
            tail=0 if t==p else self.Bq*at**(1-q)/np.sqrt(p)
            self.R[t]=float(head+tail)
    def evaluate(self,Z,batch=32):
        if Z.shape!=(self.p,)*self.K:raise ValueError("Wrong tensor dimensions.")
        diagonal=np.array([Z[(i,)*self.K] for i in range(self.p)])
        centers=[np.sum(np.sign(diagonal)*np.maximum(np.abs(diagonal)-self.lam0,0))/np.sqrt(self.p),
                 np.sum(diagonal)/np.sqrt(self.p),0.]
        center=centers[self.base_index]
        lo,hi=center-self.base_radius,center+self.base_radius
        flat=Z.ravel()
        accepted=True
        stats={}
        history=[]
        empty=False
        for t,level in self.levels.items():
            maximum=0.
            for start in range(0,len(level['indices']),batch):
                contractions=flat[level['indices'][start:start+batch]]@level['products'].T
                maximum=max(maximum,float(np.max(np.abs(contractions))))
            stats[t]=maximum
            accepted=accepted and maximum<=level['threshold']
            radius=min(self.h0,self.R[t]) if accepted else self.h0
            lo,hi=max(lo,-radius),min(hi,radius)
            if empty or lo>hi:
                empty=True;lo=hi=0.
            history.append(dict(level=t,lo=float(lo),hi=float(hi),accepted=bool(accepted),
                                raw_radius=self.R[t],max_contraction=maximum))
        return dict(lo=float(lo),hi=float(hi),length=float(hi-lo),history=history,
                    empty_intersection=empty,base_length=2*self.base_radius)
