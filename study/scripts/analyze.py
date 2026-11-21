"""Hold-one-speed-out calibration; score only unrevealed mechanical measurements."""
import csv
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reference'))
import compare

def write(name,headers,rows):
    with (ROOT/'outputs'/name).open('w',newline='') as f:
        w=csv.writer(f);w.writerow(headers);w.writerows(rows)

def fit(training):
    # Fit effective discrepancy dynamics d=b+e, b[j+1]=b[j]+u. Replicates of the
    # separate instruments are unavailable. Use the empirical first-point prior.
    first=training[:,0]
    center=first.mean()
    p=max(first.var(),1e-6)
    def likelihood(log_sd):
        q,r=np.exp(2*log_sd)
        m=np.full(len(training),center)
        v=p
        score=0.
        for y in training.T:
            innovation=y-m; s=v+r
            score+=.5*(len(y)*np.log(s)+innovation.dot(innovation)/s)
            m+=innovation*v/s; v=v*r/s+q
        return score
    opt=minimize(likelihood,np.log([.012,.012]),method='L-BFGS-B',bounds=[(np.log(1e-5),np.log(.25))]*2)
    assert opt.success
    return center,p,*np.exp(2*opt.x)

def main():
    raw=np.genfromtxt(ROOT/'outputs/plotted_widths.csv',delimiter=',',names=True)
    z=raw['smoothed_camera_mm'].reshape(5,11);r=raw['caliper_mm'].reshape(5,11)
    span=raw['blue_interpolation_span_render_pixels'].reshape(5,11)
    scores=[];fits=[];choices=[]
    for i,speed in enumerate((10,20,30,40,50)):
        center,p,q,v=fit(np.delete(z-r,i,axis=0)); fits.append((speed,center,p**.5,q**.5,v**.5))
        target=1.5 if speed==10 else 1.
        for policy in ('camera_only','training_offset','initial_only','periodic','magnitude'):
            m=center; P=p; budget=1
            for j in range(11):
                if j: P+=q
                check=j==0 and policy in ('initial_only','periodic','magnitude')
                if budget and policy=='periodic' and j==5: check=True;budget=0
                if budget and policy=='magnitude' and j in (1,3,5,7) and (abs(z[i,j]-m-target)>=.05 or j==7):check=True;budget=0
                if check:
                    choices.append((speed,policy,j*20))
                    m+=P/(P+v)*(z[i,j]-r[i,j]-m);P=P*v/(P+v)
                if j in (2,4,6,8,10):
                    if policy=='camera_only':m=0.
                    if policy=='training_offset':m=float(np.median(np.delete(z-r,i,axis=0)))
                    error=z[i,j]-m-r[i,j]
                    scores.append((speed,policy,j*20,z[i,j]-m,r[i,j],error,abs(error),span[i,j]))
    write('field_fits.csv',['held_out_speed','prior_mean_mm','prior_sd_mm','drift_sd_per_20mm','paired_noise_sd_mm'],fits)
    write('field_scores.csv',['held_out_speed','policy','position_mm','estimated_width_mm','heldout_caliper_mm','error_mm','absolute_error_mm','interpolation_span_px'],scores)
    write('field_check_positions.csv',['held_out_speed','policy','position_mm'],choices)
    exact=[];mixtures=[]
    for label,c,method in [('periodic reset nominal',compare.Config(),'reset'),('periodic Kalman 0.0371',compare.Config(camera_sd=.0371),'kalman')]:
        cam,ref,true=compare.make_inputs(c);chk,pred=compare.schedule_and_classify(c,'periodic',cam,ref)
        if method=='kalman':pred=compare.kalman(c,cam,ref,chk)
        false=int((pred & (abs(true)<=c.tol)).sum());miss=int((~pred & (abs(true)>c.tol)).sum())
        exact.append((label,len(cam),false,miss,(false+miss)/len(cam)))
    write('integer_audit.csv',['case','builds','false_total','miss_total','mean_sum'],exact)
    # Hold camera/physical disturbances fixed; vary only the inference prior and the
    # etiological frequencies when aggregating. Report specific estimands for all policies.
    c=compare.Config();cam,ref,true=compare.make_inputs(c)
    for name in compare.SCHEDULES:
        chk,reset=compare.schedule_and_classify(c,name,cam,ref)
        for label,sw,sb in [('reset',0,0),('width-heavy',.020,.0025),('bias-heavy',.005,.010),('nominal',.010,.005)]:
            pred=reset if label=='reset' else compare.kalman(replace(c,width_walk_sd=sw,bias_walk_sd=sb),cam,ref,chk)
            cells=compare.counts(pred,true,c.tol).reshape(3,4,compare.R,2).mean(axis=(0,2))
            for mix in (.05,.5,.95):
                # Preserve half the population as stable/cancelled (25% each).
                w=np.array([.25,.5*mix,.5*(1-mix),.25])
                f,m=w@cells;mixtures.append((name,label,mix,f,m,f+m))
    write('prior_prevalence.csv',['schedule','estimation_prior','process_share_among_visible_shifts','false','miss','total'],mixtures)
if __name__=='__main__':main()
