# Preliminary Wind Resource Assessment of Dhaka, Bangladesh Using NREL Wind Toolkit Data

## 1. Introduction

Wind resource assessment is an important first step in evaluating the potential application of wind energy at a particular location. Before detailed project development, the temporal variability, magnitude and directional characteristics of the wind resource need to be understood.

This pilot project investigates the wind characteristics of Dhaka, Bangladesh using hourly wind data at 100 m height for the year 2017. The analysis was performed in Python using the NREL Wind Toolkit dataset. The project was developed as an introductory wind-energy data-analysis exercise, with emphasis on understanding the relationship between meteorological wind conditions and basic wind-energy indicators.

The analysis includes basic quality control, wind-speed statistics, temporal variability, wind-direction characteristics, Weibull distribution fitting, wind power density estimation and an illustrative turbine energy calculation.

This assessment is intended as a preliminary resource-characterization exercise rather than a bankable wind-farm feasibility study.

---

## 2. Objectives

The main objectives of the project were:

1. To examine hourly wind-speed conditions at 100 m over Dhaka during 2017.
2. To characterize the temporal variability of the wind resource.
3. To investigate the prevailing wind-direction characteristics.
4. To fit a Weibull distribution to the observed wind-speed data.
5. To estimate wind power density at 100 m.
6. To demonstrate how a simplified turbine power curve can be used to estimate annual energy production and capacity factor.
7. To develop a reproducible Python workflow for basic wind-resource analysis.

---

## 3. Study Area and Data

### 3.1 Study location

The analysis represents a point location near Dhaka, Bangladesh, at approximately:

- Latitude: 23.803° N
- Longitude: 90.421° E
- Wind-data height: 100 m
- Analysis year: 2017

The dataset contains hourly wind speed, wind direction and air temperature at 100 m.

### 3.2 NREL Wind Toolkit

The meteorological data were obtained from the NREL Wind Toolkit. The downloaded CSV contains site information followed by the hourly observations. The hourly dataset provides:

- Wind speed at 100 m (m/s)
- Wind direction at 100 m (degrees)
- Air temperature at 100 m (°C)
- Year, month, day and hour information

The raw file contains 8,760 hourly observations for 2017. During the cleaning process, observations with missing values in the principal meteorological variables were removed, resulting in 8,712 valid observations for the main analysis.

The analysis was performed using Python with pandas, NumPy, Matplotlib, SciPy and Windrose.

---

## 4. Methodology

### 4.1 Data preparation and quality control

The raw NREL file contains a site-information row followed by the actual variable names and hourly observations. The metadata row was excluded before loading the meteorological observations.

A datetime index was constructed from the year, month, day and hour fields. The meteorological variables were converted to numerical values and observations containing missing values were removed.

Basic descriptive statistics were then calculated for wind speed, wind direction, air temperature and wind power density.

---

### 4.2 Wind-speed statistics

The mean, standard deviation, minimum, maximum and percentile statistics were calculated to describe the wind-speed distribution.

For the available observations, the mean wind speed at 100 m was:

**3.91 m/s**

with a standard deviation of:

**2.20 m/s**

The minimum and maximum recorded wind speeds were approximately 0.01 m/s and 32.54 m/s, respectively.

---

### 4.3 Wind Power Density

Wind Power Density (WPD) was calculated from the instantaneous wind-speed observations using:

\[
WPD = \frac{1}{2}\rho V^3
\]

where:

- \(WPD\) = wind power density (W/m²)
- \(\rho\) = air density (kg/m³)
- \(V\) = wind speed (m/s)

A constant air density of 1.225 kg/m³ was used for this introductory assessment.

The mean WPD calculated from the hourly observations was:

**81.76 W/m²**

Because wind power varies with the cube of wind speed, high-wind events contribute disproportionately to the average power density.

---

### 4.4 Temporal variability

Monthly and seasonal averages were calculated to investigate the seasonal variability of the wind resource.

The monthly mean wind speeds ranged from approximately:

- **2.99 m/s in December**
- **5.18 m/s in April**

The strongest monthly average occurred in April, while December and February represented some of the weaker periods.

Seasonal averages showed:

| Season | Mean wind speed (m/s) | Mean WPD (W/m²) |
|---|---:|---:|
| Winter | 3.21 | 44.20 |
| Spring | 4.38 | 137.87 |
| Summer | 4.19 | 76.26 |
| Autumn | 3.84 | 66.93 |

Spring therefore represented the strongest seasonal wind resource in the analysed year.

---

### 4.5 Diurnal variability

The hourly observations were grouped by hour of day to investigate the average diurnal cycle.

The mean wind speed varied substantially throughout the day. The lowest average wind speed occurred during the early morning period, while higher wind speeds occurred during the afternoon and evening hours.

For example, the average wind speed was approximately:

- 2.85 m/s at 03:00
- 4.05 m/s at 08:00
- 4.29 m/s at 15:00
- 4.51 m/s at 20:00

This indicates a clear diurnal component in the wind regime at the analysed location.

The corresponding WPD also varied strongly through the day because of its cubic dependence on wind speed.

---

### 4.6 Wind direction

Wind-direction observations were grouped into 30° directional sectors.

The highest mean wind speeds occurred in the southern sector, particularly around 180°, where the mean wind speed was approximately 4.52 m/s.

The directional analysis showed the following approximate sectoral mean wind speeds:

| Direction sector | Mean wind speed (m/s) |
|---|---:|
| 0° | 3.34 |
| 30° | 3.38 |
| 60° | 3.46 |
| 90° | 3.88 |
| 120° | 3.88 |
| 150° | 4.47 |
| 180° | 4.52 |
| 210° | 3.72 |
| 240° | 3.15 |
| 270° | 3.07 |
| 300° | 3.55 |
| 330° | 3.77 |

The results indicate that southerly to south-easterly directions were associated with relatively stronger winds in the analysed dataset.

---

### 4.7 Weibull distribution

A two-parameter Weibull distribution was fitted to the positive wind-speed observations.

The Weibull probability density function is:

\[
f(V)=\frac{k}{c}
\left(\frac{V}{c}\right)^{k-1}
\exp\left[-\left(\frac{V}{c}\right)^k\right]
\]

where:

- \(k\) = Weibull shape parameter
- \(c\) = Weibull scale parameter
- \(V\) = wind speed

The fitted parameters were:

\[
k = 1.86
\]

\[
c = 4.408\;m/s
\]

The shape parameter indicates the degree of variability in the wind-speed distribution, while the scale parameter represents the characteristic wind-speed magnitude.

---

### 4.8 Illustrative turbine-energy calculation

To demonstrate the conversion from wind resource to electrical energy, a simplified 2 MW turbine power curve was used.

The model included:

- Rated power: 2,000 kW
- Cut-in wind speed: approximately 3 m/s
- Rated wind speed: approximately 12 m/s
- Cut-out wind speed: approximately 25 m/s

The turbine model is illustrative and does not represent a specific commercial turbine.

The calculated annual energy production was approximately:

**1,536.58 MWh/year**

The corresponding capacity factor was:

**8.77%**

For comparison, a hypothetical 50-turbine array using the same simplified turbine model would have an installed capacity of 100 MW and an illustrative annual production of approximately 76.83 GWh. This calculation does not include wake losses, electrical losses, availability losses, environmental constraints, turbine micrositing or other project-level losses.

---

## 5. Results

The principal results of the assessment are summarized below.

| Parameter | Result |
|---|---:|
| Location | Dhaka, Bangladesh |
| Analysis year | 2017 |
| Wind-data height | 100 m |
| Valid observations | 8,712 |
| Mean wind speed | 3.91 m/s |
| Standard deviation | 2.20 m/s |
| Minimum wind speed | 0.01 m/s |
| Maximum wind speed | 32.54 m/s |
| Mean WPD | 81.76 W/m² |
| Weibull shape, \(k\) | 1.86 |
| Weibull scale, \(c\) | 4.408 m/s |
| Illustrative turbine rating | 2 MW |
| Illustrative annual energy | 1,536.58 MWh |
| Illustrative capacity factor | 8.77% |

The results show a relatively modest wind resource at the analysed Dhaka point during 2017. The resource also exhibits considerable seasonal and diurnal variability.

The strongest monthly wind conditions occurred during April, while winter months generally exhibited weaker wind conditions. The directional analysis indicated relatively stronger winds from southerly and south-easterly sectors.

---

## 6. Discussion

The analysis demonstrates that wind conditions at the selected Dhaka location are highly variable on monthly and hourly timescales. This variability is particularly important for wind-energy applications because electrical power is strongly dependent on wind speed.

The mean wind speed of approximately 3.91 m/s at 100 m and the mean WPD of approximately 81.76 W/m² indicate that the location does not exhibit a particularly strong wind resource compared with locations generally associated with high-quality utility-scale wind development.

However, the results should not be interpreted as a definitive statement about the wind-energy potential of Bangladesh as a whole. The analysis represents only one point location and one year. Wind resources can vary considerably with geography, terrain, surface characteristics and atmospheric circulation.

The seasonal results are particularly interesting from a meteorological perspective. Spring showed the highest mean wind speed and WPD, while winter had substantially weaker conditions. The diurnal cycle also indicates that wind speed varies systematically throughout the day.

The directional analysis suggests that the stronger winds are associated primarily with southerly to south-easterly directions. A more detailed site assessment would therefore need to examine directional frequency, directional energy contribution and potential terrain or surface influences.

The Weibull analysis provides a compact statistical representation of the wind-speed distribution. However, a fitted Weibull distribution should not be considered a replacement for the original hourly observations when estimating energy production. Direct integration of an appropriate turbine power curve over the observed wind-speed time series can provide a more direct estimate.

---

## 7. Limitations

Several limitations should be considered when interpreting the results.

### 7.1 One-year analysis period

The assessment uses only 2017 data. One year is insufficient to characterize long-term wind-resource variability or establish a representative long-term mean.

A professional resource assessment would normally require a substantially longer climatological period and/or a long-term correction procedure.

### 7.2 Point-based analysis

The assessment represents a single location near Dhaka. It does not describe the spatial variability of the wind resource across Bangladesh.

### 7.3 Constant air density

A constant air density of 1.225 kg/m³ was used for the WPD calculation. Actual air density varies with temperature and pressure. Using the available meteorological variables to calculate time-varying air density would provide a more physically realistic estimate.

### 7.4 Simplified turbine model

The turbine power curve is an educational approximation rather than the manufacturer's power curve for a specific turbine. Consequently, the resulting AEP and capacity factor should be treated as illustrative.

### 7.5 No project losses

The energy calculation does not account for wake losses, turbine availability, electrical losses, curtailment, icing, environmental constraints, turbulence-related losses or other project-specific losses.

### 7.6 No validation with measurements

The dataset was not validated against an on-site meteorological mast, LiDAR or other measurement campaign. Such validation would be required for a professional site assessment.

---

## 8. Conclusion

This pilot project developed a basic Python workflow for preliminary wind-resource assessment using hourly NREL Wind Toolkit data at 100 m for Dhaka, Bangladesh.

The analysis found a mean wind speed of approximately 3.91 m/s and a mean wind power density of approximately 81.76 W/m² during the analysed year. The fitted Weibull distribution had a shape parameter of 1.86 and a scale parameter of 4.408 m/s.

The wind resource exhibited clear seasonal and diurnal variability. Spring produced the strongest average wind conditions, while winter generally represented a weaker resource period. The directional analysis indicated relatively stronger winds from southerly and south-easterly sectors.

The illustrative 2 MW turbine calculation produced an estimated annual energy production of approximately 1.54 GWh and a capacity factor of approximately 8.8%. Because the turbine model was simplified and the assessment covered only one year at one point, these values should not be interpreted as a commercial project estimate.

Overall, the project successfully demonstrates a complete introductory wind-energy analysis workflow, beginning with meteorological observations and progressing through wind climatology, statistical distribution, wind power density and basic turbine-energy estimation.

The next logical development of this workflow would be to extend the analysis to a longer climatological period, incorporate variable air density, examine long-term wind variability, compare multiple datasets and locations, and eventually introduce industry-standard resource-assessment concepts such as long-term correction, uncertainty assessment and micrositing.

---

## 9. References

1. National Renewable Energy Laboratory (NREL). *Wind Toolkit*. National Renewable Energy Laboratory, Golden, Colorado, USA.

2. International Electrotechnical Commission (IEC). *IEC 61400-1: Wind Energy Generation Systems – Part 1: Design Requirements*. IEC.

3. Carta, J. A., Ramírez, P., & Velázquez, S. (2009). A review of wind speed probability distributions used in wind energy analysis: Case studies in the Canary Islands. *Renewable and Sustainable Energy Reviews*, 13(5), 933–955.

4. Seguro, J. V., & Lambert, T. W. (2000). Modern estimation of the parameters of the Weibull wind speed distribution for wind energy analysis. *Journal of Wind Engineering and Industrial Aerodynamics*, 85(1), 75–84.

5. Manwell, J. F., McGowan, J. G., & Rogers, A. L. *Wind Energy Explained: Theory, Design and Application*. Wiley.

---

## Project classification

This work should be considered a **preliminary/pilot wind-resource assessment** rather than a bankable wind-energy assessment. Its primary purpose is to demonstrate a reproducible workflow for processing meteorological data and translating wind characteristics into basic wind-energy metrics.