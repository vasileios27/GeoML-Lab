import xarray as xr
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Train AE Model")
    parser.add_argument("--input", type=str, default=  "/home/vvatellis/WeatherData/ERA5_hourly_data/single_level_ERA5_Greece/")
    parser.add_argument("--output", type=str, default= "GR_single.nc")
    parser.add_argument("--prefix", type=str, default= "EE" )

    return parser.parse_args()

args = parse_args()
split = True

if split == True :
    # Folder containing the NetCDF files
    folder_path = args.input  # Use the input argument for the folder path


    # Create a list of full paths for files ending with ".nc"
    prefix = args.prefix   # whatever you want to filter on
    nc_files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.endswith(".nc") and f.startswith(prefix)
        ]
    #print(nc_files)
    # # Open and merge all NetCDF files using xarray
    merged_ds = xr.open_mfdataset(nc_files, combine="by_coords")

    merged_ds = merged_ds.sel(valid_time=merged_ds.valid_time.dt.hour != 19)

    # Optionally, save the merged dataset to a new NetCDF file
    merged_ds.to_netcdf(args.output)

    print("Merged dataset saved as merged_dataset.nc")

if split == False :
    # Open the merged dataset (if not already in memory)
    merged_ds = xr.open_dataset(os.path.join("/home/vvatellis/storage/DoctoralThesis/RepresentationEOcode","GR_merged_.nc"))

    # Check the time coordinate
    print(merged_ds.valid_time)

    merged_ds = merged_ds.sel(valid_time=merged_ds.valid_time.dt.hour != 19)

    # Define split boundaries (example dates - adjust to your dataset)
    train_ds = merged_ds.sel(valid_time=slice("2000-01-01", "2007-12-31"))
    val_ds   = merged_ds.sel(valid_time=slice("2000-08-01", "2009-12-31"))
    #test_ds  = merged_ds.sel(valid_time=slice("2010-01-01", "2010-12-31"))

    # Optionally, save these splits to separate files
    train_ds.to_netcdf(os.path.join("/home/vvatellis/storage/DoctoralThesis/RepresentationEOcode","merged_ERA5_train.nc"))
    val_ds.to_netcdf(os.path.join("/home/vvatellis/storage/DoctoralThesis/RepresentationEOcode","merged_ERA5_val.nc"))
    test_ds.to_netcdf(os.path.join("/home/vvatellis/storage/DoctoralThesis/RepresentationEOcode","merged_ERA5_test.nc"))

    print("Datasets split into train, validation, and test sets.")

else : print("give a value to split")
