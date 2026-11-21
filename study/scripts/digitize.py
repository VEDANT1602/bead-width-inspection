"""Extract smoothed-camera and caliper means from Badarinath & Prabhu, Figure 10."""
import argparse
import csv
import hashlib
from pathlib import Path

import fitz
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SHA = '00418e59b0c2159e84c159984818d80b8128ade7bc06232ea9eab1af15c8992d'
# Coordinates in a 2x render of PDF p13 cropped to the rectangle below.
# x limits, two tick rows/physical widths, min/max rows for the data (omit legends).
PANELS = {10:(107,305,544,1.7,633,1.4,536,616),
          20:(359,557,529,1.2,645,.8,530,609),
          30:(128,579,104,1.1,380,.9,179,284),
          40:(107,305,733,1.2,850,.8,764,814),
          50:(359,557,733,1.2,850,.8,764,820)}

def digitize(filename):
    assert hashlib.sha256(filename.read_bytes()).hexdigest() == SHA
    with fitz.open(filename) as doc:
        pix = doc[12].get_pixmap(matrix=fitz.Matrix(8,8),clip=fitz.Rect(130,237,440,696))
    rgb = np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,3).astype(float)
    r,g,b = rgb.transpose(2,0,1)
    # Distinguish dark smooth curve from cyan framewise estimates using chromatic slope.
    blue = (b-r>90)&(g-r>55)&((b-g)/(b-r+1e-7)>.323)&(b<221)
    red = (r-g>95)&(r-b>95)
    rows=[]
    scale=4.
    for speed,(left,right,y1,a,y2,bval,top,bottom) in PANELS.items():
        lo,hi=round(top*scale),round(bottom*scale)
        L,R=round(left*scale),round(right*scale)
        x=np.arange(L+1,R)
        # Median row among the dark-blue pixels in each column; interpolate through overprinting.
        series=np.array([np.median(ys)+lo if len(ys:=np.flatnonzero(blue[lo:hi,col])) else np.nan for col in x])
        good=np.flatnonzero(np.isfinite(series))
        assert len(good)>.60*len(x)
        for k,target in enumerate(np.linspace(L,R,11)):
            # Red circles are hollow and approximately symmetric about the reference value.
            w=5 if speed==30 else 3
            xc=round(target)
            yr=np.flatnonzero(red[lo:hi,xc-w:xc+w+1].sum(axis=1)>0)
            assert len(yr)>0
            cal=(yr[0]+yr[-1])/2.+lo
            left_i=good[x[good]<=target]; right_i=good[x[good]>=target]
            yp=np.interp(target,x[good],series[good])
            nearby=good[abs(x[good]-target)<=2*scale]
            interp_span=(x[right_i[0]] if len(right_i) else target)-(x[left_i[-1]] if len(left_i) else target)
            value=lambda row: a+(row/scale-y1)*(bval-a)/(y2-y1)
            rows.append((speed,20*k,round(value(yp),5),round(value(cal),5),round(interp_span/scale,2),len(nearby)))
    return rows

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('pdf',type=Path);args=p.parse_args()
    with (ROOT/'outputs'/'plotted_widths.csv').open('w',newline='') as f:
        out=csv.writer(f);out.writerow(('speed_mm_s','position_mm','smoothed_camera_mm','caliper_mm','blue_interpolation_span_render_pixels','blue_columns_within_2px'));out.writerows(digitize(args.pdf))
