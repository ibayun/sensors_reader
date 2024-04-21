from datetime import datetime

import aiofiles
from fastapi_utilities import repeat_every
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

# from models import NewTable, session
from sample_script import read_sensor_values, run_sensor_collect

app = FastAPI()


class Sensor(BaseModel):
    value: Union[int, float]


@app.get("/ping")
async def read_ping():
    async with aiofiles.open('../sensors.txt', mode="a+") as f:
        d = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c = d + "\n"
        await f.write(c)
    return {"ping": "pong"}


from fastapi import APIRouter


router = APIRouter()
app.include_router(router)


@app.on_event("startup")
@repeat_every(seconds=2)
async def collect_data():
    sensor_value_a0=temp_ds18b20=co2_sensor_value=gray_scale=""
    try:
        sensor_value_a0, temp_ds18b20, co2_sensor_value, gray_scale = run_sensor_collect()
    except Exception as exc:
        print(exc)
    async with aiofiles.open('sensors_data_16.txt', mode="a+") as f:
        d = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c = d + ":  " + "moisture - " + str(sensor_value_a0) + " temp - " + str(temp_ds18b20)[:4] + " co2 - " + str(
            co2_sensor_value) + " gray - " + str(gray_scale) + "\n"
        await f.write(c)

