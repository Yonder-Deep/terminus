import zmq 
import sys
import serial
import time




context = zmq.Context()

sock = context.socket(zmq.REQ)
sock.connect("tcp://192.168.2.1:5556")
arduino = serial.Serial('/dev/ttyACM0', baudrate=9600)
while True:

    #sock.connect("tcp://127.0.0.1:5556")

    #with serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=0.02) as ser:
    msg = arduino.readline()
    
        
    sock.send(msg)
    
    sock.recv()
     
