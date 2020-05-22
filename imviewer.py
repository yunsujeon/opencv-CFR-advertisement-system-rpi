#from skimage.viewer import ImageViewer
#from skimage.io import imread
import cv2
import pyautogui
width, height = pyautogui.size()
img = cv2.imread('/home/pi/projects/opencv-CFR-advertisement-system-Linux/sst/snow.png',cv2.IMREAD_COLOR) #path to IMG
#view = ImageViewer(img)
#view.show()
img_resized = cv2.resize(img,dsize=(width,height),interpolation=cv2.INTER_LINEAR)
cv2.imshow('img',img_resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
