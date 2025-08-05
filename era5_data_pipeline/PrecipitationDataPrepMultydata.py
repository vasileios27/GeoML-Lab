import xarray as xr
import numpy as np
import torch
import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Data preperation for ML ")
    parser.add_argument("--input", type=str, default= "/home/vvatellis/storage/DoctoralThesis/RepresentationEOcode/GR_merged_filtered2.nc")
    parser.add_argument("--start", type=str, default= "1980-01-01")
    parser.add_argument("--end", type=str, default= "2010-12-31")
    parser.add_argument("--output", type=str, default= "./")
    parser.add_argument("--var", type=str, nargs='+', default=["tp"], help="List of variables to use")
    parser.add_argument('--mask', action='store_true', help="Apply masking if set")
    parser.add_argument("--day", type=str, default="2d", help="Day of the forecast, e.g., 2days, 3days, etc.")
    
    return parser.parse_args()

args = parse_args()
# Load dataset fully into memory first
dsGR = xr.open_dataset(args.input).load()

if args.mask:
    # Define thresholds
    tp = dsGR["tp"]
    tpValues = tp.values
    print(f"tp min ={tpValues.min()}, tp max ={tpValues.max()}")

    tp_threshold_95 = np.percentile(tpValues, 95)
    tp_threshold_99 = np.percentile(tpValues, 99)
    thresholds = {'tp': (tp_threshold_95, tp_threshold_99)}

# Select validation range
start,end = args.start, args.end
dsGR = dsGR.sel(valid_time=slice(start,end))  # Training data
#dsGR = dsGR.sel(valid_time=slice("2011-01-01", "2018-12-31")) # Validation data
#dsGR = dsGR.sel(valid_time=slice("2019-01-01", "2023-12-31")) # Test data
if args.mask:
    tp = dsGR["tp"]
    # Create extreme mask once
    tp_mask_all = (tp > thresholds['tp'][0]).astype(int)

# Get all times
times = dsGR.valid_time.values

# Create index slices (vectorized version)
if args.day == "1d": day = 4
if args.day == "2d": day = 8
if args.day == "3d": day = 12
if args.day == "4d": day = 16
if args.day == "5d": day = 20
if args.day == "6d": day = 24
for var in args.var:
    era5_list = []
    mask_list = []
    print(f"Processing variable: {var}")
    ds = dsGR[var]
    for i in range(len(times) - day):
        #t0, t1, t2 = times[i], times[i+1], times[i+8]

        # Use integer indexing instead of time-based slicing
        ds0 = ds.isel(valid_time=slice(i, i+2))     # 2 time steps: t0 and t1
        da0 = ds0.values     # (V, T=2, Y, X)

        era5_list.append(da0)
        if args.mask:
            da1 = tp_mask_all.isel(valid_time=i+day).values # (Y, X)
            mask_list.append(da1)


        

    # Stack all at once
    era5_np = np.stack(era5_list, axis=0) 
    tensor_era5 = torch.from_numpy(era5_np)           # (N, V, T, Y, X)
    if len(era5_np.shape) == 4:
        tensor_era5 = tensor_era5.unsqueeze(1)
    print("var shape:", tensor_era5.shape)
    torch.save(tensor_era5, f"{args.output}/ERA5_{args.day}_{var}_{start}_{end}.pt")
    
    if args.mask:
        tp_mask_np = np.stack(mask_list, axis=0) 
        tensor_tp_mask = torch.from_numpy(tp_mask_np)
        print("label shape:", tensor_tp_mask.shape)
        torch.save(tensor_tp_mask, f"{args.output}/tp_mask_{args.day}_{start}_{end}.pt")


    # Save to disk
    # torch.save(tensor_era5, "ERA5_var_train.pt")
    # torch.save(tensor_tp_mask, "tp_mask_train.pt")
    # torch.save(tensor_era5, "ERA5_var_validation.pt")
    # torch.save(tensor_tp_mask, "tp_mask_validation.pt")
    
    #torch.save(tensor_tp_mask, f"ERA5ml/tp_mask_{start}_{end}.pt")

