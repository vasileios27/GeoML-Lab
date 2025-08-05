#data acqusition 
# The provided Python script automates the download of specific meteorological variables 
# from the Copernicus Climate Data Store (CDS) using the cdsapi library.
import cdsapi
import os

# Define the directory path
directory_path = "/home/vvatellis/WeatherData/ERA5_hourly_data/single_levels/"
# Change to a new directory
os.chdir(directory_path)

dataset = "reanalysis-era5-single-levels"
client = cdsapi.Client()

years = [1970,2023]

months = [ "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12"]


variables= ["10m_u_component_of_wind", "10m_v_component_of_wind","total_precipitation",
            "k_index","total_cloud_cover", "convective_precipitation", 
            "vertically_integrated_moisture_divergence", "total_column_water_vapour", 
            "total_column_cloud_liquid_water"]


for variable in variables:
    for year in range(years[0], years[-1] +1, 1):

        request = {
             "product_type": ["reanalysis"],
            "variable": variable,
            "year": year,
            "month": [ "01", "02", "03",
			 "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12"],
            "day": [
                "01", "02", "03",
                "04", "05", "06",
                "07", "08", "09",
                "10", "11", "12",
                "13", "14", "15",
                "16", "17", "18",
                "19", "20", "21",
                "22", "23", "24",
                "25", "26", "27",
                "28", "29", "30",
                "31"
            ],
            "time": ["00:00", "06:00", "12:00", "18:00" ],
            "data_format": "netcdf",
            "download_format": "zip",
        }

        target = f"{variable}_Y{year}.nc.zip"
        client.retrieve(dataset, request, target)
        print(f"\nDownloaded data for {variable}-{year}")
