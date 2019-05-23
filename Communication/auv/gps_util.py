# from __future__ import print_function
import serial
import pynmea2
import time


class ReadGPS():
    def __init__(self, auv):
        assert auv.gps_infoauv
        self.gps = serial.Serial(port='/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0',
                                 baudrate=9600)
        self.handle(auv)

    def handle(self, auv):
        try:
            if self.gps.inWaiting():
                line = self.gps.readline()
                assert isinstance(line, str)
                parsed = pynmea2.parse(line)

                lat = float(parsed.latitude)
                lon = float(parsed.longitude)
                auv.gps_info['lat'] = lat
                auv.gps_info['lon'] = lon
                auv.gps_info['updated'] = time.time()
        except:
            pass