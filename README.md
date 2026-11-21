# When does a caliper check improve a camera estimate of extrusion width?

Technical report by Vedant Thaker, Independent Researcher, Jeffersonville, Indiana. Correspondence: vedant.thaker1602@gmail.com.

An extrusion camera can report the same width change after a physical disturbance or a shift in its own calibration. A caliper can distinguish the two, but applying its reading as an offset can also worsen later estimates. We tested that decision on five 200-mm paths from one published white-PLA print. We digitized the paired camera and caliper traces, fitted a discrepancy model on four speeds, and scored the fifth only at positions reserved for evaluation. Across 25 such positions, a fixed offset learned on the other paths gave a mean absolute discrepancy of 0.013 mm. Applying a first-position check and taking one more check at a width excursion gave 0.021 mm. Taking the second check halfway along the path gave 0.026 mm. A transient at the first reading made an early correction especially costly on two paths. These measurements support testing whether an offset persists before carrying it forward. They contain too few independent builds to establish an industrial inspection interval.

- [Read the paper](manuscript.pdf)
- [Read the plain-text manuscript](manuscript.md)
- [Reproduce the analysis and inspect the source and data records](study/README.md)
- [Software license](LICENSE) and [third-party terms](LICENSING.md)
- [Preparation record](study/PREPARATION.md)
- [Previous manuscript and supplements](https://github.com/VEDANT1602/bead-width-inspection/tree/7d9d76dcde1ce0291224bcf7cf6a64756a2ef5d3)
