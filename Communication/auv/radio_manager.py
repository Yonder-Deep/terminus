import sys
import os

# Sets the PYTHONPATH to include the components.
split_path = os.path.abspath(__file__).split('/')
split_path_communication = split_path[0:len(split_path) - 2]
components_path = "/".join(split_path_communication) + "/components"
from radio import Radio

# This serial code is sent when radio needs to reconnected to base station.
ESC = 'ESC\n'
# This serial code indicates that data has been received properly.
REC = 'REC\n'
# This serial code is received when a connection is established during calibrate_communication
# and is sent after communication has been established.
CAL = 'CAL\n'


class RadioManager():
    def __init__(self, test_mode=False):
        """ Set test_mode to True to skip connection to radio for testing """
        if test_mode:
            self.radio = FakeRadio()
        else:
            self.radio = Radio(
                '/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0')

    def calibrate_communication(self):
        """
        Continuously reads strings until CAL code has been received from base station.
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


class FakeRadio(Radio):
    def __init__(self):
        self.is_open = True;

    def write(self, message):
        print(">>" + message)

    def readline(self):
        print("<<" + "FakeMessage")

    def isOpen(self):
        return self.is_open

    def flush(self):
        pass

    def close(self):
        self.is_open = False
