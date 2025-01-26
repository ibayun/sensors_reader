import logging
import os

from contextlib import contextmanager
from datetime import datetime

import serial
import struct
import bluetooth
import json

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)


@contextmanager
def socketcontext(*args, **kwargs):
    bluetooth_adress = os.environ.get("BLUETOOTH_ADRESS")

    if not bluetooth_adress:
        raise ValueError("bluetooth_adress is not in .env file")
    logger.info(f"Trying to connect - {datetime.now()}\n")
    sensor_address = bluetooth_adress
    socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    socket.connect((sensor_address, 1))
    logger.info("Connected\n")
    
    try:
        yield socket
    finally:
        socket.close()
        logger.info("DisConnected\n")


def read_the_data_from_socked(socket):
    data = ''
    piece = b''
    end_of_string = b'\r\n'
    while end_of_string not in piece:
        piece = socket.recv(1048)
        data += str(piece, encoding='ascii')
    return data


def updated_parser():
    with socketcontext() as sock:
        logger.info("Start READing...\n")
        sock.send(b'1')
        parsed_data = read_the_data_from_socked(sock)
        try:
            data = json.loads(parsed_data)
            logger.info(f"{data}")
        except json.JSONDecodeError as e:
            logger.info(f"Caught the next error - {e}")
    
    return data


def run_sensor_collect():
    data = {}
    try:
        data = updated_parser()
    except KeyboardInterrupt:
        logger.info("Program was interrupted by user")
    return data


if __name__ == "__main__":
    while True:
        import time
        run_sensor_collect()
        time.sleep(2)
