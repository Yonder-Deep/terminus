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

class RadioTest:
    def __init__(self):
        """
        Instantiate the RadioTest Object.
        """
        # Connection to onboard radio.
        self.radio = Radio('/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DN038PQU-if00-port0')

    def run(self):
        """
        Reads test bits from 1 - 100 and calculates packet loss rate.
        """
        try:
            count = 0
            while self.is_radio_connected_locally():
                # Indicates that all packets were sent and we should send
                # back to base station how many we recieved.
                data = self.radio.readline()
                print(data) 
                if data == 'END\n':
                    print('Iteration Ended')
                    self.radio.write(str(count) + '\n')
                
                # Indicates that our counter should be reset and lets base
                # station know that our counter was cleared.
                elif data == 'CLR\n':
                    count = 0
                    self.radio.write('CLD\n')
                
                # We recieved a packet that isn't one of the previous
                # conditions.
                elif len(data):
                    count += 1

        except Exception, e:
            # Close serial conenction with local radio that is disconnected.
            self.radio.close()

            # Zero out motors.
            #self.mc.zero_out_motors()

            print(e)
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
    rt = RadioTest()

    # Connect systems then run radio testing. 
    rt.calibrate_communication()
    rt.run()


if __name__ == '__main__':
    main()
