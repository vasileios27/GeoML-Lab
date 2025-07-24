# ERA5 Data Acquisition Script

This script automates the retrieval of hourly ERA5 reanalysis data on single levels from the Copernicus Climate Data Store (CDS) using the `cdsapi` Python package.

## ✅ What It Does

- Downloads hourly reanalysis data for selected meteorological variables.
- Covers a user-defined range of years (currently 1970 to 2023).
- Retrieves data at four synoptic hours: 00:00, 06:00, 12:00, and 18:00 UTC.
- Saves data as compressed NetCDF files (`.nc.zip`), one per year and variable.

## 📦 Requirements

- Python 3
- `cdsapi` package
- Valid CDS API key configured at `~/.cdsapirc` ([CDS API instructions](https://cds.climate.copernicus.eu/api-how-to))

Install `cdsapi` via pip:
```bash
pip install cdsapi
````

## 🔧 How to Use

1. Modify the following parameters in the script as needed:

   * `directory_path`: where to save downloaded files.
   * `years`: start and end year (e.g., `[1970, 2023]`).
   * `variables`: list of ERA5 variables to retrieve (e.g., `"10m_u_component_of_wind"`).

2. Run the script:

```bash
python download_era5_single_levels.py
```

Each file will be named like:

```
10m_u_component_of_wind_Y1980.nc.zip
```

## 📌 Notes

* Dataset used: `reanalysis-era5-single-levels`
* Data is retrieved at daily frequency with 4 time steps.
* All months and days are included.

To add or remove variables, edit the `variables` list in the script.

## 🔗 References

* [Copernicus Climate Data Store](https://cds.climate.copernicus.eu)
* [ERA5 Documentation](https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation)

---

© 2025 — Developed as part of the GeoML-Lab initiative.

```

---

Would you like me to split the script into a cleaner and modular version, or proceed with writing more README content for other data acquisition scripts?
```
