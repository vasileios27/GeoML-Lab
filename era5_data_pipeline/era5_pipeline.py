#!/usr/bin/env python3
"""
era5_raper.py — Wrapper to run extract_all.sh with one or more data directories.
Supports @args.txt input file for convenience.

Usage:
  # Direct arguments
  python era5_raper.py \
    --data_dir /mnt/dataStorage/ERA5/single_levels/total_precipitation \
    --data_dir /mnt/dataStorage/ERA5/single_levels/2m_temperature \
    --extract_dir /mnt/dataStorage/ERA5/extracted_single_levels

  # From args.txt file
  python era5_raper.py @args.txt
"""

import argparse
import subprocess
from pathlib import Path

def run_extract(script: Path, data_dir: Path, extract_dir: Path):
    """Run the extract_all.sh script for a single data directory."""
    cmd = [
        str(script),
        "--data_dir", str(data_dir),
        "--extract_dir", str(extract_dir)
    ]
    print("→ Running:", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        raise SystemExit(f"Script failed for {data_dir} with exit code {result.returncode}")

def main():
    parser = argparse.ArgumentParser(
        description="Run extract_all.sh for one or more data directories.",
        fromfile_prefix_chars='@'  # enables @args.txt
    )
    parser.add_argument("--data_dir", required=True, action="append",
                        help="Directory with ERA5 zip files (can repeat)")
    parser.add_argument("--extract_dir", required=True,
                        help="Directory where files will be extracted")
    parser.add_argument("--script", default="./extract_all.sh",
                        help="Path to extract_all.sh (default: ./extract_all.sh)")
    args = parser.parse_args()

    script_path = Path(args.script).resolve()
    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")

    extract_dir = Path(args.extract_dir).resolve()

    for data_dir in args.data_dir:
        run_extract(script_path, Path(data_dir).resolve(), extract_dir)

if __name__ == "__main__":
    main()
