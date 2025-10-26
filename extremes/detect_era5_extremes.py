from pathlib import Path
import re
from typing import Iterable, List, Optional
import xarray as xr
import argparse, os
import numpy as np
from era5tools import find_era5_nc 

def stack_exceedances(exceed: xr.DataArray, value_da: xr.DataArray,
                      time_dim: str) -> "pd.DataFrame":
    """
    Turn a boolean exceedance mask into a tidy DataFrame with
    columns [time, lat, lon, (level,) value]. Requires pandas via xarray.
    """
    # Decide spatial and optional vertical dims
    lat = "lat" if "lat" in exceed.coords else ("latitude" if "latitude" in exceed.coords else None)
    lon = "lon" if "lon" in exceed.coords else ("longitude" if "longitude" in exceed.coords else None)
    dims = [d for d in [time_dim, lat, lon] if d is not None]
    if "level" in exceed.dims:
        dims.append("level")

    # stack to 1D index of events
    stacked_mask = exceed.where(exceed).stack(event=dims).dropna("event")
    if stacked_mask.sizes.get("event", 0) == 0:
        # no extremes
        import pandas as pd
        return pd.DataFrame(columns=[time_dim, "lat", "lon", "level", "value"])

    # get values for the same events
    stacked_val = value_da.where(exceed).stack(event=dims).dropna("event")

    # build DataFrame from the stacked coordinates + values
    df = stacked_mask.event.to_series().reset_index(name="__tmp__").drop(columns="__tmp__")
    df["value"] = stacked_val.values

    # normalize column names
    if lat and lat in df.columns and lat != "lat":
        df.rename(columns={lat: "lat"}, inplace=True)
    if lon and lon in df.columns and lon != "lon":
        df.rename(columns={lon: "lon"}, inplace=True)
    return df


def main():
    ap = argparse.ArgumentParser(description="Identify and load a single ERA5 variable from many yearly NetCDFs.")
    ap.add_argument("--root", required=True, help="Folder containing yearly NetCDF files.")
    ap.add_argument("--var", required=True, help="Variable name to load (e.g., t2m, tp, u10, v10).")
    ap.add_argument("--threshold", required=True, help="Threshold NetCDF path (e.g., tp_q95_alltime.nc).")
    ap.add_argument("--out-csv", required=True, help="Output CSV (appended).")
    ap.add_argument("--save-mask", default="", help="Optional NetCDF path to save the boolean mask (0/1).")
    args = ap.parse_args()

    # keep only GR_total_precipitation_<year>.nc

    # Make sure, that names, and abbreviation have the same result
    if args.var == "tp" or args.var == "total_precipitation": 
        args.var = "total_precipitation"
        abbreviation_var = "tp"
        


    files = find_era5_nc(args.root, variable=args.var)

    # prepare CSV (write header once)
    out_csv = Path(args.out_csv)
    wrote_header = out_csv.exists() and out_csv.stat().st_size > 0

    # load threshold
    thr_ds = xr.open_dataset(args.threshold)
    thr = thr_ds["tp_q95_alltime"] 
    # pick threshold var (prefer same base name)

    for f in files:
        # open with Dask + chunks (avoid loading into RAM)
        ds = xr.open_dataset(f)
        # pick the variable present in this file
    
        da = ds[abbreviation_var]


        # lazy boolean mask; compute only when needed
        exceed = (da >= thr).rename(f"{args.var}_exceed_q95")

        # materialize this small chunk to rows and append to CSV
        df = stack_exceedances(exceed, da, time_dim="valid_time")
        if df.empty:
            continue

        # append with header on first write only
        df.to_csv(out_csv, mode="a", index=False, header=(not wrote_header))
        wrote_header = True

        # Be nice to the scheduler
        ds.close()

    print(f"Done. CSV → {out_csv}")


if __name__ == "__main__":
    main()