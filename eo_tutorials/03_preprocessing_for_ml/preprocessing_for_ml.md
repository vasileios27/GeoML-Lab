# 🧰 Tutorial 03 — Preprocessing for Machine Learning

In this tutorial, you’ll transform ERA5 data into **ML‑ready arrays**. You will:
- Load a NetCDF file with `xarray`
- Select a target variable (default: `t2m`)
- Create **lag features** (e.g., previous 3 timesteps) for supervised learning
- Reshape from gridded data to a 2D matrix (`[samples, features]`)
- Split into **train/val/test** *by time*
- **Standardize** features using training statistics
- Save arrays to `data/processed/` as `.npy` files (and optionally `.pt` if PyTorch is available)

> **Prerequisites**
> - Completed Tutorial 01 & 02
> - Environment with `xarray`, `numpy`, `matplotlib` (already installed)
> - ERA5 test dataset at `data/era5_sample.nc`

## 📓 Notebook
Run everything interactively here:

➡️ **[03_preprocessing_for_ml.ipynb](03_preprocessing_for_ml.ipynb)**

## 📦 Outputs (created by the notebook)
- `data/processed/X_train.npy`, `y_train.npy`
- `data/processed/X_val.npy`, `y_val.npy`
- `data/processed/X_test.npy`, `y_test.npy`
- `data/processed/stats.npz` *(means, stds for feature scaling)*
- *(optional)* `data/processed/*.pt` if PyTorch is installed

## 🧠 What you’ll learn
- How to turn a spatiotemporal cube into a **tabular ML dataset**
- Why **time‑based splits** matter for forecasting
- How to **standardize** features correctly (fit on train, apply to val/test)

## ▶️ How to run
From your project root (with your virtual environment activated):

```bash
jupyter notebook  # or: jupyter lab
```

Open the notebook and follow the steps. Adjust paths if needed.
