"""Matched-budget inspection timing and state-estimation comparisons."""
import csv
import gzip
from dataclasses import dataclass, replace
from itertools import product
from pathlib import Path

import numpy as np

import run as original

ROOT = Path(__file__).resolve().parent
CELLS = list(product(("step","ramp","reversal"), ("stable","process","sensor","cancel")))
SCHEDULES = ("periodic","magnitude","ambiguity","ewma_chart","cusum")
ESTIMATORS = ("reset","kalman")
R = original.N


@dataclass(frozen=True)
class Config:
    width: int = 20
    camera_sd: float = .012
    ref_sd: float = .006
    alpha: float = .45
    tol: float = .05
    chart_lambda: float = .20
    chart_limit: float = 3.
    k: float = .5
    h: float = 5.
    width_walk_sd: float = .010
    bias_walk_sd: float = .005
    band_start: float = .010
    band_growth: float = .002


def make_inputs(c):
    blocks = []
    for shape, source in CELLS:
        cam, ref, true = original.make_runs(shape, source, c.camera_sd/.012)
        if c.ref_sd != .006:
            ref = true + (ref-true) * (c.ref_sd/.006)
        blocks.append((cam, ref, true))
    cam, ref, true = (np.concatenate(x) for x in zip(*blocks))
    for s in range(0, len(CELLS)*R, 4*R):
        assert np.array_equal(cam[s:s+R], cam[s+3*R:s+4*R])
        assert np.array_equal(cam[s+R:s+2*R], cam[s+2*R:s+3*R])
    return cam,ref,true


def schedule_and_classify(c, name, cam, ref):
    """Select each check before observing the reference; all schedules share the reset alarm."""
    n, time = cam.shape
    checks = np.zeros((n,time), dtype=bool)
    alarms = np.zeros_like(checks)
    smoothed, bias, chart, high, low = np.zeros((5,n))
    last = np.full(n,-1)
    rho = .7
    latent_var = .005**2/(1-rho**2)
    raw_sd = np.sqrt(latent_var + c.camera_sd**2)
    decay = 1-c.chart_lambda
    chart_sd = np.sqrt(c.chart_lambda/(2-c.chart_lambda) *
                       (c.camera_sd**2 + latent_var*(1+rho*decay)/(1-rho*decay)))
    for t, reading in enumerate(cam.T):
        smoothed += c.alpha*(reading-smoothed)
        pred = smoothed - bias
        corrected = reading - bias
        slot = t % c.width
        available = last < t-slot
        if name == "periodic":
            would_check = np.full(n, slot == (c.width-1)//2)
        elif name == "magnitude":
            would_check = abs(pred) >= c.tol
        elif name == "ambiguity":
            would_check = abs(abs(pred)-c.tol) <= c.band_start + c.band_growth*(t-last)
        elif name == "ewma_chart":
            chart += c.chart_lambda*(corrected-chart)
            would_check = abs(chart) >= c.chart_limit*chart_sd
        elif name == "cusum":
            z = corrected / raw_sd
            high = np.maximum(0,high+z-c.k)
            low = np.maximum(0,low-z-c.k)
            would_check = np.maximum(high,low) >= c.h
        else:
            raise ValueError(name)
        check = available & (would_check | (slot == c.width-1))
        checks[:,t] = check
        last[check] = t
        chart[check] = high[check] = low[check] = 0.
        bias[check] = reading[check] - ref[check,t]
        alarms[:,t] = abs(smoothed - bias) > c.tol
    assert (checks.reshape(n,time//c.width,c.width).sum(axis=2) == 1).all()
    return checks,alarms


def kalman(c, cam, ref, checks):
    """Two independent random-walk priors. Only indexed reference reads enter the filter."""
    n = len(cam)
    x, b, pxx, pxb, pbb = np.zeros((5,n))
    alarms = np.empty_like(checks)
    for t, reading in enumerate(cam.T):
        pxx += c.width_walk_sd**2
        pbb += c.bias_walk_sd**2
        cov_x, cov_b = pxx+pxb, pxb+pbb
        innovation_var = cov_x+cov_b+c.camera_sd**2
        kx, kb = cov_x/innovation_var, cov_b/innovation_var
        innovation = reading - x - b
        x += kx*innovation
        b += kb*innovation
        pxx -= kx*cov_x
        pxb -= kx*cov_b
        pbb -= kb*cov_b
        obs = checks[:,t]
        cov_x, cov_b = pxx[obs].copy(), pxb[obs].copy()
        innovation_var = cov_x+c.ref_sd**2
        kx, kb = cov_x/innovation_var, cov_b/innovation_var
        innovation = ref[obs,t] - x[obs]
        x[obs] += kx*innovation
        b[obs] += kb*innovation
        pxx[obs] -= kx*cov_x
        pxb[obs] -= kx*cov_b
        pbb[obs] -= kb*cov_b
        assert min(pxx.min(),pbb.min(),(pxx*pbb-pxb**2).min()) >= -1e-15
        alarms[:,t] = abs(x)>c.tol
    return alarms


def counts(alarms, truth, tol):
    out = abs(truth) > tol
    fp = np.sum(alarms & ~out,axis=1)
    fn = np.sum(~alarms & out,axis=1)
    return np.stack((fp,fn),axis=-1).reshape(len(CELLS),R,2)


def calculate(c):
    cam,ref,true = make_inputs(c)
    groups = {}
    for name in SCHEDULES:
        checks,alarms = schedule_and_classify(c,name,cam,ref)
        groups[(name,"reset")] = counts(alarms,true,c.tol)
        groups[(name,"kalman")] = counts(kalman(c,cam,ref,checks),true,c.tol)
        if c == Config() and name in original.POLICIES:
            for i, (shape, mode) in enumerate(CELLS):
                idx = slice(i*R,(i+1)*R)
                fp, fn, _, _ = original.score(name,c.width,cam[idx],ref[idx],true[idx])
                assert np.array_equal(groups[(name,"reset")][i],np.column_stack((fp,fn)))
    return groups


def sensitivity_design():
    yield "nominal",Config()
    for field,values in (
        ("width",(10,)), ("alpha",(.20,.70)), ("tol",(.035,.065)),
        ("camera_sd",(.006,.024,.0371)), ("ref_sd",(.003,.012)),
        ("chart_lambda",(.1,.4)), ("chart_limit",(2.,4.)),
        ("k",(.25,1.0)), ("h",(3.,7.)), ("width_walk_sd",(.005,.02)),
        ("bias_walk_sd",(.0025,.010)), ("band_start",(.005,.020)),
        ("band_growth",(.001,.004))):
        for val in values:
            yield f"{field}={val:g}",replace(Config(), **{field:val})


def write(name,cols,rows):
    with (ROOT/name).open("w",newline="") as f:
        w=csv.writer(f)
        w.writerow(cols)
        w.writerows(rows)


def main():
    summary, cells, perrun = [],[],[]
    for label,c in sensitivity_design():
        metrics = calculate(c)
        control = metrics[("periodic","reset")]
        for (policy,est), data in metrics.items():
            f,m = data.mean(axis=(0,1))
            diff = data-control
            d = diff.mean(axis=(0,1))
            within = (data - metrics[(policy,"reset")]).mean(axis=(0,1))
            summary.append((label,policy,est,f,m,f+m,*d,d.sum(),within.sum()))
            if label == "nominal":
                for i,(shape,source) in enumerate(CELLS):
                    cell = data[i].mean(axis=0)
                    delta = diff[i].mean(axis=0)
                    cells.append((shape,source,policy,est,*cell,cell.sum(),*delta,delta.sum()))
                    for run,(false,miss) in enumerate(data[i]):
                        perrun.append((shape,source,policy,est,run,false,miss))
    write("comparator_sensitivity.csv",["variation","schedule","estimator","false","miss","total",
          "delta_false","delta_miss","delta_total","delta_total_vs_same_schedule_reset"],summary)
    write("cell_effects.csv",["shape","source","schedule","estimator","false","miss","total",
          "delta_false","delta_miss","delta_total"],cells)
    with gzip.open(ROOT/"nominal_runs.csv.gz","wt",newline="") as f:
        w=csv.writer(f); w.writerow(["shape","source","schedule","estimator","paired_run","false","miss"])
        w.writerows(perrun)


if __name__=="__main__":
    main()
