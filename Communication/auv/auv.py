"""
The auv class orchestrates all of the sensors and motors onboard the auv and
communicates with the base station class.
"""
from __future__ import print_function
import sys
import os
import time

# Sets the PYTHONPATH to include the components.
split_path = os.path.abspath(__file__).split('/')
split_path_communication = split_path[0:len(split_path) - 2]
split_path_sensors = split_path[0:len(split_path) - 3]

components_path = "/".join(split_path_communication) + "/components"
pressure_sensor_path = "/".join(split_path_sensors) + "/Sensor"
imu_sensor_path = "/".join(split_path_sensors) + "/Sensor/Adafruit_Python_BNO055/Adafruit_BNO055"

sys.path.append(components_path)
sys.path.append(pressure_sensor_path)
sys.path.append(imu_sensor_path)

from motor_controller import MotorController
from radio import Radio
from pid import PID
import ms5837, BNO055


# This serial code is sent when radio needs to reconnected to base station.
ESC = 'ESC\n'
# This serial code indicates that data has been received properly.
REC = 'REC\n'
# This serial code is received when a conenction is established during calibrate_communication
# and is sent after communication has been established.
CAL = 'CAL\n'


# Data packet for manual mode  -   [ LEFT_SP, RIGHT_SP, FRONT_SP, BACK_SP, BALLAST, CALIBRATE ] 
MANUAL_DATA_PACKET_LENGTH = 6
IS_DEBUG_MODE   = True
BALLAST_INDEX   = 3
CALIBRATE_INDEX = 5
MISSION_DEPTH   = .65 # In meters
FEET_TO_METER   = 3.28024
LEFT_CALIBRATE  = 0
RIGHT_CALIBRATE = 1 
FRONT_CALIBRATE = 2
BACK_CALIBRATE  = 3
ALL_CALIBRATE   = 4

# New data packet for autonomous mode  -   [ TRAVEL_WP, BALLAST ]
AUTONOMOUS_DATA_PACKET_LENGTH  = 4
DEST_WP_INDEX  	    = 0
START_BALLAST_INDEX = 1


# PID Control Constants
CONTROL_TOLERANCE = 10 # tolerance before correcting heading
TARGET_TOLERANCE = 5 # torance for acknowledging reading the target
TARGET_HEADING = 0 # in degrees
P = 0.001
I = 0
D = 0


class AUV:
    def __init__(self):
        """
        Instantiate the AUV object
        """
        self.mc = MotorController()
        # Connection to onboard radio.
        try:
            # Jack Silberman's radio
            #self.radio = Radio('/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DN038PQU-if00-port0')
            # Yonder's radio
            self.radio = Radio('/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0')
        except Exception, e:
            print("Radio not found. Exception is: ", e)
            print("Exiting")
            exit(1)

	self.is_manual = True
        self.pressure_sensor = ms5837.MS5837_30BA()
        self.imu_sensor = BNO055.BNO055(serial_port='/dev/serial0', rst=18)
        self.controller = PID(self.mc, TARGET_HEADING, CONTROL_TOLERANCE, TARGET_TOLERANCE, IS_DEBUG_MODE, P, I, D)
        print("Radio is not connected.")


    def run(self):
        """
        Reads radio data. This function checks if the correct
        data packet length was passed and handles it accordingly.
        """
        try:
            print(self.is_radio_connected_locally())
            while self.is_radio_connected_locally():
                # String received contains ASCII characters. This line decodes
                # those characters into motor speed values.
                data = self.get_radio_data()
		
                # We are in manual mode!
                if   len(data) == MANUAL_DATA_PACKET_LENGTH:     # [ LEFT, RIGHT, FRONT, BACK, BALLAST, CALIBRATE ]
                   self.handle_manual_data(data)
                   self.radio.write(REC)
                elif len(data) == AUTONOMOUS_DATA_PACKET_LENGTH: # [ ABORT, HOME_WP, NAV_WP, BALLAST]
	           self.handle_autonomous_data(data)
                
                print("Data: " ,data) 

                self.print_pressure_data()
                self.print_imu_data()
     
                time.sleep(0.01)

        except Exception, e:
            # Close serial conenction with local radio that is disconnected.
            self.radio.close()

            print("Exception caught was: ", e) 
            # Zero out motors.
            self.mc.zero_out_motors()

            print('Radio disconnected')
    
    def print_pressure_data(self):
        # Reading from pressure sensor
        if self.pressure_sensor.read():
            self.depth = self.pressure_sensor.depth()
        
        print("Depth: ", self.depth, "(meters)", end = "  ")
        print("Depth: ", self.convert_to_feet(self.depth), "(feet)", end = "  ")
   
    def print_imu_data(self):
        # Reading from IMU sensor
        self.heading, self.pitch, self.roll = self.imu_sensor.read_euler()
        x_accel, y_accel, z_accel = self.imu_sensor.read_linear_acceleration()
        self.convert_heading()
                
        print("Heading: %f, Roll: %f, Pitch %f" % ( self.heading, self.roll, self.pitch ), end = "  ")
        print("X Accel: %f, Y Accel: %f, Z Accel: %f" % ( x_accel, y_accel, z_accel ), end = "  ")
  
    def get_radio_data(self):
        # String received contains ASCII characters. This line decodes
        # those characters into motor speed values.
        #print("Radio's readline: " + self.radio.readline())
        data = [ord(x) for x in list(self.radio.readline())]

        # Check for timeout.
        if len(data) == 0:
            print("len(data) == 0")
            self.mc.zero_out_motors()
            self.calibrate_communication()
            self.radio.write(ESC)

        # Indicate that some data has been received.
        self.radio.write(REC)
        
        return data;

    def handle_manual_data(self, data):
        # Parse data - remove newline.
        data = data[:-1]
                    
        if data[BALLAST_INDEX] == 1:
            print("Dude pressed ballasting button")
            self.start_ballast_sequence(data)
            data[BALLAST_INDEX] = 0
            self.radio.write(REC)

        # Begin parsing which motor(s) we want to calibrate.
        MOTOR_TO_CALIBRATE = data[CALIBRATE_INDEX]
        if MOTOR_TO_CALIBRATE == LEFT_CALIBRATE:
            self.mc.calibrate_left()
        if MOTOR_TO_CALIBRATE == RIGHT_CALIBRATE:
            self.mc.calibrate_right()
        if MOTOR_TO_CALIBRATE == FRONT_CALIBRATE:
            self.mc.calibrate_front()
        if MOTOR_TO_CALIBRATE == BACK_CALIBRATE:
            self.mc.calibrate_back()
        if MOTOR_TO_CALIBRATE == ALL_CALIBRATE:
            self.mc.calibrate_motors()
        
        # Update motor values.
        self.mc.update_motor_speeds(data)

    def handle_autonomous_data(self, data):
        data = data[:-1]
          
	if data[START_BALLAST_INDEX]:
	    self.start_ballast_sequence(1) # Number 1 for the data object in start_balance_sequence 
	else:
	    coordinates = data[NAV_WP_INDEX].split(",")
	    coordinates[0] = float(coordinates[0])
            coordinates[1] = float(coordinates[1])
            self.nav_to_waypoint(coordinates[0], coordinates[1], radio)
 
    def nav_to_waypoint(self, data, x, y, radio):
        self.original_data = data # If our new data != original_data, we have new
                                  # instructions coming in to the AUV. So, logically,
                                  # interupt the current task and parse new data.

        # Get the angle from North from our position and the long/lat position (North being up or 0)
        angle_from_north = self.get_angle_from_north(x, y)
        self.rotate_to_heading(angle_from_north)
        
        try:
            # We NEED to check if we want to ABORT/Change Waypoint WHILE 
            # we are travelling to a waypoint!
            while self.is_radio_connected_locally():
                current_data = self.get_radio_data()
               
                # New data? 
                if   len(current_data) == MANUAL_DATA_PACKET_LENGTH:
                   self.handle_manual_data(current_data)
                   return
                elif len(current_data) == AUTONOMOUS_DATA_PACKET_LENGTH: # [ NAV_WP, BALLAST]
	           if str(original_data) != str(current_data): # IF we recieved a different instruction set...
                       self.handle_autonomous_data(current_data)
                       return
            
                # No new data was given to the AUV, so, continue moving
                # to our original waypoint.    
                self.forward_loop(x, y)
		
        except Exception, e:
            # Close serial conenction with local radio that is disconnected.
            self.radio.close()

            print("Exception caught was: ", e) 
            # Zero out motors.
            self.mc.zero_out_motors()

            print('Radio disconnected')

    def rotate_to_heading(self, heading): # Heading is the angle from North on a compass.
        pass
        
    def get_angle_from_north(self, x, y): # X, Y is the long/lat we are travelling to; we know where we are; now get angle from 0
	pass

    def forward_loop(self, x, y): # Move forward until we are close-enough to x, y
        # Set motor to full-forward
        
        # Move until we are there...???
        pass

    def convert_heading(self):
        if self.heading > 180:
            self.heading = self.heading - 360

    def start_ballast_sequence(self, data):
        print("Starting ballast sequence")
        self.mc.zero_out_motors()
        self.mc.update_motor_speeds(data)
        target_depth = self.convert_to_feet(MISSION_DEPTH)
        depth_in_feet = self.convert_to_feet(self.depth)

        while( depth_in_feet <= target_depth ):
            print("Our target depth is: ", target_depth)
            if self.pressure_sensor.read():
                self.depth = self.pressure_sensor.depth()

            depth_in_feet = self.convert_to_feet(self.depth)
            print("our current depth is: ", depth_in_feet)
            time.sleep(0.01)
        print("Reached target depth of: ", target_depth, "(feet)")
 
        # Run PID to correct heading after reaching target_depth
        print("correcting heading")
        pid_feedback = self.controller.pid(self.heading)
        while(pid_feedback):
            # Adjust motor speed base off the feedback
            self.mc.pid_motor(pid_feedback)
            self.heading, self.pitch, self.roll = self.imu_sensor.read_euler()
            self.convert_heading()
            pid_feedback = self.controller.pid(self.heading)

        self.radio.write("DONE\n")
        return
        #self.begin_recording()

    def begin_recording(self):
        pass

    def convert_to_feet(self,meters):
        return meters*FEET_TO_METER

    def is_radio_connected_locally(self):
        """
        Returns a boolean to check if the auv's radio is connected to the auv.
        """
        return self.radio.isOpen()

    def is_radio_connected(self):
        """
        Returns a boolean whether the auv is connected to the base station.
        """
        pass

    def calibrate_motors(self):
        """
        Calibrates all of the motors and writes ESC code if calibrated to base station.
        """
        print('Calibrating ESC...')
        self.mc.calibrate_motors();

        # Indicate that ESCs have been calibrated.
        self.radio.write(ESC)

        print('Finished calibrating ESC')

    def calibrate_communication(self):
        """
        Continously reads strings until CAL code has been received from base station.
        Once received successfully , CAL code is written back to the base station.
        """
        self.radio.flush()

        # Wait until signal received from base station.
        print("Waiting For Data:")

        data = self.radio.readline()
        while data != CAL:
            data = self.radio.readline()

        print('sending_cal')

        # Send signal to base station.
        self.radio.write(CAL)

        print("Done calibrating AUV.")

    def calibrate_pressure_sensor(self):
    
        pressure_sensor_init = False
        while not pressure_sensor_init:
            try: 
                pressure_sensor_init = self.pressure_sensor.init()
            except IOError as e:
                print("Caught error ", e)
                print("Failed to initialize pressure sensor. Trying again")

        if not self.pressure_sensor.read():
            print("Pressure sensor did not read data.")

        print("Setting fluid density to salt water")
        self.pressure_sensor.setFluidDensity(ms5837.DENSITY_FRESHWATER)
        self.depth = self.pressure_sensor.depth()
        print("Current depth is ", self.pressure_sensor.depth(), "(meters)")
        print("Current depth is ", self.convert_to_feet(self.depth), "(feet)")
    
    def calibrate_imu_sensor(self):
        sensor_connected = False
        while not sensor_connected:
            try:
                sensor_connected = self.imu_sensor.begin()
            except RuntimeError as e:
                print("Caught error ", e)
                print("Failed to initialize imu sensor. Trying again")
            continue
        
        status, self_test, error = self.imu_sensor.get_system_status()
        if status == 0x01:
            print('System error: {0}'.format(error))

def main():
    # Instantiate motor controller
    auv = AUV()

    # Pressure sensor check
    auv.calibrate_pressure_sensor()
    
    # IMU sensor check
    auv.calibrate_imu_sensor()

    # COMM CHECK
    auv.calibrate_communication()
    # auv.calibrate_motors()

    auv.run()


if __name__ == '__main__':
    main()
