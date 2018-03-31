import serial
import time
import struct
import xbox

import math

joy = xbox.Joystick()
speed = 0
delay = 0.1
maxSpeed = 50
minSpeed = 0
turnSpeed = 50
motorIncrements = 8
maxSpeed = 100


while True:
	ser = serial.Serial('/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DN0393EE-if00-port0', 
						baudrate = 115200,
						parity = serial.PARITY_NONE,
						stopbits = serial.STOPBITS_ONE,
						bytesize = serial.EIGHTBITS
					)
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

	if motorSpeedLeft < 10:
		motorSpeedLeft = "00" + str(motorSpeedLeft)
	elif motorSpeedLeft < 100:
		motorSpeedLeft = "0" + str(motorSpeedLeft)
		
	if motorSpeedRight < 10:
		motorSpeedRight = "00" + str(motorSpeedRight)
	elif motorSpeedRight < 100:
		motorSpeedRight = "0" + str(motorSpeedRight)

#	print("Base motor ", str(motorSpeedBase)); 
	print("Left motor ", str(motorSpeedLeft));
	print("Right motor ", str(motorSpeedRight)); 
 
	speed_f = str(motorSpeedLeft) + str(motorSpeedRight)
	print("Speed f ", speed_f)
	ser.write(speed_f)
	time.sleep(0.05)

