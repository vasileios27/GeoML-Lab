#!/usr/bin/env bash
set -euo pipefail

# ------------------------
# Parse arguments
# ------------------------
data_dir=""
extract_dir=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --data_dir)
      data_dir="$2"
      shift 2
      ;;
    --extract_dir)
      extract_dir="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$data_dir" || -z "$extract_dir" ]]; then
  echo "Usage: $0 --data_dir <path> --extract_dir <path>"
  exit 1
fi

# ------------------------
# Extraction
# ------------------------
cd "$data_dir"

for zip in *.zip; do
  base="${zip%.zip}"
  out_file="$extract_dir/$base"
  echo "Extracting $zip → $out_file"
  time unzip -p "$zip" > "$out_file"
done
