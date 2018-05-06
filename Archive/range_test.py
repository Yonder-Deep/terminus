import serial
import time
import struct

ser = serial.Serial('/dev/tty.usbserial-DN038PQU', baudrate = 115200,
                                    parity = serial.PARITY_NONE,
                                    stopbits = serial.STOPBITS_ONE,
                                    bytesize = serial.EIGHTBITS
                   )
ser.flush() 
while True:
	print(list(ser.readline())[0])
