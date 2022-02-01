# 201702052 이동헌
# week08
import numpy as np
import cv2
import random
# library
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from my_library import *

# bilinear interpolation
def my_bilinear(img, x, y):
    '''
    :param img: 값을 찾을 img
    :param x: interpolation 할 x좌표
    :param y: interpolation 할 y좌표
    :return: img[x,y]에서의 value (bilinear interpolation으로 구해진)
    '''
    floorX, floorY = int(x), int(y)

    t, s = x - floorX, y - floorY

    zz = (1 - t) * (1 - s)
    zo = t * (1 - s)
    oz = (1 - t) * s
    oo = t * s

    interVal = img[floorY, floorX, :] * zz + img[floorY, floorX + 1, :] * zo + \
               img[floorY + 1, floorX, :] * oz + img[floorY + 1, floorX + 1, :] * oo

    return interVal

def backward_gaussian(img1, M):
    '''
    :param img1: 변환시킬 이미지
    :param M: 변환 matrix
    :return: 변환된 이미지
    '''
    h, w, c = img1.shape
    h2 = h*2
    w2 = w*2
    result = np.zeros((h2, w2, c), dtype=np.uint8)
    gaus2D = my_get_Gaussian2D_mask(5)
    mask = np.zeros((5, 5, c), dtype=np.uint8)
    pad_img1 = my_3D_padding(img1, mask)

    for row in range(h2):
        for col in range(w2):
            xy_prime = np.array([[col, row, 1]]).T
            xy = (np.linalg.inv(M)).dot(xy_prime)

            x_ = xy[0, 0]
            y_ = xy[1, 0]

            if x_ < 0 or y_ < 0 or (x_ + 1) >= w or (y_ + 1) >= h:
                continue

            # get 5 x 5 mask using bilinear
            for i in range(5):
                for j in range(5):
                    mask[i, j, :] = my_bilinear(pad_img1, (x_)+i, (y_)+j)

            # gaussian 2D filtering
            for i in range(c):
                filtered = (mask[:, :, i]*gaus2D)
                dst = np.sum(filtered.astype(np.uint8))
                result[row, col, i] = dst

    return result


def my_ls(matches, kp1, kp2):
    '''
    :param matches: keypoint matching 정보
    :param kp1: keypoint 정보.
    :param kp2: keypoint 정보2.
    :return: X : 위의 정보를 바탕으로 Least square 방식으로 구해진 Affine
                변환 matrix의 요소 [a, b, c, d, e, f].T
    '''
    A = []
    B = []
    for idx, match in enumerate(matches):
        trainInd = match.trainIdx
        queryInd = match.queryIdx

        x, y = kp1[queryInd].pt
        x_prime, y_prime = kp2[trainInd].pt

        A.append([x, y, 1, 0, 0, 0])
        A.append([0, 0, 0, x, y, 1])
        B.append([x_prime])
        B.append([y_prime])

    A = np.array(A)
    B = np.array(B)

    try:
        ATA = np.dot(A.T, A)
        ATB = np.dot(A.T, B)
        X = np.dot(np.linalg.inv(ATA), ATB)
    except:
        print('can\'t calculate np.linalg.inv((np.dot(A.T, A)) !!!!!')
        X = None
    return X


def get_matching_keypoints(img1, img2, keypoint_num):
    '''
    :param img1: 변환시킬 이미지
    :param img2: 변환 목표 이미지
    :param keypoint_num: 추출한 keypoint의 수
    :return: img1의 특징점인 kp1, img2의 특징점인 kp2, 두 특징점의 매칭 결과
    '''
    # opencv-contrib-python version : 3.4.2.16
    #sift = cv2.xfeatures2d.SIFT_create(keypoint_num)

    # opencv-contrib-python version > 3.4.2.16
    sift = cv2.SIFT_create(keypoint_num)

    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    bf = cv2.BFMatcher(cv2.DIST_L2)

    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    """
    matches: List[cv2.DMatch]
    cv2.DMatch의 배열로 구성

    matches[i]는 distance, imgIdx, queryIdx, trainIdx로 구성됨
    trainIdx: 매칭된 img1에 해당하는 index
    queryIdx: 매칭된 img2에 해당하는 index

    kp1[queryIdx]와 kp2[trainIdx]는 매칭된 점
    """
    return kp1, kp2, matches

def feature_matching_RANSAC(img1, img2, keypoint_num=None, iter_num=500, threshold_distance=10):
    '''
    :param img1: 변환시킬 이미지
    :param img2: 변환 목표 이미지
    :param keypoint_num: sift에서 추출할 keypoint의 수
    :param iter_num: RANSAC 반복횟수
    :param threshold_distance: RANSAC에서 inlier을 정할때의 거리 값
    :return: RANSAC을 이용하여 변환 된 결과
    '''
    kp1, kp2, matches = get_matching_keypoints(img1, img2, keypoint_num)

    h = img2.shape[0]
    w = img2.shape[1]

    matches_shuffle = matches.copy()

    inliers = [] #랜덤하게 고른 n개의 point로 구한 inlier개수 결과를 저장
    M_list = [] #랜덤하게 고른 n개의 point로 만든 affine matrix를 저장
    for i in range(iter_num):
        print('\rcalculate RANSAC ... %d ' % (int((i + 1) / iter_num * 100)) + '%', end='\t')
        # 1.1 matching 되는 점을 임의로 섞는다.
        random.shuffle(matches_shuffle)
        # 1.2 3개를 뽑아낸다.
        rand_three = matches_shuffle[:3]
        # 2. 1에서 뽑은 matches 를 이용하여 affine matrix M을 구함
        X = my_ls(rand_three, kp1, kp2)

        if X is None:
            continue

        affineM = np.array([ [X[0][0], X[1][0], X[2][0]],
                             [X[3][0], X[4][0], X[5][0]],
                             [0, 0, 1] ])
        # 3. 2에서 구한 affine을 모든 matches point와 연산하여 inlier의 개수를 파악
        M_list.append(affineM)

        count_inliers = 0
        for idx, match in enumerate(matches):
            trainInd = match.trainIdx
            queryInd = match.queryIdx

            kp1_x, kp1_y = kp1[queryInd].pt
            kp2_x, kp2_y = kp2[trainInd].pt

            xy = np.array([kp1_x, kp1_y, 1]).T
            xy_prime = np.dot(affineM, xy)

            if L2_distance(xy_prime[:2], (kp2_x, kp2_y)) < threshold_distance:
                count_inliers += 1
        inliers.append(count_inliers)

    # 4. iter_num 반복하여 가장 많은 inlier를 가지는 M을 최종 affine matrix로 채택
    inliers = np.array(inliers)
    max_inliers_idx = np.argmax(inliers)
    best_M = np.array(M_list[max_inliers_idx])

    result = backward_gaussian(img1, best_M)
    return result.astype(np.uint8)

def L2_distance(vector1, vector2):
    return np.sqrt(np.sum((vector1-vector2)**2))

def main():
    src = cv2.imread('/Users/dongheon97/Desktop/pic_dst.png')
    # resize : src * 0.5
    src = cv2.resize(src, None, fx=0.5, fy=0.5)
    src2 = cv2.imread('/Users/dongheon97/Desktop/pic_src.png')

    result_RANSAC = feature_matching_RANSAC(src, src2)
    cv2.imshow('input', src)
    cv2.imshow('gaussian_backward 201702052', result_RANSAC)
    cv2.imshow('goal', src2)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
