import json
import logging
import time
from datetime import datetime

import uvicorn
from fastapi_utilities import repeat_every
from datetime import date
from fastapi import FastAPI, APIRouter

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
    data = extract_data_query(interval=interval, start_date=start_date, end_date=end_date)
    return data


@app.on_event("startup")
@repeat_every(seconds=7)
async def collect_data():
    #sensor_value_a0 = temp_ds18b20 = co2_sensor_value = gray_scale = ""
    d = datetime.now()
    #while not sensor_value_a0:
        #try:
    data = run_sensor_collect()
        #except Exception as exc:
            #print(exc)
            
        #time.sleep(3)
    if data:
        moisture = data.get('moisture')
        temperature = data.get('temperature')
        co2_sensor_value = data.get('co2_sensor_value') 
        gray_scale = data.get('gray_scale')
        
        pressure = data.get('pressure')
        altimeter = data.get('altimeter')
        gray_scale = data.get('gray_scale')
        inas_data = data.get("ina3221")
        busvoltage1 = ''
        busvoltage2 = ''
        busvoltage3 = ''
        if inas_data:
            busvoltage1 = inas_data.get('busvoltage1')

            busvoltage2 = inas_data.get('busvoltage2')
            busvoltage3 = inas_data.get('busvoltage3')
            
            shuntvoltage1 = inas_data.get('shuntvoltage1')
            shuntvoltage2 = inas_data.get('shuntvoltage2')
            shuntvoltage3 = inas_data.get('shuntvoltage3')
            
            loadvoltage1 = inas_data.get('loadvoltage1')
            loadvoltage2 = inas_data.get('loadvoltage2')
            loadvoltage3 = inas_data.get('loadvoltage3')
            
            current_mA1 = inas_data.get('current_mA1')
            current_mA2 = inas_data.get('current_mA2')
            current_mA3 = inas_data.get('current_mA3')

        timestamp_data = d.timestamp()
        data_for_insert = {"moisture": moisture, "temperature": temperature, "co2": co2_sensor_value, "gray": gray_scale}
        if any([busvoltage1,busvoltage2,busvoltage3]):
            data_for_insert.update(
                {
                    "busvoltage1":busvoltage1, 
                    "busvoltage2":busvoltage2,
                    "busvoltage3":busvoltage3,
                    "shuntvoltage1":shuntvoltage1,
                    "shuntvoltage2":shuntvoltage2,
                    "shuntvoltage3":shuntvoltage3,
                    "loadvoltage1":loadvoltage1,
                    "loadvoltage2":loadvoltage3,
                    "loadvoltage3":loadvoltage3,
                    "current_mA1":current_mA1,
                    "current_mA2":current_mA2,
                    "current_mA3":current_mA3,
                }
            )
        json_data = json.dumps(data_for_insert)
        logger.debug(f'{d} - {json_data}')
        write_sensors_data(json_data=json_data, timestamp_data=timestamp_data)
    else:
        logger.debug(f'No solar energy... -- {sensor_value_a0}')


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config="log.ini")
