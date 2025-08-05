# 🔄 ERA5 Climate Data Pipeline Overview
This project outlines a complete pipeline for working with ERA5 climate reanalysis data, from initial acquisition to machine learning–ready datasets. The process begins with downloading hourly reanalysis data from the Copernicus Climate Data Store (CDS) using the official CDS API. The raw data is then extracted, spatially subset, and preprocessed to prepare it for downstream machine learning applications.

The pipeline is designed to support reproducible research and can be adapted for various tasks, including climate impact modeling, weather classification, and extreme event detection.

<p align="center"> <img src="../plots/era5_pipline.png" alt="ERA5 Data Pipeline Diagram" width="700"/> </p>
Figure: Schematic overview of the ERA5 data pipeline. It includes data acquisition from Copernicus via API, automated extraction and merging of NetCDF files, spatial subsetting for Europe, and the transformation of datasets into ML-ready formats.


The pipeline is composed of several modular steps that handle the entire workflow from raw ERA5 data to machine learning–ready datasets. Below is a breakdown of each stage represented in the diagram:

1. **📥 Data Acquisition ([`era_sigle_data_acquisition.py`](#era5-data-acquisition-script))** 
   The process begins with downloading ERA5 hourly single-level reanalysis data from the Copernicus Climate Data Store using the CDS API. This script allows the user to specify the variables, years, and times of interest, and saves the data in zipped NetCDF format, organized by variable and year.

2. **🗜️ Extraction ([`extract_all.sh`](#era5-file-extraction-script))**
   Once the data is downloaded, the `extract_all.sh` shell script is used to unzip and extract the NetCDF files from the downloaded `.zip` archives. This prepares the files for subsequent processing.

3. **🗂️ Preprocessing by Region ([`datapre.py`](#regional-preprocessing-script))**
   The extracted NetCDF files are then spatially subset and preprocessed using `datapre.py`. This step focuses on trimming the dataset to a region of interest (e.g., Europe), applying any spatial constraints, and merging files if necessary. The result is a region-specific NetCDF file, cleaned and ready for transformation.

4. **🧰 Dataset Preparation for ML ([`dataGR4ML.py`](#general-ml-dataset-preparer))**
   For general-purpose ML workflows, `dataGR4ML.py` transforms the regional NetCDF data into a format suitable for training machine learning models. This typically involves restructuring time-series data, normalizing variables, and saving the final outputs in ML-friendly formats such as NumPy arrays or `.h5` files.

5. **🌧️ Dataset Preparation for Precipitation Studies ([`PrecipitationDataPrepMultydata.py`](#dataset-combiner))**
   For precipitation-related tasks or multi-variable experiments, `PrecipitationDataPrepMultydata.py` handles the preparation of merged datasets. This script combines multiple ERA5 variables, ensuring time-alignment and consistency, and outputs structured data tailored for supervised learning or forecasting tasks.

Together, these components form a flexible and reproducible workflow for transforming raw climate reanalysis data into high-quality datasets for machine learning applications in climate science.


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

## 🧾 Request Format
The code works based on the request, which is constructed in the code. For example 
```bash
request = {
    "product_type": ["reanalysis"],
    "variable": variable,
    "year": year,
    "month": [ "01", ..., "12"],
    "day": [ "01", ..., "31"],
    "time": ["00:00", "06:00", "12:00", "18:00"],
    "data_format": "netcdf",
    "download_format": "zip",
}
```
 * "product_type": always set to "reanalysis" for ERA5 historical data.
 * "time": specifies the hourly timestamps to download. ERA5 provides hourly data (00:00 to 23:00), but this script downloads 4 synoptic times (00:00, 06:00, 12:00, 18:00) commonly used in meteorology.
 * "data_format": format of the output file. Options include:
 * "netcdf": easier to read with scientific tools and Python libraries.
 * "grib": more compact, typically used in numerical weather prediction models.
 * "download_format": downloads the file as a .zip archive.
   
  🌍 Optional: Geographical Subsetting
  To restrict the download to a specific geographic area, add the area key to the request dictionary:
```bash
"area": [90, -180, -90, 180],  # Format: [North, West, South, East]
```
For example, to download data only over Europe, the request should have the format 
```bash
request = {
    "product_type": ["reanalysis"],
    "variable": variable,
    "year": year,
    "month": [ "01", ..., "12"],
    "day": [ "01", ..., "31"],
    "time": ["00:00", "06:00", "12:00", "18:00"],
    "data_format": "netcdf",
    "download_format": "zip",
    "area": [72, -25, 34, 45]
}
```

# ERA5 File Extraction Script

**Script**: `extract_all.sh`

This Bash script automates the extraction of `.nc` (NetCDF) files from `.zip` archives downloaded from the CDS API. It ensures that each file is uncompressed and stored in a structured format for subsequent preprocessing.

#### 🔧 What It Does

* Iterates through all `.zip` files in a specified input directory (e.g., for a specific variable).
* Uses `unzip -p` to extract the contents (NetCDF files) directly without creating temporary folders.
* Saves the extracted `.nc` files into a target directory, maintaining a clear and consistent naming convention.

#### 💡 Usage

Update the following variables in the script:

```bash
data_dir="ERA5_hourly_data/single_levels/10m_v_component_of_wind"
extract_dir="ERA5_hourly_data/single_level_extracted"
```

Then run:

```bash
bash extract_all.sh
```

Each `.zip` archive will be extracted to `.nc` format and saved under the specified directory for further processing.

---

# Regional Preprocessing Script

**Script**: `datapre.py`

This script handles the **spatial subsetting** and **temporal alignment** of ERA5 NetCDF files. It focuses on selecting a specific geographic region (e.g., Europe) and prepares the data for merging or transformation.

#### 🔧 What It Does

* Loads individual NetCDF files using `xarray`.
* Applies latitude and longitude slicing to subset data over a defined region.
* Optionally trims the temporal resolution or selects specific variables.
* Saves the processed files into a new folder (`../ProcessedRegionData/`).

#### 💡 Region Example

In the code, Europe is defined as:

```python
data = data.sel(latitude=slice(72, 34), longitude=slice(-25, 45))
```

You can modify these bounds to match your region of interest.

---

# General ML Dataset Preparer

**Script**: `dataGR4ML.py`

This script converts preprocessed NetCDF data into a format suitable for general machine learning applications.

#### 🔧 What It Does

* Opens the processed NetCDF files and reads the data using `xarray`.
* Flattens or reshapes data dimensions (e.g., time × lat × lon → 2D array).
* Optionally filters by a specific time range.
* Saves the final dataset into `.npy` or `.h5` formats ready for ML training/testing.

#### 💡 Output Example

```python
np.save("Europe_precipitation.npy", final_array)
```

This allows you to use NumPy directly in scikit-learn, PyTorch, or TensorFlow workflows.

---

# Dataset Combiner

**Script**: `PrecipitationDataPrepMultydata.py`

This script is specifically designed to **combine multiple ERA5 variables** (e.g., precipitation, temperature, wind) into a unified ML-ready dataset. It is ideal for studies that rely on **multi-feature learning**, such as flood forecasting, drought detection, or general climate impact studies.

#### 🔧 What It Does

* Loads several NetCDF files at once, each representing a different variable.
* Applies consistent spatial and temporal alignment.
* Stacks the data into a multi-dimensional NumPy array:
  `(time, lat, lon, features)`
* Optionally normalizes the data per feature.
* Outputs the full dataset and a label array if precipitation is used as a target variable.

#### 💡 Example Use Case

Creating an input-output dataset for supervised learning:

```python
X.shape = (n_samples, height, width, n_features)
y.shape = (n_samples,)  # e.g., for binary classification: heavy vs. light rainfall
```

---

Would you like me to generate a markdown file with all this content or integrate it directly into your full `README.md`?


## 🔗 References

* [Copernicus Climate Data Store](https://cds.climate.copernicus.eu)
* [ERA5 Documentation](https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation)

---

© 2025 — Developed as part of the GeoML-Lab initiative.
