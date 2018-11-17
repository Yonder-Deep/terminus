import os
import time
import pigpio
import serial

serial_port = serial.Serial('/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DN038PQU-if00-port0',
                            baudrate = 115200,
                            parity = serial.PARITY_NONE,
                            stopbits = serial.STOPBITS_ONE,
                            bytesize = serial.EIGHTBITS,
                            timeout = 5
                            )

class auv_radio:
        
    def __init__(self, serial_port):
        
        self.radio = serial_port
        self.connected_to_base_station = False

        
    def calibrate_communication(self):
        
        self.radio.flush()

        print("Calibrating communication...")
        print("Waiting for data 'CAL\n'")
        
        data = self.radio.readline()

        print("Received data ", data)
        
        while data != 'CAL\n':
            print("Data != 'CAL\n'...Trying again")
            data = self.radio.readline()
        
        print("Recieved 'CAL\n' ... Sending data back")
        self.radio.write('CAL\n')

        self.connected_to_base_station = True
        print("Done calibrating communication")

    def receive_data(self):
        print("Beginning to receive data")
        while self.connected_to_base_station:
            data = [ord(x) for x in list(self.radio.readline())]
            print(len(data), data)
            if len(data) == 0:
                print("Length of data recieved was 0 - corrupted.")
                continue

            print("Recieved data correctly, sending back reponse to base")
            self.radio.write('REC\n')


auv_radio = auv_radio(serial_port)
auv_radio.calibrate_communication()
auv_radio.receive_data()
