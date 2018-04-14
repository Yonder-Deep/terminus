import serial
import time
import struct

while True:
	ser = serial.Serial('/dev/ttyUSB0', baudrate = 9600,
						parity = serial.PARITY_NONE,
						stopbits = serial.STOPBITS_ONE,
						bytesize = serial.EIGHTBITS
					)
	print ser.read()
	time.sleep(1)
