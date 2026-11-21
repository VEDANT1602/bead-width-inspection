"""Recompute paired inspection schedules. Requires Python 3 and NumPy."""
import csv
from collections import defaultdict
from pathlib import Path

import numpy as np


T, N, TOL = 160, 320, 0.05
ROOT = Path(__file__).resolve().parent
POLICIES = ("periodic", "magnitude", "ambiguity")


def make_runs(shape, mode, noise_multiplier=1):
    # Shared draws across all etiologies make the camera-only witness exact.
    rng = np.random.default_rng(90217)
    onset = rng.integers(24, 87, size=N)
    sign = rng.choice([-1, 1], N)
    amplitude = rng.uniform(0.07, 0.115, size=N) * sign
    age = np.arange(T) - onset[:, None]
    if shape == "step":
        waveform = (age >= 0).astype(float)
    elif shape == "ramp":
        waveform = np.clip((age + 1) / 24, 0, 1)
    else:
        waveform = ((age >= 0) & (age < 14)).astype(float) - 0.75 * (age >= 42)
    signal = waveform * amplitude[:, None]
    native = rng.normal(0, 0.005, (N, T))
    for t in range(1, T):
        native[:, t] += 0.7 * native[:, t - 1]
    true = native.copy()
    if mode in ("process", "cancel"):
        true += signal
    camera = native + rng.normal(0, 0.012 * noise_multiplier, (N, T))
    if mode in ("process", "sensor"):
        camera += signal
    reference = true + rng.normal(0, 0.006, (N, T))
    return camera, reference, true


def score(policy, width, camera, ref, true):
    bias = np.zeros(N)
    ewma = np.zeros(N)
    last = np.full(N, -1)
    observed = np.zeros((N, T), bool)
    alarms = np.zeros_like(observed)
    for t in range(T):
        ewma += 0.45 * (camera[:, t] - ewma)
        pred = ewma - bias
        available = last < t - t % width
        if policy == "periodic":
            check = np.full(N, t % width == (width - 1) // 2)
        else:
            # The ambiguity band represents an assumed drift allowance since
            # the previous inspection; it is not a calibrated probability.
            radius = 0.01 + 0.002 * (t - last)
            trigger = np.abs(pred) >= TOL if policy == "magnitude" else np.abs(np.abs(pred) - TOL) <= radius
            check = available & (trigger | (t % width == width - 1))
        bias[check] = camera[check, t] - ref[check, t]
        last[check] = t
        observed[:, t] = check
        alarms[:, t] = np.abs(ewma - bias) > TOL
    assert (observed.sum(axis=1) == T // width).all()
    out = np.abs(true) > TOL
    fp = (alarms & ~out).sum(axis=1)
    fn = (~alarms & out).sum(axis=1)
    delays = np.full(N, -1)
    for i in np.flatnonzero(out.any(axis=1)):
        start = np.flatnonzero(out[i])[0]
        detected = np.flatnonzero((out[i] & alarms[i])[start:start + 20])
        delays[i] = detected[0] if len(detected) else 20
    return fp, fn, out.sum(axis=1), delays


def main():
    fields = "shape mode camera_noise block policy run false_alarm missed true_out delay20".split()
    with (ROOT / "results.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        for shape in ("step", "ramp", "reversal"):
            assert np.array_equal(make_runs(shape, "process")[0], make_runs(shape, "sensor")[0])
            assert np.array_equal(make_runs(shape, "cancel")[0], make_runs(shape, "stable")[0])
            for mode in ("stable", "process", "sensor", "cancel"):
                for noise, width in ((1, 20), (1, 10), (2, 20)):
                    args = make_runs(shape, mode, noise)
                    for policy in POLICIES:
                        count = score(policy, width, *args)
                        for i, values in enumerate(zip(*count)):
                            writer.writerow([shape, mode, 0.012 * noise, width, policy, i, *values])
    # Give each shape, cause and paired run equal weight, as in Table 1.
    counts = defaultdict(list)
    paired = defaultdict(lambda: defaultdict(list))
    with (ROOT / "results.csv").open(newline="") as f:
        for row in csv.DictReader(f):
            key = (float(row["camera_noise"]), int(row["block"]), row["policy"])
            errors = [int(row["false_alarm"]), int(row["missed"])]
            counts[key].append(errors)
            if key[:2] == (.012, 20):
                paired[int(row["run"])][row["policy"]].append(sum(errors))
    print("Camera SD, segments per check, policy, false alarms, misses, total:")
    for key, values in sorted(counts.items()):
        fp, fn = np.mean(values, axis=0)
        print(*key, round(fp, 3), round(fn, 3), round(fp + fn, 3))
    for method in ("magnitude", "ambiguity"):
        delta = [np.mean(p[method]) - np.mean(p["periodic"]) for p in paired.values()]
        se = np.std(delta, ddof=1) / np.sqrt(N)
        print(method, "minus periodic, mean and approximate 95% Monte Carlo interval:",
              np.round([np.mean(delta), np.mean(delta) - 1.96*se, np.mean(delta) + 1.96*se], 3))


if __name__ == "__main__":
    main()
