import os
import time
import pigpio 
import serial

CENTER_PWM_RANGE = 400
CENTER_PWM_VALUE = 1500
MAX_SPEED = 100

LEFT_GPIO_PIN =    4
RIGHT_GPIO_PIN =  14
CENTER_GPIO_PIN = 11

LEFT_MOTOR_INDEX =  0
RIGHT_MOTOR_INDEX = 1
CENTER_MOTOR_INDEX =  2
BALLAST =     3

class MotorController:
    def __init__(self, motor_pins, pi):
        """
        Instantiate the Pi Motor Controller.

        motor_pins: List of GIPO pins to instantiate motors on.
        pi:         Raspberry Pi GPIO object
        """
        # Connection to onboard radio.
        self.radio = serial.Serial('/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DN038PQU-if00-port0', 
                                    baudrate = 115200,
                                    parity = serial.PARITY_NONE,
                                    stopbits = serial.STOPBITS_ONE,
                                    bytesize = serial.EIGHTBITS, 
                                    timeout = 5
                                    )

        # Motor object definitions.
        self.motors = [Motor(gpio_pin=pin, pi=pi) for pin in motor_pins]

    def run(self):
        try:
            while self.is_radio_connected_locally():

                data = [ord(x) for x in list(self.radio.readline())]

                # Check for timeout.
                if len(data) == 0:
                    self.zero_out_motors()
                    self.calibrate_communication()
                    self.radio.write('ESC\n')
                    continue
           
                # Indicate that some data has been received.
                self.radio.write('REC\n')
            
                # Check for packet loss - skip if packet is invalid.
                if len(data) == 5:
                    # Parse data - remove newline.
                    data = data[:-1]
                    print("Received data packet: " + str(data))
            
                    # Update motor values.
                    self.motors[LEFT_MOTOR].set_speed(data[LEFT_MOTOR_INDEX])
                    self.motors[RIGHT_MOTOR].set_speed(data[RIGHT_MOTOR_INDEX])
                    self.motors[CENTER_MOTOR].set_speed(data[CENTER_MOTOR_INDEX])
        except:
            # Close serial conenction with local radio that is disconnected.
            self.radio.close()

            # Zero out motors.
            self.zero_out_motors()

            print('Radio disconnected')
            exit(1)

    def is_radio_connected_locally(self):
        return self.radio.isOpen()

    def is_radio_connected(self):
        pass

    def zero_out_motors(self):
        for motor in self.motors:
            motor.set_speed(0)

    def calibrate_motors(self):
        print('Calibrating ESC...')
        for motor in self.motors:
            motor.calibrate_motor()

        # Indicate that ESCs have been calibrated.
        self.radio.write('ESC\n')

        print('Finished calibrating ESC') 

    def calibrate_communication(self):
        self.radio.flush()

        # Wait until signal received from base station.
        print("Waiting For Data:")
        
        data = self.radio.readline()
        while data != 'CAL\n':
            data = self.radio.readline()
       
        # Send signal to base station.
        self.radio.write('CAL\n')

        print("Done calibrating AUV.")

class Motor:
    def __init__(self, gpio_pin, pi):
        """
        Instantiate a motor.

        gpio_pin: Pin on Raspberry Pi that this motor is connected to.i
        pi:         Raspberry Pi GPIO object
        """
        self.pin = gpio_pin
        self.pi  = pi

    def set_speed(self, speed):    
        # Threshold for positive or negative speed.
        if speed > MAX_SPEED:
            speed -= MAX_SPEED
            speed *= -1

        # Conversion from received radio speed to PWM value. 
        pwm_speed = speed * (CENTER_PWM_RANGE) / MAX_SPEED + CENTER_PWM_VALUE

        # Change speed of motor.
        self.pi.set_servo_pulsewidth(self.pin, pwm_speed)

    def calibrate_motor(self):
        self.set_speed(0)
        time.sleep(2)
        self.set_speed(MAX_SPEED / 2)
        time.sleep(2)
        self.set_speed(0)
        time.sleep (2)
        self.set_speed(0)
        time.sleep(2)


def main():
    # Connection to Raspberry Pi GPIO ports.
    pi = pigpio.pi()

    # Instantiate motor controller
    controller = MotorController(motor_pins=[LEFT_GPIO_PIN, RIGHT_GPIO_PIN], pi=pi)
    
    # COMM CHECK
    controller.calibrate_communication()
    controller.calibrate_motors()
    controller.run()


if __name__ == '__main__':
    main()


