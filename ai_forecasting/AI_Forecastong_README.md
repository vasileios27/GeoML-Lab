
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


<p align="center"> <img src="../plots/GeoML_API_Pipeline.png)" alt="API Pipeline Diagram" width="700"/> </p>


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

| Model                             | Institution / Developer | Input Data                 | Forecast Range | Strengths                                                          | Known Limitations                    | Reference                  |
| --------------------------------- | ----------------------- | -------------------------- | -------------- | ------------------------------------------------------------------ | ------------------------------------ | -------------------------- |
| **GraphCast**                     | DeepMind × ECMWF        | ERA5 Reanalysis            | 6 h → 10 days  | Excellent global skill; very fast inference                        | Underestimates heavy rainfall        | *Lam et al., 2023*         |
| **Pangu-Weather**                 | Huawei Noah’s Ark Lab   | ERA5 (0.25°)               | Up to 15 days  | High skill at all levels; performs well for winds                  | Smooths local extremes               | *Bi et al., 2023*          |

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
