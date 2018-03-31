import time
import zmq
import serial

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://169.254.199.158:5556")
arduino = serial.Serial('/dev/ttyACM0', baudrate=9600)

while True:
    speed = socket.recv()
    print speed
    arduino.write(speed)
    #time.sleep(0.01)
    socket.send('')
    
