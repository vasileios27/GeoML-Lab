# import xarray as xr
# import numpy as np

# path_gc = "/home/vasileios/dataStorage2/models_output/graphcast/graphcast-target1970010200-forecastD1.grib"

# ds_tp = xr.open_dataset(
#     path_gc,
#     engine="cfgrib",
#     backend_kwargs={"filter_by_keys": {"shortName": "tp"}},
# )

# tp_all = ds_tp["tp"]             # (time, step, lat, lon)
# valid_time_all = ds_tp["valid_time"]  # (time, step)

# # 1) Choose the LAST time in the dataset (time index 1)
# tp_time_last = tp_all.isel(time=-1)          # -> (step, lat, lon)
# vt_time_last = valid_time_all.isel(time=-1)  # -> (step,)

# print("vt_time_last:", vt_time_last.values)

# # 2) Choose the LAST step (D1, valid at 1970-01-02 00:00)
# tp_gc_D1 = tp_time_last.isel(step=-1)        # -> (lat, lon)
# vt_gc_D1 = vt_time_last.isel(step=-1)        # scalar datetime

# print("GraphCast D1 valid_time:", vt_gc_D1.values)
# print("tp_gc_D1 shape:", tp_gc_D1.shape)
# print("tp_gc_D1 finite count:", np.isfinite(tp_gc_D1.values).sum())


# era5_path = "/home/vasileios/dataStorage/GR_tp.nc"
# ds_era5 = xr.open_dataset(era5_path)

# tp_era5_all = ds_era5["tp"]  # dims: ('valid_time', 'latitude', 'longitude') or similar

# tp_era5_D1 = tp_era5_all.sel(valid_time=vt_gc_D1.values, method="nearest")
# print("ERA5 D1 shape:", tp_era5_D1.shape)
# print("ERA5 time used:", tp_era5_D1["valid_time"].values)


# if "lat" in tp_era5_D1.dims:
#     tp_era5_D1 = tp_era5_D1.rename(lat="latitude", lon="longitude")

# tp_gc_D1_reg = tp_gc_D1.interp(
#     latitude=tp_era5_D1.latitude,
#     longitude=tp_era5_D1.longitude,
# )

# print("tp_gc_D1_reg shape:", tp_gc_D1_reg.shape)
# print("tp_gc_D1_reg finite count:", np.isfinite(tp_gc_D1_reg.values).sum())


# diff = tp_gc_D1_reg - tp_era5_D1
# mean_fcst = float(tp_gc_D1_reg.mean().values)
# mean_era5 = float(tp_era5_D1.mean().values)
# bias = float(diff.mean().values)
# rmse = float(np.sqrt((diff**2).mean().values))

# print("mean_fcst:", mean_fcst)
# print("mean_era5:", mean_era5)
# print("bias:", bias)
# print("rmse:", rmse)


# import cfgrib
# import numpy as np

# path_gc = "/home/vasileios/dataStorage2/models_output/graphcast/graphcast-target1970010200-forecastD1.grib"

# datasets = cfgrib.open_datasets(path_gc)

# for i, ds in enumerate(datasets):
#     print(f"\n=== GROUP {i} ===")
#     print("Variables:", list(ds.data_vars))

#     for var_name, da in ds.data_vars.items():
#         print(f"\n  -> Variable: {var_name}")
#         print(f"     dims:  {da.dims}")
#         print(f"     shape: {da.shape}")

#         dims = da.dims
#         arr = da.values

#         # Case 1: has time and step (e.g. tp, maybe some 4D fields)
#         if "time" in dims and "step" in dims:
#             time_axis = dims.index("time")
#             step_axis = dims.index("step")

#             # sum over all non-time/step axes
#             non_ts_axes = tuple(
#                 idx for idx, d in enumerate(dims) if d not in ("time", "step")
#             )

#             finite_counts = np.isfinite(arr).sum(axis=non_ts_axes)  # -> (time, step)
#             print("     finite count per (time, step):")
#             print(finite_counts)

#         # Case 2: has only time
#         elif "time" in dims:
#             time_axis = dims.index("time")
#             non_t_axes = tuple(
#                 idx for idx, d in enumerate(dims) if d != "time"
#             )
#             finite_counts = np.isfinite(arr).sum(axis=non_t_axes)  # -> (time,)
#             print("     finite count per time index:")
#             print(finite_counts)

#         # Case 3: has only step
#         elif "step" in dims:
#             step_axis = dims.index("step")
#             non_s_axes = tuple(
#                 idx for idx, d in enumerate(dims) if d != "step"
#             )
#             finite_counts = np.isfinite(arr).sum(axis=non_s_axes)  # -> (step,)
#             print("     finite count per step index:")
#             print(finite_counts)

#         # Case 4: no time/step (e.g. static fields, 2D fields)
#         else:
#             total_finite = np.isfinite(arr).sum()
#             print("     total finite values:", int(total_finite))

# print("\nDone.")

import xarray as xr
import cfgrib
import numpy as np
import matplotlib.pyplot as plt

path_gc = "/home/vasileios/dataStorage2/models_output/graphcast/graphcast-target1970010306-forecastD1.grib"

print("\n=== Opening ONLY tp dataset ===")
ds_tp = xr.open_dataset(
    path_gc,
    engine="cfgrib",
    backend_kwargs={"filter_by_keys": {"shortName": "tp"}}
)

print(ds_tp)

# Extract tp
tp = ds_tp["tp"]   # dims: (time, step, lat, lon)
valid_time = ds_tp["valid_time"]

print("\n=== TP shape ===")
print(tp.shape)

print("\n=== Valid times ===")
vt_vals = valid_time.values
print(vt_vals)

# Identify which time/step combinations have finite values
print("\n=== Finite value count per (time, step) ===")
finite_table = np.sum(np.isfinite(tp.values.reshape(2, 5, -1)), axis=2)
print(finite_table)

# -------- VISUALIZE EACH TIME/STEP -------- #
for t in range(tp.shape[0]):
    for s in range(tp.shape[1]):

        field = tp.isel(time=t, step=s)
        vt = valid_time.isel(time=t, step=s).values

        finite_count = int(np.isfinite(field.values).sum())

        print(f"\nPlotting time={t}, step={s}, valid_time={vt}, finite={finite_count}")

        plt.figure(figsize=(8,4))
        field.plot()
        plt.title(f"GraphCast tp | time={t}, step={s}\nvalid_time={vt}\nfinite={finite_count}")
        plt.tight_layout()
        plt.savefig(f"tp_graphcast_t{t}_s{s}.png")
        plt.close()

print("\nPlots saved.")
