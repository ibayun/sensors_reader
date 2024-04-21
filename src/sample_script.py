import smbus2
import time

# Address through I2C
ARDUINO_ADDRESS = 0x12

# Initialize I2C
bus = smbus2.SMBus(1)

def read_sensor_values():
    # Reading 10 bytes (2 bytes per sensor)
    data = bus.read_i2c_block_data(ARDUINO_ADDRESS, 0, 10)
    import struct
    # print(struct.unpack('<f', bytes(data))[0])
    # Convert to int data from the sensoar that stoers in the A0 pin
    sensor_value_a0 = (data[1] << 8) | data[0]

    # COnvert 4 bytes of the float for DS18B20
    temp_ds18b20 = struct.unpack('<f', bytes(data)[2:6])[0]

    # CO2 sensor extract the data
    co2_sensor_value = (data[7] << 8) | data[6]

    # Gray scale sensor
    gray_scale = (data[9] << 8) | data[8]
    return sensor_value_a0, temp_ds18b20, co2_sensor_value, gray_scale

def run_sensor_collect():
    sensor_value_a0=temp_ds18b20=co2_sensor_value=gray_scale = ""
    try:

        # Read data from the  sensors
        sensor_value_a0, temp_ds18b20, co2_sensor_value, gray_scale = read_sensor_values()

        # print("---------------------------------------")
        # print("Humidity: ", sensor_value_a0)
        #print("Temperature DS18B20:", temp_ds18b20)
        #print("CO2 sensor value:", co2_sensor_value)
        #print("Gray scale sensor value:", gray_scale)
        from datetime import datetime
        with open('sensors_21.txt', "a+") as f:
            d = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c = d + ":  " + "moisture - " + str(sensor_value_a0) + " temp - " + str(temp_ds18b20)[:4] + " co2 - " + str(co2_sensor_value) + " gray - " + str(gray_scale) + "\n"
            f.write(c)
            #time.sleep(5) # waiting fo the next values

    except KeyboardInterrupt:
        print("Program was interruted by user")
    return sensor_value_a0, temp_ds18b20, co2_sensor_value, gray_scale
