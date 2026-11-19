# Spending eight reference checks on a 160-segment print

When a camera starts reporting a wider bead, the printer might be feeding more material, or the camera calibration might have shifted. The monitor can buy a second opinion from a reference instrument eight times during the build. Which segments should it inspect?

Look at the first paired step-change run. In one simulation 91 segments are outside tolerance. In the other, the camera sees the same trace and every segment is in tolerance. The reference readings are what let the monitor distinguish them. Each policy gets exactly one reading per block, even when its preferred trigger never fires. [Process-change record](results.csv?plain=1#L2882) · [Sensor-change record](results.csv?plain=1#L5762) · [Inspection budget in code](run.py#L63)

At the nominal camera noise of 0.012 mm, triggering on a large deviation averaged 0.96 false alarms per build, against 4.11 for periodic inspection. Missed violations went the other way, from 5.24 to 7.64. This trade-off matters if reprinting an undetected defect costs more than stopping on a false alarm.

![False alarms and misses for each policy and inspection budget](figure.png)

The simulator pairs the same builds across three timing rules. It varies the disturbance shape and source, and then repeats the comparison with sixteen checks. At that larger budget the ambiguity trigger gives the fewest total errors at nominal noise, 4.59 per build. Alarms have no effect on extrusion in this experiment. A production decision needs the delay of the reference check and the effect of adjusting feed mid-print. [Complete counts](results.csv) · [Methods](manuscript.md) · [Paper PDF](manuscript.pdf)

## Reproduce the comparison

Run from the repository root with Python 3.11. The study used Python 3.11.9 and NumPy 1.26.0. The simulation generates its inputs locally.

```bash
python -m pip install -r requirements.txt
python run.py
python verify.py
```

`run.py` regenerates the 34,560 records in `results.csv` and prints policy means and paired uncertainty estimates. `verify.py` uses the Python standard library to recalculate the six table rows directly from that file. The figure can also be redrawn from the saved results.

```bash
python -m pip install -r requirements-plot.txt
python make_figure.py
```

Repository maintained by **Vedant Thaker**.
