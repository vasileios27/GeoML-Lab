# GeoML-Lab
GeoML is a repository dedicated to exploring and advancing machine learning applications in Earth observation.
This lab serves as a collection of projects, tutorials, and experiments focused on processing multi-spectral and 
multi-temporal remote sensing data using state-of-the-art deep learning techniques. From building basic autoencoders 
for grayscale imagery to developing sophisticated convolutional and 3D autoencoders for multi-channel, time-series data, 
GeoML-Lab aims to empower researchers and practitioners to unlock the full potential of Earth observation in environmental 
monitoring, land cover classification, and beyond. Contributions and collaborations are warmly welcomed!

## 🌍 ERA5 Data Pipeline: A Starting Point for Climate-Driven ML

As part of this growing initiative, we have begun developing practical workflows for working with key Earth observation datasets. One of the first components of this effort is the [era5_data_pipeline](https://github.com/vasileios27/GeoML-Lab/tree/main/era5_data_pipeline) folder, which contains a complete pipeline for downloading, processing, and preparing ERA5 reanalysis data. This includes automated data acquisition scripts, preprocessing routines, and utilities designed to streamline the use of climate reanalysis data in machine learning workflows.

<p align="center"> <img src="plots/era5_pipline.png" alt="ERA5 Data Pipeline Diagram" width="700"/> </p>
Figure: Overview of the ERA5 data pipeline, from acquisition via Copernicus to the generation of machine learning-ready datasets. The pipeline includes data extraction, NetCDF handling, merging, and regional preprocessing for Europe.


## Comparative Forecasting of Extreme Weather: AI Models

The project focuses on the evaluation and application of advanced AI models for forecasting extreme weather events, with an emphasis on severe precipitation. These models will be compared against each other to assess their relative performance. Using long-term reanalysis datasets such as ERA5, the goal is to train and test deep learning architectures capable of predicting rare and intense phenomena. Ultimately, the project aims to measure their accuracy under real-world extreme conditions and explore their potential integration into future early-warning systems.

Perfect — your README introduction already establishes the purpose clearly.
Here’s a continuation you can paste directly below it, including a well-structured **AI model comparison table** and a **link placeholder** for your detailed model documentation.

---

### AI Models Selected for Medium-Range Extreme Forecasting

The following AI models will be evaluated for their capability to forecast **severe precipitation and other extreme weather events** within the **medium-range (1–15 days)** window.
Each model was selected based on its performance in recent peer-reviewed studies and its potential for transferability to reanalysis-driven training (e.g., ERA5).

| Model                             | Institution / Developer   | Input Data                   | Forecast Range | Strengths                                                             | Known Limitations                                                        | Reference                         |
| --------------------------------- | ------------------------- | ---------------------------- | -------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------ | --------------------------------- |
| **GraphCast**                     | DeepMind × ECMWF          | ERA5 Reanalysis              | 6 h → 10 days  | Strong global generalization; fast inference; open-source baseline    | Underestimates heavy rainfall; coarse resolution for convective extremes | *Lam et al., 2023*                |
| **Pangu-Weather**                 | Huawei Noah’s Ark Lab     | ERA5 (0.25°)                 | Up to 15 days  | High skill at surface/upper-air levels; better extreme-wind detection | Requires large compute; some smoothing of precipitation tails            | *Bi et al., 2023*                 |

---

### Detailed Model Instructions and Usage

A full technical overview—including **setup guides**, **input/output formats**, and **evaluation workflows**—is provided in the supplementary documentation:

👉 [**Model Documentation and Implementation Guide**](https://github.com/vasileios27/GeoML-Lab/tree/main/AI_Model_Guide.md)

That page contains:

* Installation and environment setup for each model
* Data preprocessing workflow using ERA5 reanalysis
* Evaluation metrics (MCC, CSI, ROC, BSS, RPSS)
* Benchmark scripts for comparing extreme-forecast performance


---

© 2025 — Developed as part of the GeoML-Lab initiative.