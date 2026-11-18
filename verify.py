"""Recompute the nominal-noise inspection table from saved run-level counts."""
import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean


EXPECTED = {
    (8, "periodic"): ("4.11", "5.24", "9.35"),
    (8, "magnitude"): ("0.96", "7.64", "8.60"),
    (8, "ambiguity"): ("4.22", "5.23", "9.45"),
    (16, "periodic"): ("2.10", "3.68", "5.78"),
    (16, "magnitude"): ("0.61", "5.47", "6.07"),
    (16, "ambiguity"): ("1.42", "3.17", "4.59"),
}


def verify(directory):
    seen = set()
    groups = defaultdict(list)
    with (directory / "results.csv").open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            key = tuple(row[k] for k in ("shape", "mode", "camera_noise", "block", "policy", "run"))
            if key in seen:
                raise ValueError(f"Duplicate run {key}")
            seen.add(key)
            if float(row["camera_noise"]) == 0.012:
                checks = 160 // int(row["block"])
                groups[checks, row["policy"]].append((int(row["false_alarm"]), int(row["missed"])))
    if len(seen) != 34560 or groups.keys() != EXPECTED.keys():
        raise ValueError("Unexpected simulation grid")
    for key, expected in EXPECTED.items():
        values = groups[key]
        if len(values) != 3840:
            raise ValueError(f"{key} has {len(values)} runs instead of 3840")
        false_alarm, missed = map(mean, zip(*values))
        observed = tuple(f"{v:.2f}" for v in (false_alarm, missed, false_alarm + missed))
        if observed != expected:
            raise ValueError(f"{key} gave {observed}, expected {expected}")
    print("Verified 34,560 unique runs and all six nominal-noise table rows.")


if __name__ == "__main__":
    verify(Path(__file__).resolve().parent)
