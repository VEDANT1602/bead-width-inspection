# When does a caliper check improve a camera estimate of extrusion width?

Vedant Thaker  
Independent Researcher, Jeffersonville, Indiana, USA  
vedant.thaker1602@gmail.com

21 November 2026

### Abstract

An extrusion camera can report the same width change after a physical disturbance or a shift in its own calibration. A caliper can distinguish the two, but applying its reading as an offset can also worsen later estimates. We tested that decision on five 200-mm paths from one published white-PLA print. We digitized the paired camera and caliper traces, fitted a discrepancy model on four speeds, and scored the fifth only at positions reserved for evaluation. Across 25 such positions, a fixed offset learned on the other paths gave a mean absolute discrepancy of 0.013 mm. Applying a first-position check and taking one more check at a width excursion gave 0.021 mm. Taking the second check halfway along the path gave 0.026 mm. A transient at the first reading made an early correction especially costly on two paths. These measurements support testing whether an offset persists before carrying it forward. They contain too few independent builds to establish an industrial inspection interval.

## The ambiguity in a width trace

A width monitor gives the operator a choice when its reading departs from target. Adjusting flow responds to a physical width change. Recalibrating the camera responds to optical drift. For camera reading z = w + b + e, where w is physical width, b is optical bias and e is measurement noise, replacing (w, b) by (w + h, b − h) leaves every camera reading unchanged. Even a noiseless camera cannot identify an arbitrary pair of trajectories. An independent measurement r = w + u at one position anchors width there. Its value further along the path depends on how long the discrepancy persists.

This note tests that persistence using physical paths with two instruments. Its primary outcome is the absolute discrepancy between a corrected camera estimate and a caliper value that the correction rule has never seen. A separate fault simulation asks how assumptions about the source of a disturbance change a decision based on tolerance crossings.

## Five paths with paired instrument readings

Badarinath and Prabhu printed a 20-layer white-PLA wall with five 200-mm regions at 10, 20, 30, 40 and 50 mm/s [1]. Their last-layer camera observations were smoothed over 20 frames. They took local caliper measurements at 20-mm intervals and reported five measurements per neighborhood and 50 individual readings per path. Figure 10 shows a camera curve and a red caliper series with 11 plotted stations, including both endpoints. We used the 55 visible pairs as summaries. Their relationship to the individual readings at the endpoints cannot be recovered from the plot.

The extraction maps the top position axis and marked width ticks to physical units. It reads the center of each red marker and the darker of the two blue traces, interpolating where one ink covers the other. Plotted width values depend on line thickness, registration and the source smoothing. We report precision at the scale of the plot. The 0.0371-mm value in [1] is the maximum reported RMSE across color/material tests in Section 4.3 and Appendix A.2. It supplies a separate stress-test scale. A camera-only error standard deviation cannot be identified from that statistic.

## Held-out calibration and a decision available during printing

Each fold holds out one entire path. On the other four, the model treats the paired discrepancy d = z − r as a drifting offset b with additive noise. Between neighboring stations, b has zero-mean independent increments of variance Q. Observation variance is R. The first-station mean and variance come from the four training starts. Gaussian innovation likelihood across the four ordered paths estimates Q and R. The fitted drift standard deviation ranged from 0.010 to 0.020 mm per 20-mm step, and fitted observation standard deviation from 0.007 to 0.015 mm. These effective parameters include local instrument, registration and plotting effects. They cannot separate mechanical reference noise from camera noise.

At an acquired station the offset estimate m becomes m + P(d − m)/(P + R) and its variance becomes PR/(P + R), where P is the predicted variance [4]. Each subsequent 20-mm step adds Q to P. Both two-check policies acquire the 0-mm caliper value. The fixed schedule checks again at 100 mm. The magnitude schedule can check at 20, 60, 100 or 140 mm. It uses the first estimated width at least 0.05 mm from a rounded nominal width of 1.5 mm at 10 mm/s or 1.0 mm otherwise, and checks at 140 mm if no threshold crossing occurs. The threshold is an assigned action threshold. No reference candidate coincides with a score position.

All methods are evaluated at 40, 80, 120, 160 and 200 mm. Comparators are the smoothed camera as plotted, a constant offset equal to the training paths’ median paired discrepancy, and a first-position-only correction. Each plotted path has five scored stations. We report all five path outcomes and their equal-weight mean. The design supplies one specimen and no replication across printers.

## What happened after a correction

On the 20-mm/s path the initial camera read approximately 1.142 mm against a 1.060-mm caliper point. At 50 mm/s the discrepancy went the other way, about 0.935 versus 1.003 mm. On both paths the first correction carried a large discrepancy into positions where the two instruments subsequently agreed more closely. Timing a second check by magnitude beat the halfway check on the 20-mm/s path, lost on three paths and tied on one. At 10 mm/s the halfway check had the lowest discrepancy of all five methods.

Across all paths the fixed training offset and the smoothed camera differed by less than one micrometre in mean absolute discrepancy. The figures do not resolve such a small ordering between them. Dropping the 40-mm station on the 20-mm/s path, where overprinting required the widest interpolation, gave mean discrepancies of 0.0130, 0.0137, 0.0219 and 0.0234 mm for fixed training offset, camera, magnitude and halfway respectively. Crossing five action thresholds from 0.025 to 0.100 mm with three process variances from one-quarter to four times fitted Q gave magnitude-policy errors of 0.019–0.027 mm.


| Speed (mm/s) | Camera | Fixed offset | Start only | Magnitude | Halfway |
| --- | --- | --- | --- | --- | --- |
| 10 | 0.017 | 0.018 | 0.018 | 0.019 | 0.009 |
| 20 | 0.010 | 0.009 | 0.068 | 0.009 | 0.049 |
| 30 | 0.013 | 0.014 | 0.013 | 0.013 | 0.012 |
| 40 | 0.015 | 0.014 | 0.035 | 0.020 | 0.020 |
| 50 | 0.012 | 0.010 | 0.070 | 0.045 | 0.037 |
| Mean | 0.013 | 0.013 | 0.041 | 0.021 | 0.026 |
Mean absolute discrepancy (mm) against five withheld caliper stations per speed. All five regions belong to one specimen.

## What the paired observations leave unidentified

The physical specimen has no imposed optical faults or separately labeled process faults. To isolate those cases we also compared matched camera traces in a synthetic tolerance-alarm task. In each of 12 shape/source cells, 320 trajectories have 160 segments and eight independent reference opportunities, one per 20 segments. Process and sensor shifts can have identical camera readings. A true width departure of more than 0.05 mm defines a violation. False alarms and missed violations receive equal weight. The supplement compares periodic, magnitude, ambiguity, EWMA and two-sided CUSUM timing [2,3], each with a single-reading reset or a two-state filter [4].

With the nominal filter and equal-weight fault cells, magnitude timing averaged 6.800 false-plus-missed segments per build. Changing the presumed share of physical faults among visible shifts from 5% to 95%, while keeping stable and cancellation sources at 25% each, moved the lowest-count nominal-filter schedule from magnitude to EWMA. With a bias-heavy filter the corresponding lowest-count schedules were periodic and CUSUM. For an arithmetic check, nominal periodic reset gave (15,790 false + 20,115 missed)/3,840 = 9.35026. Periodic filtering at assigned camera SD 0.0371 mm gave (9,821 + 26,092)/3,840 = 9.35234. They round to the same number for different reasons.

For a line operator the unresolved issue is whether an observed discrepancy will recur at the next location. An independently varied camera offset, a measured drift time scale, and repeat builds would test that assumption. On the available print, fitting a fixed offset transferred better on average than carrying a startup check forward and updating it once. The evidence covers width estimation on a single specimen. Production fault rates, alarm costs and reference latency require separate observation.

## Data and code availability

The accompanying supplement contains the attributed digitization, fold-specific model fits, scored stations, synthetic count audit, scripts and reference register. Badarinath and Prabhu’s measurements are available in Figure 10 of [1], under CC BY 4.0. Code and source identification for the synthetic comparison are pinned at https://github.com/VEDANT1602/bead-width-inspection/tree/7d9d76dcde1ce0291224bcf7cf6a64756a2ef5d3 .

[Study files, software and source records](https://github.com/VEDANT1602/bead-width-inspection/tree/main/study)

## Author and disclosures

Vedant Thaker is the sole author and set the research question. OpenAI Codex assisted with digitizing the published camera and caliper observations, implementing the estimators, checking the rounded error totals and drafting the analysis.

This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors. The author declares no competing interests.

## References

[1] R. Badarinath and V. Prabhu. Real-Time Sensing of Output Polymer Flow Temperature and Volumetric Flowrate in Fused Filament Fabrication Process. Materials 15(2), 618 (2022). <https://doi.org/10.3390/ma15020618>

[2] NIST/SEMATECH. e-Handbook of Statistical Methods, section 6.3.1.4, EWMA Control Charts. <https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc314.htm>

[3] NIST/SEMATECH. e-Handbook of Statistical Methods, section 6.3.1.3, Cusum Control Charts. <https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc313.htm>

[4] R. E. Kalman. A New Approach to Linear Filtering and Prediction Problems. Journal of Basic Engineering 82(1), 35–45 (1960). <https://doi.org/10.1115/1.3662552>
