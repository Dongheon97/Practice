# 201702052 이 동 헌
# SIFT

import cv2
import numpy as np
from cv2 import KeyPoint

# library
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from my_library import *

def find_local_maxima(src, ksize):
    (h, w) = src.shape
    pad_img = np.zeros((h + ksize, w + ksize))
    pad_img[ksize // 2:h + ksize // 2, ksize // 2:w + ksize // 2] = src
    dst = np.zeros((h, w))

    for row in range(h):
        for col in range(w):
            max_val = np.max(pad_img[row: row + ksize, col:col + ksize])
            if max_val == 0:
                continue
            if src[row, col] == max_val:
                dst[row, col] = src[row, col]

    return dst

def SIFT(src):
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY).astype(np.float32)

    print("get keypoint")
    dst = cv2.cornerHarris(gray, 3, 3, 0.04)
    dst[dst < 0.01 * dst.max()] = 0
    dst = find_local_maxima(dst, 21)
    dst = dst / dst.max()
    
    #harris corner에서 keypoint를 추출
    y, x = np.nonzero(dst)

    keypoints = []
    for i in range(len(x)):
        # x, y, size, angle, response, octave, class_id
        pt_x = int(x[i]) #point x
        pt_y = int(y[i]) #point y
        size = None
        key_angle = -1.
        response = dst[y[i], x[i]] # keypoint에서 harris corner의 측정값
        octave = 0 # octave는 scale 변화를 확인하기 위한 값 (현재 과제에서는 사용안함)
        class_id = -1
        keypoints.append(KeyPoint(pt_x, pt_y, size, key_angle, response, octave, class_id))

    print('get Ix and Iy...')
    Ix, Iy = calc_derivatives(gray)

    print('calculate angle and magnitude')
    # magnitude / orientation 계산
    magnitude = np.sqrt((Ix ** 2) + (Iy ** 2))
    angle = np.arctan2(Iy, Ix)  # radian 값
    angle = np.rad2deg(angle)  # radian 값을 degree로 변경 > -180 ~ 180도로 표현
    angle = (angle + 360) % 360  # -180 ~ 180을 0 ~ 360의 표현으로 변경

    # @@@@ descriptor_angle 선언 @@@@
    descriptor_angle = np.zeros(angle.shape)

    # keypoint 방향
    print('calculate orientation assignment')
    for i in range(len(keypoints)):
        x, y = keypoints[i].pt
        orient_hist = np.zeros(36, ) #point의 방향을 저장
        for row in range(-8, 8):
            for col in range(-8, 8):
                p_y = int(y + row)
                p_x = int(x + col)
                if p_y < 0 or p_y > src.shape[0] - 1 or p_x < 0 or p_x > src.shape[1] - 1:
                    continue # 이미지를 벗어나는 부분에 대한 처리
                gaussian_weight = np.exp((-1 / 16) * (row ** 2 + col ** 2))
                orient_hist[int(angle[p_y, p_x] // 10)] += magnitude[p_y, p_x] * gaussian_weight
        ###################################################################
        ## ToDo
        ## orient_hist에서 가중치가 가장 큰 값을 추출하여 keypoint의 angle으로 설정
        ## 가장 큰 가중치의 0.8배보다 큰 가중치의 값도 keypoint의 angle로 설정
        ## keypoint 저장에는 KeyPoint module을 사용할 것 
        ## angle은 0 ~ 360도의 표현으로 저장해야 함
        ## np.max(find value), np.argmax(find index)를 활용하면 쉽게 구할 수 있음
        ## keypoints[i].angle = ???
        ###################################################################
        max_angle = orient_hist.argmax()  # histogram's column = angle / 10
        max_value = orient_hist[max_angle]
        keypoints[i].angle = int(max_angle) * 10  # histogram's column = 360 / 10
        # 0.8일 때도 추가
        thres = max_value * 0.8
        for i in range(len(orient_hist)):
            if(orient_hist[i] > thres):
                keypoints.append(KeyPoint(x, y, size, i*10, response, octave, class_id)) # i * 10 => angle

    print('calculate descriptor')
    descriptors = np.zeros((len(keypoints), 128))  # 8 orientation * 4 * 4 = 128 dimensions

    for i in range(len(keypoints)):
        x, y = keypoints[i].pt
        theta = np.deg2rad(keypoints[i].angle)
        # 키포인트 각도 조정을 위한 cos, sin값
        cos_angle = np.cos(theta)
        sin_angle = np.sin(theta)

        for row in range(-8, 8):
            for col in range(-8, 8):
                # 회전을 고려한 point값을 얻어냄
                row_rot = np.round((cos_angle * col) + (sin_angle * row))
                col_rot = np.round((cos_angle * col) - (sin_angle * row))

                p_y = int(y + row_rot)
                p_x = int(x + col_rot)
                if p_y < 0 or p_y > (src.shape[0] - 1) \
                        or p_x < 0 or p_x > (src.shape[1] - 1):
                    continue
                ###################################################################
                ## ToDo
                ## descriptor을 완성
                ## 4×4의 window에서 8개의 orientation histogram으로 표현
                ## 최종적으로 128개 (8개의 orientation * 4 * 4)의 descriptor를 가짐
                ## gaussian_weight = np.exp((-1 / 16) * (row_rot ** 2 + col_rot ** 2))
                ###################################################################
                gaussian_weight = np.exp((-1/16) * (row_rot ** 2 + col_rot ** 2))

                # 조정한 point에서 angle과 magnitude를 가져온다.
                descriptor_angle[p_y, p_x] = angle[p_y, p_x] - keypoints[i].angle
                # 8개의 histogram으로 나타내기 위해 / 45
                descriptor_angle[p_y, p_x] /= 45

                # counting filter_num
                patch_row = (row+8) // 4    # -8 <= row < 8
                patch_col = (col+8) // 4    # -8 <= col < 8
                filter_num = patch_row*4 + patch_col

                # index = patch 마다 8개 angle + 해당 각도
                index = (filter_num * 8) + int(descriptor_angle[p_y, p_x])

                descriptors[i, index] += magnitude[p_y, p_x] * gaussian_weight

    return keypoints, descriptors


def main():
    src = cv2.imread("/Users/dongheon97/Desktop/front.jpeg")
    #dst = cv2.rotate(src, cv2.ROTATE_90_CLOCKWISE)
    dst = cv2.imread("/Users/dongheon97/Desktop/test.jpeg")

    kp1, des1 = SIFT(src)
    kp2, des2 = SIFT(dst)

    ## Matching 부분 ## 
    bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=True)
    des1 = des1.astype(np.uint8)
    des2 = des2.astype(np.uint8)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key = lambda x:x.distance)

    result = cv2.drawMatches(src, kp1, dst, kp2, matches[:20], outImg=None, flags=2)
    
    # 결과의 학번 작성하기!
    cv2.imshow('output', result)
    cv2.waitKey()
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    main()
