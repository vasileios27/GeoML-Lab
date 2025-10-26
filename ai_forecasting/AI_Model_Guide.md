# 🧠 AI Model Guide

*Part of the GeoML-Lab Multi-Model Framework for Extreme Weather Forecasting*

---

## 🌍 Overview

This document provides setup and usage instructions for the **AI weather forecasting models** used in the GeoML-Lab initiative.
All models are containerized with a **FastAPI interface** for easy benchmarking and reproducibility.
The goal is to compare their skill in forecasting **medium-range (1–15 day)** extreme weather events — focusing primarily on **severe precipitation**.

Each model can be run locally, on a cluster, or in the cloud.

---

## ⚙️ Model Setup and Containerization

Each AI model is packaged in its own Docker container following the same structure:

```
containers/
├── graphcast/
│   ├── Dockerfile
│   └── app/
│       ├── main.py
│       ├── models/
│       │   ├── params/
│       │   └── stats/
│       └── requirements.txt
├── panguweather/
├── fuxi/
├── fourcastnet/
└── climax/
```

### 🧩 Common Features

* Unified **FastAPI** endpoints:

  * `/echo`: runs model inference
  * `/healthz`: checks model readiness
* Input: ERA5 NetCDF files (`.nc`)
* Output: Predicted NetCDF files (e.g., temperature, precipitation, pressure)
* Portable via Docker: identical runtime across models

---

## 🚀 Running Models

### Example (GraphCast)

```bash
docker run --rm -p 8000:8000 geoml/graphcast
```

Once running, check health:

```bash
curl http://localhost:8000/healthz
```

Expected:

```json
{"status": "ok"}
```

Run inference:

```bash
curl -X POST "http://localhost:8000/echo" \
  -F "model_name=GraphCast_small-ERA5_1979-2015.npz" \
  -F "file=@/data/ERA5_input.nc;type=application/netcdf" \
  -o prediction_graphcast.nc
```

---

## 🧱 Model Details

| Model                    | Description                                                     | Input Variables                | Forecast Range | Output Variables                   | Framework           |
| ------------------------ | --------------------------------------------------------------- | ------------------------------ | -------------- | ---------------------------------- | ------------------- |
| **GraphCast**            | Graph neural network for 3D weather prediction (DeepMind/ECMWF) | ERA5: T, U, V, Q, geopotential | 6h–10d         | Same as input (multi-level fields) | JAX / Haiku         |
| **Pangu-Weather**        | Transformer-based global forecaster (Huawei)                    | ERA5 multi-level vars          | Up to 15d      | Full atmospheric fields            | PyTorch             |
| **FuXi**                 | Hybrid spectral-transformer model (Tsinghua/CMA)                | ERA5 vars                      | 1–10d          | Core weather vars                  | PyTorch             |
| **FourCastNet**          | Fourier neural operator model (NVIDIA/Caltech)                  | ERA5 1° regridded              | 1–10d          | Pressure, wind, T2m                | PyTorch             |
| **ClimaX / EarthFormer** | General-purpose foundation model for EO data                    | ERA5, CMIP                     | Variable       | Multivariate (custom)              | PyTorch / Lightning |

---

## 🧮 Evaluation Workflow

Each model’s output is validated against **ERA5 reanalysis** or **station data** using both traditional and extreme-aware metrics.

### 1️⃣ Preprocessing

* Regrid all outputs to a common spatial resolution (e.g., 1.0°)
* Align time coordinates for lead times (e.g., 6h, 24h, 72h, …)
* Extract variables of interest (`tp`, `t2m`, `u10`, `v10`, etc.)

### 2️⃣ Metrics for Overall Performance

| Metric   | Description                                 |
| -------- | ------------------------------------------- |
| **RMSE** | Mean squared error for continuous variables |
| **ACC**  | Anomaly correlation coefficient             |
| **MAE**  | Mean absolute error                         |

### 3️⃣ Extreme-Aware Metrics

| Metric                                     | Purpose                                             |
| ------------------------------------------ | --------------------------------------------------- |
| **MCC (Matthews Correlation Coefficient)** | Balanced classification skill under class imbalance |
| **CSI (Critical Success Index)**           | Hit rate for event detection                        |
| **ROC / AUC**                              | Model discrimination ability (hit vs. false alarm)  |
| **BSS (Brier Skill Score)**                | Probabilistic forecast reliability                  |
| **RPSS (Ranked Probability Skill Score)**  | Multi-category probabilistic performance            |

### 4️⃣ Example Evaluation Command (Python)

```python
from sklearn.metrics import matthews_corrcoef, roc_auc_score
import numpy as np

y_true = np.load("true_extreme.npy")
y_pred = np.load("pred_extreme.npy")

mcc = matthews_corrcoef(y_true, y_pred > 0.9)
roc = roc_auc_score(y_true, y_pred)
print(f"MCC={mcc:.3f}, ROC AUC={roc:.3f}")
```

---

## 🧩 Model Integration Example

You can integrate multiple model containers in a single evaluation pipeline using **docker-compose**:

```yaml
version: "3.9"
services:
  graphcast:
    image: geoml/graphcast
    ports: ["8001:8000"]

  panguweather:
    image: geoml/panguweather
    ports: ["8002:8000"]

  fuxi:
    image: geoml/fuxi
    ports: ["8003:8000"]
```

This setup allows you to run:

```bash
curl http://localhost:8001/echo  # GraphCast
curl http://localhost:8002/echo  # PanguWeather
```

and compare predictions automatically.

---

## 🧪 Data Sources

| Dataset                                  | Description                                            | Resolution | Period       | Access                                                  |
| ---------------------------------------- | ------------------------------------------------------ | ---------- | ------------ | ------------------------------------------------------- |
| **ERA5 Reanalysis**                      | ECMWF global reanalysis (used for training/validation) | 0.25°      | 1940–present | [CDS API](https://cds.climate.copernicus.eu/api-how-to) |
| **ERA5-Land / Observations**             | Used for regional downscaling and ground validation    | 0.1°       | 1981–present | Same as above                                           |
| **Gauge-based Precipitation (optional)** | Point-scale validation of heavy rainfall               | Variable   | 2000–present | E-OBS / GHCN                                            |

---

## 📊 Output Analysis

Outputs are stored as `.nc` files:

```
/outputs/
├── GraphCast_2024-01-01_10d.nc
├── PanguWeather_2024-01-01_10d.nc
└── FuXi_2024-01-01_10d.nc
```

A post-processing notebook (`/notebooks/evaluation.ipynb`) will:

* Compare model performance per variable and region
* Visualize probability maps of extremes
* Compute extreme quantile biases (e.g., 95th, 99th percentile)

---

## 🖼️ Visualization Example

You can plot results using `matplotlib` or `xarray`:

```python
import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset("outputs/GraphCast_2024-01-01_10d.nc")
ds['tp'].isel(time=0).plot()
plt.title("GraphCast 24h Precipitation Forecast")
plt.show()
```

---

## 🧰 Troubleshooting

| Issue                                    | Fix                                                    |
| ---------------------------------------- | ------------------------------------------------------ |
| Model container fails to load checkpoint | Check `app/models/params/` path                        |
| “python-multipart” missing               | `pip install python-multipart`                         |
| Slow inference                           | Ensure GPU support is enabled in Docker                |
| Output file missing variables            | Confirm matching input variable list and model version |

---

## 🔗 References

* **Olivetti & Messori (2024)** – *Advances and Prospects of Deep Learning for Medium-Range Extreme Weather Forecasting*
* **Materia et al. (2024)** – *AI for Climate Prediction of Extremes (WIREs Climate Change)*
* **Lam et al. (2023)** – *GraphCast: Learning Skillful Medium-Range Global Weather Forecasting*
* **Bi et al. (2023)** – *Pangu-Weather: A Transformer-Based Forecasting Model*
* **Zhong et al. (2023)** – *FuXi: Global Weather Forecasting with AI*
* **Pathak et al. (2022)** – *FourCastNet: Learning the Weather with Fourier Neural Operators*

---

## 🧾 License

© 2025 Vasileios Vatellis — **GeoML-Lab Initiative**
All models and configurations are distributed under research licenses of their respective institutions.
