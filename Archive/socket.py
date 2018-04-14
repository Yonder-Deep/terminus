import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://192.168.2.1:5556")

while True:
    message = socket.recv()

    print message
    #time.sleep(0.01)

    socket.send('')
    
