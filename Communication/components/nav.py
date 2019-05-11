import serial
import time
import struct
import xbox
import math
import os

class NavController:
	def __init__(self, joy, button_cb, debug=False):
		self.joy = joy
		self.counter = 0
		self.state = None
		self.maxSpeed = 50
		self.turnSpeed = 50
		self.motorIncrements = 8
		self.maxSpeed = 100
		self.debug = debug	
		self.cb = button_cb

	def handle(self):
		motorSpeedRight = 0
		motorSpeedLeft = 0	
		# ballastSpeed = 0
		# ballast = 0

		# In place turn
		in_place_turn = self.joy.rightBumper()  # Press right bumper for in place turn
		forward_drive = self.joy.rightTrigger()  # Right trigger speed
		backward_drive = self.joy.leftTrigger()  # Left trigger speed
		ballast = self.joy.B()
		# print("[CONTL]", in_place_turn, forward_drive, backward_drive, ballast)



		if in_place_turn:
				rightStickValue = math.floor(self.joy.rightX() * self.motorIncrements) / self.motorIncrements

				motorSpeedRight = int(self.turnSpeed * (-rightStickValue))
				motorSpeedLeft = int(self.turnSpeed * rightStickValue)
				motorSpeedBase = 0
				self.cb['MAN'](motorSpeedLeft, motorSpeedRight, 0, 0)
		# Left, right, down, up controls
		elif forward_drive or backward_drive:
			if forward_drive:
				motorSpeedBase = int(forward_drive*self.maxSpeed)	
			elif backward_drive:
				motorSpeedBase = int(-1*backward_drive * self.maxSpeed)
			
			# Don't change; Raman's magic code
			leftStickValue = math.floor( ( (self.joy.leftX() + 1) / 2) * self.motorIncrements) / self.motorIncrements
			motorSpeedLeft = int(leftStickValue * motorSpeedBase)
			motorSpeedRight = int((1 - leftStickValue) * motorSpeedBase) 

			if motorSpeedLeft < 0:
				motorSpeedLeft *= -1
				motorSpeedLeft += 100

			if motorSpeedRight < 0:
				motorSpeedRight *= -1
				motorSpeedRight += 100

			if self.debug:
				print("Left motor ", str(motorSpeedLeft));
				print("Right motor ", str(motorSpeedRight)); 

			self.cb['MAN'](motorSpeedLeft, motorSpeedRight, 0, 0)

		elif ballast:
			self.cb['BAL']()


