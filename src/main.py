import json
import logging
from datetime import datetime

import uvicorn
from fastapi_utilities import repeat_every
from datetime import date
from fastapi import FastAPI, APIRouter

from connector import ch_client
from sample_script import run_sensor_collect
from queries import *


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)


app = FastAPI()
router = APIRouter()
app.include_router(router)


@app.get("/ping")
async def read_ping():
    return {"ping": "pong"}


@app.get("/exctract_data")
async def get_data(interval: int = 120, start_date: date = date(2024, 4, 28), end_date: date = date(2024, 4, 29)):
    data_query = exctract_data_query(interval=interval, start_date=start_date, end_date=end_date)
    data = ch_client.execute(data_query)
    return data


@app.on_event("startup")
@repeat_every(seconds=4)
async def collect_data():
    sensor_value_a0 = temp_ds18b20 = co2_sensor_value = gray_scale = ""
    d = datetime.now()
    try:
        sensor_value_a0, temp_ds18b20, co2_sensor_value, gray_scale = run_sensor_collect()
    except Exception as exc:
        print(exc)

    timestamp_data = d.timestamp()
    data = {"moisture": sensor_value_a0, "temperature": temp_ds18b20, "co2": co2_sensor_value, "gray": gray_scale}
    json_data = json.dumps(data)
    logger.debug(f'{timestamp_data} - {json_data}')
    query = f"Insert into device_data (datas, timestamp) VALUES ('{json_data}', {timestamp_data})"
    ch_client.execute(query)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config="log.ini")
