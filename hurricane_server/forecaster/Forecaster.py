# will handle model workflow

# considering making this a class so certain processes don't have to be redone.

# create a function that returns structured output to return as http response
from earth2studio.data import GFS_FX, HRRR
from earth2studio.io import ZarrBackend
from earth2studio.models.px import StormCast
import earth2studio.run as run
import numpy as np
from datetime import datetime, timedelta

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
        today = datetime.today() - timedelta(days=1)
        date = today.isoformat().split("T")[0]
        io = run.deterministic(
            [date], nsteps, Forecaster.model, Forecaster.data, self.io
        )
        # print(io.root.tree())
        # now post process
        # # Assume these are 1D arrays
        lats = io["lat"][:]
        lons = io["lon"][:]
        # ilats = io["ilat"][:]
        # ilons = io["ilon"][:]
        # print(f'lats: {lats}\nlons: {lons}\nlat_idx: {ilats}\nlon_idx: {ilons}')
        
        
        # target_lat = 34.0522
        # target_lon = 260.0001 
        # find_nearest_grid_point(target_lat, target_lon, lats, lons)
        indices = find_closest_coords(lat, lon, lats, lons)
        print(f'indices: {indices}\nlatitude:{io["lat"][indices[0], indices[1]]}, longitude:{io["lon"][indices[0], indices[1]]}')
        try: 
            fc = build_forecast_dict(io, indices[0], indices[1])
            return fc
        except Exception as e:
            print("Error in forecast: ", e)
            raise e

def find_closest_coords(input_lat, input_lon, lats, lons):
    min_diff = float('inf')
    best_row, best_col = None, None

    for i in range(lats.shape[0]):
        for j in range(lats.shape[1]):
            lat_diff = abs(lats[i, j] - input_lat)
            lon_diff = abs(lons[i, j] - input_lon)
            total_diff = lat_diff + lon_diff

            if total_diff < min_diff:
                min_diff = total_diff
                best_row, best_col = i, j

    return best_row, best_col

def build_forecast_dict(io, lat_idx, lon_idx, lead_time_idx=0):
    try:
        print("creating structure")
        fc = {
                "time": int(io["time"][0]),
                "location": {
                    "latitude": float(io["lat"][lat_idx, lon_idx]),
                    "longitude": float(io["lon"][lat_idx, lon_idx]),
                },
                "forecast": {
                    "zonal_wind": float(io["u10m"][0, lead_time_idx, lat_idx, lon_idx]),
                    "meridional_wind": float(
                        io["v10m"][0, lead_time_idx, lat_idx, lon_idx]
                    ),
                    "mean_sea_level_pressure": float(
                        io["mslp"][0, lead_time_idx, lat_idx, lon_idx]
                    ),
                    "total_precipitation": float(
                        io["p1hl"][0, lead_time_idx, lat_idx, lon_idx]
                    ),  # or use "tp" if available
                    "cloud_cover": float(
                        io["refc"][0, lead_time_idx, lat_idx, lon_idx]
                    ),  # adjust based on preferred field
                    "temperature_2m": float(
                        io["t2m"][0, lead_time_idx, lat_idx, lon_idx]
                    ),
                },
            }
    
    # import sys

    # print(f'Forecast: {fc}\nSize: {sys.getsizeof(fc)}\n')
        return fc
    except Exception as e:
        print("Error in build_forecast_dict: ", e)
        return {"Error": e}
