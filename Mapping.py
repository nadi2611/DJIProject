import math

import keyPressModule as kp
from djitellopy import Tello
from time import sleep
import numpy as np
import cv2
##### parameters #####

forwardSpeed = 400 / 10 # centimeter per second
angularSpeed = 360 / 10 # centimeter per second
interval = 0.25

distanceInterval = forwardSpeed * interval
angularInterval = angularSpeed * interval

x,y = 500, 500
angle = 0
yawAngle = 0
points = []
######################

def drawPoints(img, points):
    for point in points:
        cv2.circle(img,(point[0],point[1]), 5, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, points[-1], 10, (0, 255, 0), cv2.FILLED)


def getKeyboardInput():
    lr, fb, up, yaw = 0, 0, 0, 0
    land = False
    takeoff = False
    speed = 50
    distance = 0
    global yawAngle, x, y, angle

    if kp.getKey("LEFT"):
        lr = -speed
        distance = distanceInterval
        angle = -180
    elif kp.getKey("RIGHT"):
        lr = speed
        distance = -distanceInterval
        angle = 180

    if kp.getKey("UP"):
        fb = speed
        distance = distanceInterval
        angle = 270
    elif kp.getKey("DOWN"):
        fb = -speed
        distance = -distanceInterval
        angle = -90

    if kp.getKey("w"): up = speed
    elif kp.getKey("s"): up = -speed

    if kp.getKey("a"):
        yaw = speed
        yawAngle += angularInterval
    elif kp.getKey("d"):
        yaw = -speed
        yawAngle -= angularInterval

    if kp.getKey("q"): land = True
    elif kp.getKey("e"): takeoff = True

    sleep(interval)

    angle += yawAngle
    x += int(distance*math.cos(math.radians(angle)))
    y += int(distance*math.sin(math.radians(angle)))

    return [lr, fb, up, yaw, land, takeoff, x, y]


kp.init()
tello = Tello()
tello.connect()
print(tello.get_battery())



while True:
    vals = getKeyboardInput()
    if vals[4] == True:
        tello.land()
    elif vals[5] == True:
        tello.takeoff()
    else:
        tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)

    image = np.zeros((1000,1000,3), np.uint8)
    points.append((vals[6], vals[7]))
    drawPoints(image, points)
    cv2.imshow("Output Map", image)
    sleep(0.05)



