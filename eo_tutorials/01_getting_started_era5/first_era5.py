import xarray as xr
import matplotlib.pyplot as plt

# Load the NetCDF file
ds = xr.open_dataset("../data/era5_sample.nc")

# === Inspect the dataset ===
print(ds)               # Overview: variables, dimensions, attributes
print(ds.data_vars)     # List of available variables
print(ds.coords)        # Coordinates (time, latitude, longitude, etc.)

# === Check the time dimension ===
print("Available times:", ds.valid_time.values)      # All timestamps
print("First time:", ds.valid_time.values[0])        # First timestep
print("Last time:", ds.valid_time.values[-1])        # Last timestep
print("Number of timesteps:", ds.sizes['valid_time']) # Length of the time dimension

# === Inspect one variable ===
t2m = ds['t2m']
print(t2m)              # Metadata (units, shape, etc.)

# === Look at a single pixel ===
example_pixel = t2m.sel(latitude=37.98, longitude=23.72, method="nearest")
print("Pixel time-series at Athens (37.98N, 23.72E):")
print(example_pixel.values)

# === Plot the first timestep ===
t2m.isel(valid_time=0).plot()
plt.title("ERA5 2m Temperature (First timestep)")
plt.show()