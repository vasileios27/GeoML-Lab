# 🌍 Tutorial 01 — Getting Started with Earth Observation (EO) in Python

## 1. Create and Activate a Virtual Environment

We’ll use `venv` and `pip`, since this is the most common setup on servers.

```bash
# Step 1: Create a new environment
python3 -m venv eo_env

# Step 2: Activate the environment
source eo_env/bin/activate

# Step 3: Upgrade pip
pip install --upgrade pip
```

---

## 2. Install Essential Packages

We’ll install the core tools for EO data handling, visualization, and Jupyter Notebooks:

```bash
pip install xarray netCDF4 matplotlib notebook
```

Explanation:

* `xarray` → work with ERA5 and NetCDF data easily
* `netCDF4` → backend for reading ERA5 files
* `matplotlib` → plotting maps/time series
* `notebook` → interactive Jupyter Notebook environment

---

## 3. Example ERA5 Data

For this tutorial, a small **ERA5 test dataset** is already provided in the Git repository.
After cloning the repo, you’ll find the file inside the `data/` folder:

```
data/era5_sample.nc
```

---

## 4. Start Jupyter Notebook

From inside the tutorial folder, run:

```bash
jupyter notebook
```

This will open a Jupyter interface in your browser.
Create a new notebook: **Python 3 (ipykernel)**.

---

## 5. Explore ERA5 Data in the Notebook

Paste the following code into a notebook cell:

```python
import xarray as xr
import matplotlib.pyplot as plt

# Load the NetCDF file
ds = xr.open_dataset("data/era5_sample.nc")

# === Inspect the dataset ===
print(ds)               # Overview: variables, dimensions, attributes
print(ds.data_vars)     # List of available variables
print(ds.coords)        # Coordinates (time, latitude, longitude, etc.)

# === Check the time dimension ===
print("Available times:", ds.time.values)      # All timestamps
print("First time:", ds.time.values[0])        # First timestep
print("Last time:", ds.time.values[-1])        # Last timestep
print("Number of timesteps:", ds.dims['time']) # Length of the time dimension

# === Inspect one variable ===
t2m = ds['t2m']
print(t2m)              # Metadata (units, shape, etc.)

# === Look at a single pixel ===
example_pixel = t2m.sel(latitude=37.98, longitude=23.72, method="nearest")
print("Pixel time-series at Athens (37.98N, 23.72E):")
print(example_pixel.values)

# === Plot the first timestep ===
t2m.isel(time=0).plot()
plt.title("ERA5 2m Temperature (First timestep)")
plt.show()
```

---

### 🔑 What you learned in this tutorial

* How to create and activate a Python environment with `venv`
* How to install EO packages and Jupyter Notebook
* How to start Jupyter and run a notebook
* How to open and explore an ERA5 NetCDF file with `xarray`
* How to plot your first ERA5 map

---

### 🔑 What each command does

* `print(ds)` → prints a summary of the dataset (variables, dimensions, attributes).
* `ds.data_vars` → shows the available variables (e.g., `t2m`, `u10`, `v10`).
* `ds.coords` → lists coordinates like time, latitude, longitude.
* `ds.time.values` → prints all available time steps.
* `ds.dims['time']` → gives number of time steps.
* `.sel(latitude=…, longitude=…)` → extracts data at a specific point (nearest pixel).
* `.isel(time=0)` → selects the first timestep for plotting.
---
