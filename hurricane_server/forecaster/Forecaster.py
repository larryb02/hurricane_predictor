# will handle model workflow

# considering making this a class so certain processes don't have to be redone.

# create a function that returns structured output to return as http response
from earth2studio.data import GFS_FX, HRRR
from earth2studio.io import ZarrBackend
from earth2studio.models.px import StormCast
import earth2studio.run as run
import numpy as np


class Forecaster:
    package = StormCast.load_default_package()
    model = StormCast.load_model(package)
    data = HRRR(max_workers=2, cache=True)
    conditioning_data_source = GFS_FX()
    model.conditioning_data_source = conditioning_data_source

    def __init__(self):
        self.io = ZarrBackend()

    def forecast(self, date, lat, lon):
        """
        Generates a deterministic output
        params:
            date: Datetime
            location: lon, lat of input location
        returns:
            Dict
                dict containing model predictions
        """
        nsteps = 1
        # today = datetime.today() - timedelta(days=1)
        date = date.isoformat().split("T")[0]
        io = run.deterministic(
            [date], nsteps, Forecaster.model, Forecaster.data, self.io
        )
        # now post process
        # # Assume these are 1D arrays
        lats = io["lat"][:]
        lons = io["lon"][:]

        # Convert -90 to 270 if longitudes are 0–360
        target_lat = 35.0
        target_lon = 270.0 if lons.max() > 180 else -90.0
        # Find the closest indices
        lat_idx = np.abs(lats - target_lat).argmin()
        lon_idx = np.abs(lons - target_lon).argmin()

        return build_forecast_dict(io, lat_idx, lon_idx)


def build_forecast_dict(io, lat_idx, lon_idx, lead_time_idx=0):
    return {
        "time": int(io["time"][0]),
        "location": {
            "latitude": float(io["lat"][lat_idx, lon_idx]),
            "longitude": float(io["lon"][lat_idx, lon_idx]),
        },
        "forecast": {
            "zonal_wind": float(io["u10m"][0, lead_time_idx, lat_idx, lon_idx]),
            "meridional_wind": float(io["v10m"][0, lead_time_idx, lat_idx, lon_idx]),
            "mean_sea_level_pressure": float(
                io["mslp"][0, lead_time_idx, lat_idx, lon_idx]
            ),
            "total_precipitation": float(
                io["p1hl"][0, lead_time_idx, lat_idx, lon_idx]
            ),  # or use "tp" if available
            "cloud_cover": float(
                io["refc"][0, lead_time_idx, lat_idx, lon_idx]
            ),  # adjust based on preferred field
            "temperature_2m": float(io["t2m"][0, lead_time_idx, lat_idx, lon_idx]),
        },
    }
