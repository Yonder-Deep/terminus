"""
The radio class enables communication over wireless serial radios.
"""
import serial

class Radio:
    def __init__(self, serial_path, baudrate = 115200):
        """
        Initializes the radio object.

        serial_path: Absolute path to serial port for specified device.
        """

        # Establish connection to the serial radio.
        self.ser = serial.Serial(serial_path,
                                baudrate = baudrate, parity = serial.PARITY_NONE,
                                stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS,
                                timeout = 2
                                )
    def write(self,message):
        """
        Sends provided message over serial connection.

        message: A string message that is sent over seral connection.
        """
        try:
             self.ser.write(message)
             return 1
        except Exception as e:
             return -1

    def readline(self):
        """
        Returns a string from the serial connection.
        """
        try:
             return self.ser.readline()
        except Exception as e:
             return -1

    def isOpen(self):
        """
        Returns a boolean if the serial connection is open.
        """
        return self.ser.isOpen()

    def flush(self):
        """
        Clears the buffer of the serial connection.
        """
        self.ser.flush()

    def close(self):
        """
        Closes the serial connection
        """
        self.ser.close()
