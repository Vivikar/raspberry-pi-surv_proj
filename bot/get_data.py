#from picamera import PiCamera
import subprocess
import time
from os import system

#camera = PiCamera()
def snap():
    #camera.rotation = 180
    camera.capture('/home/pi/Desktop/Surveillance_Project/bot/ph.jpeg')

def vid():
    #camera.rotation = 180
    camera.start_recording('/home/pi/Desktop/Surveillance_Project/bot/vid.h264')
    time.sleep(10)
    camera.stop_recording()
    system("MP4Box -add " + "/home/pi/Desktop/Surveillance_Project/bot/vid.h264" + " " + "/home/pi/Desktop/Surveillance_Project/bot/vidmp4.mp4")
    system("rm "+ "/home/pi/Desktop/Surveillance_Project/bot/vid.h264")
