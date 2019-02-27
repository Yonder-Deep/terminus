'''
This class manages the serial connection between the 
AUV and Base Station along with sending controller 
commands.
'''
import sys
import os

# Sets the PYTHONPATH to include the components.
split_path = os.path.abspath(__file__).split('/')
split_path = split_path[0:len(split_path) - 2]
components_path = "/".join(split_path) + "/components"
sys.path.append(components_path)

import serial
import time
import struct
import math
import argparse
from nav import NavController
from nav import xbox
from radio import Radio

speed = 0
delay = 0.1
maxSpeed = 50
minSpeed = 0
turnSpeed = 50
motorIncrements = 8
maxSpeed = 100
speed_callibration = 10
#Hey we're using spaces
class BaseStation:
    def __init__(self, debug=False):

        '''
        Initialize Serial Port and Class Variables

        debug: debugging flag
        '''
	# Jack Silberman's radio
        #self.radio = Radio('/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DN0393EE-if00-port0')
	# Yonder's radio
        self.radio = Radio('/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0')
        self.speed_f = 0       
        self.joy = None 	
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
        self.radio.flush()

        print("Press the start button to establish connection to AUV...")

        # Wait until connection is established.
        while not self.connected_to_auv:
            
            # Send calibrate signal on start press.
            if self.joy.Start() == 1:
                
                print("Attempting to connect to AUV...")
                
                #Send Calibration Signal To AUV
                self.radio.write('CAL\n')

                #print(self.radio.readline())

                # Await response from AUV. Times out after 1 second.
                self.connected_to_auv = (self.radio.readline() == 'CAL\n')
                if not self.connected_to_auv:
                    print("self.radio.readline(): ", self.radio.readline())
                    print("self.connected_to_auv: ", self.connected_to_auv)
                    print("Connection timed out, please try again...\n")
		self.radio.flush()

        print("Connection established with AUV.")


 
    def run(self):
        ''' 
        Runs the controller loop for the AUV.
        '''

        #Check ESC Connection Status 
        data = self.radio.readline()
        while data != "ESC\n":
            data = self.radio.readline()
        
        self.esc_connected = True
        
        #Start Control Loop
	i = 1
	self.radio.write(chr(speed_callibration))
        while self.esc_connected:
            print("counter: ", i)
            #Get packet
            self.speed_f = self.navController.getPacket()
   
	    if self.debug:
                with open('data.txt', 'w') as f:
                    f.write(self.speed_f)

            print("Speed f ", self.speed_f)
            

            self.radio.write(self.speed_f)
 	    print("self.speed_f[3] is: ", self.speed_f[3])
	    if ord(self.speed_f[3]) == 1:
		print("entering ballast state")
		self.enter_ballast_state() 
		print("Finished ballasting")
		self.radio.write(chr(speed_callibration))
            
            # Await response from AUV.
            if self.radio.readline() != 'REC\n':
            
                self.connected_to_auv = False
            
                print("WARNING - AUV disconnected")
            
                self.calibrate_communication()
            
                data = self.radio.readline()
                
                while data != "ESC\n":
                    data = self.radio.readline()
            
            time.sleep(0.08)

    def enter_ballast_state(self): 
		reconnected_after_ballasting = False
		while not reconnected_after_ballasting:
			data = self.radio.readline()
			if data == "DONE\n":
				print("data recieved is done, exiting ballasting")
				reconnected_after_ballasting = True
		return
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
