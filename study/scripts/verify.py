"""Independent fixed-time scalar smoother and matrix covariance cross-check on simulator source arrays."""
import csv
import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reference'))
from run import make_runs
totals=[]
for sd in (.012,.0371):
    fp=fn=0
    for shape in ('step','ramp','reversal'):
        for mode in ('stable','process','sensor','cancel'):
            z,r,w=make_runs(shape,mode,sd/.012); n,T=w.shape
            m=np.zeros((n,2));P=np.zeros((2,2));state=np.zeros(n);bias=np.zeros(n)
            for k in range(T):
                if sd==.012:
                    state=.55*state+.45*z[:,k]
                    if k%20==9:bias=z[:,k]-r[:,k]
                    estimate=state-bias
                else:
                    P+=np.diag([.010**2,.005**2])
                    def update(y,h,variance):
                        global P,m
                        gain=P@h/(h@P@h+variance)
                        m+=(y-m@h)[:,None]*gain
                        P=(np.eye(2)-np.outer(gain,h))@P
                    update(z[:,k],np.array([1.,1.]),sd**2)
                    if k%20==9:update(r[:,k],np.array([1.,0.]),.006**2)
                    estimate=m[:,0]
                a=abs(estimate)>.05;b=abs(w[:,k])>.05
                fp+=np.sum(a&~b);fn+=np.sum(b&~a)
    totals.append((int(fp),int(fn)))
with (ROOT/'outputs/integer_audit.csv').open() as f:
    out=list(csv.DictReader(f))
assert totals==[(int(r['false_total']),int(r['miss_total'])) for r in out]
with (ROOT/'outputs/field_scores.csv').open() as f:x=list(csv.DictReader(f))
with (ROOT/'outputs/field_check_positions.csv').open() as f:actions=list(csv.DictReader(f))
assert len(x)==125
for r in x:
    assert not any(all(r[field]==q[field] for field in ('held_out_speed','policy','position_mm')) for q in actions)
print('Matrix and smoothing checks:',totals,'; scored held-out entries:',len(x))
