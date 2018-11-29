import xbox
import serial
import struct
import math
import os
import time


speed = 0
delay = 0.1
maxSpeed = 50
minSpeed = 0
turnSpeed = 50
motorIncrements = 8
maxSpeed = 100

serial_port = serial.Serial('/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DN0393EE-if00-port0',
							baudrate = 115200,
							parity = serial.PARITY_NONE,
							stopbits = serial.STOPBITS_ONE,
							bytesize = serial.EIGHTBITS,
							timeout = 5)

class base_station:
	
	def __init__(self, base_radio, base_controller):

		self.base_radio = base_radio
		self.base_controller = base_controller

	def start(self):
		print("Starting to send values")
		while self.base_radio.connected_to_auv:
			motorSpeedRight = 0
			motorSpeedLeft = 0

			if self.base_controller.joy.rightBumper():
				rightStickValue = math.floor(self.base_controller.joy.rightX() * motorIncrements) / motorIncrements
				motorSpeedRight = int(turnSpeed * (-rightStickValue))
				motorSpeedLeft = int(turnSpeed * rightStickValue)
				motorSpeedBase = 0
			else:
				if self.base_controller.joy.rightTrigger() > 0:
					motorSpeedBase = int(self.base_controller.joy.rightTrigger()*maxSpeed)
				else:
					motorSpeedBase = int(-1*self.base_controller.joy.leftTrigger() * maxSpeed)

				leftStickValue = math.floor( ( (self.base_controller.joy.leftX() + 1 ) / 2) * motorIncrements) / motorIncrements
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
			self.base_radio.serial.write(speed_f)
			# Await response from AUV.
			if self.base_radio.serial.readline() != 'REC\n':
				print("waiting response from auv")
				self.base_radio.connected_to_auv = False
				print("WARNING - AUV disconnected")
				self.calibrate_communication()
				data = self.base_radio.serial.readline()
				while data != "ESC\n":
					data = self.base_radio.seial.readline()
			time.sleep(0.05)


class base_radio:
	
	def __init__(self, serial_port, joystick):

		self.serial = serial_port
		self.connected_to_auv = False
		self.joy = joystick
		
	def calibrate_communication(self):

		self.serial.flush()

		print("Press the start button to establish connection to AUV")		
		while not self.connected_to_auv:
			
			if self.joy.Start() == 1:
				print("Attempting to connect to AUV... ")
				self.serial.write('CAL\n')
				
				print("Sent 'CAL\\n', expecting to recieve 'CAL\\n' back")
				data_rec = self.serial.readline()
				print("Data recieved is ", data_rec)
				self.connected_to_auv = (data_rec == 'CAL\n')

				if not self.connected_to_auv:
					print("Connection timed out, try again...\n")			
		print("Connection established with AUV radios")			

class base_controller:

	def __init__(self):
		
		self.joy = xbox.Joystick()

	def calibrate(self):	
		print("Press the back button to calibrate the controller...")
		while not self.joy.Back():
			pass
		print("Controller calibrated.\n")


controller = base_controller()
radio = base_radio(serial_port, controller.joy)

base_station = base_station(radio, controller)
base_station.base_controller.calibrate()
base_station.base_radio.calibrate_communication()

base_station.start()
