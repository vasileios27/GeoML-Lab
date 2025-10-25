
# 🌍 Tutorial 02 — Time Series Analysis

In this tutorial, you’ll learn how to work with **time-series data from ERA5** in a Jupyter Notebook.
We will:

* Extract data for a specific location
* Explore temporal patterns
* Compute basic statistics
* Visualize results with line plots

---

## 1. Open the Dataset

**Markdown cell:**

We’ll start by opening the same ERA5 test file from the previous tutorial.

**Code cell:**

```python
import xarray as xr
import matplotlib.pyplot as plt

# Open dataset
ds = xr.open_dataset("data/era5_sample.nc")
ds
```

---

## 2. Select a Variable and Location

**Markdown cell:**

Now let’s extract **2m temperature (`t2m`)** for a specific location (Athens, Greece).
We use `.sel()` to select the nearest grid point to given coordinates.

**Code cell:**

```python
# Select 2m temperature
t2m = ds['t2m']

# Example location: Athens, Greece (lat=37.98, lon=23.72)
t2m_point = t2m.sel(latitude=37.98, longitude=23.72, method="nearest")
t2m_point
```

---

## 3. Plot the Time Series

**Markdown cell:**

Let’s plot the temperature values over time at Athens.

**Code cell:**

```python
t2m_point.plot(marker="o", linestyle="-", figsize=(10,4))
plt.title("ERA5 2m Temperature at Athens")
plt.ylabel("Temperature (K)")
plt.xlabel("Time")
plt.show()
```

---

## 4. Compute Basic Statistics

**Markdown cell:**

We can quickly compute the **mean, max, and min temperature**.

**Code cell:**

```python
print("Mean Temperature:", float(t2m_point.mean()))
print("Max Temperature:", float(t2m_point.max()))
print("Min Temperature:", float(t2m_point.min()))
```

---

## 5. Compute Anomalies

**Markdown cell:**

An **anomaly** is the deviation from the mean value.
Let’s calculate and plot anomalies for Athens.

**Code cell:**

```python
t2m_anomaly = t2m_point - t2m_point.mean()

t2m_anomaly.plot(figsize=(10,4))
plt.title("Temperature Anomalies (Athens)")
plt.ylabel("Anomaly (K)")
plt.xlabel("Time")
plt.show()
```

---

## 6. Regional Average (Optional)

**Markdown cell:**

Instead of a single point, we can compute the **regional mean temperature**.
Example: Greece (lat: 34–42, lon: 19–28).

**Code cell:**

```python
t2m_region = t2m.sel(latitude=slice(42, 34), longitude=slice(19, 28))
t2m_mean = t2m_region.mean(dim=["latitude", "longitude"])

t2m_mean.plot(figsize=(10,4))
plt.title("Regional Mean 2m Temperature (Greece)")
plt.ylabel("Temperature (K)")
plt.xlabel("Time")
plt.show()
```

---

## ✅ Summary

By the end of this tutorial, you learned how to:

* Extract data for a location or region
* Work with ERA5 time series
* Compute mean, min, max
* Calculate anomalies
* Visualize time series with matplotlib
