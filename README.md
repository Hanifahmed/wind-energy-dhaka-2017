# Preliminary Wind Resource Assessment of Dhaka, Bangladesh

A beginner-level wind resource assessment using hourly **NREL Wind Toolkit** data for Dhaka, Bangladesh.

This project explores how meteorological wind data can be processed in Python and converted into basic wind-energy indicators such as wind-speed statistics, wind power density, Weibull parameters, wind direction characteristics, annual energy production, and capacity factor.

> **Project status:** Completed pilot project
> **Level:** Beginner / introductory wind-energy data analysis
> **Location:** Dhaka, Bangladesh
> **Analysis year:** 2017
> **Wind-data height:** 100 m

---

## 1. Project Overview

Wind resource assessment is one of the first steps in understanding whether a location may be suitable for wind-energy development.

In this project, hourly wind data for a location near Dhaka were analysed to answer some basic questions:

* How strong is the wind?
* How does wind speed vary during the year?
* Is there a clear daily cycle?
* Which wind directions are most important?
* What does the wind-speed distribution look like?
* What is the estimated wind power density?
* How would a simplified wind turbine respond to this wind resource?

The analysis was carried out using Python in Google Colab.

The project is intended primarily as a **learning and portfolio project**, not as a commercial wind-farm feasibility study.

---

## 2. Objectives

The main objectives were to:

1. Load and clean hourly wind-energy data.
2. Construct a proper datetime index.
3. Perform basic quality control.
4. Calculate descriptive wind-speed statistics.
5. Investigate monthly and seasonal wind variability.
6. Examine the diurnal wind-speed cycle.
7. Analyse wind-direction characteristics.
8. Fit a Weibull distribution to the wind-speed data.
9. Calculate wind power density.
10. Apply a simplified turbine power curve.
11. Estimate annual energy production and capacity factor.

---

## 3. Data

### NREL Wind Toolkit

The project uses hourly data from the **NREL Wind Toolkit**.

The downloaded dataset contains:

| Variable        | Description              | Unit    |
| --------------- | ------------------------ | ------- |
| Wind speed      | Wind speed at 100 m      | m/s     |
| Wind direction  | Wind direction at 100 m  | degrees |
| Air temperature | Air temperature at 100 m | °C      |
| Year            | Observation year         | —       |
| Month           | Observation month        | —       |
| Day             | Observation day          | —       |
| Hour            | Observation hour         | —       |

### Study location

The selected point is near Dhaka:

* **Latitude:** ~23.803° N
* **Longitude:** ~90.421° E
* **Height:** 100 m
* **Year:** 2017

The original dataset contains 8,760 hourly records for the year. After basic cleaning and removal of incomplete observations, **8,712 valid observations** were used in the main analysis.

---

## 4. Python Libraries

The analysis uses:

```text
Python
NumPy
Pandas
Matplotlib
SciPy
Windrose
```

The project was developed in **Google Colab**.

---

## 5. Analysis Workflow

The project follows a simple workflow:

```text
NREL Wind Toolkit
        ↓
Raw CSV data
        ↓
Data cleaning
        ↓
Datetime construction
        ↓
Quality control
        ↓
Wind-speed statistics
        ↓
Monthly / seasonal analysis
        ↓
Diurnal analysis
        ↓
Wind-direction analysis
        ↓
Weibull distribution
        ↓
Wind Power Density
        ↓
Simplified turbine power curve
        ↓
AEP and Capacity Factor
```

---

## 6. Main Results

### Wind-speed statistics

The analysed dataset produced:

| Parameter          |         Result |
| ------------------ | -------------: |
| Valid observations |          8,712 |
| Mean wind speed    |   **3.91 m/s** |
| Standard deviation |   **2.20 m/s** |
| Minimum wind speed |      ~0.01 m/s |
| Maximum wind speed |     ~32.54 m/s |
| Mean WPD           | **81.76 W/m²** |

The average wind speed at 100 m was approximately **3.91 m/s**.

---

### Seasonal variability

The wind resource showed noticeable seasonal variability.

| Season | Mean wind speed |        Mean WPD |
| ------ | --------------: | --------------: |
| Winter |        3.21 m/s |      44.20 W/m² |
| Spring |    **4.38 m/s** | **137.87 W/m²** |
| Summer |        4.19 m/s |      76.26 W/m² |
| Autumn |        3.84 m/s |      66.93 W/m² |

Spring produced the strongest average wind conditions in the analysed year.

---

### Monthly variability

Monthly mean wind speed ranged approximately from:

* **2.99 m/s — December**
* **5.18 m/s — April**

April therefore represented the strongest monthly wind period in this dataset.

---

### Diurnal variability

A clear daily variation in wind speed was observed.

Examples of mean wind speeds included approximately:

|  Hour | Mean wind speed |
| ----: | --------------: |
| 03:00 |        2.85 m/s |
| 08:00 |        4.05 m/s |
| 15:00 |        4.29 m/s |
| 20:00 |        4.51 m/s |

The results show that wind conditions were generally stronger during the afternoon and evening than during the early morning.

---

## 7. Wind Direction

The wind-direction analysis showed that relatively stronger winds were associated with southerly to south-easterly directions.

The highest mean wind speed occurred around the **180° sector**, with an average of approximately **4.52 m/s**.

This directional information is important because wind-energy production depends not only on wind speed but also on the directional distribution of the resource.

A wind rose was therefore included in the analysis to provide a visual representation of the wind regime.

---

## 8. Weibull Distribution

A two-parameter Weibull distribution was fitted to the positive wind-speed observations.

The fitted parameters were:

```text
Shape parameter (k)  = 1.86
Scale parameter (c)  = 4.408 m/s
```

The Weibull distribution provides a convenient statistical description of the wind-speed regime.

The probability density function is:

$$
f(V)=\frac{k}{c}
\left(\frac{V}{c}\right)^{k-1}
e^{-(V/c)^k}
$$

where:

* \(k\) = shape parameter
* \(c\) = scale parameter
* \(V\) = wind speed

---

## 9. Wind Power Density

Wind Power Density was calculated using:

$$
WPD = \frac{1}{2}\rho V^3
$$

where:

* \(WPD\) = wind power density in W/m²
* \(\rho\) = air density
* \(V\) = wind speed

A constant air density of:

```text
ρ = 1.225 kg/m³
```

was used for this introductory analysis.

The resulting mean wind power density was:

### **81.76 W/m²**

Because wind power depends on the cube of wind speed, periods of high wind speed contribute strongly to the average available wind power.

---

## 10. Simplified Turbine Calculation

To demonstrate the conversion from wind resource to electrical energy, a simplified **2 MW hypothetical turbine** was used.

The model assumed approximately:

```text
Rated power       = 2,000 kW
Cut-in speed      = 3 m/s
Rated speed       = 12 m/s
Cut-out speed     = 25 m/s
```

The turbine power curve is **not the manufacturer's power curve of a real turbine**. It is a simplified educational model.

The resulting estimate was:

| Parameter                |                Result |
| ------------------------ | --------------------: |
| Turbine rating           |                  2 MW |
| Annual energy production | **1,536.58 MWh/year** |
| Capacity factor          |             **8.77%** |

These values should therefore be interpreted as an **illustrative calculation**.

---

## 11. Important Limitations

This project has several important limitations.

### 1. Only one year of data

The analysis uses 2017 only.

One year is not sufficient to establish a representative long-term wind climate or long-term energy yield.

### 2. Single location

Only one point near Dhaka was analysed.

The results should not be interpreted as representing the entire wind resource of Bangladesh.

### 3. Simplified turbine model

The turbine power curve is hypothetical and does not represent a specific commercial turbine.

### 4. Constant air density

A constant air density of 1.225 kg/m³ was used.

A more advanced analysis would calculate air density from temperature and pressure.

### 5. No long-term correction

No MCP or other long-term correction technique was applied.

### 6. No measured-data validation

The NREL data were not validated against a meteorological mast or LiDAR measurement campaign.

### 7. No wind-farm losses

The AEP estimate does not include:

* Wake losses
* Electrical losses
* Availability losses
* Curtailment
* Turbine degradation
* Environmental constraints
* Other project-specific losses

Therefore, the calculated AEP should **not** be treated as a bankable energy estimate.

---

## 12. What I Learned

This project was developed as an early Python and wind-energy learning exercise.

The main concepts explored were:

* Working with meteorological time-series data
* Data cleaning with pandas
* Datetime handling
* Descriptive statistics
* Wind-speed distributions
* Weibull fitting
* Wind Power Density
* Wind-direction analysis
* Wind roses
* Turbine power curves
* Annual Energy Production
* Capacity Factor
* Basic wind-resource assessment workflow

The project also helped connect meteorological concepts with practical wind-energy applications.

---

## 13. Future Improvements

Possible future improvements include:

* Extending the analysis to a multi-year period
* Comparing NREL data with ERA5
* Calculating variable air density
* Performing long-term wind-resource correction
* Comparing multiple locations in Bangladesh
* Using actual commercial turbine power curves
* Including turbine availability and loss assumptions
* Performing uncertainty analysis
* Investigating extreme wind conditions
* Comparing different hub heights
* Developing a more systematic resource-assessment workflow

These improvements are intentionally left for later projects rather than being added to this introductory pilot.

---

## 14. Project Structure

A simple project structure is used:

```text
wind_energy_forecast/
│
├── data/
│   └── NREL_Wind_Toolkit_Dhaka_2017.csv
│
├── notebooks/
│   └── Dhaka_Wind_Resource_Assessment.ipynb
│
├── figures/
│   ├── wind_speed_distribution.png
│   ├── monthly_wind_speed.png
│   ├── seasonal_wind_speed.png
│   ├── diurnal_wind_speed.png
│   ├── wind_rose.png
│   └── weibull_fit.png
│
├── report/
│   └── Dhaka_Wind_Resource_Assessment_Report.pdf
│
└── README.md
```

---

## 15. Tools

* **Python** — data analysis
* **Pandas** — data handling
* **NumPy** — numerical calculations
* **SciPy** — Weibull distribution fitting
* **Matplotlib** — visualization
* **Windrose** — wind-direction visualization
* **Google Colab** — development environment

---

## 16. Data Source

National Renewable Energy Laboratory (NREL), **Wind Toolkit**.

The NREL Wind Toolkit provides wind-resource data for research and analysis applications.

---

## 17. Project Note

This project is part of a series of small pilot projects developed to build practical skills in **meteorology, wind-energy analysis, Python and renewable-energy data science**.

The emphasis of this project is not on producing a commercial wind-farm assessment, but on understanding the basic workflow from:

**meteorological data → wind climatology → wind resource → turbine response → energy estimate**

---

## 18. License

This repository is intended for educational and portfolio purposes.

The original meteorological data remain subject to the terms and conditions of the respective data provider.
