
import serial

ser = serial.Serial('/dev/rfcomm0', 9600, timeout=1)  # Измените на ваш порт и скорость передачи данных


def read_sensor_values(raw):
    # Reading bytes (2 bytes per int value sensor, 4 for float)
    data = raw[0] + raw[1] if len(raw)>1 else raw[0]
    import struct
    # print(struct.unpack('<f', bytes(data))[0])
    # Преобразуем первые 2 байта в число типа int для датчика на A0
    moisture = (data[1] << 8) | data[0]
    # Преобразуем следующие 2 байта в число типа float для датчика DS18B20
    temperature = struct.unpack('<f', bytes(data)[2:6])[0]
    # CO2 sensor extract the data
    co2_sensor_value = (data[7] << 8) | data[6]
    # co2_sensor_value = 0
    # Gray scale sensor
    gray_scale = (data[9] << 8) | data[8]

    pressure = struct.unpack('<f', bytes(data)[10:14])[0]
    altimeter = (data[15] << 8) | data[14]
    return moisture, temperature, co2_sensor_value, gray_scale, pressure, altimeter


def retrieve_data():
    ser.write(b'1')
    data = ""
    try:
        data = ser.readlines()
    except Exception as exc:
        print(exc)
    return data
    
def run_sensor_collect():
    moisture=temperature=co2_sensor_value=gray_scale = ""
    try:
        moisture, temperature, co2_sensor_value, gray_scale, *args = read_sensor_values(retrieve_data())
    except KeyboardInterrupt:
        print("Program was interruted by user")
    return moisture, temperature, co2_sensor_value, gray_scale
    
if __name__ == "__main__":
    print(run_sensor_collect())

