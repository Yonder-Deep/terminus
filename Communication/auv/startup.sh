#!/bin/bash
sudo killall pigpiod
sudo pigpiod
sudo python /home/pi/dev/terminus/Communication/auv/auv.py 
