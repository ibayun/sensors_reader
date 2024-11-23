There is a table wich shows how sensors should be connected with arduino

Name | pins | voltage | additional |
|---|---|---|---|
| Moisture | A0 | +5 | |
| CO2          | A2 | +5 |  |
| Gray sensoe | A3 | +5 |  old version. need 5?k resistor |
| Light Intensity | A3 | +5 | |
| Bluetooth | RX, TX | +5 | |
| Temerature | A4, A5 | +3| AHT20, BMP280|
| DC/Current | A4, A5 | +5| ina3221 |

more info woh to work with many sensors by i2c [here](https://learn.adafruit.com/working-with-multiple-i2c-devices/overview)
