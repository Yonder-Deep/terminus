from __future__ import print_function
import serial
import pynmea2

if __name__ == '__main__':
    with serial.Serial(port='/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0', baudrate=9600) as ser:
        while True:
            line = ser.readline()
            print(line)
            parsed = pynmea2.parse(line)
            print(type(parsed), end='\t')
            try:
                print(parsed.lattude, parsed.longitude)
            except:
                print("meh")
