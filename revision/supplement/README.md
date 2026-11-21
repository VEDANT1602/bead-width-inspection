# Equal-budget bead-width monitoring

The original generator and verifier are verbatim copies of the [pinned public study](https://github.com/VEDANT1602/bead-width-inspection/tree/3cb566931328d94fb0a33af65f63c73402ac453b). The programs generate all study inputs locally. The public baseline used Python 3.11.9/NumPy 1.26.0. All new comparisons below used CPython 3.12.14 and NumPy 2.3.5 on Linux x86-64. The plot used Matplotlib 3.10.8. The study’s archived lock files include wheels and transitive dependencies. Use a separate environment for each lock.

From this directory run:

```sh
python -m pip install --require-hashes -r revision-cp312-linux-x86_64.lock
python run.py
python verify.py
python compare.py
python generator_grid.py
python validate.py
python plot.py
```

For other platforms version pins for the new analysis are in requirements.txt. Results.csv contains the original 34,560 run-condition records. Its regenerated SHA-256 is 5a594e0dc8df8ddcedd8ddc93dae29b996209abbb369cb28ad8d87e4f5d98747.

* comparator_sensitivity.csv — 270 rows across 27 fixed settings, five schedulers and two alarm estimators. Eight checks per trace unless width=10 (16 checks). Each setting varies one parameter relative to nominal. All delta columns use its own periodic/reset control, except the final column comparing estimators on an identical inspection schedule.
* nominal_runs.csv.gz — 38,400 individually matched records. The key is fault shape, source, scheduler, estimator and paired run index. Rows with the same run index share generator noise across all comparisons.
* cell_effects.csv — means and absolute paired differences in false positives, missed segments and their sum within each of 12 design cells, each retaining 320 run indices. source_effects.png averages the three shapes within each source.
* generator_grid.csv — retained three-rule, single-check bias-reset comparison over 54 Cartesian settings. The expanded chart and filtering comparisons are in comparator_sensitivity.csv.
* validate.py — tests that masking all uninspected references gives exactly the same schedules and decisions, verifies the sequential Kalman estimate against batch Gaussian conditioning around every decision boundary on an eight-segment fixture, and recomputes score aggregates from the saved run-level CSV. compare.py directly checks every one of the 11,520 original nominal per-run false/miss pairs across the three legacy schedulers and validates covariance positivity and one check per block.
* parameter-ledger.md — numeric scales, origins, alternatives tested and unswept limitations.

No physical printer files are embedded. The 0.0371-mm camera noise case uses a published aggregate error as a magnitude stress test of this generator. It is not imputed field data.
