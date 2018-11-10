import serial
import time
import struct
import xbox
import math
import os

class NavController:
	def __init__(self, joy, debug=False):
		self.joy = joy
		self.state = None
		self.maxSpeed = 50
		self.turnSpeed = 50
		self.motorIncrements = 8
		self.maxSpeed = 100
		self.debug = debug	
	def getPacket(self):

		motorSpeedRight = 0
		motorSpeedLeft = 0	

		if self.joy.rightBumper():
				rightStickValue = math.floor(self.joy.rightX() * self.motorIncrements) / self.motorIncrements
				motorSpeedRight = int(self.turnSpeed * (-rightStickValue))
				motorSpeedLeft = int(self.turnSpeed * rightStickValue)
				motorSpeedBase = 0
		else:
				if self.joy.rightTrigger() > 0:
					motorSpeedBase = int(self.joy.rightTrigger()*self.maxSpeed)
				else:
						motorSpeedBase = int(-1*self.joy.leftTrigger() * self.maxSpeed)

				leftStickValue = math.floor( ( (self.joy.leftX() + 1 ) / 2) * self.motorIncrements) / self.motorIncrements
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
		if self.debug:
			print("Base motor ", str(motorSpeedBase)); 
			print("Left motor ", str(motorSpeedLeft));
			print("Right motor ", str(motorSpeedRight)); 

		ballast = 0  
					
		speed_f = chr(motorSpeedLeft) + chr(motorSpeedRight) + chr(motorSpeedBase) + chr(ballast) + '\n'

		return speed_f


