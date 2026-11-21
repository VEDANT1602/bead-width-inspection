# Carrying a caliper offset along a printed bead: five paths on one specimen

Vedant Thaker  
Independent Researcher, Jeffersonville, Indiana, USA  
vedant.thaker1602@gmail.com

Measurement report

**Research period (author-reported)** · August 2–13, 2026 &nbsp; | &nbsp; **Manuscript revised** · November 21, 2026

### Abstract

A local caliper reading can correct an optical width estimate only to the extent that the discrepancy persists along the bead. Five 200-mm paths on one published white-PLA specimen provide a retrospective test of that assumption. At 25 withheld stations, the mean absolute camera–caliper discrepancy was 0.0133 mm without a correction, 0.0128 mm with a fixed offset trained on the other paths, and 0.0256 mm with checks at the start and midpoint. Re-reading the printed figure under 54 extraction conventions reversed the ranking of the first two methods in four cases. A single check at 0, 20, 60 or 100 mm gave discrepancies of 0.0395, 0.0167, 0.0231 and 0.0147 mm, respectively, at the same 15 late stations. The startup discrepancy transferred poorly on this print. Repeated builds with an independently varied camera bias would be needed to estimate drift or prescribe an inspection interval.

## The ambiguity in a width trace

A width monitor gives the operator a choice when its reading departs from target. Adjusting flow responds to a physical width change. Recalibrating the camera responds to optical drift. For camera reading z = w + b + e, where w is physical width, b is optical bias and e is measurement noise, replacing (w, b) by (w + h, b − h) leaves every camera reading unchanged. Even a noiseless camera cannot identify an arbitrary pair of trajectories. An independent measurement r = w + u at one position anchors width there. Its value further along the path depends on how long the discrepancy persists.

This note tests that persistence using physical paths with two instruments. Its primary outcome is the absolute discrepancy between a corrected camera estimate and a caliper value that the correction rule has never seen. A separate fault simulation asks how assumptions about the source of a disturbance change a decision based on tolerance crossings.

## Five paths with paired instrument readings

Badarinath and Prabhu printed a 20-layer white-PLA wall with five 200-mm regions at 10, 20, 30, 40 and 50 mm/s [1]. Their last-layer camera observations were smoothed over 20 frames. They took local caliper measurements at 20-mm intervals and reported five measurements per neighborhood and 50 individual readings per path. Figure 10 shows a camera curve and a red caliper series with 11 plotted stations, including both endpoints. We used the 55 visible pairs as summaries. Their relationship to the individual readings at the endpoints cannot be recovered from the plot.

The extraction maps the top position axis and marked width ticks to physical units. It reads the center of each red marker and the darker of the two blue traces, interpolating where one ink covers the other. Plotted width values depend on line thickness, registration and the source smoothing. We report precision at the scale of the plot. The 0.0371-mm value in [1] is the maximum reported RMSE across color/material tests in Section 4.3 and Appendix A.2. It supplies a separate stress-test scale. A camera-only error standard deviation cannot be identified from that statistic.

In the extracted PDF the plot is rasterized. The width covered by one row of the 8× rendering is 0.00018 mm in the large panel and about 0.00084–0.00086 mm in the four small panels. Rendering resolution sets the coordinate increment. Ink thickness, overlapping traces and horizontal registration can contribute larger errors. We therefore repeated the extraction with three color cutoffs, three horizontal registrations (−0.25, 0, +0.25 PDF point), three locations across the blue ink thickness, and two center rules for the red caliper marks. Each of the 54 combinations refits the four training paths in each fold. They are deterministic reading choices applied to the same figure. Their range measures sensitivity to those choices and supplies no sampling interval for the original instruments.

## Held-out calibration and a decision available during printing

Each fold holds out one entire path. On the other four, the model treats the paired discrepancy d = z − r as a drifting offset b with additive noise. Between neighboring stations, b has zero-mean independent increments of variance Q. Observation variance is R. The first-station mean and variance come from the four training starts. Gaussian innovation likelihood across the four ordered paths estimates Q and R. The fitted drift standard deviation ranged from 0.010 to 0.020 mm per 20-mm step, and fitted observation standard deviation from 0.007 to 0.015 mm. These effective parameters include local instrument, registration and plotting effects. They cannot separate mechanical reference noise from camera noise.

At an acquired station the offset estimate m becomes m + P(d − m)/(P + R) and its variance becomes PR/(P + R), where P is the predicted variance [4]. Each subsequent 20-mm step adds Q to P. Both two-check policies acquire the 0-mm caliper value. The fixed schedule checks again at 100 mm. The magnitude schedule can check at 20, 60, 100 or 140 mm. It uses the first estimated width at least 0.05 mm from a rounded nominal width of 1.5 mm at 10 mm/s or 1.0 mm otherwise, and checks at 140 mm if no threshold crossing occurs. The threshold is an assigned action threshold. No reference candidate coincides with a score position.

All methods are evaluated at 40, 80, 120, 160 and 200 mm. Comparators are the smoothed camera as plotted, a constant offset equal to the training paths’ median paired discrepancy, and a first-position-only correction. Each plotted path has five scored stations. We report all five path outcomes and their equal-weight mean. The design supplies one specimen and no replication across printers.

## What happened after a correction

On the 20-mm/s path the initial camera read approximately 1.142 mm against a 1.060-mm caliper point. At 50 mm/s the discrepancy went the other way, about 0.935 versus 1.003 mm. On both paths the first correction carried a large discrepancy into positions where the two instruments subsequently agreed more closely. Timing a second check by magnitude beat the halfway check on the 20-mm/s path, lost on three paths and tied on one. At 10 mm/s the halfway check had the lowest discrepancy of all five methods.

Unrounded, the five halfway path means give 0.02559925 mm against the 25 hidden values. Each path contributed exactly five scores. Averaging the five path means after rounding each to three decimal places gives 0.0254 mm. Table 1 retains four decimals and the accompanying CSV records the score at every location.

Across the 54 readings, median station-wise spread in reconstructed camera width was 0.00222 mm. The maximum was 0.03288 mm at 30 mm/s and 120 mm. The corresponding median and maximum caliper-marker spreads were 0.00034 and 0.00225 mm. The camera-only mean absolute discrepancy ranged from 0.01297 to 0.01410 mm; the fixed offset ranged from 0.01280 to 0.01440 mm. The fixed offset had the smaller value in 50 extractions and the camera alone in four. Both were below the magnitude policy (0.01703–0.02219 mm) and halfway policy (0.02507–0.02855 mm) in every extraction. This exercise cannot recover the precision or synchronization of the original measurements.



| Speed (mm/s) | Camera | Fixed offset | Start only | Magnitude | Halfway |
| --- | --- | --- | --- | --- | --- |
| 10 | 0.0167 | 0.0177 | 0.0179 | 0.0187 | 0.0088 |
| 20 | 0.0097 | 0.0088 | 0.0680 | 0.0090 | 0.0493 |
| 30 | 0.0127 | 0.0136 | 0.0127 | 0.0133 | 0.0124 |
| 40 | 0.0153 | 0.0144 | 0.0349 | 0.0203 | 0.0203 |
| 50 | 0.0120 | 0.0095 | 0.0698 | 0.0452 | 0.0373 |
| Mean | 0.0133 | 0.0128 | 0.0407 | 0.0213 | 0.0256 |
Mean absolute discrepancy (mm) against five withheld caliper stations per speed. All five regions belong to one specimen.

## Does a mid-path check transfer better?

A second comparison holds both the number of checks and the evaluation locations fixed. For each held-out path the filter receives exactly one reading at 0, 20, 60 or 100 mm. Before that reading, it propagates the training-predicted prior mean and variance without seeing any held-out caliper value. The same three later stations at 120, 160 and 200 mm are scored in all cases (15 values overall). A start-only check gave 0.03949 mm mean absolute discrepancy. The values for 20, 60 and 100 mm were 0.01673, 0.02306 and 0.01466 mm. On the same 15 points the camera alone gave 0.01106 mm and the training offset 0.00962 mm. Moving the read away from the start reduced carry-forward error on average. Differences in the time from measurement to assessment, local width and path-specific disturbances remain entangled. These paths cannot identify a bead-start mechanism independently of registration or an instrument offset.

## What the paired observations leave unidentified

The physical specimen has no imposed optical faults or separately labeled process faults. To isolate those cases we also compared matched camera traces in a synthetic tolerance-alarm task. In each of 12 shape/source cells, 320 trajectories have 160 segments and eight independent reference opportunities, one per 20 segments. Process and sensor shifts can have identical camera readings. A true width departure of more than 0.05 mm defines a violation. False alarms and missed violations receive equal weight. The supplement compares periodic, magnitude, ambiguity, EWMA and two-sided CUSUM timing [2,3], each with a single-reading reset or a two-state filter [4].

With the nominal filter and equal-weight fault cells, magnitude timing averaged 6.800 false-plus-missed segments per build. Changing the presumed share of physical faults among visible shifts from 5% to 95%, while keeping stable and cancellation sources at 25% each, moved the lowest-count nominal-filter schedule from magnitude to EWMA. With a bias-heavy filter the corresponding lowest-count schedules were periodic and CUSUM. For an arithmetic check, nominal periodic reset gave (15,790 false + 20,115 missed)/3,840 = 9.35026. Periodic filtering at assigned camera SD 0.0371 mm gave (9,821 + 26,092)/3,840 = 9.35234. They round to the same number for different reasons.

For a line operator the unresolved issue is whether an observed discrepancy will recur at the next location. An independently varied camera offset, a measured drift time scale, and repeat builds would test that assumption. On this print the start correction carried too much local discrepancy forward. Near-equal errors for a fixed offset and the camera alone neither establish zero drift nor identify a drift time scale. The evidence covers width estimation on a single specimen. Production fault rates, alarm costs and reference latency require separate observation.

## Data and code availability

The accompanying supplement contains the attributed digitization, fold-specific model fits, scored stations, synthetic count audit, scripts and reference register. Badarinath and Prabhu’s measurements are available in Figure 10 of [1], under CC BY 4.0. The 54 re-extractions, individual station estimates and one-check interior comparisons are included. The source reports 50 mechanical readings per path; these are local repeats and cannot be treated as 50 independent positions. The original readings, repeat identifiers, raw camera frame widths and station alignment would permit a direct measurement-error analysis. The source states that data are available from its corresponding author. Code and source identification for the synthetic comparison are pinned at https://github.com/VEDANT1602/bead-width-inspection/tree/7d9d76dcde1ce0291224bcf7cf6a64756a2ef5d3 .

[Study files, software and source records](https://github.com/VEDANT1602/bead-width-inspection/tree/main/study)

## Author and disclosures

Vedant Thaker is the sole author and set the research question. OpenAI Codex assisted with digitizing the published camera and caliper observations, implementing and executing the estimators, re-reading the figure under alternative extraction conventions, checking the rounded error totals and drafting the analysis.

This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors. The author declares no competing interests.

## References

[1] R. Badarinath and V. Prabhu. Real-Time Sensing of Output Polymer Flow Temperature and Volumetric Flowrate in Fused Filament Fabrication Process. Materials 15(2), 618 (2022). <https://doi.org/10.3390/ma15020618>

[2] NIST/SEMATECH. e-Handbook of Statistical Methods, section 6.3.1.4, EWMA Control Charts. <https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc314.htm>

[3] NIST/SEMATECH. e-Handbook of Statistical Methods, section 6.3.1.3, Cusum Control Charts. <https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc313.htm>

[4] R. E. Kalman. A New Approach to Linear Filtering and Prediction Problems. Journal of Basic Engineering 82(1), 35–45 (1960). <https://doi.org/10.1115/1.3662552>
