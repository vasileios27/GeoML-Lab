

import pandas as pd
from pathlib import Path
from datetime import timedelta
import xarray as xr
import cfgrib
import numpy as np
import matplotlib.pyplot as plt
import re
import glob

xr.set_options(use_new_combine_kwarg_defaults=True)




def parse_filename_info(fname):
    """
    Extract model, target_datetime, lead_days from filename.
    Examples:
      fourcastnet-target1970010200-forecastD1.grib
      graphcast-target1970010200-forecastD1.grib
      fourcastnetv2-small-target1978010506-forecastD10.grib
    """
    base = fname.split("/")[-1]

    # model name from prefix
    if base.startswith("fourcastnetv2"):
        model = "fourcastnetv2"
    elif base.startswith("fourcastnet"):
        model = "fourcastnet"
    elif base.startswith("graphcast"):
        model = "graphcast"
    else:
        model = "unknown"

    # extract target datetime: the bit between 'target' and '-forecast'
    m_time = re.search(r"target(\d{10})", base)
    if not m_time:
        raise ValueError(f"Cannot parse target time from {base}")
    tstr = m_time.group(1)  # e.g. '1970010200'
    target_datetime = pd.to_datetime(tstr, format="%Y%m%d%H")

    # extract lead days from 'forecastD<number>'
    m_lead = re.search(r"forecastD(\d+)", base)
    if m_lead:
        lead_days = int(m_lead.group(1))
    else:
        lead_days = None

    return model, target_datetime, lead_days

def build_catalog(root):
    """
    Build a catalog for one model from a given folder.

    root: folder that contains ONLY one model's GRIB files, e.g.
          /home/.../models_output/graphcast

    Returns a DataFrame with:
      - path
      - target_datetime
    """
    files = sorted(Path(root).glob("*.grib"))
    records = []

    for f in files:
        name = f.name
        # extract targetYYYYMMDDHH from filename
        m = re.search(r"target(\d{10})", name)
        if not m:
            continue
        tstr = m.group(1)  # e.g. 1970010200
        target_datetime = pd.to_datetime(tstr, format="%Y%m%d%H")

        records.append({
            "path": str(f),
            "target_datetime": target_datetime,
        })

    return pd.DataFrame(records)



def load_tp_from_grib(path):
    """Return the tp DataArray from the FourCastNet GRIB file."""
    datasets = cfgrib.open_datasets(path)
    ds_tp = datasets[10]   # tp is ALWAYS in group 10 for these files
    return ds_tp["tp"], ds_tp["valid_time"]

def load_tp_fourcastnet(path, target_time=None):
    """
    Wrapper so FourCastNet matches the same interface as GraphCast:
    returns (tp_fcst(step, lat, lon), valid_times(step)).
    """
    tp, valid_times = load_tp_from_grib(path)  # your existing function
    return tp, valid_times


def load_tp_graphcast(path, target_time):
    """
    Load GraphCast total precipitation (tp) for the forecast that verifies at `target_time`.

    Parameters
    ----------
    path : str
        Path to the GraphCast GRIB file, e.g.
        "/home/.../graphcast-target1970010200-forecastD1.grib"
    target_time : np.datetime64 or pandas.Timestamp
        Target valid time (from your catalog, e.g. row['target_datetime']).

    Returns
    -------
    tp_fcst : xarray.DataArray
        Total precipitation with dims (step, latitude, longitude)
        for the chosen GraphCast forecast.
    valid_times_1d : xarray.DataArray
        1D array of valid_time for each step (dims: step)
        corresponding to that forecast.
    """
    # Open all GRIB groups
    datasets = cfgrib.open_datasets(path)

    # Group 5 is the one with tp(time, step, lat, lon)
    ds_tp = datasets[5]
    tp_all = ds_tp["tp"]                # (time, step, lat, lon)
    valid_time_all = ds_tp["valid_time"]  # (time, step)

    # Ensure target_time is np.datetime64 for comparison
    target_time = np.datetime64(target_time)

    # Find which (time, step) pairs match the target_time
    vt_vals = valid_time_all.values  # shape (ntime, nstep)
    idx = np.argwhere(vt_vals == target_time)

    if idx.size == 0:
        raise ValueError(
            f"Target time {target_time} not found in GraphCast valid_time "
            f"for file {path}."
        )

    # Take the first match (time_idx, step_idx)
    time_idx, step_idx = idx[0]

    # We want the full forecast sequence for that time_idx (all steps),
    # not just the single step that hits the target.
    tp_fcst = tp_all.isel(time=time_idx)             # -> (step, lat, lon)
    valid_times_1d = valid_time_all.isel(time=time_idx)  # -> (step,)

    return tp_fcst, valid_times_1d



def evaluate_single_case_extended(fcst_path, target_time, ds_era5, tp_threshold, model="fourcastnet"):
    """
    Evaluate one forecast (FourCastNet or GraphCast) against ERA5 for a single case.

    Parameters
    ----------
    fcst_path : str
        Path to the model GRIB file.
    target_time : datetime-like
        Target valid time (from filename / catalog).
    ds_era5 : xarray.Dataset
        ERA5 dataset with 'tp' and coordinate 'valid_time' over Greece.
    tp_threshold : xarray.DataArray
        Climatological q95 threshold mask from tp_q95_alltime.nc
        with dims ('latitude', 'longitude') on global grid.
    model : {"fourcastnet", "graphcast"}
        Which model to load.

    Returns
    -------
    metrics : dict
        Scalar metrics.
    tp_fcst_D1_reg : xarray.DataArray
        D1 forecast precipitation regridded/interpolated to ERA5 Greece grid.
    tp_era5_D1 : xarray.DataArray
        ERA5 tp at the same valid time and domain.
    """
    # ---- 1. Load model forecast depending on 'model' ----
    if model == "fourcastnet":
        tp_fcst, valid_times = load_tp_fourcastnet(fcst_path, target_time)
    elif model == "graphcast":
        tp_fcst, valid_times = load_tp_graphcast(fcst_path, target_time)
    else:
        raise ValueError(f"Unknown model: {model}")

    # tp_fcst: (step, latitude, longitude)
    # valid_times: (step,)

    # Last step = D1
    tp_fcst_D1 = tp_fcst.isel(step=-1)
    vt_D1 = valid_times.isel(step=-1)

    # ---- 2. Load ERA5 at same valid_time ----
    tp_era5_D1 = ds_era5["tp"].sel(valid_time=vt_D1.values, method="nearest")

    # ---- 3. Align lat/lon names and grids ----
    if "lat" in tp_era5_D1.dims:
        tp_era5_D1 = tp_era5_D1.rename(lat="latitude", lon="longitude")

    # Interpolate model to ERA5 Greece grid (robust to tiny coord differences)
    tp_fcst_D1_reg = tp_fcst_D1.interp(
        latitude=tp_era5_D1.latitude,
        longitude=tp_era5_D1.longitude
    )

    if tp_fcst_D1_reg.shape != tp_era5_D1.shape:
        raise ValueError(
            f"[{model}] Shape mismatch after alignment: "
            f"fcst {tp_fcst_D1_reg.shape}, era5 {tp_era5_D1.shape}"
        )

    # ---- 4. Basic metrics ----
    diff = tp_fcst_D1_reg - tp_era5_D1

    mean_fcst = float(tp_fcst_D1_reg.mean().values)
    mean_era5 = float(tp_era5_D1.mean().values)
    bias = float(diff.mean().values)
    rmse = float(np.sqrt((diff ** 2).mean().values))

    # ---- 5. Spatial correlation ----
    f = tp_fcst_D1_reg.values.ravel()
    o = tp_era5_D1.values.ravel()
    mask_corr = np.isfinite(f) & np.isfinite(o)
    if mask_corr.sum() > 10:
        corr = float(np.corrcoef(f[mask_corr], o[mask_corr])[0, 1])
    else:
        corr = np.nan

    # ---- 6. Threshold mask and extreme metrics ----
    tp_threshold_GR = tp_threshold.interp(
        latitude=tp_era5_D1.latitude,
        longitude=tp_era5_D1.longitude
    )

    thr_vec = tp_threshold_GR.values.ravel()
    f_vec = f
    o_vec = o

    mask = np.isfinite(f_vec) & np.isfinite(o_vec) & np.isfinite(thr_vec)

    if mask.sum() == 0:
        # Fail loudly instead of returning all NaNs
        raise RuntimeError(f"[{model}] No valid grid points for extreme metrics (mask is empty).")

    f_valid = f_vec[mask]
    o_valid = o_vec[mask]
    thr_valid = thr_vec[mask]

    f_ext = f_valid > thr_valid
    o_ext = o_valid > thr_valid

    hits = int(np.sum(f_ext & o_ext))
    misses = int(np.sum(~f_ext & o_ext))
    false_alarms = int(np.sum(f_ext & ~o_ext))

    denom_csi = hits + misses + false_alarms
    denom_pod = hits + misses
    denom_far = hits + false_alarms

    csi = hits / denom_csi if denom_csi > 0 else np.nan
    pod = hits / denom_pod if denom_pod > 0 else np.nan
    far = false_alarms / denom_far if denom_far > 0 else np.nan

    metrics = {
        "model": model,
        "target_time": np.datetime64(target_time),
        "valid_time_grib": np.datetime64(vt_D1.values),
        "era5_time_used": np.datetime64(tp_era5_D1["valid_time"].values),
        "mean_fcst_tp": mean_fcst,
        "mean_era5_tp": mean_era5,
        "bias": bias,
        "rmse": rmse,
        "corr": corr,
        "thr_source": "tp_q95_alltime.nc",
        "thr_mean_used": float(np.nanmean(thr_valid)),
        "hits": hits,
        "misses": misses,
        "false_alarms": false_alarms,
        "csi": csi,
        "pod": pod,
        "far": far,
    }

    return metrics, tp_fcst_D1_reg, tp_era5_D1




def plot_tp_case(tp_fcst_D1, tp_era5_D1, vmax=None, title_suffix=""):
    """
    Plot:
    - ERA5 total precipitation
    - FourCastNet D1 total precipitation
    - Forecast - ERA5 difference
    """
    if vmax is None:
        # set upper color limit from joint distribution (e.g. 99th percentile)
        combined = np.concatenate([
            tp_fcst_D1.values.ravel(),
            tp_era5_D1.values.ravel()
        ])
        vmax = np.nanpercentile(combined, 99)

    diff = tp_fcst_D1 - tp_era5_D1

    fig, axes = plt.subplots(1, 3, figsize=(15, 4), constrained_layout=True)

    # ERA5
    im0 = tp_era5_D1.plot(
        ax=axes[0],
        vmax=vmax,
        vmin=0,
        add_colorbar=True
    )
    axes[0].set_title(f"ERA5 tp [m]{title_suffix}")

    # Forecast
    im1 = tp_fcst_D1.plot(
        ax=axes[1],
        vmax=vmax,
        vmin=0,
        add_colorbar=True
    )
    axes[1].set_title(f"FourCastNet D1 tp [m]{title_suffix}")

    # Difference
    im2 = diff.plot(
        ax=axes[2],
        add_colorbar=True
    )
    axes[2].set_title(f"Forecast - ERA5 [m]{title_suffix}")

    for ax in axes:
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

    plt.savefig("tp_case_plot.png")


if __name__ == "__main__":
    
    # usage
    cat_four = build_catalog("/home/vasileios/dataStorage2/models_output/fourcastnet")
    catalog_gc   = build_catalog("/home/vasileios/dataStorage2/models_output/graphcast")
    #print(cat_gc.head())

    era5_path = "/home/vasileios/dataStorage/GR_tp.nc"
    ds_era5 = xr.open_dataset(era5_path)
    # print(ds_era5)
    # print(ds_era5.data_vars)

    # Load climatological tp 95th percentile mask
    thr_path = "/home/vasileios/Documents/GeoML-Lab/extremes/tp_q95_alltime.nc"
    ds_thr = xr.open_dataset(thr_path)

    # Pick the variable name (adapt if it's different)
    if "tp_q95" in ds_thr.data_vars:
        tp_threshold = ds_thr["tp_q95"]
    else:
        tp_threshold = list(ds_thr.data_vars.values())[0]

    # Make sure lat/lon names match what we use later
    if "lat" in tp_threshold.dims:
        tp_threshold = tp_threshold.rename(lat="latitude", lon="longitude")

    loader_map = {
        "fourcastnet": load_tp_fourcastnet,
        "graphcast": load_tp_graphcast,
        #"fourcastnetv2": load_tp_fourcastnetv2,  # later
    }



    # 3) Loop over all GraphCast files
    all_metrics = []
    for _, row in catalog_gc.iterrows():
        fcst_path = row["path"]
        target_time = row["target_datetime"]

        metrics_gc, tp_gc_D1_reg, tp_era5_D1 = evaluate_single_case_extended(
            fcst_path=fcst_path,
            target_time=target_time,
            ds_era5=ds_era5,
            tp_threshold=tp_threshold,
            model="graphcast",
        )
        all_metrics.append(metrics_gc)

    df_metrics_gc = pd.DataFrame(all_metrics)
    #df_metrics_gc.to_csv("metrics_graphcast_only.csv", index=False)
    print(df_metrics_gc.head())


    #plot_tp_case(tp_fcst_D1, tp_era5_D1, title_suffix=f"\n{metrics['target_time']}")

# import pandas as pd

# path_gc = "/home/vasileios/dataStorage2/models_output/graphcast-target1970010200-forecastD1.grib"
# target_time = pd.to_datetime("1970-01-02 00:00:00")

# tp_gc, vt_gc = load_tp_graphcast(path_gc, target_time)

# print(tp_gc.shape)      # expect: (5, 721, 1440)
# print(vt_gc)    


# path= "/home/vasileios/dataStorage2/models_output/fourcastnet-target1970010200-forecastD1.grib"

# datasets = cfgrib.open_datasets(path)
# # for i, ds in enumerate(datasets):
# #     print(f"\n=== Dataset group {i} ===")
# #     print(ds)

# ds_tp = datasets[10]  # the last group in your printout
# tp = ds_tp["tp"]
# print(tp)