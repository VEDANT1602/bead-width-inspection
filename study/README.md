# Independent extrusion-width checks

The primary data are 55 pairs digitized from the smoothed vision curve and caliper symbols in Figure 10 of Badarinath & Prabhu (2022). The five paths belong to one printed specimen. Users can run the numerical analysis from the included CSV without the publisher PDF.

## Reproduce

Tested on x86-64 Linux with Python 3.12.14. Install the pinned dependencies in requirements.txt. Run from this directory.

```sh
python scripts/analyze.py
python scripts/sensitivity.py
python scripts/verify.py
```

Optional extraction of the input CSV from the primary figure:

```sh
curl -L --fail https://mdpi-res.com/d_attachment/materials/materials-15-00618/article_deploy/materials-15-00618-v2.pdf -o /tmp/materials-15-00618-v2.pdf
python scripts/digitize.py /tmp/materials-15-00618-v2.pdf
```

The extraction checks the exact SHA-256 and reports horizontal interpolation spans; the returned decimal places encode the extraction for reproducibility, not instrument precision. The one observation with a span of 12.75 reference-render pixels is the 20-mm/s path at 40 mm. All other spans are 5.5 pixels or less. Excluding that held-out station leaves 24 scores per policy. This exclusion changes the score set only; training fits keep all visible training pairs.

The data tables distinguish fitted parameters (`field_fits.csv`), reads (`field_check_positions.csv`), withheld score sites (`field_scores.csv`), threshold and process-variance sensitivity (`field_sensitivity.csv`), and synthetic stress tests (`integer_audit.csv`, `prior_prevalence.csv`). The initial-only, magnitude and periodic rules all see the start point. The camera and training-offset rules acquire zero points. The population in the synthetic prevalence sweep allocates 25% each to stable and cancellation, and divides the remaining half between sensor and process shifts. No held-out speed was used for fitting its discrepancy parameters.

## Source rights and attribution

The data in outputs/plotted_widths.csv were digitized by the present analysis from Figure 10 in Rakshith Badarinath and Vittaldas Prabhu, “Real-Time Sensing of Output Polymer Flow Temperature and Volumetric Flowrate in Fused Filament Fabrication Process,” Materials 15, 618 (2022). © 2022 the original authors, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). [Article and source figure](https://doi.org/10.3390/ma15020618). We mapped pixels to millimetres, isolated colored lines, and interpolated crossings. The original figure, paper and videos are not redistributed. Preserve this attribution with the data and derived scores. The upstream authors did not endorse this analysis.

The scripts in reference/ are from the MIT-licensed [Vedant Thaker research repository](https://github.com/VEDANT1602/bead-width-inspection/tree/7d9d76dcde1ce0291224bcf7cf6a64756a2ef5d3). Additional analysis code uses the same MIT license. The accompanying license applies to the author’s code. See references.md for the source register.

## Figure-reading sensitivity and interior checks

Run `python scripts/figure_sensitivity.py /path/to/materials-15-00618-v2.pdf` after downloading the identified article above. The script requires the original PDF hash and verifies the central camera trace against the bundled digitization. It saves the 54 repeated fits, all corresponding digitized station values, and the paired one-check interior scores under `outputs`. Width spans and score ranges in the paper are across deliberately varied analysis conventions on one raster. A half-offset of 0.25 PDF point is two output pixels in the 8x render. The 100-mm, 60-mm, 20-mm and 0-mm checks each have exactly 15 common evaluation stations and no withheld reference is observed before its chosen acquisition.

Section 4.3 of Badarinath and Prabhu reports five mechanical readings in the vicinity of each interval, 50 per path. These are local repeats rather than 50 evenly spaced observations. The source identifies V. Prabhu as corresponding author; it makes underlying data available on request. The aggregate figures cannot recover station IDs, repeat variability or camera timestamps.
