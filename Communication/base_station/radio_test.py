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
from radio import Radio

speed = 0
delay = 0.1
maxSpeed = 50
minSpeed = 0
turnSpeed = 50
motorIncrements = 8
maxSpeed = 100

class BaseStation:
    def __init__(self, args, debug=False):

        '''
        Initialize Serial Port and Class Variables
        args: Command line arguments.
        debug: debugging flag
        '''
        self.radio = Radio('/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DN0393EE-if00-port0')
        self.connected_to_auv = False
        self.navController = None
        self.debug = debug
        
        # Number of data points to send per test iteration.
        self.buffsize = 100

        # Delay amount
        self.delay = 0.005
        
        # Define file to write to if it exists.
        self.file = None
        if args.out:
            self.file = open(args.out, "w")

    def calibrate_communication(self):
        '''
        Ensure communication between AUV and Base Station
        ''' 
        
        # Flush the serial connection.
        self.radio.flush()

        print("Press the start button to establish connection to AUV...")

        # Wait until connection is established.
        while not self.connected_to_auv:
            print("Attempting to connect to AUV...")
                
            #Send Calibration Signal To AUV
            self.radio.write('CAL\n')

            # Await response from AUV. Times out after 1 second.
            self.connected_to_auv = (self.radio.readline() == 'CAL\n')
            if not self.connected_to_auv:
                print("Connection timed out, please try again...\n")

        print("Connection established with AUV.")


 
    def run(self):
        ''' 
        Runs the controller loop for the AUV.
        '''

       	self.start_time = time.time() 
        #Start Control Loop
        while True:

            # Send the sequence of bits to the AUV.
            for i in range(ord('a'), ord('a') + self.buffsize):
                packet = chr(i) + '\n'
                self.radio.write(packet)
 
                time.sleep(self.delay)

            # Waiting for num packets received by AUV.
            count = self.radio.readline()
            while len(count) == 0:
                self.radio.write('END\n')
                count = self.radio.readline()
                time.sleep(self.delay)
            
            # Calculate the packet loss for the last sequence of bits sent.
            ratio = float(count) / self.buffsize
            time_elapsed = time.time() - self.start_time
            
            # Log to the outfile.
            if self.file:
                self.file.write("{} {}\n".format(time_elapsed, ratio))
            
            if self.debug:
                print("Time elapsed: {} Packet Health: {}\n".format(time_elapsed, ratio))

            # Indicate to the AUV to clear its counter.
            while self.radio.readline() != 'CLD\n':
                self.radio.write('CLR\n')
                time.sleep(self.delay)
            

# TODO: Comment run, find out when auv disconnects.
def main(): 

    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--out', required=False, help='File to output logged results to.')

    args = parser.parse_args()
    bs = BaseStation(args, debug=args.debug)
    
    bs.calibrate_communication()
    
    bs.run()


if __name__ == '__main__':
    main()
