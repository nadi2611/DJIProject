import keyPressModule as kp
from djitellopy import Tello
from time import sleep


def getKeyboardInput():
    lr, fb, up, yaw = 0, 0, 0, 0
    land = False
    takeoff = False
    speed = 50

    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("w"): up = speed
    elif kp.getKey("s"): up = -speed

    if kp.getKey("a"): yaw = speed
    elif kp.getKey("d"): yaw = -speed

    if kp.getKey("q"): land = True
    elif kp.getKey("e"): takeoff = True

    return [lr, fb, up, yaw, land, takeoff]


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
