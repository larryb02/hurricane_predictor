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
data = HRRR()

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

f = open("outputs/model_output.txt", "w")
f.write(io)
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
