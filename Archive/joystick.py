# Code to be used on base station to send control to AUV
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.1.16:5555")

while True:
    speed = raw_input("Enter a speed: ")
    socket.send(speed)

    socket.recv()
