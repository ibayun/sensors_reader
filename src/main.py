
from datetime import datetime
import logging

import aiofiles
from fastapi_utilities import repeat_every
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from connector import ch_client
# from models import NewTable, session
from sample_script import read_sensor_values, run_sensor_collect

class IgnoreChangeDetectedFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return '%d change%s detected: %s' != record.msg

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)
logger.addFilter(IgnoreChangeDetectedFilter())

app = FastAPI()


class Sensor(BaseModel):
    value: Union[int, float]


@app.get("/ping")
async def read_ping():
    ping_file_name = f'{datetime.now().date()}_ping'
    async with aiofiles.open(ping_file_name, mode="a+") as f:
        d = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c = d + "\n"
        await f.write(c)
    return {"ping": "pong"}


from fastapi import APIRouter


router = APIRouter()
app.include_router(router)


@app.on_event("startup")
@repeat_every(seconds=4)
async def collect_data():
    sensor_value_a0=temp_ds18b20=co2_sensor_value=gray_scale=""
    d = datetime.now()
    log_file_name = f'sesnsors_{d.date()}'
    try:
        sensor_value_a0, temp_ds18b20, co2_sensor_value, gray_scale = run_sensor_collect()
    except Exception as exc:
        print(exc)
    async with aiofiles.open(log_file_name, mode="a+") as f:
        dates_ = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c = dates_ + ":  " + "moisture - " + str(sensor_value_a0) + " temp - " + str(temp_ds18b20)[:4] + " co2 - " + str(co2_sensor_value) + " gray - " + str(gray_scale) + "\n"

        await f.write(c)

    import json
    timestamp_data = d.timestamp()
    data = {"moisture": sensor_value_a0, "temperature": temp_ds18b20, "co2": co2_sensor_value, "gray": gray_scale}
    json_data = json.dumps(data)
    # print(timestamp_data, json_data)
    logger.debug(f'{timestamp_data} - {json_data}')
    query = f"Insert into device_data (datas, timestamp) VALUES ('{json_data}', {timestamp_data})"
    ch_client.execute(query)

import uvicorn


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config="log.ini")
