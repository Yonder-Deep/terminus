from state import State
import ms5837

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
        self.calibrate_pressure_sensor(auv)
        self.calibrate_imu_sensor(auv)
        self.calibrate_communication(auv)
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

    def calibrate_communication(self, auv):
        """
        Continuously reads strings until CAL code has been received from base station.
        Once received successfully , CAL code is written back to the base station.
        """
        auv.radio.flush()

        # Wait until signal received from base station.
        print("Waiting For Data:")

        data = auv.radio.readline()
        while data != CAL:
            data = auv.radio.readline()

        print('sending_cal')

        # Send signal to base station.
        auv.radio.write(CAL)

        print("Done calibrating AUV.")

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
        print("Current depth is ", auv.convert_to_feet(auv.depth), "(feet)")

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