# 📄 **README — Extreme Precipitation Evaluation Report**

### *Case Study: 2023-12-21 00:00 UTC*

### *Models: GraphCast vs FourCastNet*

---

## 1. Overview

This report evaluates the ability of two AI-based global weather forecasting models:

* **GraphCast**
* **FourCastNet**

to predict an extreme precipitation event affecting Greece.

**Verification time:**
📅 **2023-12-21 00:00 UTC**


**Forecast lead times evaluated:**

| Lead day | Hours |
| -------- | ----- |
| D1       | 24h   |
| D2       | 48h   |
| D4       | 96h   |
| D6       | 144h  |
| D10      | 240h  |

ERA5 6-hour accumulated precipitation is used as the ground truth.
![Total accumolated precipitation forecast for 2023-12-21 00:00 ](./plots/era5_tp_6h_accum_20231221_0000.png)
![Total hourly precipitation forecast for 2023-12-21 00:00 ](./plots/era5_tp_6h_hourly_20231221_0000.png)
---

## 2. Methods Summary

* Models produce accumulated precipitation fields (`tp`)
* Regridded → **ERA5 Greece domain**
* Matched by valid_time
* Metrics computed:

  * Bias
  * RMSE
  * Spatial Correlation
  * CSI (Critical Success Index)
  * POD (Probability of Detection)
  * FAR (False Alarm Ratio)
  * Peak intensity ratio
  * Peak displacement distance (km)
  * Center-of-mass displacement (km)

---

## 3. ERA5 Ground Truth

**Figure 1. ERA5 6-hour accumulated precipitation**
`./plots/era5_tp_19700102_0000.png` *(insert the final ERA5 plot)*

---

# 4. FourCastNet Forecast Evaluation (Filled Metrics)

## 🔵 **4.1 Lead Time D1 (24h)**

**Figure FourCastNet D1 (24h) forecast vs ERA5**
![Total precipitation forecast for 2023-12-21 00:00](./plots/tp_case_fourcast_20231221_0000_D1.png)
**Figure GraphCast D1 (24h) forecast vs ERA5**
![Total precipitation forecast for 2023-12-21 00:00](./plots/tp_case_graphcast_20231221_0000_D1.png)
### **Metrics — D1**


# Select D1 (lead_days == 1)

=== 🔍 FOURCASTNET vs GRAPHCAST — D1 Metrics ===

| Metric               | FourCastNet          | GraphCast            |
|----------------------|----------------------|----------------------|
| Hits                 | 720                  | 716                  |
| Misses               | 0                    | 4                    |
| False Alarms         | 230                  | 147                  |
| Bias (m)             | 0.00622              | 0.00140              |
| RMSE (m)             | 0.0090               | 0.0038               |
| Correlation          | 0.635                | 0.651                |
| CSI                  | 0.758                | 0.826                |
| POD                  | 1.000                | 0.994                |
| FAR                  | 0.242                | 0.170                |
| Peak Ratio           | 2.14                 | 0.98                 |
| Intensity Change (%) | 214.19%              | 98.18%               |
| Peak Shift (km)      | 316.8 km             | 526.6 km             |
| CoM Shift (km)       | 59.6 km              | 100.7 km             |

---

## 🔵 **4.2 Lead Time D2 (48h)**

**Figure FourCastNet D2 (48h) forecast vs ERA5**
![Total precipitation forecast for 2023-12-21 00:00](./plots/tp_case_fourcast_20231221_0000_D2.png)
**Figure GraphCast D2 (48h) forecast vs ERA5**
![Total precipitation forecast for 2023-12-21 00:00](./plots/tp_case_graphcast_20231221_0000_D2.png)

### **Metrics — D2**

=== 🔍 FOURCASTNET vs GRAPHCAST — D2 Metrics ===

| Metric               | FourCastNet          | GraphCast            |
|----------------------|----------------------|--------------------- |
| Hits                 | 720                  | 705                  |
| Misses               | 0                    | 15                   |
| False Alarms         | 228                  | 168                  |
| Bias (m)             | 0.00542              | 0.00165              |
| RMSE (m)             | 0.0086               | 0.0034               |
| Correlation          | 0.524                | 0.669                |
| CSI                  | 0.759                | 0.794                |
| POD                  | 1.000                | 0.979                |
| FAR                  | 0.241                | 0.192                |
| Peak Ratio           | 1.98                 | 0.91                 |
| Intensity Change (%) | 198.39%              | 90.95%               |
| Peak Shift (km)      | 524.6 km             | 393.9 km             |
| CoM Shift (km)       | 87.4 km              | 18.1 km              |

---

## 🔵 **4.3 Lead Time D4 (96h)**

**Figure FourCastNet D4 (96h) forecast vs ERA5**
![Total precipitation forecast for 2023-12-21 00:00](./plots/tp_case_fourcast_20231221_0000_D4.png)
**Figure GraphCast D4 (96h) forecast vs ERA5**
![Total precipitation forecast for 2023-12-21 00:00](./plots/tp_case_graphcast_20231221_0000_D4.png)

### **Metrics — D4**

=== 🔍 FOURCASTNET vs GRAPHCAST — D4 Metrics ===

| Metric               | FourCastNet         | GraphCast          |
|----------------------|----------------------|---------------------|
| Hits                 | 720                  | 700                  |
| Misses               | 0                    | 20                   |
| False Alarms         | 269                  | 185                  |
| Bias (m)             | 0.00369              | 0.00104              |
| RMSE (m)             | 0.0066               | 0.0035               |
| Correlation          | 0.431                | 0.582                |
| CSI                  | 0.728                | 0.773                |
| POD                  | 1.000                | 0.972                |
| FAR                  | 0.272                | 0.209                |
| Peak Ratio           | 1.58                 | 0.94                 |
| Intensity Change (%) | 158.11%              | 93.54%               |
| Peak Shift (km)      | 543.7 km             | 546.5 km             |
| CoM Shift (km)       | 111.3 km             | 88.6 km              |

---

## 🔵 **4.4 Lead Time D6 (144h)**

**Figure FourCastNet D6 (144h) forecast vs ERA5**
![Total precipitation forecast for 2023-12-21 00:00](./plots/tp_case_fourcast_20231221_0000_D6.png)
**Figure GraphCast D6 (144h) forecast vs ERA5**
![Total precipitation forecast for 2023-12-21 00:00](./plots/tp_case_graphcast_20231221_0000_D6.png)

### **Metrics — D6**
=== 🔍 FOURCASTNET vs GRAPHCAST — D6 Metrics ===

| Metric               | FourCastNet         | GraphCast          |
|----------------------|----------------------|---------------------|
| Hits                 | 720                  | 720                  |
| Misses               | 0                    | 0                    |
| False Alarms         | 501                  | 499                  |
| Bias (m)             | 0.02120              | 0.02029              |
| RMSE (m)             | 0.0267               | 0.0257               |
| Correlation          | -0.217               | -0.262               |
| CSI                  | 0.590                | 0.591                |
| POD                  | 1.000                | 1.000                |
| FAR                  | 0.410                | 0.409                |
| Peak Ratio           | 4.75                 | 3.81                 |
| Intensity Change (%) | 475.23%              | 380.94%              |
| Peak Shift (km)      | 590.4 km             | 594.1 km             |
| CoM Shift (km)       | 301.1 km             | 305.8 km             |
---

## 🔵 **4.5 Lead Time D10 (240h)**

**Figure FourCastNet D10 (240h) forecast vs ERA5**
![Total precipitation forecast for 2023-12-21 00:00](./plots/tp_case_fourcast_20231221_0000_D10.png)
**Figure GraphCast D10 (240h) forecast vs ERA5**
![Total precipitation forecast for 2023-12-21 00:00](./plots/tp_case_graphcast_20231221_0000_D10.png)

### **Metrics — D10**
=== 🔍 FOURCASTNET vs GRAPHCAST — D1 Metrics ===

| Metric               | FourCastNet          | GraphCast            |
|----------------------|----------------------|----------------------|
| Hits                 | 720                  | 720                  |
| Misses               | 0                    | 0                    |
| False Alarms         | 501                  | 501                  |
| Bias (m)             | 0.00617              | 0.02074              |
| RMSE (m)             | 0.0121               | 0.0237               |
| Correlation          | -0.355               | -0.246               |
| CSI                  | 0.590                | 0.590                |
| POD                  | 1.000                | 1.000                |
| FAR                  | 0.410                | 0.410                |
| Peak Ratio           | 3.25                 | 3.06                 |
| Intensity Change (%) | 324.87%              | 305.90%              |
| Peak Shift (km)      | 871.6 km             | 566.8 km             |
| CoM Shift (km)       | 333.2 km             | 253.1 km             |
---


# 6. GraphCast vs FourCastNet — Lead-by-Lead Comparison

===  GraphCast vs FourCastNet — Pairwise Metrics (GC_vs_FC) ===

| Lead | mean_GC (m) | mean_FC (m) | Bias (GC−FC) (m) | RMSE(GC,FC) (m) | Corr(GC,FC) |
|------|-------------|-------------|------------------|-----------------|------------|
| D1   | 0.003667    | 0.008483    | -0.004816        | 0.006885        | 0.822      |
| D2   | 0.003914    | 0.007685    | -0.003772        | 0.007002        | 0.658      |
| D4   | 0.003309    | 0.005959    | -0.002650        | 0.005667        | 0.573      |
| D6   | 0.022562    | 0.023471    | -0.000908        | 0.009314        | 0.810      |
| D10  | 0.023005    | 0.008438    | 0.014568         | 0.017845        | 0.431      |


**Figure FourCastNet D10 (240h) forecast vs ERA5**
![Total precipitation forecast for 2023-12-21 00:00](./plots/tp_case_GC_FC_vs_ERA5_20231221_0000_D1.png)
![Total precipitation forecast for 2023-12-21 00:00](./plots/tp_case_GC_FC_vs_ERA5_20231221_0000_D2.png)
![Total precipitation forecast for 2023-12-21 00:00](./plots/tp_case_GC_FC_vs_ERA5_20231221_0000_D4.png)
![Total precipitation forecast for 2023-12-21 00:00](./plots/tp_case_GC_FC_vs_ERA5_20231221_0000_D6.png)
![Total precipitation forecast for 2023-12-21 00:00](./plots/tp_case_GC_FC_vs_ERA5_20231221_0000_D10.png)
---

# 7. Summary & Conclusions

(Write your own science interpretation here, e.g.):

* FC detects extremes well at all leads (POD=1.0), but generates **large false alarms** at longer leads.
* FC shows **large positive bias** and **strong overestimation** of precipitation intensity.
* Spatial displacement grows significantly after D6.
* GC comparison to follow.

---


