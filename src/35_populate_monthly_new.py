import pickle
import xarray as xr
import time
import os

# Change these two variables for each run
####################################################
path = "../ncs/r_250_mon_ERA5_1979-2025.nc"
out_key = "r250" # Can be any name you want for the new column
####################################################

ds = xr.open_dataset(path, decode_times=True)
for var in ds.data_vars:
    key = var


base_file = '../main_data/base_file.pkl'
out_file = f'../aux_data/df_monthly_{out_key}.pkl'

os.makedirs(os.path.dirname(out_file), exist_ok=True)

with open(base_file, 'rb') as f:
    df_new = pickle.load(f)

st = time.time()
for i in range(len(df_new)):
    if i % 1000 == 0:
        print(f"Processing {i} of {len(df_new)}")
    value = ds[key].sel(
        valid_time=df_new.iloc[i]["date"],
        latitude=df_new.iloc[i]["nearest_latitude"],
        longitude=df_new.iloc[i]["nearest_longitude"],
        method="nearest",
    )
    try:
        df_new.loc[i, out_key] = value.values[0]
    except:
        df_new.loc[i, out_key] = value.values

with open(out_file, 'wb') as f:
    pickle.dump(df_new, f)

et = time.time()
print(f"Time taken: {et - st} seconds")