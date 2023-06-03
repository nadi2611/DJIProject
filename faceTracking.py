import math
import time

from djitellopy import Tello
from time import sleep
import numpy as np
import cv2

#### parameters ####


yawPid = [0.4, 0.4, 0]
pitchPid = [-0.005, -0.005, 0]

yawSpeedPerror = 0
pitchSpeedPerror = 0

w,h = 360, 240
optimalArea = 6500
cap = cv2.VideoCapture(0)
counter = 0

def findFace(img):
    faceCascade = cv2.CascadeClassifier("faces/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    myFaceListCenter = []
    myFaceListArea = []

    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x + w, y + h), (0,0,255), 2)

        centerX = x + w // 2
        centerY = y + h // 2
        area = w * h

        cv2.circle(img, (centerX, centerY), 5, (0, 255, 0), cv2.FILLED)

        myFaceListArea.append(area)
        myFaceListCenter.append([centerX, centerY])

    if len(myFaceListArea) != 0:
        indexMaxArea = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListCenter[indexMaxArea], myFaceListArea[indexMaxArea]]

    else:
        return img, [[-1,-1], -1]

def trackFace(tello, info, width, pid, yawSpeedPerror, pitchSpeedPerror):

    global forwardBackwardAreaRange, counter

    area = info[1]
    x, y = info[0]
    forwardBackwardSpeed = 0


    yawSpeedError = x - width // 2
    pitchSpeedError = area - optimalArea # if 2000 > 6500 -> Error = +4500

    speed = pid[0] * yawSpeedError + pid[1] * (yawSpeedError - yawSpeedPerror)
    speed = int(np.clip(speed, -100, 100))

    pitchSpeed = pitchPid[0] * pitchSpeedError + pitchPid[1] * (pitchSpeedError - pitchSpeedPerror)
    pitchSpeed = int(np.clip(pitchSpeed, -100, 100))


    print(area)
    if x == -1:
        counter += 1
        speed = 0
        yawSpeedError = 0

        pitchSpeed = 0
        pitchSpeedError = 0


    tello.send_rc_control(0, pitchSpeed, 0, speed)
    return yawSpeedError, pitchSpeedError


tello = Tello()
tello.connect()
tello.streamon()
tello.takeoff()
tello.send_rc_control(0, 0, 25, 0)
time.sleep(2.5)


while True:
    #_, img = cap.read()
    img = tello.get_frame_read().frame
    img = cv2.resize(img, (w,h))
    img, info = findFace(img)
    yawSpeedPerror, pitchSpeedPerror = trackFace(tello, info, w, yawPid, yawSpeedPerror, pitchSpeedPerror)
    print("Center", info[0])
    cv2.imshow("Output", img)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        tello.land()
        break
