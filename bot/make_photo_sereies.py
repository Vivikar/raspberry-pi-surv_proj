import cv2

import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

import json
import time

path = '/home/pi/Desktop/Surveillance_Project/detect_frames'
camera = PiCamera()
camera.resolution = tuple((1270, 720))
count = 1
#camera.rotation = 180
time.sleep(10)
for i in range(10):
    camera.capture('/home/pi/Desktop/Surveillance_Project/Send_SSH/' + str(count) + '.jpeg')
    time.sleep(2)
    count += 1
