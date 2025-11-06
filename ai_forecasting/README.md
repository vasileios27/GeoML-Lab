
# 🌦️ GeoML-Lab API — Multi-Model Framework

## 🧭 General Description

All supported AI models — including **GraphCast**, **Pangu-Weather**, — are deployed as **individual containers**.
Each container exposes a consistent **FastAPI interface** for inference, health checks, and NetCDF file handling, enabling side-by-side benchmarking and interoperability.

The system architecture is designed for:

* **Modularity:** Swap models without changing the API interface
* **Reproducibility:** Containerized environments ensure consistent dependencies
* **Scalability:** Ready for local, cluster, or cloud-based deployment
* **Transparency:** Each model can be independently validated against ERA5 or observational datasets

---

## 🔁 API Workflow Overview

Each container follows the same pipeline:

1. **Input ingestion** — User uploads a NetCDF file (ERA5 or observational data).
2. **Model selection** — The request specifies the AI model (e.g., `GraphCast`, `Pangu-Weather`).
3. **Inference execution** — The model predicts future atmospheric variables.
4. **Output handling** — Results are returned as NetCDF files, ready for visualization or evaluation.


<p align="center"> <img src="../plots/GeoML_API_Pipeline.png" alt="ERA5 Data Pipeline Diagram" width="700"/> </p>


---

## ⚙️ Comparative Forecasting of Extreme Weather: AI Models

This project focuses on the **evaluation and application of advanced AI models** for forecasting **extreme weather**, with an emphasis on **severe precipitation** and **medium-range (1–15 day)** forecasts.
The models will be compared against each other to assess their skill in predicting rare, high-impact phenomena using **ERA5 reanalysis data**.

Ultimately, the project aims to:

* Measure **accuracy and reliability** under real-world extreme conditions
* Investigate **model bias** for high quantiles (e.g., 95th–99th percentile precipitation)
* Enable **integration into early-warning systems** for hydrometeorological hazards

---

### 📊 AI Models Under Evaluation

Here’s an expanded version of your table with single-level and pressure-level variables added (using exactly the parameters you provided):

| Model           | Input Data      | Forecast Range | Variables — Single Level                                                                                                                                                                                     | Variables — Pressure Level                                        | Reference                                                          |
| --------------- | --------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------- | ------------------------------------------------------------------ |
| **FourCastNet** | ERA5 Reanalysis | 6 h → 10 days  | `10u` (10-m u-wind), `10v` (10-m v-wind), `2t` (2-m temperature), `sp` (surface pressure), `msl` (mean sea-level pressure), `tcwv` (total column water vapour), `100u` (100-m u-wind), `100v` (100-m v-wind) | `t`, `u`, `v`, `z`, `r` at levels **1000, 850, 500, 250, 50 hPa** | [*Pathak et al., 2022*](https://doi.org/10.48550/arXiv.2202.11214) |
| **GraphCast**   | ERA5 Reanalysis | 6 h → 10 days  | `10u`, `10v`, `2t`, `sp`, `msl`, `tcwv`, `100u`, `100v`                                                                                                                                                      | `t`, `u`, `v`, `z`, `r` at levels **1000, 850, 500, 250, 50 hPa** | [*Lam et al., 2023*](https://doi.org/10.1126/science.adi2336)      |

If you also want to note grid/area (since you had them in your snippet), we can add a small footnote like:

* **Grid/Area used in this work:** 0.25° × 0.25°, global (N: 90°, W: 0°, S: −90°, E: 359.75°); product type: *reanalysis*;

---

## 📘 Detailed Model Documentation

Full technical details—including **environment setup**, **inference examples**, **evaluation metrics**, and **benchmark scripts**—are provided in the documentation:

👉 [**AI Model Guide**](https://github.com/vasileios27/GeoML-Lab/blob/main/ai_forecasting/AI_Model_Guide.md)

That document explains:

* Model-specific environment variables and Docker build instructions
* Data preprocessing using **ERA5**
* Model inference endpoints and expected I/O formats
* Recommended **extreme-aware metrics**: MCC, CSI, ROC, BSS, and RPSS

---

## 🧠 Notes

* All models operate via **FastAPI microservices** with consistent endpoints (`/echo`, `/healthz`).
* **NetCDF (.nc)** remains the standard format for all input and output data.
* Containers are designed to run **independently or in parallel**, allowing distributed benchmarking.
* Each container can be deployed via:

  ```bash
  docker run --rm -p 8000:8000 geolab/<model-name>
  ```
* Results can be aggregated and compared through a common evaluation pipeline (to be detailed in `AI_Model_Guide.md`).

---

## 📄 License

© 2025 Vasileios Vatellis — **GeoML-Lab**
Developed as part of the **GeoML-Lab initiative** for advancing AI-driven Earth observation and medium-range extreme weather forecasting.

---
