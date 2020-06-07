import numpy as np
import cv2
import pyautogui
import time

screen_id = 0

width, height = pyautogui.size()
image = cv2.imread('/home/pi/projects/opencv-CFR-advertisement-system-rpi/sst/cocacola.jpg')

#cv2.imshow('image',image)
#cv2.waitKey(1000)
#cv2.destroyAllWindows()

window_name = 'projector'
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.moveWindow(window_name, width, height)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
cv2.imshow(window_name, image)
cv2.waitKey(1000)
while True:
    print("ii")
    time.sleep(5)
cv2.destroyAllWindows()

