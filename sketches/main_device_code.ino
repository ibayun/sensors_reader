
#include <Adafruit_Sensor.h>
#include "Adafruit_BMP280.h"
#include <microDS18B20.h>
#include <GyverPower.h>
#include <ArduinoJson.h>
#include <SoftwareSerial.h>
#include "Wire.h"
#include "SDL_Arduino_INA3221.h"

const int RX_PIN = 0; // Bluetooth RX digital PWM-supporting pin
const int TX_PIN = 1; // Bluetooth TX digital PWM-supporting pin
SDL_Arduino_INA3221 ina3221; // instance of ina 3221
const int BLUETOOTH_BAUD_RATE = 9600;
#define SERIAL_TX_BUFFER_SIZE 1024
#define SERIAL_RX_BUFFER_SIZE 1024

SoftwareSerial bluetooth(RX_PIN, TX_PIN);

MicroDS18B20<A1> ds; // Initialize a new object ds for sensor DS18B20
Adafruit_BMP280 bmp; // I2C
int val = 0;


//Variables
float pressure;		//To store the barometric pressure (Pa)
float temperature;	//To store the temperature (oC)
int altimeter; 		//To store the altimeter (m) (you can also use it as a float variable)

// channels for ina 3221
#define CHANNEL_1 1
#define CHANNEL_2 2
#define CHANNEL_3 3

void setup() {
  power.setSleepMode(POWERDOWN_SLEEP);
	bmp.begin();		//Begin the sensor
  ina3221.begin();
  int id = ina3221.getManufID();
  bluetooth.begin(BLUETOOTH_BAUD_RATE);
  Serial.begin(9600);	//Begin serial communication at 9600bps
  Serial.println("Run:");
}

void loop() {
  StaticJsonDocument<200> doc;

  //ina data
  float busvoltage1 = ina3221.getBusVoltage_V(CHANNEL_1);
  float busvoltage2 = ina3221.getBusVoltage_V(CHANNEL_2);
  float busvoltage3 = ina3221.getBusVoltage_V(CHANNEL_3);
  float shuntvoltage1 = ina3221.getShuntVoltage_mV(CHANNEL_1);
  float shuntvoltage2 = ina3221.getShuntVoltage_mV(CHANNEL_2);
  float shuntvoltage3 = ina3221.getShuntVoltage_mV(CHANNEL_3);
  float loadvoltage1 = busvoltage1 + (shuntvoltage1 / 1000);
  float loadvoltage2 = busvoltage2 + (shuntvoltage2 / 1000);
  float loadvoltage3 = busvoltage3 + (shuntvoltage3 / 1000);
  float current_mA1 = ina3221.getCurrent_mA(CHANNEL_1);
  float current_mA2 = ina3221.getCurrent_mA(CHANNEL_2);
  float current_mA3 = ina3221.getCurrent_mA(CHANNEL_3);

  //Read values from the sensor:
  pressure = bmp.readPressure();
  temperature = bmp.readTemperature();
  altimeter = bmp.readAltitude (1008.90537); //Change the "1050.35" to your city current barrometric pressure (https://www.wunderground.com)


  int moisture = analogRead(A0); // moisture
  int mq7 = analogRead(A2); // CO2 saensor
  int graysc = analogRead(A3); // Grayscale sensor

  doc["moisture"] = moisture;
  doc["temperature"] = temperature;
  doc["co2_sensor_value"] = mq7;
  doc["pressure"] = pressure;
  doc["altimeter"] = altimeter;
  doc["gray_scale"] = graysc;

  doc["ina3221"]["busvoltage1"] = busvoltage1;
  doc["ina3221"]["busvoltage2"] = busvoltage2;
  doc["ina3221"]["busvoltage3"] = busvoltage3;
  doc["ina3221"]["shuntvoltage1"] = shuntvoltage1;
  doc["ina3221"]["shuntvoltage2"] = shuntvoltage2;
  doc["ina3221"]["shuntvoltage3"] = shuntvoltage3;
  doc["ina3221"]["loadvoltage1"] = loadvoltage1;
  doc["ina3221"]["loadvoltage2"] = loadvoltage2;
  doc["ina3221"]["loadvoltage3"] = loadvoltage3;
  doc["ina3221"]["current_mA1"] = current_mA1;
  doc["ina3221"]["current_mA2"] = current_mA2;
  doc["ina3221"]["current_mA3"] = current_mA3;

  serializeJson(doc, bluetooth);
  serializeJson(doc, Serial);

  Serial.println();
  delay(2000);
}

