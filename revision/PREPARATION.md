# Preparation record

Scheduling independent width checks when extrusion drift and camera bias produce identical readings

Vedant Thaker · 21 November 2026

## Original work

Vedant Thaker is the sole author. He designed the original bead-width monitoring experiment, wrote its manuscript, developed its original software, and requested the comparisons and checks reported in this revision.

The author reports that the research project began on 2 August 2026. The previous versions and the new revision represent different stages of the work.

## Revision activities

OpenAI Codex assisted with the identifiability derivation, implementation and execution of the matched inspection and Kalman comparisons, sensitivity calculations, and verification of the published measurement scale, as well as literature checks and preparation of the revised text. The author set the research question and requested the revision.

## Computational checks

The original run regenerated the archived CSV byte for byte. All 11,520 nominal per-run false/miss pairs from the three original schedules matched the expanded implementation. The new code checked one inspection in every block, both exact camera-trace identities and positive-semidefinite propagated covariances. Replacing unobserved reference entries with missing values left every nominal decision unchanged. A batch Gaussian-conditioning calculation verified the sequential Kalman decisions around each estimated width on a separate test fixture. The supplement contains 38,400 nominal run records and 270 means covering 27 parameter settings, five schedules and two estimators.

## Data and version records

The original simulation, verifier and 34,560-row results.csv are available in the baseline repository. The accompanying supplement supplies the expanded comparison, run-level data, parameter ledger and reproducible environments. From the supplement directory, run python compare.py, python generator_grid.py, python validate.py and python plot.py after installing the revision lock. The physical study [1] provides published summary measurements only for this comparison.

[Original pinned software](https://github.com/VEDANT1602/bead-width-inspection/tree/3cb566931328d94fb0a33af65f63c73402ac453b) · [Revision code and data](https://github.com/VEDANT1602/bead-width-inspection/tree/main/revision/supplement)

The reported checks are computational. No independent personal rerun or line-by-line review of these revisions by the author is asserted here.
