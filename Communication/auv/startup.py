import os
import time
import pigpio 
import serial

CENTER_PWM_RANGE = 400
CENTER_PWM_VALUE = 1500
MAX_SPEED = 100

LEFT_PIN =    4
RIGHT_PIN =  14

LEFT_MOTOR =  0
RIGHT_MOTOR = 1
BACK_MOTOR =  2
BALLAST =     3

class MotorController:
    def __init__(self, motor_pins, pi):
        """
        Instantiate the Pi Motor Controller.

        motor_pins: List of GIPO pins to instantiate motors on.
        pi:         Raspberry Pi GPIO object
        """
        # Connection to onboard radio.
        self.radio = serial.Serial('/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DN038PQU-if00-port0', baudrate = 115200)

        # Motor object definitions.
        self.motors = [Motor(gpio_pin=pin, pi=pi) for pin in motor_pins]

    def run(self):
        while self.is_radio_connected_locally():

            data = [ord(x) for x in list(self.radio.readline())]
            if len(data) != 5:
                continue
            data = data[:-1]

            print "Received data packet: " + str(data)

            self.motors[LEFT_MOTOR].set_speed(data[LEFT_MOTOR])
            self.motors[RIGHT_MOTOR].set_speed(data[RIGHT_MOTOR])

        # Close serial conenction with local radio that is disconnected.
        self.radio.close()

        # Zero out motors.
        for motor in self.motors:
            motor.set_speed(0)

        print 'Radio disconnected'
        exit(1)

    def is_radio_connected_locally(self):
        return self.radio.isOpen()

    def is_radio_connected(self):
        pass

    def calibrate_motors(self):
        print 'Calibrating ESC...'
        for motor in self.motors:
            motor.calibrate_motor()

        print 'Finished calibrating ESC' 

    def calibrate_communication(self):
        self.radio.flush()
        
        # Wait until signal received from base station.
        while self.radio.readline() != 'CAL\n': 
            pass
       
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
    controller = MotorController(motor_pins=[LEFT_PIN, RIGHT_PIN], pi=pi)
    
    # COMM CHECK
    controller.calibrate_communication()
    controller.calibrate_motors()
    controller.run()


if __name__ == '__main__':
    main()


