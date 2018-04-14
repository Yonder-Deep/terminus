import serial
import time
import struct
import xbox
import math
import os


speed = 0
delay = 0.1
maxSpeed = 50
minSpeed = 0
turnSpeed = 50
motorIncrements = 8
maxSpeed = 100


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

class BaseStation:
    def __init__(self):
        self.joy = None
        self.ser = serial.Serial('/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DN0393EE-if00-port0', 
                                    baudrate = 115200,
                                    parity = serial.PARITY_NONE,
                                    stopbits = serial.STOPBITS_ONE,
                                    bytesize = serial.EIGHTBITS,
                                    timeout = 1 
                                )
        self.connected_to_auv = False

    def calibrate_controller(self):
        input("Calibrating joystick driver. If successful Ctrl-C the driver
                program. Otherwise, reconnect the controller and rerun this
                progam. Press any key to continue...")

        # Run the controller driver.
        os.system('sudo xboxdrv --detach-kernel-driver')
        
        # Construct joystick and check that the driver/contrller are working.
        self.joy = xbox.Joystick()
        
        # Stop the program if the joystick failed to connect.
        if not joy.connected():
            print("Controller connection failed. Please try again.")
            exit(1)

    def calibrate_communication(self):
        # Flush the serial connection.
        ser.flush()

        print("Press the start button to establish connection to AUV...")

        # Wait until connection is established.
        while not self.connected_to_auv:
            # Send calibrate signal to AUV.
            if joy.Start() == 1:
                print("Attempting to connect to AUV...")
                ser.write('CAL\n')
	
            # Await response from AUV. Times out after 1 second.
            self.connected_to_auv = ser.readline() == 'CAL\n'

        print("Connection established with AUV.")

    def run(self):
        pass

def main(): 
    bs = BaseStation()
    bs.calibrate_controller()
    bs.calibrate_communication()
    bs.run()


if __name__ == '__main__':
    main()

