from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from .forecaster.Forecaster import Forecaster
"""
Exposing api for communication between locally hosted nvidia stormcast model and hurricane client
"""
app = FastAPI(title='Hurricane Prediction Server', description='Silly little project', version='1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Location(BaseModel):
    date: datetime
    lon: float
    lat: float
fc = Forecaster()
@app.get('/')
async def hello_world():
    return "Let's get this show on the road."

@app.post('/forecast')
# async def forecast(date: datetime, lat, lon):
async def forecast(loc: Location) -> dict:
    try:
        print(f'This is the date format: {loc.date}')
        res = fc.forecast(loc.date, loc.lat, loc.lon)
        # print(res)
        return res
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error processing data: {e}")