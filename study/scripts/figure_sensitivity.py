"""Perturb Figure 10 digitization conventions, refit all training folds, and retime one check."""
import argparse
import csv
import hashlib
from itertools import product
from pathlib import Path
import sys

import fitz
import numpy as np

from analyze import fit
from digitize import PANELS, SHA

SPEEDS = [10, 20, 30, 40, 50]
EVAL = [2,4,6,8,10]
ROOT = Path(__file__).resolve().parents[1]

def read_ink(pdf):
    if hashlib.sha256(pdf.read_bytes()).hexdigest() != SHA:
        raise ValueError("Expected the version-2 source PDF specified in the README.")
    with fitz.open(pdf) as doc:
        pix = doc[12].get_pixmap(matrix=fitz.Matrix(8,8), clip=fitz.Rect(130,237,440,696))
    rgb = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height,pix.width,3).astype(np.int16)
    return rgb.transpose(2,0,1)

def traces(rgb, color):
    red, green, blue = rgb
    camera_mask = (blue-red>90)&(green-red>55)&((blue-green)/(blue-red+1e-7)>color)&(blue<221)
    caliper_mask = (red-green>95)&(red-blue>95)
    cache = {}
    for speed,(left,right,y1,a,y2,b,top,bottom) in PANELS.items():
        lo,hi=4*top,4*bottom
        xs=np.arange(4*left+1,4*right)
        ink=camera_mask[lo:hi,xs]
        by_column=[np.flatnonzero(ink[:,i])+lo for i in range(len(xs))]
        observed=np.array([bool(len(v)) for v in by_column])
        known=xs[observed]
        if len(known)<.55*len(xs):raise ValueError("Insufficient dark curve pixels")
        lines={q:np.array([np.quantile(v,q) for v in by_column if len(v)]) for q in (.25,.50,.75)}
        cache[speed]=(known,lines,caliper_mask[lo:hi,:],lo)
    return cache

def extract(cache,dx,q,marker):
    camera=[];caliper=[]
    for speed,(left,right,y1,a,y2,b,top,bottom) in PANELS.items():
        known,lines,red,lo=cache[speed]
        cam_widths=[];ref_widths=[]
        for j,x in enumerate(np.linspace(4*left,4*right,11)):
            # A shift of two samples in the 8x rendering is 1/4 PDF point.
            # The caliper reference is centered at the marked station. A wider
            # symmetric search captures an intact hollow marker near its center.
            row=np.interp(np.clip(x+dx,4*left,4*right),known,lines[q])
            xc=round(x); width=5 if speed==30 else 3
            row_ids=np.flatnonzero(red[:,xc-width:xc+width+1].any(axis=1))
            counts=red[:,xc-width:xc+width+1].sum(axis=1)
            if marker=="edge_mid":center=(row_ids[0]+row_ids[-1])/2+lo
            else:center=np.average(row_ids,weights=counts[row_ids])+lo
            conv=lambda y: a+(y/4-y1)*(b-a)/(y2-y1)
            cam_widths.append(round(conv(row),5));ref_widths.append(round(conv(center),5))
        camera.append(cam_widths);caliper.append(ref_widths)
    return np.array(camera),np.array(caliper)

def evaluate(z,r):
    outcomes={k:[] for k in ('camera','fixed','start','halfway','magnitude')}
    late={k:[] for k in ('camera','fixed','check_0','check_20','check_60','check_100')}
    for i,speed in enumerate(SPEEDS):
        train=np.delete(z-r,i,axis=0)
        offset=np.median(train)
        mu,p,q,v=fit(train)
        for method in outcomes:
            m=0. if method=='camera' else (offset if method=='fixed' else mu)
            P=p; used=False
            for j in range(11):
                if j:P+=q
                acquire=(method in ('start','halfway','magnitude') and j==0) or (method=='halfway' and j==5)
                if method=='magnitude' and not used and j in (1,3,5,7):
                    if abs(z[i,j]-m-(1.5 if i==0 else 1.))>=.05 or j==7:acquire=True;used=True
                if acquire:
                    m+=P/(P+v)*(z[i,j]-r[i,j]-m);P=P*v/(P+v)
                if j in EVAL:outcomes[method].append(abs(z[i,j]-r[i,j]-m))
        for key in late:
            if key=='camera':m=0.
            elif key=='fixed':m=offset
            else:
                j=int(key.split('_')[1])//20
                prior_var=p+j*q
                m=mu+prior_var/(prior_var+v)*(z[i,j]-r[i,j]-mu)
            late[key].append((speed,*(abs(z[i,j]-r[i,j]-m) for j in (6,8,10))))
    return {k:float(np.mean(a)) for k,a in outcomes.items()},late

def dump(path,columns,rows):
    with open(path,'w',newline='') as f:
        w=csv.writer(f);w.writerow(columns);w.writerows(rows)

def main():
    p=argparse.ArgumentParser();p.add_argument('pdf',type=Path);p.add_argument('--out',type=Path,default=ROOT/'outputs');a=p.parse_args()
    rgb=read_ink(a.pdf);a.out.mkdir(exist_ok=True,parents=True)
    rows=[];widths=[]
    for color in (.30,.323,.35):
        cache=traces(rgb,color)
        for dx,q,marker in product((-2,0,2),(.25,.5,.75),('edge_mid','ink_mean')):
            z,r=extract(cache,dx,q,marker)
            scores,late=evaluate(z,r)
            rows.append((color,dx,q,marker,*scores.values()))
            for i,speed in enumerate(SPEEDS):
                for j in range(11):widths.append((color,dx,q,marker,speed,20*j,z[i,j],r[i,j]))
            if (color,dx,q,marker)==(.323,0,.5,"edge_mid"):
                central=z.copy()
                dump(a.out/'interior_checks.csv',['policy','held_out_speed','abs_error_120_mm','abs_error_160_mm','abs_error_200_mm'],[(k,*row) for k,per in late.items() for row in per])
    dump(a.out/'figure_reading_scores.csv',['blue_color_cut','horizontal_shift_8x_px','ink_quantile','marker_center',*scores],rows)
    dump(a.out/'figure_reading_widths.csv',['blue_color_cut','horizontal_shift_8x_px','ink_quantile','marker_center','speed_mm_s','position_mm','camera_mm','caliper_mm'],widths)
    original=np.genfromtxt(ROOT/'outputs'/'plotted_widths.csv',delimiter=',',names=True)
    np.testing.assert_array_equal(central.ravel(),original['smoothed_camera_mm'])
if __name__=='__main__':main()
