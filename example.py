from datetime import datetime, timedelta

from loguru import logger
from tqdm import tqdm

logger.remove()
logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)

import os

os.makedirs("outputs", exist_ok=True)
from dotenv import load_dotenv

load_dotenv()  # TODO: make common example prep function

from earth2studio.data import GFS_FX, HRRR
from earth2studio.io import ZarrBackend
from earth2studio.models.px import StormCast

# Load the default model package which downloads the check point from NGC
package = StormCast.load_default_package()
model = StormCast.load_model(package)

# Create the data source
data = HRRR(max_workers=2,cache=True)

# Create and set the conditioning data source
conditioning_data_source = GFS_FX()
model.conditioning_data_source = conditioning_data_source

# Create the IO handler, store in memory
io = ZarrBackend()

# %%
# Execute the Workflow
# --------------------
# With all components initialized, running the workflow is a single line of Python code.
# Workflow will return the provided IO object back to the user, which can be used to
# then post process. Some have additional APIs that can be handy for post-processing or
# saving to file. Check the API docs for more information.
#
# For the forecast we will predict for 4 hours

# %%
import earth2studio.run as run

nsteps = 1
today = datetime.today() - timedelta(days=1)
date = today.isoformat().split("T")[0]
io = run.deterministic([date], nsteps, model, data, io)

print(io.root.tree())

# %%
# Post Processing
# ---------------
# The last step is to post process our results. Cartopy is a great library for plotting
# fields on projections of a sphere. Here we will just plot the temperature at 2 meters
# (t2m) 4 hours into the forecast.
#
# Notice that the Zarr IO function has additional APIs to interact with the stored data.

# with open("outputs/model_output.txt", "w") as f:
#     # for key in io.root.keys():
#     f.write(f"{io.root.tree()}")
    
#     # f.write(io.root.keys())

from pprint import pprint
import numpy as np

# # Assume these are 1D arrays
lats = io["lat"][:]
lons = io["lon"][:]

# Convert -90 to 270 if longitudes are 0–360
target_lat = 35.0
target_lon = 270.0 if lons.max() > 180 else -90.0

# Find the closest indices
lat_idx = np.abs(lats - target_lat).argmin()
lon_idx = np.abs(lons - target_lon).argmin()

# Select a specific lat/lon or use slicing
lat_idx = 10  # choose appropriate index
lon_idx = 20

# Select a specific time index (e.g., first timestep)
time_idx = 0

# lets get the data for {lon}, {lat}
# structured_output = {
#     "time": "",
#     "location": {
#         "latitude": lats[lat_idx],
#         "longitude": lons[lon_idx]
#     },
#     "forecast": {
#         "u10": "",
#         "v10": "",
#         "mean_sea_level_pressure": "",
#         "total_precipitation": "",
#         "cloud_cover": "",
#         "temperature_2m": io["t2m"][0, 1]
#     }
# }
def build_forecast_dict(io, lat_idx, lon_idx, lead_time_idx=0):
    return {
        "time": int(io["time"][0]),
        "location": {
            "latitude": float(io["lat"][lat_idx, lon_idx]),
            "longitude": float(io["lon"][lat_idx, lon_idx])
        },
        "forecast": {
            "u10": float(io["u10m"][0, lead_time_idx, lat_idx, lon_idx]),
            "v10": float(io["v10m"][0, lead_time_idx, lat_idx, lon_idx]),
            "mean_sea_level_pressure": float(io["mslp"][0, lead_time_idx, lat_idx, lon_idx]),
            "total_precipitation": float(io["p1hl"][0, lead_time_idx, lat_idx, lon_idx]),  # or use "tp" if available
            "cloud_cover": float(io["refc"][0, lead_time_idx, lat_idx, lon_idx]),  # adjust based on preferred field
            "temperature_2m": float(io["t2m"][0, lead_time_idx, lat_idx, lon_idx])
        }
    }

structured_output = build_forecast_dict(io, lat_idx, lon_idx)

# pprint(structured_output)
with open("outputs/structured_data.txt", "w") as f:
    f.write(str(structured_output))
# %%

# import cartopy
# import cartopy.crs as ccrs
# import matplotlib.pyplot as plt

# forecast = f"{date}"
# variable = "t2m"
# step = 4  # lead time = 1 hr

# plt.close("all")

# # Create a correct Lambert Conformal projection
# projection = ccrs.LambertConformal(
#     central_longitude=262.5,
#     central_latitude=38.5,
#     standard_parallels=(38.5, 38.5),
#     globe=ccrs.Globe(semimajor_axis=6371229, semiminor_axis=6371229),
# )

# # Create a figure and axes with the specified projection
# fig, ax = plt.subplots(subplot_kw={"projection": projection}, figsize=(10, 6))

# # Plot the field using pcolormesh
# im = ax.pcolormesh(
#     io["lon"][:],
#     io["lat"][:],
#     io[variable][0, step],
#     transform=ccrs.PlateCarree(),
#     cmap="Spectral_r",
# )

# # Set state lines
# ax.add_feature(
#     cartopy.feature.STATES.with_scale("50m"), linewidth=0.5, edgecolor="black", zorder=2
# )

# # Set title
# ax.set_title(f"{forecast} - Lead time: {step}hrs")

# # Add coastlines and gridlines
# ax.coastlines()
# ax.gridlines()
# plt.savefig(f"outputs/09_{date}_t2m_prediction.jpg")
