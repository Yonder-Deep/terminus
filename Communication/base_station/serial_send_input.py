import serial
import time
import struct
import xbox

speed = 0
delay = 0.1
maxSpeed = 50
minSpeed = 0

while True:
	ser = serial.Serial('/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DN0393EE-if00-port0', 		
						baudrate = 115200,
						parity = serial.PARITY_NONE,
						stopbits = serial.STOPBITS_ONE,
						bytesize = serial.EIGHTBITS
					)

	speed = raw_input("Enter speed ")	
#	string = raw_input("Enter string ")
	val = chr(int(speed))
	bytes_sent = ser.write(val)
	print("Type: ", val)
	print("bytes_sent is: ", bytes_sent)
