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

IS_DEBUG_MODE = True
BALLAST_INDEX = 3
MISSION_DEPTH = .65 # In meters
FEET_TO_METER = 3.28024

# PID Control Constants
CONTROL_TOLERANCE = 10 # tolerance before correcting heading
TARGET_TOLERANCE = 5 # torance for acknowledging reading the target
TARGET_HEADING = 50 # in degrees
P = 0.02
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

        self.pressure_sensor = ms5837.MS5837_30BA()
        self.imu_sensor = BNO055.BNO055(serial_port='/dev/serial0', rst=18)
        self.controller = PID(self.mc, TARGET_HEADING, CONTROL_TOLERANCE, TARGET_TOLERANCE, IS_DEBUG_MODE, P, I, D)
        print("Radio is not connected.")


    def run(self):
        """
        Reads motor speeds. This function checks if the correct
        motor speed  is received and updates motor speeds continuously.
        """
        try:

                # Reading from IMU sensor
            self.heading, self.pitch, self.roll = self.imu_sensor.read_euler()
            x_accel, y_accel, z_accel = self.imu_sensor.read_linear_acceleration()
            self.convert_heading()
                
            print("Data: " ,data, end = "  ")
            print("Depth: ", self.depth, "(meters)", end = "  ")
            print("Depth: ", self.convert_to_feet(self.depth), "(feet)", end = "  ")
            print("Heading: %f, Roll: %f, Pitch %f" % ( self.heading, self.roll, self.pitch ), end = "  ")
            print("X Accel: %f, Y Accel: %f, Z Accel: %f" % ( x_accel, y_accel, z_accel ), end = "  ")
            time.sleep(0.01)
            # Adjust motor speed base off the feedback
            while(True):
                self.mc.pid_motor(pid_feedback)
                self.heading, self.pitch, self.roll = self.imu_sensor.read_euler()
                self.convert_heading()
                pid_feedback = self.controller.pid(self.heading)
        except Exception, e:
            self.mc.zero_out_motors()

    
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



    auv.run()


if __name__ == '__main__':
    main()
