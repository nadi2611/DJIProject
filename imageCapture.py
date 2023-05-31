from djitellopy import Tello
from time import sleep
import cv2

tello = Tello()
tello.streamon()

while True:
    img = tello.get_frame_read().frame
    img = cv2.resize(img, (512, 512))
    cv2.imshow("Image",img)
    cv2.waitKey(1)