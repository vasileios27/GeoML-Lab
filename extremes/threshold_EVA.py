
import numpy as np
import pandas as pd
import xarray as xr
from pyextremes import EVA

# --- load data ---
ds = xr.open_dataset("/Users/vasileios_vatellis/Documents/GeoML-Lab/analysis/GR_tp.nc")  # your file
# Example: tp(time, lat, lon)
tp = ds["tp"]

log_file = open("EVA_grib_summary.txt", "w")


# Reuse coordinates from original dataset
lats = ds["latitude"]
lons = ds["longitude"]

# Helper: make an empty DataArray with same lat/lon grid
def make_empty_da(var_name):
    return xr.DataArray(
        np.full((len(lats), len(lons)), np.nan),
        coords={"latitude": lats, "longitude": lons},
        dims=("latitude", "longitude"),
        name=var_name,
    )

# 10-year return level dataset
rl10_da = make_empty_da("rl10")
ds_threshold_10 = xr.Dataset({"rl10": rl10_da})

# 20-year return level dataset
rl20_da = make_empty_da("rl20")
ds_threshold_20 = xr.Dataset({"rl20": rl20_da})

# 50-year return level dataset
rl50_da = make_empty_da("rl50")
ds_threshold_50 = xr.Dataset({"rl50": rl50_da})


for i_lat in ds["latitude"].values:
    for i_lon in ds["longitude"].values:
        tp_point = tp.sel(latitude=i_lat, longitude=i_lon)
        time_index = pd.to_datetime(tp_point["valid_time"].values)

        # build a 1D pandas Series
        s = pd.Series(tp_point.values, index=time_index, name="tp").dropna()
        model = EVA(s)
        model.get_extremes(
            method="BM",
            extremes_type="high",
            block_size="365.2425D",
        )

        model.fit_model()
        summary = model.get_summary(
            return_period=[10, 20, 50],
            alpha=0.95,
            n_samples=1000
        )
        #print(summary)

        rl10_val = summary.loc[10.0, "return value"]
        rl20_val = summary.loc[20.0, "return value"]
        rl50_val = summary.loc[50.0, "return value"]

        ds_threshold_10["rl10"].loc[i_lat, i_lon] = rl10_val
        ds_threshold_20["rl20"].loc[i_lat, i_lon] = rl20_val
        ds_threshold_50["rl50"].loc[i_lat, i_lon] = rl50_val

        log_file.write("===========================================\n")
        log_file.write(f"Grid point (i_lat={i_lat}, i_lon={i_lon})\n")
        log_file.write(summary.to_string())         # pretty printed DataFrame
        log_file.write("\n\n")



ds_threshold_10.to_netcdf("GR_tp_threshold_rl10_BM.nc")
ds_threshold_20.to_netcdf("GR_tp_threshold_rl20_BM.nc")
ds_threshold_50.to_netcdf("GR_tp_threshold_rl50_BM.nc")

# -------------------------------------------------------------------
# Return levels (rl10, rl20, rl50, etc.)
#
# rl10  = 10-year return level
# rl20  = 20-year return level
# rl50  = 50-year return level
#
# What this means:
# A "return level" is the magnitude of precipitation expected to be
# exceeded once, on average, every X years.
# Example: rl10 is the precipitation amount associated with an
# event that statistically occurs once every 10 years.
#
# Interpretation:
# - rl10  describes moderately rare extreme rainfall once every 10 years
# - rl20  describes more rare, stronger events once every 20 years
# - rl50  describes very rare, very strong extremes once every 50 years
#
# Higher return period → larger rainfall → more extreme.
#
# These return levels are computed from the GEV distribution fitted
# to the annual block maxima (BM) at each grid point.
# -------------------------------------------------------------------
