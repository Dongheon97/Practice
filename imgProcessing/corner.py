import cv2 
import numpy as np

img = cv2.imread('/Users/dongheon97/Desktop/flag_src.png')
img = cv2.resize(img, (0, 0), fx=0.75, fy=0.75)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(img, 100, 0.01, 10)
corners = np.int0(corners)

for corner in corners:
  x, y = corner.ravel()
  cv2.circle(img, (x, y), 5, (255, 0, 0), -1) 

cv2.imshow('Frame', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
