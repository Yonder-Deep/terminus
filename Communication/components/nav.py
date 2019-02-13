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
		ballastSpeed = 0
		ballast = 0

		# In place turn
		if self.joy.rightBumper():
				rightStickValue = math.floor(self.joy.rightX() * self.motorIncrements) / self.motorIncrements

				motorSpeedRight = int(self.turnSpeed * (-rightStickValue))
				motorSpeedLeft = int(self.turnSpeed * rightStickValue)
				motorSpeedBase = 0
		# Left, right, down, up controls
		else:
				self.rightTrig = self.joy.rightTrigger()
				if self.rightTrig > 0:
					motorSpeedBase = int(self.rightTrig*self.maxSpeed)
					
				else:
					motorSpeedBase = int(-1*self.joy.leftTrigger() * self.maxSpeed)

				# Don't change; Raman's magic code
				leftStickValue = math.floor( ( (self.joy.leftX() + 1 ) / 2) * self.motorIncrements) / self.motorIncrements
				motorSpeedLeft = int(leftStickValue * motorSpeedBase)
				motorSpeedRight = int((1 - leftStickValue) * motorSpeedBase) 
				
				if self.joy.B():
					ballast = 1
					motorSpeedLeft = 0
					motorSpeedRight = 0
					#setting ballast speed to half speed downwards
					ballastSpeed = 125

				if self.joy.X():
					motorSpeedLeft = 0
					motorSpeedRight = 0
					#setting ballast speed to half speed upwards
					ballastSpeed = 25
		if motorSpeedLeft < 0:
				motorSpeedLeft *= -1
				motorSpeedLeft += 100

		if  motorSpeedRight < 0:
				motorSpeedRight *= -1
				motorSpeedRight += 100

		if ballastSpeed < 0:
				ballastSpeed *= -1
				ballastSpeed += 100	
		if self.debug:
			print("Base motor ", str(motorSpeedBase)); 
			print("Left motor ", str(motorSpeedLeft));
			print("Right motor ", str(motorSpeedRight)); 

					
		speed_f = chr(motorSpeedLeft) + chr(motorSpeedRight) + chr(ballastSpeed) + chr(ballast) + '\n'
		"""for i, speed in enumerate(speed_f):
			print("index ", i)
			print("is speed: ", speed)
			
		print("returning speed_f, which is: ", speed_f)
		print("lelngth of speed_f is: ", len(speed_f) )"""

		return speed_f


