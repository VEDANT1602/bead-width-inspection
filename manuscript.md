# Carrying a caliper offset along a printed bead: five paths on one specimen

Vedant Thaker  
Independent Researcher, Jeffersonville, Indiana, USA  
vedant.thaker1602@gmail.com

Measurement report · November 24, 2026

### Abstract

A caliper check at the start of a printed bead helps downstream only if the local camera–caliper discrepancy persists. This report compares four possible check positions on five paths digitized from a published figure of one white-PLA specimen. Each rule received one caliper reading. All were scored against the same 15 downstream stations. Moving the check from 0 to 100 mm reduced mean absolute discrepancy from 0.0395 to 0.0147 mm. Leaving the camera uncorrected gave 0.0111 mm, and a fixed offset learned from the other four paths gave 0.0096 mm. Both comparisons survived 54 ways of reading the figure. A start or midpoint correction therefore carried more local error forward than it removed on this specimen.

## Width and camera bias give the same optical signal

An apparent increase in extrusion width can have two causes that call for different actions. Adjusting flow changes the bead itself. Correcting camera bias changes the reading. In the observation equation z = w + b + e, replacing physical width w and bias b by w + h and b − h leaves the reading z unchanged for any trajectory h. A caliper anchors width at one location. Whether its correction transfers to a later location is an empirical question.

## Published specimen and calibration rule

Badarinath and Prabhu printed a 20-layer white-PLA wall with five 200-mm regions at speeds of 10, 20, 30, 40 and 50 mm/s [1]. They smoothed the last-layer optical measurements over 20 frames and took caliper measurements near stations 20 mm apart. The investigators report five local repeats and 50 readings per path. Figure 10 shows 11 caliper marks per path including both ends. The analysis pairs these 55 marks with the optical curve at the same plotted positions. The relationship between the endpoint marks and individual caliper readings is unavailable.

Each fold holds out one complete path. On the other four paths, the ordered discrepancy d = z − r between optical reading z and caliper reading r supplies a starting mean m and variance P from the first stations. The offset follows a random walk with increment variance Q per 20-mm step and observation variance R. A Gaussian innovation likelihood estimates Q and R from the training paths. The fitted standard deviations were 0.010–0.020 mm for drift per step and 0.007–0.015 mm for observation noise. These estimates also absorb registration and digitization errors.

For a check j steps into the held-out path, the predicted variance is V = P + jQ. The rule observes the local discrepancy once and uses the offset m + V(d − m)/(V + R) for all later estimates [4]. Its four possible acquisition sites are 0, 20, 60 and 100 mm. The camera baseline uses no offset. The fixed-offset baseline subtracts the median of all paired discrepancies on the four training paths. Neither baseline acquires a check on the held-out path. Each estimate is compared with the caliper marks at 120, 160 and 200 mm. The mean absolute discrepancy gives equal weight to all five paths.

## The start discrepancy did not carry to the end of the bead

At 20 mm/s the start camera reading exceeded the plotted caliper value by about 0.082 mm. At 50 mm/s it fell short by about 0.068 mm. In both cases the instruments agreed more closely farther along the path. On the 15 common test stations, even the best single check by average discrepancy added 0.0036 mm compared with leaving the camera uncorrected. Results varied by path. The 100-mm check beat the uncorrected camera on three of five paths and the fixed offset on two.

| Held-out path correction | Mean absolute discrepancy (mm) | Range over figure extractions (mm) |
| --- | --- | --- |
| Camera alone | 0.0111 | 0.0108–0.0124 |
| Offset from four training paths | 0.0096 | 0.0094–0.0117 |
| One check at 0 mm | 0.0395 | 0.0355–0.0404 |
| One check at 20 mm | 0.0167 | 0.0155–0.0200 |
| One check at 60 mm | 0.0231 | 0.0216–0.0236 |
| One check at 100 mm | 0.0147 | 0.0142–0.0231 |

Table 1. Errors against the same 15 downstream caliper marks. The middle column uses the central extraction convention. The ranges summarize 54 readings of one figure.

The extraction aligns the marked axes, locates each red caliper marker and interpolates the darker camera trace across occlusions. Three optical color cutoffs, three horizontal alignments (−0.25, 0 and +0.25 PDF point), three positions across the blue ink and two caliper-marker center rules give 54 settings. Under each setting, the model for each held-out path is refitted on the other four paths. For each setting separately, every single-check rule had a higher mean downstream discrepancy than either baseline. Moving the check from 0 to 100 mm lowered discrepancy by 0.0154–0.0249 mm across these settings. These ranges describe sensitivity to reading the plot. Repeated digitizations do not add specimens.

## Why the comparison depends on the scored stations

A second analysis includes earlier positions and allows a second check. Each path is scored at 40, 80, 120, 160 and 200 mm. A fixed schedule checks at 0 and 100 mm. A magnitude schedule checks at 0 mm and again at the first eligible position (20, 60, 100 or 140 mm) at which the estimated width differs by at least 0.05 mm from 1.5 mm for the slowest path or 1.0 mm for the others. It uses 140 mm if there is no crossing. The threshold and nominal widths are assigned for this comparison.

| Speed (mm/s) | Camera | Fixed offset | Start only | Magnitude | Start and midpoint |
| --- | --- | --- | --- | --- | --- |
| 10 | 0.0167 | 0.0177 | 0.0179 | 0.0187 | 0.0088 |
| 20 | 0.0097 | 0.0088 | 0.0680 | 0.0090 | 0.0493 |
| 30 | 0.0127 | 0.0136 | 0.0127 | 0.0133 | 0.0124 |
| 40 | 0.0153 | 0.0144 | 0.0349 | 0.0203 | 0.0203 |
| 50 | 0.0120 | 0.0095 | 0.0698 | 0.0452 | 0.0373 |
| Mean | 0.0133 | 0.0128 | 0.0407 | 0.0213 | 0.0256 |

Table 2. Mean absolute discrepancy in mm for five unseen stations per path. All five regions belong to one specimen.

On these 25 stations, the two baselines trade places in four of the 54 extractions. Their nominal 0.0005-mm separation does not support choosing one over the other. A fixed offset and the uncorrected camera each outperformed both two-check policies under every extraction. The source study reports a maximum RMSE of 0.0371 mm across separate color and material tests [1, §4.3]. That figure cannot identify the measurement uncertainty of the 25 plotted station pairs.

Speed, location and specimen history vary together in these five regions. The plot cannot distinguish a startup transient from a local measurement or alignment error. To estimate an inspection interval, an experiment would need repeated prints with aligned raw instrument readings and independently varied camera offsets.

## Data and code availability

The study files include the 55 digitized pairs, fitting and extraction scripts, and downstream errors under all 54 conventions. The source figure is Figure 10 of Badarinath and Prabhu [1], licensed CC BY 4.0. The article offers raw measurements on request. The source authors were asked for the caliper repeats, station coordinates and matching optical series on November 21, 2026. Only plotted summaries entered the present analysis.

The supplement retains a separate simulation comparing EWMA, CUSUM and filter-based alarm timing [2–4]. Its fault mix, noise and costs are assigned. No simulated observation enters Tables 1 or 2. The numerical tables and run instructions are in the accompanying study directory and the [public study repository](https://github.com/VEDANT1602/bead-width-inspection/tree/main/study).

## Author and disclosures

Vedant Thaker is the sole author. He posed the reference-timing question and identified a bead-start transient as a possible explanation to test against checks farther along the path. OpenAI Codex assisted with digitizing the published camera and caliper observations, implementing and executing the estimators, re-reading the figure under alternative extraction conventions, checking the rounded error totals and drafting the analysis.

This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors. The author declares no competing interests.

## References

[1] R. Badarinath and V. Prabhu. Real-Time Sensing of Output Polymer Flow Temperature and Volumetric Flowrate in Fused Filament Fabrication Process. Materials 15(2), 618 (2022). <https://doi.org/10.3390/ma15020618>

[2] NIST/SEMATECH. e-Handbook of Statistical Methods, section 6.3.1.4, EWMA Control Charts. <https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc314.htm>

[3] NIST/SEMATECH. e-Handbook of Statistical Methods, section 6.3.1.3, Cusum Control Charts. <https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc313.htm>

[4] R. E. Kalman. A New Approach to Linear Filtering and Prediction Problems. Journal of Basic Engineering 82(1), 35–45 (1960). <https://doi.org/10.1115/1.3662552>
