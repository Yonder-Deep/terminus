#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError
from time import sleep

SHUNT_OHMS = 0.0003
MAX_EXPECTED_AMPS = 1.0
    
ina = INA219(SHUNT_OHMS)
ina.configure()
    
while True:
    print("Voltage: %.3f V" % ina.voltage())
    try:
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
        print("Current: %.3f A" % (ina.current()/1000))
        print("Power: %.3f W" % (ina.power()/1000))
    except DeviceRangeError as e:
        print (e)    
    sleep(5)