import logging
import os

from contextlib import contextmanager
from datetime import datetime

import bluetooth
import json

from dotenv import load_dotenv

from utils import log_execution_time


load_dotenv()

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)


@contextmanager
def socketcontext(*args, **kwargs):
    bluetooth_adress = os.environ.get("BLUETOOTH_ADRESS")

    if not bluetooth_adress:
        raise ValueError("bluetooth_adress is not in .env file")
    logger.info(f"Trying to connect - {datetime.now()}\n")
    socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    
    try:
        socket.connect((bluetooth_adress, 1))
        logger.info("Connected\n")
        yield socket
    except Exception as exc:
        logger.info(exc)
        yield None
    finally:
        socket.close()
        logger.info("DisConnected\n")


def read_the_data_from_socked(socket):
    raw_data = ''
    piece = b''
    end_of_string = b'\r\n'
    while end_of_string not in piece:
        piece = socket.recv(1048)
        raw_data += str(piece, encoding='ascii')
    return raw_data


def updated_parser():
    with socketcontext() as sock:
        if not sock:
            return []
        logger.info("Start READing...\n")
        sock.send(b'1')
        parsed_data = read_the_data_from_socked(sock)
        try:
            raw_data = json.loads(parsed_data)
            logger.info(f"{raw_data}")
        except json.JSONDecodeError as e:
            logger.info(f"Caught the next error - {e}")
    
    return raw_data


def run_sensor_collect():
    raw_data = {}
    try:
        raw_data = updated_parser()
    except KeyboardInterrupt:
        logger.info("Program was interrupted by user")
    return raw_data

def set_up_data_from_ina_sensor(inas_data, data_for_insert):
    busvoltage1 = inas_data.get('busvoltage1', "")

    busvoltage2 = inas_data.get('busvoltage2', "")
    busvoltage3 = inas_data.get('busvoltage3', "")

    shuntvoltage1 = inas_data.get('shuntvoltage1', "")
    shuntvoltage2 = inas_data.get('shuntvoltage2', "")
    shuntvoltage3 = inas_data.get('shuntvoltage3', "")

    loadvoltage1 = inas_data.get('loadvoltage1', "")
    loadvoltage2 = inas_data.get('loadvoltage2', "")
    loadvoltage3 = inas_data.get('loadvoltage3', "")

    current_mA1 = inas_data.get('current_mA1', "")
    current_mA2 = inas_data.get('current_mA2', "")
    current_mA3 = inas_data.get('current_mA3', "")
    if any([busvoltage1, busvoltage2, busvoltage3]):
        data_for_insert.update(
            {
                "busvoltage1": busvoltage1,
                "busvoltage2": busvoltage2,
                "busvoltage3": busvoltage3,
                "shuntvoltage1": shuntvoltage1,
                "shuntvoltage2": shuntvoltage2,
                "shuntvoltage3": shuntvoltage3,
                "loadvoltage1": loadvoltage1,
                "loadvoltage2": loadvoltage3,
                "loadvoltage3": loadvoltage3,
                "current_mA1": current_mA1,
                "current_mA2": current_mA2,
                "current_mA3": current_mA3,
            }
        )


@log_execution_time
async def extract_data_from_device():
    d = datetime.now()
    raw_data = run_sensor_collect()
    if raw_data:
        moisture = raw_data.get('moisture')
        temperature = raw_data.get('temperature')
        co2_sensor_value = raw_data.get('co2_sensor_value')

        pressure = raw_data.get('pressure')
        altimeter = raw_data.get('altimeter') # TODO
        gray_scale = raw_data.get('gray_scale')
        inas_data = raw_data.get("ina3221")
        data_for_insert = {
            "moisture": moisture,
            "temperature": temperature,
            "co2": co2_sensor_value,
            "gray": gray_scale,
            "pressure": pressure,
        }
        if inas_data:
            set_up_data_from_ina_sensor(inas_data, data_for_insert)
        await data_for_insert
    logger.info("Have no data")


if __name__ == "__main__":
    while True:
        import time
        run_sensor_collect()
        time.sleep(2)
