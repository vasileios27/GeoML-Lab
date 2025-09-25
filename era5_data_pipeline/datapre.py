
import os, zipfile
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import shutil

# Europe's latitude limits are roughly  35°N to 72°N, and its longitude limits are roughly 25°W to 65°E for europ .
# Vars done
# mean_sea_level_pressure, 10m_u_component_of_wind, 10m_v_component_of_wind, 2m_temperature
# k_index, total_cloud_cover, total_precipitation, convective_precipitation


# Step 1: Define Paths
data_dir =      "/mnt/dataStorage/ERA5/single_levels/total_precipitation"  # Directory with ZIP files
extract_dir =   "/mnt/dataStorage/ERA5/extracted_single_levels"  # Temporary folder for extracted files
output_dir =    "/mnt/dataStorage/ERA5/GR_single_levels"  # Directory for subsetted Greece region
os.makedirs(extract_dir, exist_ok=True)  # Ensure extraction folder exists
os.makedirs(output_dir, exist_ok=True)  # Ensure output folder exists

# Step 2: Define Greece Region (Latitude & Longitude Bounds)
lat_min, lat_max = 34, 42
lon_min, lon_max = 19, 28
# # Step 2: Define Europ Region (Latitude & Longitude Bounds)
# lat_min, lat_max = 35, 72
# lon_min, lon_max = -25, 65

# Step 3: Loop Over ZIP Files and Extract
# Loop over ZIP files in the data directory
# for zip_file in os.listdir(data_dir):
#     if zip_file.endswith(".zip"):
#         zip_path = os.path.join(data_dir, zip_file)

#         output_name = os.path.splitext(zip_file)[0]
#         output_path = os.path.join(extract_dir, output_name)

#          # ✅ Skip if already extracted
#         if os.path.exists(output_path):
#             print(f"✅ Skipping already extracted file: {zip_file}")
#             continue

#         # Open the ZIP file
#         print(f"Extracting: {zip_file}")
#         with zipfile.ZipFile(zip_path, "r") as zip_ref:
#             # Get list of all files within the ZIP
#             name_list = zip_ref.namelist()
            
#             # Check if the ZIP contains exactly one file
#             if len(name_list) == 1:
#                 # Create the desired output file name.
#                 # For example, if the zip file is "data1.zip", the output will be "data1.nc"

                
#                 # Open the file inside the ZIP and write it to the output path
#                 with zip_ref.open(name_list[0]) as source_file:
#                     with open(output_path, "wb") as target_file:
#                         shutil.copyfileobj(source_file, target_file)
#             else:
#                 # If the ZIP contains multiple files, extract each and rename them accordingly.
#                 for member in zip_ref.infolist():
#                     # Here you can define your naming scheme. As an example, we prefix with the zip file's base name.
#                     member_name = os.path.basename(member.filename)
#                     output_name = os.path.splitext(zip_file)[0] + "_" + member_name
#                     output_path = os.path.join(extract_dir, output_name)
                    
#                     with zip_ref.open(member) as source_file:
#                         with open(output_path, "wb") as target_file:
#                             shutil.copyfileobj(source_file, target_file)

#         print(f"Extracted: {zip_file} to {extract_dir}")
       


# Step 4: Process Extracted NetCDF Files
for file in os.listdir(extract_dir):
    folder_name = data_dir.rstrip("/").split("/")[-1]
    if file.endswith(".nc") and file.startswith(folder_name):  # Process only NetCDF files
        file_path = os.path.join(extract_dir, file)
        
        # Step 5: Load Dataset
        ds = xr.open_dataset(file_path)

        # Step 6: Subset the Data (Keep Only Greece)
        ds_region = ds.sel(latitude=slice(lat_max, lat_min), longitude=slice(lon_min, lon_max))

        # Step 7: Generate Output Filename
        output_filename = f"EE_{file}"  # Prefix "GR_" for Greece region
        output_path = os.path.join(output_dir, output_filename)

        # Step 8: Save the Subsetted Dataset
        ds_region.to_netcdf(output_path)

        print(f"Processed: {file} -> {output_filename}")

print("✅ All ZIP files extracted and processed successfully!")




