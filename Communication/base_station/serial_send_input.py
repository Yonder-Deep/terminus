import serial
import time
import struct
import xbox

speed = 0
delay = 0.1
maxSpeed = 50
minSpeed = 0
ser = serial.Serial('/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DN0393EE-if00-port0', 		
					baudrate = 115200,
					parity = serial.PARITY_NONE,
					stopbits = serial.STOPBITS_ONE,
					bytesize = serial.EIGHTBITS
				)

ser.flush()
while True:

	speed = input("Enter speed ")	
#	string = raw_input("Enter string ")
#	val = chr(int(speed))
#	for i in range(100):
	val = chr(speed)
	bytes_sent = ser.write(val + "\n")
	print("num_sent ", val)
	time.sleep(0.01)
	print("bytes_sent is: ", bytes_sent)
