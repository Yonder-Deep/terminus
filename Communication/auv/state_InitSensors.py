from state import State
import sys
import os

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

from radio_manager import *
import ms5837
import BNO055

METER_TO_FEET = 3.28024

# This serial code is sent when radio needs to reconnected to base station.
ESC = 'ESC\n'
# This serial code indicates that data has been received properly.
REC = 'REC\n'
# This serial code is received when a connection is established during calibrate_communication
# and is sent after communication has been established.
CAL = 'CAL\n'


class InitSensors(State):
    def __init__(self, auv):
        print('Initializing sensors')
        auv.pressure_sensor = ms5837.MS5837_30BA()
        auv.imu_sensor = BNO055.BNO055(serial_port='/dev/serial0', rst=18)
        auv.radio = RadioManager(test_mode=False)  # TODO: Change to False for real radio
        self.calibrate_pressure_sensor(auv)
        self.calibrate_imu_sensor(auv)
        auv.radio.calibrate_communication()
        # self.calibrate_motors(auv)

    def handle(self, auv):
        raise NotImplementedError()

    def get_state_name(self):
        return 'INIT'

    def calibrate_motors(self, auv):
        """
        Calibrates all of the motors and writes ESC code if calibrated to base station.
        """
        print('Calibrating ESC...')
        auv.mc.calibrate_motors()

        # Indicate that ESCs have been calibrated.
        auv.radio.write(ESC)

        print('Finished calibrating ESC')

    def calibrate_pressure_sensor(self, auv):
        pressure_sensor_init = False
        while not pressure_sensor_init:
            try:
                pressure_sensor_init = auv.pressure_sensor.init()
            except IOError as e:
                print("Caught error ", e)
                print("Failed to initialize pressure sensor. Trying again")

        if not auv.pressure_sensor.read():
            print("Pressure sensor did not read data.")

        print("Setting fluid density to salt water")
        auv.pressure_sensor.setFluidDensity(ms5837.DENSITY_FRESHWATER)
        auv.depth = auv.pressure_sensor.depth()
        print("Current depth is ", auv.pressure_sensor.depth(), "(meters)")
        print("Current depth is ", auv.depth * METER_TO_FEET, "(feet)")

    def calibrate_imu_sensor(self, auv):
        sensor_connected = False
        while not sensor_connected:
            try:
                sensor_connected = auv.imu_sensor.begin()
            except RuntimeError as e:
                print("Caught error ", e)
                print("Failed to initialize imu sensor. Trying again")
            continue

        status, self_test, error = auv.imu_sensor.get_system_status()
        if status == 0x01:
            print('System error: {0}'.format(error))
