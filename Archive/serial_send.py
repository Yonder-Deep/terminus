import serial
import time
import struct
import xbox
import math
import os

#print("Calibrating joystick driver...")
#os.system('sudo xboxdrv --detach-kernel-driver')
#time.sleep(2)

joy = xbox.Joystick()
speed = 0
delay = 0.1
maxSpeed = 50
minSpeed = 0
turnSpeed = 50
motorIncrements = 8
maxSpeed = 100
notConnected = True
	
ser = serial.Serial('/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DN0393EE-if00-port0', 
					baudrate = 115200,
					parity = serial.PARITY_NONE,
					stopbits = serial.STOPBITS_ONE,
					bytesize = serial.EIGHTBITS,
					timeout = 1 
				)

ser.flush()

while not joy.connected():
	pass


while notConnected:
	# Send calibrate signal to AUV.
	if joy.Start() == 1:
		print("Attempting to connect to AUV...")
		ser.write('CAL\n')
	
		# Await response from AUV.
		if ser.readline() == 'CAL\n':
			notConnected = False	

print("Connection Received")




while False:

	motorSpeedRight = 0
	motorSpeedLeft = 0	
	
	if joy.rightBumper():
		rightStickValue = math.floor(joy.rightX() * motorIncrements) / motorIncrements
		motorSpeedRight = int(turnSpeed * (-rightStickValue))
		motorSpeedLeft = int(turnSpeed * rightStickValue)
		motorSpeedBase = 0
	else:
		if joy.rightTrigger() > 0:
			motorSpeedBase = int(joy.rightTrigger()*maxSpeed)
		else:
			motorSpeedBase = int(-1*joy.leftTrigger() * maxSpeed)

		leftStickValue = math.floor( ( (joy.leftX() + 1 ) / 2) * motorIncrements) / motorIncrements
		motorSpeedLeft = int(leftStickValue * motorSpeedBase)
		motorSpeedRight = int((1 - leftStickValue) * motorSpeedBase) 
	
	if motorSpeedLeft < 0:
		motorSpeedLeft *= -1
		motorSpeedLeft += 100
		
	if  motorSpeedRight < 0:
		motorSpeedRight *= -1
		motorSpeedRight += 100

	if motorSpeedBase < 0:
		motorSpeedBase *= -1
		motorSpeedBase += 100	
	print("Base motor ", str(motorSpeedBase)); 
	print("Left motor ", str(motorSpeedLeft));
	print("Right motor ", str(motorSpeedRight)); 
 
	ballast = 0
	speed_f = chr(motorSpeedLeft) + chr(motorSpeedRight) + chr(motorSpeedBase) + chr(ballast) + '\n'
	print("Speed f ", speed_f)
	ser.write(speed_f)
	time.sleep(0.05)

