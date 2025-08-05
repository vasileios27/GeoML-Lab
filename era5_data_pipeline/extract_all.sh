#!/usr/bin/env bash
set -euo pipefail

# adjust these to your real, absolute paths:
data_dir="ERA5_hourly_data/single_levels/10m_v_component_of_wind"
extract_dir="ERA5_hourly_data/single_level_extracted"



cd "$data_dir"

for zip in *.zip; do
  base="${zip%.zip}"
  echo "Extracting $zip → $extract_dir/$base"
  time unzip -p "$zip" > "../../single_level_extracted/$base"
done
