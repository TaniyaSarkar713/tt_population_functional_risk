"""Finite exact checks for D1, a classical Gaussian-sequence specialization."""
import csv
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.special import logsumexp
from scipy.stats import hypergeom

ROOT = Path(__file__).resolve().parents[1]


def benchmark(K, p, tau, M, alpha=0.05, s=None):
    if s is None:
        s = max(1, int(np.floor((p / np.log(p))**(1/K))))
    b = min(M * s**(-K/2), tau*np.sqrt(np.log1p(p/(4*s*s))))
    eta = 0.5*np.sqrt(np.expm1(0.25))
    lower = (1-2*alpha-eta)*s*b/np.sqrt(p)
    return s, b, lower


def main():
    # Enumeration provides an independent check of the overlap formula.
    p, s, rho2 = 8, 3, 0.2
    supports = [set(x) for x in itertools.combinations(range(p),s)]
    direct = np.mean([np.exp(rho2*len(S&T)) for S in supports for T in supports])
    j = np.arange(s+1)
    exact = np.sum(hypergeom.pmf(j,p,s,s)*np.exp(rho2*j))
    assert np.isclose(direct,exact,rtol=1e-13)
    records = []
    for K in (3,4,6):
        for p in (16,64,128,512,2048,8192,32768,10**6):
            tau, M = p**-0.5, 1.0
            s,b,lower = benchmark(K,p,tau,M)
            j = np.arange(s+1)
            rho2 = (b/tau)**2
            logmoment = logsumexp(hypergeom.logpmf(j,p,s,s)+rho2*j)
            analytic_bound = s*s*np.expm1(rho2)/p
            assert b*s**(K/2)<=M*(1+1e-12)
            assert logmoment<=analytic_bound+1e-7
            assert analytic_bound<=0.25+1e-12
            rate = tau*(np.log(p)/p)**((K-2)/(2*K))
            records.append(dict(K=K,p=p,s=s,b=b,log_second_moment=float(logmoment),
                                analytic_log_bound=float(analytic_bound),
                                lower_length=float(lower),rate=float(rate),
                                lower_divided_by_rate=float(lower/rate)))
    dest=ROOT/'results'
    with (dest/'diagonal_benchmark.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    result=dict(status='PASS',enumerated_support_pairs=len(supports)**2,
                enumeration_moment=float(direct),hypergeometric_moment=float(exact),
                grid_cases=len(records),max_log_second_moment=max(r['log_second_moment'] for r in records),
                universal_log_bound=0.25,
                scope='Diagonal observations only; full-tensor likelihood has overlap power K.')
    (dest/'diagonal_benchmark_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
