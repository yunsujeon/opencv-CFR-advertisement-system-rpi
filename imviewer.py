import numpy as np
import cv2
import pyautogui

screen_id = 0

print ('a')
# get the size of the screen
width, height = pyautogui.size()
print (width)
print (height)
image = cv2.imread('/home/pi/projects/opencv-CFR-advertisement-system-rpi/sst/snow.png')

window_name = 'projector'
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.moveWindow(window_name, width, height)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                      cv2.WINDOW_FULLSCREEN)
cv2.imshow(window_name, image)
cv2.waitKey()
cv2.destroyAllWindows()
