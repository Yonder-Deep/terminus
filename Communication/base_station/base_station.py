'''
This class manages the serial connection between the 
AUV and Base Station along with sending controller 
commands.
'''

import serial
import time
import struct
import xbox
import math
import os
import argparse
from nav import NavController

speed = 0
delay = 0.1
maxSpeed = 50
minSpeed = 0
turnSpeed = 50
motorIncrements = 8
maxSpeed = 100

class BaseStation:
    def __init__(self, debug=False):

        '''
        Initialize Serial Port and Class Variables

        debug: debugging flag
        '''

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
        self.navController = None
        self.debug = debug
        self.esc_connected = False

    def calibrate_controller(self):
        '''
        Instantiates a new Xbox Controller Instance and NavigationController
        '''

        # Remove the xpad module that interferes with xboxdrv.
        #os.system('sudo rmmod xpad 2> /dev/null')

        # Construct joystick and check that the driver/controller are working.
        self.joy = xbox.Joystick()

        #Instantiate New NavController With Joystick
        self.navController = NavController(self.joy, self.debug)

        # Check that the xbox controller is connected.
        print("Press the back button to calibrate the controller...")
        while not self.joy.Back():
            pass
        print("Controller calibrated.\n")
        
        self.calibrate_communication()

    def calibrate_communication(self):
        '''
        Ensure communication between AUV and Base Station
        '''
        
        esc_connected = False
        
        # Flush the serial connection.
        self.ser.flush()

        print("Press the start button to establish connection to AUV...")

        # Wait until connection is established.
        while not self.connected_to_auv:
            
            # Send calibrate signal on start press.
            if self.joy.Start() == 1:
                
                print("Attempting to connect to AUV...")
                
                #Send Calibration Signal To AUV
                self.ser.write('CAL\n')

                # Await response from AUV. Times out after 1 second.
                self.connected_to_auv = (self.ser.readline() == 'CAL\n')
                if not self.connected_to_auv:
                    print("Connection timed out, please try again...\n")

        print("Connection established with AUV.")


 
    def run(self):
        ''' 
        Runs the controller loop for the AUV.
        '''

        #Check ESC Connection Status 
        data = self.ser.readline()
        while data != "ESC\n":
            data = self.ser.readline()
        
        self.esc_connected = True
        
        #Start Control Loop
        while self.esc_connected:
            
            #Get packet
            speed_f = self.navController.getPacket()
            
            if self.debug:
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

    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()

    bs = BaseStation(debug=args.debug)
    
    bs.calibrate_controller()
    
    bs.run()


if __name__ == '__main__':
    main()
