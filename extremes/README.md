# ⚡ Extreme Event Definitions and Examples

*Part of the GeoML-Lab Multi-Model Framework for Extreme Weather Forecasting*

---

## 🌍 Purpose

This document describes **how GeoML-Lab defines and identifies extreme events** in weather and climate data.
These definitions form the foundation for:

* **Labeling events** used in model training and evaluation
* **Establishing thresholds** for classification and regression tasks
* **Comparing AI model performance** on rare, high-impact phenomena

---

## 📈 General Definition

An **extreme event** is defined as an atmospheric or hydrological phenomenon that **significantly deviates from the local climatological distribution**, typically beyond a specified percentile threshold.
In most analyses, GeoML-Lab adopts:

* **Upper-tail extremes:** 95th percentile (e.g., heavy rain, heatwaves, high wind)
* **Lower-tail extremes:** 1st–5th percentile (e.g., cold spells, low pressure anomalies)

All thresholds are computed over a **30-year reference climatology (e.g., 1970–2023)** using **ERA5 reanalysis** or compatible datasets.

---

## 🌧️ Categories of Extreme Events

| Type                      | Definition                                                    | Typical Threshold                                 | Relevant Variables   | 
| ------------------------- | ------------------------------------------------------------- | ------------------------------------------------- | -------------------- | 
| **Extreme Precipitation** | The accumulated liquid and frozen water, comprising rain and snow, that falls to the Earth's surface | >95th percentile of total precipitation (`tp`)    | `tp`, `cape`, `tcwv` | 

👉 [**tp parameter detail**](https://codes.ecmwf.int/grib/param-db/228) 
---

## ERA5 Threshold over Greece for total precipitation

<p align="center"> <img src="../plots/threshold_plot.png" alt="tp threshold plot" width="700"/> </p>

The figure above shows the threshold values of total precipitation (tp_q95_alltime) across Greece, calculated for each grid point. These thresholds serve as reference levels for identifying local extremes. During analysis, any grid cell exceeding its corresponding threshold will be marked as an extreme grid point. If more than 150 grid points are classified as extreme in a single time snapshot, that day will be defined as an extreme precipitation day.


The figure below presents the monthly frequency of extreme precipitation days identified across Greece, based on the threshold exceedance criterion described above.
The data originate from the unique_extreme_days.txt file, which lists all detected extreme days. Each bar represents the total number of extreme days occurring within a given month, allowing for a clear visualization of seasonal patterns and the temporal distribution of extreme precipitation events throughout the study period.

<p align="center"> <img src="../plots/Frequency_of_Extreme_Days_per_Month.png" alt="Frequency of Extreme" width="700"/> </p>
## 🧾 License

© 2025 Vasileios Vatellis — **GeoML-Lab Initiative**
All definitions and figures are provided for research and non-commercial purposes.
