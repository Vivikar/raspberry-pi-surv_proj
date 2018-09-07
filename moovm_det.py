from imutils.object_detection import non_max_suppression
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import warnings
import imutils
import json
import cv2
import subprocess
from os import system
from telebot import types

import MySQLdb
import datetime
import time
import os


#connecting to database
db = MySQLdb.connect(host="localhost", user="newuser", passwd="pi", db="surv_pics")
#initializing cursor
cur = db.cursor()
#paths to floders containing det_frames and images saves from db
path = '/var/lib/mysql/det_frames/'
backup_path = '/home/pi/Desktop/SQL_SAVED_IMAGES/'
#link to current bot conversation
mymessage = None
#checks in need exit surv()
flag = False

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, help="path to the JSON configuration file")
args = vars(ap.parse_args())

# filter warnings, load the configuration
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = tuple(conf["resolution"])
camera.rotation = conf["rotation"]
camera.framerate = conf["fps"]
rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))

def snap():
    camera.capture('/home/surv_proj/bot/ph.jpeg')

def vid(duration):
    if os.path.isfile('/home/surv_proj/bot/vid.h264'):
        os.remove('/home/surv_proj/bot/vid.h264')
    camera.start_recording('/home/surv_proj/bot/vid.h264')
    time.sleep(duration)
    camera.stop_recording()
    if os.path.isfile('/home/surv_proj/bot/vidmp4.mp4'):
        os.remove('/home/surv_proj/bot/vidmp4.mp4')
    system("MP4Box -add " + "/home/surv_proj/bot/vid.h264" + " " + "/home/surv_proj/bot/vidmp4.mp4")
    time.sleep(1)

def send_body(bot,message, counter, timestamp):
    capt = timestamp + "| detected " + str(counter) +" body moovment."
    
    keyb = types.InlineKeyboardMarkup()
    call_bb = types.InlineKeyboardButton(text="Get full photo", callback_data=timestamp)
    keyb.add(call_bb)
    bot.send_photo(message.chat.id, open(path + 'frame' + str(counter) + '.jpg','rb'), caption=capt, reply_markup=keyb)


def should_exit():
    if flag:
        raise SystemExit(0)


def trunc_table():

    cur.execute("TRUNCATE TABLE surv_pics.images")
    print("Table truncated")

def save_ims():
    #creating folder to save images
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S/')
    folder_path = backup_path + timestamp
    os.mkdir(folder_path)
    #saving photos
    cur.execute("SELECT * FROM surv_pics.images")
    im_count = 1
    myresults = cur.fetchall()
    for data in myresults:
        name = data[1].fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S_')
        outfile=open(folder_path + name + str(im_count) +".jpeg", 'wb')
        outfile.write(data[2]) # third column contains image
        outfile.close()
        print("Wrote")
    
    #clean table
    trunc_table()
    return folder_path


def send_uncropped(call, bot, tms):
    cur.execute("SELECT * FROM surv_pics.images WHERE timestamp = '" + tms +"'")
    myresults = cur.fetchall()
    for data in myresults:
        outfile=open('/home/surv_proj/temp/uncrsaved.jpeg','wb')
        outfile.write(data[2]) # num (2) depends on image column
        outfile.close()
    bot.send_photo(mymessage.chat.id, open('/home/surv_proj/temp/uncrsaved.jpeg', 'rb'))
    os.remove('/home/surv_proj/temp/uncrsaved.jpeg')



def surv(bot,message):

    # allow the camera to warmup, then initialize the average frame, last
    # uploaded timestamp, and frame motion counter
    print("[INFO] Starting surveillance. Warming up...")
    time.sleep(conf["camera_warmup_time"])
    avg = None      
    lastUploaded = datetime.datetime.now()
    motionCounter = 0
    count = 1

    # capture frames from the camera
    for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image and initialize
            # the timestamp and occupied/unoccupied flag
            frame = f.array
            timestamp = datetime.datetime.now()
            occupied = False

            # resize the frame, convert it to grayscale, and blur it
            orig_frame = frame.copy()
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            
            # if the average frame is None, initialize it
            if avg is None:
                    print("[INFO] Starting background model...")
                    avg = gray.copy().astype("float")
                    rawCapture.truncate(0)
                    continue

            # accumulate the weighted average between the current frame and
            # previous frames, then compute the difference between the current
            # frame and running average
            cv2.accumulateWeighted(gray, avg, 0.5)
            frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

            # threshold the delta image, dilate the thresholded image to fill
            # in holes, then find contours on thresholded image
            thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
                    cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if imutils.is_cv2() else cnts[1]

            # loop over the contours
            for c in cnts:
                    # if the contour is too small, ignore it
                    if cv2.contourArea(c) < conf["min_area"]:
                            continue
                    occupied = True

            if occupied:
                    # check to see if enough time has passed between uploads
                    if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
                            # increment the motion counter
                            motionCounter += 1

                            # check to see if the number of frames with consistent motion is
                            # high enough
                            if motionCounter >= conf["min_motion_frames"]:
                                # detect body
                                (rects, weights) = hog.detectMultiScale(frame, winStride=(2, 2),padding=(6, 6), scale=1.05)
                                rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
                                pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

                                # save & send image
                                for (xA, yA, xB, yB) in pick:                            
                                    cv2.imwrite(os.path.join(path, 'frame%d.jpg' % count), frame[yA:yB,xA:xB])
                                    cv2.imwrite(os.path.join(path, 'origframe%d.jpg' % count), orig_frame)

                                    ts = time.time()
                                    sqltimestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                                    send_body(bot,message,count, sqltimestamp)
                                    
                                    #inserting to sql database
                                    cur.execute("INSERT INTO surv_pics.images(timestamp, image) VALUES('" + sqltimestamp +
                                                "', LOAD_FILE('/var/lib/mysql/det_frames/origframe" + str(count) + ".jpg'))")
                                    
                                    print("Image {0} saved and added to database".format(str(count)))
                                    count += 1
                                lastUploaded = timestamp

            # otherwise, the room is not occupied
            else:
                    motionCounter = 0

            # check to see if the frames should be displayed to screen
            if conf["show_video"]:
                    # display the security feed
                    cv2.imshow("Security Feed", frame)
                    key = cv2.waitKey(1) & 0xFF
                    
             # clear the stream in preparation for the next frame and exit if should
            rawCapture.truncate(0)
            if flag:
                break
    #stopping surveillance
    bot.send_message(message.chat.id, "Done")

    print("[INFO] Stopping background model... Exiting")


