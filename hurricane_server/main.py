from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from forecaster.Forecaster import Forecaster
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

fc = Forecaster()
@app.get('/')
async def hello_world():
    return "Let's get this show on the road."

from datetime import datetime

@app.post('/forecast')
async def forecast(date: datetime, location):
    return fc.forecast(0, 0)