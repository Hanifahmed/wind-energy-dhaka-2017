import os
from pathlib import Path
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




# =========================================================
# Configuration
# =========================================================
EMAIL = os.getenv("NREL_EMAIL", "your_email@example.com")
API_KEY = os.getenv("NREL_API_KEY", "")
LON = 90.4125
LAT = 23.8103
YEAR = "2017"


PROJECT_DIR = Path(".")
DATA_DIR = PROJECT_DIR / "data"
FIG_DIR = PROJECT_DIR / "Figures"
REPORT_DIR = PROJECT_DIR / "report"


DATA_DIR.mkdir(exist_ok=True)
FIG_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)


CSV_FILE = DATA_DIR / f"nrel_dhaka_100m_{YEAR}.csv"


plt.rcParams["figure.dpi"] = 120
plt.rcParams["axes.grid"] = True




# =========================================================
# Utility
# =========================================================
def save_figure(fig, filename: str) -> None:
    out = FIG_DIR / filename
    fig.tight_layout()
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)




def download_wind_csv(api_key: str, email: str, lon: float, lat: float, year: str, out_path: Path) -> Path:
    if not api_key:
        raise ValueError("NREL_API_KEY is missing. Set it as an environment variable.")


    url = "https://developer.nrel.gov/api/wind-toolkit/v2/wind/wtk-bangladesh-download.csv"
    params = {
        "wkt": f"POINT({lon} {lat})",
        "attributes": "windspeed_100m,winddirection_100m,temperature_100m",
        "names": year,
        "utc": "true",
        "leap_day": "true",
        "interval": "60",
        "email": email,
        "api_key": api_key,
    }


    r = requests.get(url, params=params, timeout=120)
    r.raise_for_status()


    out_path.write_bytes(r.content)
    print(f"Saved CSV to: {out_path}")
    return out_path




# =========================================================
# Data loading and cleaning
# =========================================================
def load_and_prepare(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path, skiprows=1)


    df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]


    rename_map = {
        "wind_speed_at_100m_(m/s)": "windspeed_100m",
        "wind_direction_at_100m_(deg)": "winddir_100m",
        "air_temperature_at_100m_(c)": "temp_100m",
    }
    df = df.rename(columns=rename_map)


    required = ["year", "month", "day", "hour", "windspeed_100m", "winddir_100m", "temp_100m"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


    df["datetime"] = pd.to_datetime(df[["year", "month", "day", "hour"]], errors="coerce")
    df = df.dropna(subset=["datetime"]).copy()
    df = df.set_index("datetime").sort_index()


    for col in ["windspeed_100m", "winddir_100m", "temp_100m"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")


    df = df.dropna(subset=["windspeed_100m", "winddir_100m", "temp_100m"]).copy()


    # Wind Power Density using constant density assumption
    rho = 1.225
    df["wpd"] = 0.5 * rho * (df["windspeed_100m"] ** 3)


    # Season mapping
    season_map = {
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring",
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn",
    }
    df["season"] = df.index.month.map(season_map)
    df["month"] = df.index.month
    df["hour"] = df.index.hour


    return df




# =========================================================
# Statistics
# =========================================================
def basic_stats(df: pd.DataFrame) -> pd.DataFrame:
    stats = df[["windspeed_100m", "winddir_100m", "temp_100m", "wpd"]].describe().T
    stats["cv_percent"] = (stats["std"] / stats["mean"]) * 100
    return stats




def weibull_fit(series: pd.Series) -> dict:
    from scipy.stats import weibull_min


    s = series.dropna()
    s = s[s > 0]
    shape, loc, scale = weibull_min.fit(s, floc=0)
    return {"k": shape, "c": scale, "loc": loc}




def monthly_means(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("month")[["windspeed_100m", "winddir_100m", "temp_100m", "wpd"]].mean()




def seasonal_means(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("season")[["windspeed_100m", "winddir_100m", "temp_100m", "wpd"]].mean()




def daily_means(df: pd.DataFrame) -> pd.DataFrame:
    daily = df.resample("D")[["windspeed_100m", "wpd"]].mean()
    daily["windspeed_roll_30d"] = daily["windspeed_100m"].rolling(window=30, min_periods=1).mean()
    daily["wpd_roll_30d"] = daily["wpd"].rolling(window=30, min_periods=1).mean()
    return daily




def diurnal_cycle(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("hour")[["windspeed_100m", "temp_100m", "wpd"]].mean()




def direction_sector_stats(df: pd.DataFrame) -> pd.DataFrame:
    bins = np.arange(0, 361, 30)
    labels = bins[:-1]
    df = df.copy()
    df["winddir_bin"] = pd.cut(df["winddir_100m"], bins=bins, include_lowest=True, labels=labels, right=False)
    sector = df.groupby("winddir_bin", observed=False)["windspeed_100m"].mean()
    return sector




def power_curve_vestas_v100(ws: float) -> float:
    curve = {
        0: 0, 1: 0, 2: 0, 3: 0,
        4: 80, 5: 180, 6: 350, 7: 600,
        8: 950, 9: 1400, 10: 1750, 11: 1950,
        12: 2000, 13: 2000, 14: 2000, 15: 2000,
        16: 2000, 17: 2000, 18: 2000, 19: 2000,
        20: 2000, 21: 2000, 22: 2000, 23: 2000,
        24: 2000, 25: 2000, 26: 0, 27: 0,
    }
    if pd.isna(ws):
        return 0.0
    return float(curve.get(int(round(ws)), 0.0))




def turbine_energy_assessment(df: pd.DataFrame, n_turbines: int = 50) -> dict:
    temp = df.copy()
    temp["power_kw"] = temp["windspeed_100m"].apply(power_curve_vestas_v100)


    aep_single_mwh = temp["power_kw"].sum() / 1000.0
    rated_mw = 2.0
    hours_year = 8760
    cf_single = aep_single_mwh / (rated_mw * hours_year)


    farm_aep_mwh = aep_single_mwh * n_turbines
    farm_capacity_mw = rated_mw * n_turbines


    return {
        "df_power": temp,
        "single_turbine_aep_mwh": aep_single_mwh,
        "single_turbine_cf": cf_single,
        "farm_aep_mwh": farm_aep_mwh,
        "farm_capacity_mw": farm_capacity_mw,
        "n_turbines": n_turbines,
    }




# =========================================================
# Plotting
# =========================================================
def plot_daily_trends(daily: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(daily.index, daily["windspeed_100m"], alpha=0.4, label="Daily mean wind speed")
    ax.plot(daily.index, daily["windspeed_roll_30d"], color="red", label="30-day rolling mean")
    ax.set_title("Daily Mean Wind Speed at 100 m (Dhaka, 2017)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Wind Speed (m/s)")
    ax.legend()
    save_figure(fig, "dhaka_daily_windspeed_2017.png")


    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(daily.index, daily["wpd"], alpha=0.4, label="Daily mean WPD")
    ax.plot(daily.index, daily["wpd_roll_30d"], color="green", label="30-day rolling mean")
    ax.set_title("Daily Mean Wind Power Density at 100 m (Dhaka, 2017)")
    ax.set_xlabel("Date")
    ax.set_ylabel("WPD (W/m²)")
    ax.legend()
    save_figure(fig, "dhaka_daily_wpd_2017.png")




def plot_diurnal_cycle(diurnal: pd.DataFrame) -> None:
    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(diurnal.index, diurnal["windspeed_100m"], marker="o", color="blue")
    ax1.set_xlabel("Hour of Day")
    ax1.set_ylabel("Wind Speed (m/s)", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")


    ax2 = ax1.twinx()
    ax2.plot(diurnal.index, diurnal["wpd"], marker="s", color="green")
    ax2.set_ylabel("WPD (W/m²)", color="green")
    ax2.tick_params(axis="y", labelcolor="green")


    plt.title("Average Diurnal Cycle at 100 m (Dhaka, 2017)")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "dhaka_diurnal_cycle_2017.png", dpi=300, bbox_inches="tight")
    plt.close(fig)




def plot_wind_rose(sector_stats: pd.Series) -> None:
    theta = np.deg2rad(sector_stats.index.astype(float))
    radii = sector_stats.values


    fig = plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    ax.bar(theta, radii, width=np.deg2rad(30), bottom=0, color="skyblue", edgecolor="black", alpha=0.75)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_title("Wind Rose (Mean Wind Speed by 30° Sector, Dhaka 2017)", y=1.08)
    save_figure(fig, "dhaka_wind_rose_2017.png")




def plot_distribution(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["windspeed_100m"], bins=30, edgecolor="black", alpha=0.75)
    ax.set_title("Wind Speed Distribution at 100 m (Dhaka, 2017)")
    ax.set_xlabel("Wind Speed (m/s)")
    ax.set_ylabel("Frequency")
    save_figure(fig, "dhaka_windspeed_distribution_2017.png")




def plot_speed_vs_power(df_power: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df_power["windspeed_100m"], df_power["power_kw"], s=10, alpha=0.3)
    ax.set_title("Wind Speed vs Illustrative Turbine Power Output")
    ax.set_xlabel("Wind Speed (m/s)")
    ax.set_ylabel("Power Output (kW)")
    save_figure(fig, "dhaka_windspeed_vs_power_2017.png")




def plot_seasonal_diurnal_heatmap(df: pd.DataFrame) -> None:
    pivot = df.pivot_table(index="hour", columns="month", values="windspeed_100m", aggfunc="mean")


    fig, ax = plt.subplots(figsize=(12, 6))
    im = ax.imshow(pivot.values, aspect="auto", cmap="YlGnBu", origin="lower")
    ax.set_title("Hourly Mean Wind Speed by Month (Dhaka, 2017)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Hour of Day")
    ax.set_xticks(np.arange(12))
    ax.set_xticklabels(pivot.columns.tolist())
    ax.set_yticks(np.arange(24))
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Wind Speed (m/s)")
    save_figure(fig, "dhaka_hour_month_heatmap_2017.png")




def plot_power_sample(df_power: pd.DataFrame, n_turbines: int) -> None:
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df_power.index[:500], df_power["power_kw"].iloc[:500], label="Single turbine", alpha=0.8)
    ax.plot(df_power.index[:500], df_power["power_kw"].iloc[:500] * n_turbines,
            label=f"{n_turbines}-turbine farm", alpha=0.8)
    ax.set_title("Illustrative Turbine and Farm Power Output (First 500 Hours)")
    ax.set_xlabel("Time")
    ax.set_ylabel("Power (kW)")
    ax.legend()
    save_figure(fig, "dhaka_power_output_sample_2017.png")




# =========================================================
# Reporting
# =========================================================
def write_report(
    stats_df: pd.DataFrame,
    monthly_df: pd.DataFrame,
    seasonal_df: pd.DataFrame,
    weibull_params: dict,
    energy: dict
) -> None:
    report_text = f"""# Dhaka 100 m Wind Resource Assessment (2017)


## Overview
This report summarizes a point-based wind resource assessment for Dhaka using NREL Wind Toolkit hourly data at 100 m for 2017.


## Core statistics
- Mean wind speed: {stats_df.loc['windspeed_100m', 'mean']:.2f} m/s
- Wind speed standard deviation: {stats_df.loc['windspeed_100m', 'std']:.2f} m/s
- Mean wind power density: {stats_df.loc['wpd', 'mean']:.2f} W/m²
- Mean air temperature: {stats_df.loc['temp_100m', 'mean']:.2f} °C


## Weibull parameters
- Shape parameter k: {weibull_params['k']:.3f}
- Scale parameter c: {weibull_params['c']:.3f}


## Seasonal interpretation
The strongest seasonal mean wind conditions occur during the months associated with the pre-monsoon and monsoon transition, while winter conditions are weaker overall. This indicates moderate seasonality but not a uniformly strong utility-scale offshore-style resource at this inland location.


## Illustrative turbine yield
The turbine yield estimate is based on a simplified Vestas V100 2.0 MW power curve and should be interpreted as an illustrative engineering estimate rather than a validated production forecast.


- Single turbine AEP: {energy['single_turbine_aep_mwh']:.2f} MWh
- Single turbine capacity factor: {energy['single_turbine_cf']:.2%}
- Wind farm size: {energy['n_turbines']} turbines
- Wind farm installed capacity: {energy['farm_capacity_mw']:.1f} MW
- Wind farm AEP: {energy['farm_aep_mwh']:.2f} MWh


## Key caveat
This assessment is based on a single modeled point and one calendar year. It is suitable as a pilot resource-analysis workflow, but not sufficient alone for bankable project development or site certification.


## Output tables
### Monthly means
{monthly_df.round(3).to_markdown()}


### Seasonal means
{seasonal_df.round(3).to_markdown()}
"""
    (REPORT_DIR / "dhaka_wind_assessment_report.md").write_text(report_text, encoding="utf-8")




# =========================================================
# Main
# =========================================================
def main():
    if not CSV_FILE.exists():
        print("CSV not found locally. Attempting download...")
        download_wind_csv(API_KEY, EMAIL, LON, LAT, YEAR, CSV_FILE)


    df = load_and_prepare(CSV_FILE)


    print("\n--- Basic Statistics ---")
    stats_df = basic_stats(df)
    print(stats_df.round(3))


    monthly_df = monthly_means(df)
    print("\n--- Monthly Averages ---")
    print(monthly_df.round(3))


    seasonal_df = seasonal_means(df)
    print("\n--- Seasonal Averages ---")
    print(seasonal_df.round(3))


    daily_df = daily_means(df)
    diurnal_df = diurnal_cycle(df)
    sector_df = direction_sector_stats(df)
    weibull_params = weibull_fit(df["windspeed_100m"])
    energy = turbine_energy_assessment(df, n_turbines=50)


    print("\n--- Weibull Parameters ---")
    print(weibull_params)


    print("\n--- Illustrative Turbine + Farm Energy ---")
    print(f"Single turbine AEP: {energy['single_turbine_aep_mwh']:.2f} MWh")
    print(f"Single turbine CF: {energy['single_turbine_cf']:.2%}")
    print(f"Farm AEP ({energy['n_turbines']} turbines): {energy['farm_aep_mwh']:.2f} MWh")
    print(f"Installed capacity: {energy['farm_capacity_mw']:.1f} MW")


    # Save enriched dataframe
    df_out = energy["df_power"].copy()
    df_out.to_csv(DATA_DIR / "dhaka_2017_cleaned_analysis.csv")


    # Figures
    plot_daily_trends(daily_df)
    plot_diurnal_cycle(diurnal_df)
    plot_wind_rose(sector_df)
    plot_distribution(df)
    plot_speed_vs_power(energy["df_power"])
    plot_seasonal_diurnal_heatmap(df)
    plot_power_sample(energy["df_power"], energy["n_turbines"])


    # Report
    write_report(stats_df, monthly_df, seasonal_df, weibull_params, energy)


    print(f"\nSaved cleaned analysis CSV to: {DATA_DIR / 'dhaka_2017_cleaned_analysis.csv'}")
    print(f"Saved figures to: {FIG_DIR}")
    print(f"Saved report to: {REPORT_DIR / 'dhaka_wind_assessment_report.md'}")




if __name__ == "__main__":
    main()