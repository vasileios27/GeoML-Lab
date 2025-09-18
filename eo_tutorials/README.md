# 🌍 EO Tutorials — Getting Started with Earth Observation in Python

Welcome to the **Earth Observation (EO) tutorial series**.
These tutorials are designed to help new students (with basic Python knowledge) gain hands-on experience with EO data, from the first steps of setting up an environment to building simple machine learning models.

We assume:

* You already have **Linux knowledge**
* You know **basic Python syntax**
* You can use basic command-line tools (`wget`, `git`)

---

## 📘 Tutorial Structure

### 01 — Getting Started with ERA5

* Create and activate a **Python virtual environment** with `venv` + `pip`
* Install essential packages (`xarray`, `netCDF4`, `matplotlib`, etc.)
* Open and explore an **ERA5 NetCDF file**
* Plot your first EO map

👉 Goal: Get your environment ready and explore ERA5 data for the first time.

---

### 02 — Time Series Analysis

* Extract data for a **specific location or region**
* Work with **time-series of ERA5 variables** (e.g., temperature over time)
* Compute **basic statistics** (mean, anomalies, trends)
* Visualize results with line plots

👉 Goal: Learn how to extract useful information from EO datasets over time.

---

### 03 — Preprocessing for Machine Learning

* Reshape ERA5/xarray data into **arrays suitable for ML**
* Handle **missing values** and normalize data
* Split datasets into **training, validation, and test sets**
* Save preprocessed data for later use

👉 Goal: Prepare EO data to be used as input for ML models.

---

### 04 — Basic Machine Learning Model

* Build a simple **PyTorch model**
* Train it on the preprocessed ERA5 data
* Evaluate predictions (e.g., predicting temperature/precipitation trends)
* Visualize model performance

👉 Goal: Learn how to connect EO data with ML, creating a first end-to-end pipeline.

---

## 🎯 Overall Learning Outcomes

By the end of this tutorial series, you will be able to:

1. Work comfortably with EO data in **NetCDF format** using `xarray`.
2. Extract and visualize EO information over space and time.
3. Prepare data for machine learning workflows.
4. Implement and train a **basic ML model** in PyTorch with EO data.

---


