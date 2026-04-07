Wind Energy Resource Assessment — Dhaka (2017)
--
Overview

This project presents a point-based wind resource assessment using the NREL Wind Toolkit for Dhaka, Bangladesh. The analysis focuses on wind characteristics at 100 m hub height, providing a structured workflow aligned with industry wind resource assessment practices.

The project demonstrates data processing, statistical analysis, and visualization techniques commonly used in early-stage wind feasibility studies.

---

Objectives

- Analyze wind speed and direction at 100 m height
- Estimate wind power density (WPD)
- Evaluate temporal variability (monthly, seasonal, diurnal)
- Characterize wind distribution using Weibull fitting
- Perform directional analysis using wind rose
- Provide an illustrative turbine energy estimate

---

Dataset

- Source: NREL Wind Toolkit (WTK)
- Temporal resolution: Hourly
- Year: 2017
- Location: Dhaka (23.8103°N, 90.4125°E)
- Height: 100 m

---

Methodology

1. Data Processing

- Cleaning and restructuring raw CSV data
- Datetime indexing for time-series analysis
- Unit consistency checks

2. Wind Resource Metrics

Wind Power Density (WPD) computed as:

[
WPD = \frac{1}{2} \rho v^3
]

where:

- \rho = 1.225 , \text{kg/m}^3
- v = wind speed at 100 m

3. Statistical Analysis

- Mean, standard deviation, coefficient of variation
- Monthly and seasonal aggregation
- Diurnal cycle analysis

4. Distribution Analysis

- Weibull distribution fitted to wind speeds
- Parameters:
  - Shape factor k
  - Scale factor c

5. Directional Analysis

- Wind directions grouped into 30° sectors
- Mean wind speed per sector (wind rose)

6. Energy Estimation (Illustrative)

- Simplified turbine power curve (2 MW class)
- Annual Energy Production (AEP)
- Capacity factor estimation

---

Key Results

Metric| Value
Mean Wind Speed| ~3.91 m/s
Mean WPD| ~81.8 W/m²
Capacity Factor| ~8.8%

Interpretation

- Wind speeds are low for utility-scale deployment
- Resource is marginal for large turbines
- Suitable mainly for:
  - Small-scale applications
  - Academic and methodological demonstration

---

Project Structure

notebooks/     → analysis notebook  
data/          → raw or processed data  
figures/       → generated plots  
report/        → markdown summary  

---

How to Run

1. Clone repository:

git clone https://github.com/yourusername/wind-energy-dhaka-2017.git

2. Install dependencies:

pip install -r requirements.txt

3. Open notebook:

notebooks/Wind_energy_dhaka_2017.ipynb

---

Important Notes

- API keys are not included in the repository
- Dataset can be downloaded using the provided script
- Energy calculations are illustrative, not bankable

---

Scientific Context

Wind resource assessment methods used here are consistent with:

- Burton et al. (2011), Wind Energy Handbook
- Carta et al. (2009), Renewable and Sustainable Energy Reviews
- Manwell et al. (2010), Wind Energy Explained

---



Author

Hanif Ahmed
MSc Marine Geoscience — University of Bremen

---
