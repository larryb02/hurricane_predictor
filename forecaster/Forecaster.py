# will handle model workflow

# considering making this a class so certain processes don't have to be redone.

# create a function that returns structured output to return as http response
from earth2studio.data import GFS_FX, HRRR
from earth2studio.io import ZarrBackend
from earth2studio.models.px import StormCast
import earth2studio.run as run


class Forecaster:
    package = StormCast.load_default_package()
    model = StormCast.load_model(package)
    data = HRRR(max_workers=2, cache=True)
    conditioning_data_source = GFS_FX()
    model.conditioning_data_source = conditioning_data_source

    def __init__(self):
        self.io = ZarrBackend()

    def forecast(self, date, location):
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

        return "computing!"
