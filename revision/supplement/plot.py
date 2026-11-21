"""Paired effects of inspection and filtering choices within fault sources."""
import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np

root=Path(__file__).resolve().parent
with (root/'cell_effects.csv').open() as f:
    cells=list(csv.DictReader(f))
policies=("periodic","magnitude","ambiguity","ewma_chart","cusum")
names=["Periodic","Magnitude","Ambiguity","EWMA chart","CUSUM"]
sources=("stable","process","sensor","cancel")
fig,axes=plt.subplots(ncols=2,figsize=(7.7,3.15),sharey=True,layout="constrained")
for ax,est in zip(axes,("reset","kalman")):
    values=np.array([[np.mean([float(row['delta_total']) for row in cells if
                       row['schedule']==s and row['estimator']==est and row['source']==m]) for m in sources] for s in policies])
    im=ax.imshow(values,cmap="RdBu_r",norm=TwoSlopeNorm(vmin=-12,vcenter=0,vmax=12),aspect="auto")
    ax.set_yticks(range(5),names)
    ax.set_xticks(range(4),["Stable","Process","Sensor","Cancel"])
    ax.set_title("Single-check bias reset" if est=="reset" else "Two-state Kalman filter",fontsize=11)
    ax.tick_params(length=0,labelsize=8)
    for i in range(5):
        for j in range(4):
            ax.text(j,i,format(values[i,j],"+.1f").replace("-0.0","0.0").replace("+0.0","0.0"),ha="center",va="center",color="white" if abs(values[i,j])>6.3 else "#1a2027",fontsize=8.5)
    ax.spines[:].set_visible(False)
fig.savefig(root/'source_effects.png',dpi=220,facecolor='white')
