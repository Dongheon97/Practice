import cv2
import numpy as np

src = cv2.imread('/Users/dongheon97/Desktop/dataset/real/3.jpeg', cv2.IMREAD_COLOR)
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
ret, thres1 = cv2.threshold(src_gray, 120, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ret, thres2 = cv2.threshold(src_gray, 20, 255, cv2.THRESH_OTSU)

cv2.imwrite('/Users/dongheon97/Desktop/dataset/real/gray3.jpeg', thres2)
cv2.imshow('gray', src_gray)
cv2.imshow('otsu', thres2)
cv2.waitKey()
cv2.DestroyAllWindows()

