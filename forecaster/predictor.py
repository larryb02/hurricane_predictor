# will handle model workflow

# considering making this a class so certain processes don't have to be redone.

# create a function that returns structured output to return as http response
from earth2studio.data import GFS_FX, HRRR
from earth2studio.io import ZarrBackend
from earth2studio.models.px import StormCast

class Forecaster:
    def __init__(self):
        pass

    def forecast(self):
        return "computing!"