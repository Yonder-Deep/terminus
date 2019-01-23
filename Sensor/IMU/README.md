# Set up BNO055 on Raspberry Pi
Detailed guide from [Adafruit](https://cdn-learn.adafruit.com/downloads/pdf/bno055-absolute-orientation-sensor-with-raspberry-pi-and-beaglebone-black.pdf)
## Setup UART
Type the following command in terminal shell on Raspberry Pi, and edit as follows
```
sudo raspi-config
```
`5 Interfacing Options` >> `P6 Serial`
> Login shell to be accessible over serial: `No`
> Serial port hardware to be enabled `Yes`

After the settings it should ask for reboot. choose `Yes`
## Connect BNO055 to Raspberry Pi
|BNO055|RPi|
| ------------ | ------------ |
|Vin|3V3|
|GND|GND|
|SDA|RXD|
|SCL|TXD|
|PS1|3V3 (BNO's Vin)|

## Install library and run test code
```
git clone https://github.com/adafruit/Adafruit_Python_BNO055.git
cd ~/Adafruit_Python_BNO055
sudo python setup.py install
cd xcexamples
nano simpletest.py
```
