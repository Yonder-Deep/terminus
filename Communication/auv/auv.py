"""
The auv class orchestrates all of the sensors and motors onboard the auv and
communicates with the base station class.
"""
import sys
import os

# Sets the PYTHONPATH to include the components.
split_path = os.path.abspath(__file__).split('/')
split_path = split_path[0:len(split_path) - 2]
components_path = "/".join(split_path) + "/components"
sys.path.append(components_path)

from motor_controller import MotorController
from radio import Radio

# This serial code is sent when radio needs to reconnected to base station.
ESC = 'ESC\n'
# This serial code indicates that data has been received properly.
REC = 'REC\n'
# This serial code is received when a conenction is established during calibrate_communication
# and is sent after communication has been established.
CAL = 'CAL\n'

class AUV:
    def __init__(self):
        """
        Instantiate the AUV object
        """
        self.mc = MotorController()
        # Connection to onboard radio.
        self.radio = Radio('/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DN038PQU-if00-port0')



    def run(self):
        """
        Reads motor speeds. This function checks if the correct
        motor speed  is received and updates motor speeds continuously.
        """
        try:
            print(self.is_radio_connected_locally())
            while self.is_radio_connected_locally():
                print('Looped')
                # String received contains ASCII characters. This line decodes
                # those characters into motor speed values.
                data = [ord(x) for x in list(self.radio.readline())]

                # Check for timeout.
                if len(data) == 0:
                    self.zero_out_motors()
                    self.calibrate_communication()
                    self.radio.write(ESC)
                    continue

                # Indicate that some data has been received.
                self.radio.write(REC)

                # Check for packet loss - skip if packet is invalid.
                print(len(data))
                
                if len(data) == 5:
                    # Parse data - remove newline.
                    data = data[:-1]

                    # Update motor values.

                    self.mc.update_motor_speeds(data)

        except Exception, e:
            # Close serial conenction with local radio that is disconnected.
            self.radio.close()

            # Zero out motors.
            self.mc.zero_out_motors()

            print('Radio disconnected')
            
            exit(1)

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

        # Send signal to base station.
        self.radio.write(CAL)

        print("Done calibrating AUV.")

def main():
    # Instantiate motor controller
    auv = AUV()

    # COMM CHECK
    auv.calibrate_communication()
    auv.calibrate_motors()
    auv.run()


if __name__ == '__main__':
    main()