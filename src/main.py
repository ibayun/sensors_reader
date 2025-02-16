import asyncio
import logging
import json
from datetime import datetime

import uvicorn
from fastapi_utilities import repeat_every
from datetime import date
from fastapi import FastAPI, APIRouter

from queries import *
from services import extract_data_from_device
from utils import log_execution_time

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
    data = extract_data_query(interval=interval, start_date=start_date, end_date=end_date)
    return data


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(collect_data())

@log_execution_time
async def collect_data():
    while True:
        data = await extract_data_from_device()
        if data:
            await write_sensors_data(json_data=json.dumps(data), timestamp_data=datetime.now().timestamp())
        else:
            logger.info('Devices are sleeping...')
        await asyncio.sleep(5)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config="log.ini")
