import math
import time

from djitellopy import Tello
from time import sleep
import numpy as np
import cv2

#### parameters ####



w,h = 360, 240
cap = cv2.VideoCapture(0)

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
        print(centerX, centerY)
        return img, [myFaceListCenter[indexMaxArea], myFaceListArea[indexMaxArea]]

    else:
        return img, [[-1,-1], -1]

def trackFace(tello, info, width, height, pid, yawSpeedPerror, pitchSpeedPerror, upDownSpeedPerror):

    global forwardBackwardAreaRange, counter

    area = info[1]
    x, y = info[0]
    forwardBackwardSpeed = 0


    yawSpeedError = x - width // 2
    upDownSpeedError = y - height // 2
    pitchSpeedError = area - optimalArea # if 2000 > 6500 -> Error = +4500

    speed = pid[0] * yawSpeedError + pid[1] * (yawSpeedError - yawSpeedPerror)
    speed = int(np.clip(speed, -100, 100))

    upDownSpeed = upDownPid[0] * upDownSpeedError + upDownPid[1] * (upDownSpeedError - upDownSpeedPerror)
    upDownSpeed = int(np.clip(upDownSpeed, -100, 100))

    pitchSpeed = pitchPid[0] * pitchSpeedError + pitchPid[1] * (pitchSpeedError - pitchSpeedPerror)
    pitchSpeed = int(np.clip(pitchSpeed, -100, 100))


    if x == -1 or y == -1:
        counter += 1
        speed = 0
        yawSpeedError = 0

        upDownSpeed = 0
        upDownSpeedError = 0

        pitchSpeed = 0
        pitchSpeedError = 0


    tello.send_rc_control(0, pitchSpeed, upDownSpeed, speed)
    return yawSpeedError, pitchSpeedError, upDownSpeedError




while True:
    _, img = cap.read()
    img = cv2.resize(img, (w,h))
    img, info = findFace(img)
    cv2.imshow("Output", img)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break
