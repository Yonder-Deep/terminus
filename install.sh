#!/bin/bash

# Dependencies for the project.
mkdir -p dependencies
cd dependencies

# Remove and update dependencies
rm -rf Adafruit_BNO055
rm -rf Adafruit_Sensor

# Adafruit BNO055 Sensor Driver for Arduino
git clone https://github.com/adafruit/Adafruit_BNO055.git
# Adafruit general sensor driver for Arduino
git clone https://github.com/adafruit/Adafruit_Sensor.git


echo  -e "\n-------------------------NOTE------------------------\nPlease copy dependencies/Adafruit_Sensor and dependencies/Adafruit_BNO055.git to your Arduino/libaries folder to use the sensor in the Arduino IDE."


