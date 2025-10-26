from pathlib import Path
import re
from typing import Iterable, List, Optional
import xarray as xr
import argparse, os
import numpy as np


GR_PATTERN = re.compile(r'^GR_(?P<var>[A-Za-z0-9_]+)_(?:Y)?(?P<year>\d{4})\.nc$')
__all__ = ["GR_PATTERN"]
# pattern = r'^GR_(?P<var>[A-Za-z0-9_]+)_(?:Y)?(?P<year>\d{4})\.nc$'
#           └─┬─┘ └────────────┬────────────┘  └┬┘  └───┬───┘ └┬┘
#            ^   literal "GR_"   var group (letters/digits/_)  _
#            |                                               optional "Y"
#         start of line                                        |
#                                                     year = 4 digits
#                                                                literal ".nc"
#                                                                    end of line

def find_era5_nc(
    root: str,
    variable: str = "total_precipitation",
    years: Optional[Iterable[int]] = None, ) -> List[str]:
    """
    Return sorted list of GR_<variable>_<year>.nc under `root`.
    Sorts by year. Only *.nc files are considered.

    Example:
        find_era5_nc("/data/ERA5/GR_single_levels", "total_precipitation")
        -> [".../GR_total_precipitation_1979.nc", ..., ".../GR_total_precipitation_2020.nc"]
    """
    root_path = Path(root)
    hits: list[tuple[int, Path]] = []

    for fp in root_path.rglob("*.nc"):
        m = GR_PATTERN.fullmatch(fp.name)
        if not m:
            continue
        var = m.group("var")
        yr = int(m.group("year"))
        if var != variable:
            continue
        if years is not None and yr not in years:
            continue
        hits.append((yr, fp))

    hits.sort(key=lambda t: t[0])  # sort by year
    return [str(fp) for _, fp in hits]