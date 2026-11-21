"""Cross thresholds with discrepancy-process misspecification on identical held-out physical stations."""
import csv
from pathlib import Path
import numpy as np
from analyze import ROOT,fit

a=np.genfromtxt(ROOT/'outputs/plotted_widths.csv',delimiter=',',names=True)
z=a['smoothed_camera_mm'].reshape(5,11);r=a['caliper_mm'].reshape(5,11)
out=[]
for threshold in (.025,.035,.05,.075,.10):
    for q_scale in (.25,1.,4.):
        scores=[]
        for i,speed in enumerate((10,20,30,40,50)):
            start,p,q,v=fit(np.delete(z-r,i,axis=0))
            yhat=start; P=p; used=False
            for j in range(11):
                if j:P+=q*q_scale
                trigger=abs(z[i,j]-yhat-(1.5 if i==0 else 1.))>=threshold
                check=j==0 or (not used and j in (1,3,5,7) and (trigger or j==7))
                if check:
                    if j:used=True
                    yhat+=P/(P+v)*(z[i,j]-r[i,j]-yhat);P=P*v/(P+v)
                if j in (2,4,6,8,10):scores.append(abs(z[i,j]-yhat-r[i,j]))
        out.append((threshold,q_scale,np.mean(scores)))
with (ROOT/'outputs/field_sensitivity.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['trigger_mm','fitted_process_variance_multiplier','heldout_MAE_mm']);w.writerows(out)
