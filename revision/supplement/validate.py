"""Check counts, paired arithmetic, masking and the Kalman recursion."""
import csv
import gzip
from pathlib import Path
import numpy as np
import compare as c

root=Path(__file__).resolve().parent


def check_kalman_against_batch_posterior():
    # Small joint Gaussian prior across all times gives a separate exact conditional mean.
    cfg=c.Config(width=4,tol=.011)
    cam=np.array([[.07,-.02,.09,.04,-.08,.01,.12,-.03]])
    ref=np.array([[np.nan,.02,np.nan,np.nan,np.nan,np.nan,-.05,np.nan]])
    checks=np.isfinite(ref)
    out=c.kalman(cfg,cam,ref,checks)
    for t in range(cam.size):
        n=t+1
        rw_cov=np.minimum.outer(np.arange(1,n+1),np.arange(1,n+1))
        prior=np.kron(np.diag([cfg.width_walk_sd**2,cfg.bias_walk_sd**2]),rw_cov)
        h=np.column_stack((np.eye(n),np.eye(n)))
        r=np.full(n,cfg.camera_sd**2)
        y=cam[0,:n]
        for k in np.flatnonzero(checks[0,:n]):
            obs=np.zeros(2*n); obs[k]=1
            h=np.vstack((h,obs));r=np.append(r,cfg.ref_sd**2);y=np.append(y,ref[0,k])
        post=prior@h.T@np.linalg.solve(h@prior@h.T+np.diag(r),y)
        for epsilon in (-1e-6,1e-6):
            at_boundary=c.replace(cfg,tol=abs(post[t])+epsilon)
            sequential=c.kalman(at_boundary,cam[:,:n],ref[:,:n],checks[:,:n])
            assert sequential[0,-1] == (epsilon<0)
        assert out[0,t] == (abs(post[t])>cfg.tol)


def check_reference_mask():
    cfg=c.Config()
    cam,ref,_=c.make_inputs(cfg)
    for name in c.SCHEDULES:
        ck,first=c.schedule_and_classify(cfg,name,cam,ref)
        masked=np.where(ck,ref,np.nan)
        ck2,again=c.schedule_and_classify(cfg,name,cam,masked)
        assert np.array_equal(ck2,ck) and np.array_equal(first,again)
        assert np.array_equal(c.kalman(cfg,cam,ref,ck),c.kalman(cfg,cam,masked,ck))


def check_outputs():
    with gzip.open(root/'nominal_runs.csv.gz','rt') as f:
        rows=list(csv.DictReader(f))
    keys={(r['shape'],r['source'],r['schedule'],r['estimator'],r['paired_run']) for r in rows}
    assert len(rows)==len(keys)==38400
    results=list(csv.DictReader((root/'comparator_sensitivity.csv').open()))
    assert len(results)==270
    for s in results:
        if s['variation']!='nominal':continue
        g=[r for r in rows if (r['schedule'],r['estimator'])==(s['schedule'],s['estimator'])]
        assert np.isclose(np.mean([int(r['false'])+int(r['miss']) for r in g]),float(s['total']))
    b=list(csv.DictReader((root/'cell_effects.csv').open()))
    assert len(b)==120
    print("Verified 38,400 unique nominal records, 270 sensitivity summaries, 120 cell means, reference masking and batch-posterior agreement.")


if __name__=='__main__':
    check_reference_mask()
    check_kalman_against_batch_posterior()
    check_outputs()
