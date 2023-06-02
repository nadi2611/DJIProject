import math
import time

from djitellopy import Tello
from time import sleep
import numpy as np
import cv2

#### parameters ####

forwardBackwardAreaRange = [3000, 4000]
pid = [0.4, 0.4, 0]
yawSpeedPerror = 0
w,h = 360, 240
optimalArea = 5000
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

def trackFace(tello, info, width, pid, yawSpeedPerror, optimalArea):

    global forwardBackwardAreaRange, counter

    area = info[1]
    x, y = info[0]
    forwardBackwardSpeed = 0

    yawSpeedError = x - width // 2

    speed = pid[0] * yawSpeedError + pid[1] * (yawSpeedError - yawSpeedPerror)
    speed = int(np.clip(speed, -100, 100))


    print(area)
    if area > forwardBackwardAreaRange[0] and area < forwardBackwardAreaRange[1]:
        forwardBackwardSpeed = 0
    elif area > forwardBackwardAreaRange[1]:
        forwardBackwardSpeed = - 20
    elif area < forwardBackwardAreaRange[0] and area != -1:
        forwardBackwardRange = 20
    if x == -1:
        counter += 1
        speed = 0
        yawSpeedError = 0
    if counter == 20:
        print(counter)
        counter = 0

    tello.send_rc_control(0, forwardBackwardSpeed, 0, speed)
    return yawSpeedError


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
    yawSpeedPerror = trackFace(tello, info, w, pid, yawSpeedPerror, optimalArea)
    print("Center", info[0])
    cv2.imshow("Output", img)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        tello.land()
        break
