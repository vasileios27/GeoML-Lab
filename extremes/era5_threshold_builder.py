#!/usr/bin/env python3
#!/usr/bin/env python3
"""
ERA5 Threshold Builder (per-grid 95th percentile)

This script scans a directory of yearly ERA5 NetCDF files named like
`GR_<variable>_Y<year>.nc` (e.g., `GR_total_precipitation_Y1996.nc`),
loads only the files for the requested variable, and computes the **95th
percentile threshold at each grid point** across **all available time steps**.
It then saves the threshold field to NetCDF.

What “threshold per grid point” means
-------------------------------------
For each latitude/longitude (and level, if present), we aggregate the full
time series and take the 95th percentile. The result is a static map (no
time dimension) you can use to flag extremes by testing:
    data(t, y, x) >= threshold(y, x)

Key behavior & assumptions
--------------------------
- File discovery: looks for files matching `GR_<var>_Y<year>.nc` under --root.
- Variable selection: you pass human name or abbreviation via --var.
  - Example mapping already handled: "total_precipitation" ↔ "tp"
  - The internal NetCDF data var actually read is the abbreviation (e.g., "tp").
- Time dimension: the 95th percentile is computed over the **time** coord
  (named "valid_time" in your files). No daily sums/aggregation are done.
- Output: one NetCDF file named `<abbr>_q95_alltime.nc` (float32, compressed)
  that contains the per-grid 95th percentile field.

Typical usage
-------------
    python detect_era5_extremes.py \
        --root /path/to/ERA5/GR_single_levels \
        --var tp

Output files
------------
- `var_q95_alltime.nc` : DataArray with dims like (latitude, longitude[, level])
  containing the 95th percentile over all time steps.

"""

from pathlib import Path
import re
from typing import Iterable, List, Optional
import xarray as xr
import argparse, os
import numpy as np
from era5tools import find_era5_nc 


def main():
    ap = argparse.ArgumentParser(description="Identify and load a single ERA5 variable from many yearly NetCDFs.")
    ap.add_argument("--root", required=True, help="Folder containing yearly NetCDF files.")
    ap.add_argument("--var", required=True, help="Variable name to load (e.g., t2m, tp, u10, v10).")
    args = ap.parse_args()

    # keep only GR_total_precipitation_<year>.nc

    # Make sure, that names, and abbreviation have the same result
    if args.var == "tp" or args.var == "total_precipitation": 
        args.var = "total_precipitation"
        abbreviation_var = "tp"
        


    files = find_era5_nc(args.root, variable=args.var)

    #print(f"Found {len(files)} files for variable 'total_precipitation'.\n {files[1]}")
    ds = xr.open_mfdataset(files)
    #print(ds)

    VAR = abbreviation_var if abbreviation_var in ds.data_vars else list(ds.data_vars)[0]
    da = ds[VAR]


    # 1) 95th percentile across all time values, per grid point
    #    Result: a 2D field (or 3D if you have extra dims like level) with no time dim.
    q95 = da.quantile(0.95, dim="valid_time", skipna=True, keep_attrs=True)

    # keep a helpful name/attrs
    q95.name = f"{VAR}_q95_alltime"
    q95.attrs["description"] = "95th percentile over all available time steps"
    # print(q95)
    # print(q95.values)

    # Save the threshold field as a NetCDF
    q95.name = f"{VAR}_q95_alltime"
    enc = {q95.name: {"zlib": True, "complevel": 4, "dtype": "float32"}}
    q95.astype("float32").to_netcdf(f"{VAR}_q95_alltime.nc", encoding=enc)

    return q95



if __name__ == "__main__":
    q95 = main()
