# from fastapi_utilities import repeat_every
# from fastapi_utilities.cli.template.src.api import router
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

# from sample_script import read_sensor_values

app = FastAPI()


class Sensor(BaseModel):
    value: Union[int, float]


@app.get("/ping")
def read_ping():
    return {"ping": "pong"}

#
# @router.on_event("startup")
# @repeat_every(seconds=50)
# async def collect_data():
#     sensor_value_a0, temp_ds18b20, co2_sensor_value, gray_scale = read_sensor_values()
#     pass
