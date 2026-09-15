"""Bounded endpoint comparison, as in review_revision/empirical/code/numerics.py.

This is evaluation rounding, not statistical slack or interval certification.
Strict coverage is retained alongside the four-ULP convention.
"""
import numpy as np


def coverage_events(lo,hi,truth,ulps=4):
    lo,hi=np.array(lo,float,copy=True),np.array(hi,float,copy=True)
    for _ in range(ulps):
        lo=np.nextafter(lo,-np.inf);hi=np.nextafter(hi,np.inf)
    return (lo<=truth)&(truth<=hi)
