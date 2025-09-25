#!/usr/bin/env python3
"""
Unzip ERA5 files into extraction directories.

Usage:
  python era5_pipeline.py \
    --data-dir /mnt/dataStorage/ERA5/single_levels/total_precipitation \
    --data-dir /mnt/dataStorage/ERA5/pressure_levels/temperature
"""

import argparse
import zipfile
from pathlib import Path
import time

def unzip_era5(data_dir: Path, extract_dir: Path):
    data_dir = Path(data_dir).resolve()
    extract_dir = Path(extract_dir).resolve()
    extract_dir.mkdir(parents=True, exist_ok=True)

    for zip_file in data_dir.glob("*.zip"):
        base = zip_file.stem  # filename without .zip
        out_file = extract_dir / base
        print(f"Extracting {zip_file} → {out_file}")

        t0 = time.time()
        with zipfile.ZipFile(zip_file, "r") as z:
            inner = z.namelist()[0]  # assume one file inside
            with z.open(inner) as src, open(out_file, "wb") as dst:
                dst.write(src.read())
        print(f"✔ Done in {time.time() - t0:.1f}s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unzip ERA5 .zip files.")
    parser.add_argument(
        "--data-dir",
        required=True,
        action="append",
        help="One or more directories containing .zip files (can repeat)."
    )
    args = parser.parse_args()

    for data_dir in args.data_dir:
        d = Path(data_dir).resolve()
        extract_dir = d.parent.parent / f"extracted_single_levels/{d.name}"
        print(f"\n=== Processing {d} → {extract_dir} ===")
        unzip_era5(d, extract_dir)
