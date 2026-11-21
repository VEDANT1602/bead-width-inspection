"""Original three rules across the 54-condition generator grid."""
import csv
from itertools import product
from pathlib import Path

import numpy as np

import run as original

ROOT = Path(__file__).resolve().parent
SHAPES = ("step", "ramp", "reversal")
SOURCES = ("stable", "process", "sensor", "cancel")
POLICIES = original.POLICIES
CELLS = list(product(SHAPES, SOURCES))
N = original.N


def traces(shape, source, noise, rho, scale, cache):
    """Change only background persistence and fault amplitude on paired draws."""
    camera, reference, true = cache[(shape, source, noise)]
    if rho == 0.7 and scale == 1:
        return camera, reference, true
    native = cache[(shape, "stable", noise)][2]
    modified = native.copy()
    if rho != 0.7:
        innovations = native[:, 1:] - 0.7 * native[:, :-1]
        for k in range(1, original.T):
            modified[:, k] = rho * modified[:, k-1] + innovations[:, k-1]
    drift_delta = (scale - 1) * (cache[(shape, "process", noise)][2] - native)
    physical_delta = modified - native
    inline_delta = modified - native
    if source in ("process", "cancel"):
        physical_delta = physical_delta + drift_delta
    if source in ("process", "sensor"):
        inline_delta = inline_delta + drift_delta
    return camera + inline_delta, reference + physical_delta, true + physical_delta


def save(name, header, rows):
    with (ROOT / name).open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    noise_factors = (0.5, 1.0, 2.0)
    cache = {(s,m,n):original.make_runs(s,m,n) for s,m,n in product(SHAPES,SOURCES,noise_factors)}
    summary = []
    for rho, noise, scale in product((0.4,0.7,0.9),noise_factors,(0.65,1.0,1.35)):
        batches = {c:traces(*c,noise,rho,scale,cache) for c in CELLS}
        for s in SHAPES:
            assert np.array_equal(batches[(s,"process")][0], batches[(s,"sensor")][0])
            assert np.array_equal(batches[(s,"cancel")][0], batches[(s,"stable")][0])
        for width in (20,10):
            data = np.array([[original.score(p,width,*batches[c]) for p in POLICIES] for c in CELLS])
            assert (data[:,:,0] + data[:,:,1] <= original.T).all()
            for p, policy in enumerate(POLICIES):
                false, miss = data[:,p,0].mean(), data[:,p,1].mean()
                summary.append((rho,noise * 0.012,scale,original.T//width,policy,false,miss,false+miss))
    save("generator_grid.csv",["rho","camera_sd_mm","amplitude_multiplier","checks","policy",
                            "false","miss","total"],summary)


if __name__ == "__main__":
    main()
