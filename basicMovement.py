from djitellopy import Tello
from time import sleep

tello = Tello()
tello.connect()
tello.takeoff()
tello.send_rc_control(0, 100, 0, 0)
sleep(4)
tello.send_rc_control(0, 0, 0, 0)
tello.land()
