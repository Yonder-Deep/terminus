import sys
import os
split_path = os.path.abspath(__file__).split('/')
split_path_sensors = split_path[0:len(split_path) - 3]
pressure_sensor_path = "/".join(split_path_sensors) + "/Sensor"
imu_sensor_path = "/".join(split_path_sensors) + "/Sensor/Adafruit_Python_BNO055/Adafruit_BNO055"
sys.path.append(pressure_sensor_path)
sys.path.append(imu_sensor_path)

FEET_TO_METER = 3.28024

from pid import PID
import ms5837, BNO055

class Sensors():
    def __init__(self):
        self.pressure_sensor = ms5837.MS5837_30BA()
        self.imu_sensor = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

    @classmethod
    def calibrate_pressure_sensor(pressure_sensor):

        pressure_sensor_init = False
        while not pressure_sensor_init:
            try:
                pressure_sensor_init = pressure_sensor.init()
            except IOError as e:
                print("Caught error ", e)
                print("Failed to initialize pressure sensor. Trying again")

        if not pressure_sensor.read():
            print("Pressure sensor did not read data.")

        print("Setting fluid density to salt water")
        pressure_sensor.setFluidDensity(ms5837.DENSITY_FRESHWATER)
        depth = pressure_sensor.depth()
        print("Current depth is ", pressure_sensor.depth(), "(meters)")
        print("Current depth is ", depth * FEET_TO_METER, "(feet)")