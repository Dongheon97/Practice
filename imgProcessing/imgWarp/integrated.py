import cv2
import numpy as np
import os

#from yolov5.detect import ObjectDetection

if __name__=="__main__":
    # Take a picture
    ##cap = cv2.VideoCapture(0)
    #cap.set(3, )
    #cap.set(4, )

    ##ret, obj_img = cap.read()

    #obj_path = "/Users/dongheon97/Downloads/images/images/capture/taken"
    obj_path = "/Users/dongheon97/Downloads/images/images/capture/taken"
    ##cv2.imwrite(takenPic, obj_path+".jpeg")
    obj_img = cv2.imread(obj_path+".jpeg", cv2.IMREAD_COLOR)#

    print("take a picture")

    # Get ref_img & obj_img
    ref_path = "/Users/dongheon97/Desktop/target/bullseye_large"
    ref_img = cv2.imread(ref_path+".jpeg", cv2.IMREAD_COLOR)

    obj_gray = cv2.cvtColor(obj_img, cv2.COLOR_BGR2GRAY)
    ref_gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)

    
    MAX_NUM_FEATURES = 500

    orb = cv2.ORB_create(MAX_NUM_FEATURES)
    k1, d1 = orb.detectAndCompute(obj_gray, None)
    k2, d2 = orb.detectAndCompute(ref_gray, None)

    #surf = cv2.xfeatures2d.SURF_create(MAX_NUM_FEATURES)
    #surf = cv2.SIFT_create(MAX_NUM_FEATURES)
    #k1, d1 = surf.detectAndCompute(obj_gray, None)
    #k2, d2 = surf.detectAndCompute(ref_gray, None)

    # Feature matching
    #matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matcher = cv2.BFMatcher()
    matches = list(matcher.match(d1, d2, None))

    # Eliminate features by distance
    matches.sort(key=lambda x: x.distance, reverse=False)

    numGoodMatches = int(len(matches) * 0.2)
    matches = matches[:numGoodMatches]

    result = cv2.drawMatches(ref_img, k2, obj_img, k1, matches, outImg=None, flags=2)
    cv2.imwrite('/Users/dongheon97/Desktop/matched.png', result)
    # Calculate warping matrix
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = k1[match.queryIdx].pt
        points2[i, :] = k2[match.trainIdx].pt

    # Get Matrix using library
    matrix, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    ref_img = cv2.imread(ref_path+".jpeg", cv2.COLOR_BGR2GRAY)
    height, width, channel = ref_img.shape

    warp_img = cv2.warpPerspective(obj_img, matrix, (width, height))

    warp_path = "/Users/dongheon97/dev/purdue/warped"
    #cv2.imwrite(warp_path+".jpeg", warp_img)

    print("image warping")

    cv2.imshow('origin', obj_img)
    cv2.imshow('warped', warp_img)
    cv2.imshow('result', result)
    cv2.waitKey()
    cv2.destroyAllWindows()

    # Object Detection
    #yolo = ObjectDetection(None)
    #bullets = yolo.run()

    #print(bullets)
