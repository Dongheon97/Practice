import cv2
import numpy as np

if __name__=="__main__":
  src = cv2.imread('/Users/dongheon97/Desktop/target/bullseye_large.jpeg', cv2.IMREAD_COLOR)
  #src = np.array(src)
  h, w, c = src.shape
  dst = np.zeros((h+40,w+40,3))
  dst[20:h+20, 20:w+20, :] = src
  #src[0:10, :, :] = 0
  #src[h-10:h, :, :] = 0
  #src[:, 0:10, :] = 0
  #src[:, w-10:w, :] = 0

  cv2.imwrite('/Users/dongheon97/Desktop/target/bullsye_frame.jpeg', dst)

