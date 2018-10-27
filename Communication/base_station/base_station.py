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
esc_connected = False

class BaseStation:
    def __init__(self):
        global speed_f
        self.joy = None
        self.ser = serial.Serial('/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DN0393EE-if00-port0',
                                    baudrate = 115200,
                                    parity = serial.PARITY_NONE,
                                    stopbits = serial.STOPBITS_ONE,
                                    bytesize = serial.EIGHTBITS,
                                    timeout = 5
                                )
        self.connected_to_auv = False

    def calibrate_controller(self):
        # Remove the xpad module that interferes with xboxdrv.
        #os.system('sudo rmmod xpad 2> /dev/null')

        # Construct joystick and check that the driver/controller are working.
        self.joy = xbox.Joystick()

        # Check that the xbox controller is connected.
        print("Press the back button to calibrate the controller...")
        while not self.joy.Back():
            pass
        print("Controller calibrated.\n")

    def calibrate_communication(self):
        esc_connected = False
        # Flush the serial connection.
        self.ser.flush()

        print("Press the start button to establish connection to AUV...")

        # Wait until connection is established.
        while not self.connected_to_auv:
            # Send calibrate signal to AUV.
            if self.joy.Start() == 1:
                print("Attempting to connect to AUV...")
                self.ser.write('CAL\n')

                # Await response from AUV. Times out after 1 second.
                self.connected_to_auv = (self.ser.readline() == 'CAL\n')
                if not self.connected_to_auv:
                    print("Connection timed out, please try again...\n")

        print("Connection established with AUV.")

    def run(self):
        global esc_connected
        data = self.ser.readline()
        while data != "ESC\n":
            data = self.ser.readline()
        esc_connected = True

        while esc_connected:
            motorSpeedRight = 0
            motorSpeedLeft = 0

            if self.joy.rightBumper():
                rightStickValue = math.floor(self.joy.rightX() * motorIncrements) / motorIncrements
                motorSpeedRight = int(turnSpeed * (-rightStickValue))
                motorSpeedLeft = int(turnSpeed * rightStickValue)
                motorSpeedBase = 0
            else:
                if self.joy.rightTrigger() > 0:
			        motorSpeedBase = int(self.joy.rightTrigger()*maxSpeed)
                else:
                    motorSpeedBase = int(-1*self.joy.leftTrigger() * maxSpeed)

                leftStickValue = math.floor( ( (self.joy.leftX() + 1 ) / 2) * motorIncrements) / motorIncrements
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
            with open('data.txt', 'w') as f:
                f.write(speed_f)
            print("Speed f ", speed_f)
            self.ser.write(speed_f)
            # Await response from AUV.
            if self.ser.readline() != 'REC\n':
                self.connected_to_auv = False
                print("WARNING - AUV disconnected")
                self.calibrate_communication()
                data = self.ser.readline()
                while data != "ESC\n":
                    data = self.ser.readline()
            time.sleep(0.05)

# TODO: Comment run, find out when auv disconnects.
def main():
    bs = BaseStation()
    bs.calibrate_controller()
    bs.calibrate_communication()
    bs.run()


if __name__ == '__main__':
    main()
