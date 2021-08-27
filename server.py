from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

sensor_values=[None,None,None]

class sensorInput(BaseModel):
    temperature_value_c: str
    temperature_value_f: str
    light_value : str


@app.get("/")
async def root():
    return sensor_values


@app.post("/values")
async def receive_data(payload:sensorInput):
    temperature_value_c = payload.temperature_value_c
    temperature_value_f = payload.temperature_value_f
    light_value =light_value

    sensor_values= [temperature_value_c,temperature_value_f,light_value]