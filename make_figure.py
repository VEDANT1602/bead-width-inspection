"""Rebuild the published figure from this repository's results.csv."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
TEAL, ORANGE, NAVY, SMOKE = "#006b68", "#ab4b26", "#223c57", "#717d87"
plt.rcParams.update({"font.size":9.5, "axes.spines.top":False, "axes.spines.right":False,
                     "figure.dpi":130, "savefig.dpi":250, "font.family":"DejaVu Sans"})


def read_results():
    with (ROOT / "results.csv").open(encoding="utf8", newline="") as stream:
        return list(csv.DictReader(stream))


def save_figure(fig):
    fig.tight_layout(pad=0.7)
    fig.savefig(ROOT / "figure.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def calibration():
    tab = read_results()
    fig, ax = plt.subplots(figsize=(6.3,2.45))
    specs = [(s,b) for b in ("20","10") for s in ("periodic","magnitude","ambiguity")]
    false, missed = [], []
    for s,b in specs:
        group = [r for r in tab if r["camera_noise"]=="0.012" and r["block"]==b and r["policy"]==s]
        false.append(np.mean([float(r["false_alarm"]) for r in group]))
        missed.append(np.mean([float(r["missed"]) for r in group]))
    ax.bar(range(6),false,color=TEAL,label="False alarm")
    ax.bar(range(6),missed,bottom=false,color="#b9cbd2",label="Missed segment")
    ax.set_xticks(range(6),["Periodic","Magnitude","Ambiguity"]*2)
    ax.axvline(2.5,color="#94a8ae",linewidth=.8)
    ax.set_xlabel("8 reference checks                         16 reference checks")
    ax.set_ylabel("Segments per trace")
    ax.legend(frameon=False,ncol=2,loc="upper right")
    save_figure(fig)


if __name__ == "__main__":
    calibration()
