import os
import time
import pigpio 
import serial

pi = pigpio.pi()

max_value = 2000 
min_value = 1000
center_range = 400
center = 1500


class PiController:
    def __init__(self, motor_pins):
        self.radio = serial.Serial('/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DN038PQU-if00-port0', baudrate = 115200)
        
        self.motors = [Motor(pin) for pin in motor_pins]
        
    def run(self):
        while self.is_radio_connected_locally():

            data = self.radio.read(6)
            print "Received speed: " + str(data) + "end"
            if data != '': 
                self.motors[0].set_speed(int(data[0:3]))
                self.motors[1].set_speed(int(data[3:6]))

            #for motor in self.motors:
            #    motor.set_speed(data)
        
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
    
    def calibrate_radio_communication(self):
        pass

class Motor:
    def __init__(self, gpio_pin):
        self.pin = gpio_pin

    def set_speed(self, speed):    
        if speed > 100:
            speed -= 100
            speed *= -1
        pi.set_servo_pulsewidth(self.pin, speed * (center_range) / 100 + center)
    
    def calibrate_motor(self):
        self.set_speed(0)
        time.sleep(2)
        self.set_speed(50)
        time.sleep(2)
        self.set_speed(0)
        time.sleep (2)
        self.set_speed(0)
        time.sleep(2)


if __name__ == '__main__':
    comm = PiController([4, 14])
    comm.calibrate_motors()
    comm.run()

    
