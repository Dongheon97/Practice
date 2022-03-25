import cv2
import numpy as np

if __name__=="__main__":
    src = cv2.imread("/Users/dongheon97/Downloads/4.jpeg", cv2.IMREAD_COLOR)
    h, w, c = src.shape
    src[:, :1, :] = 255
    src[:, 412:, :] = 255
    src[0, :, :] = 255
    src[530, :, :] = 255
    print(h, w, c)
    
    dst = np.full((h, h, c), 255, np.uint8)
    print(dst.shape)
    dst[:, 58:471, :] = src
    cv2.imwrite('/Users/dongheon97/Downloads/profile.jpeg', dst)