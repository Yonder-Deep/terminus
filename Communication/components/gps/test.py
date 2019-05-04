import time
import serial
import string
from pynmea import nmea
import axis_convert

ser = serial.Serial()
ser.port = "/dev/ttyUSB0"
ser.baudrate = 4800
ser.timeout = 1
ser.open()
gpgga = nmea.GPGGA()


def get_gps():
	while True:
	    data = ser.readline()
	    if data[0:6] == '$GPGGA':
		##method for parsing the sentence
		gpgga.parse(data)
                lats = gpgga.latitude
		lat_ = (float(lats[2]+lats[3]+lats[4]+lats[5]+lats[6]+lats[7]+lats[8]))/60
		real_lat = (float(lats[0]+lats[1])+lat_)
                print "Latitude values : " + str(real_lat)
		longs = gpgga.longitude
                
                _long = (float(longs[3]+longs[4]+longs[5]+longs[6]+longs[7]+longs[8]+longs[9]))/60
                real_long = (float(longs[0]+longs[1]+longs[2])+_long) 

                return (float(real_lat), float(real_long))
                break



orig = get_gps()
print(orig)
print(type(orig[0]))
g = axis_convert.GeoTool(*orig)
while True:
    new = get_gps()
    print(g.get_location(*new))
