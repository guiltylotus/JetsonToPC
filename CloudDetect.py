import numpy as np
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def Kmean(frame):
    """ Detect Cloud in Frame
    input: frame
    output: frame with red pixel (cloud) 
    """

    # img = cv2.imread('images/Cloud6.png')
    img = np.copy(frame)
    imgClone = np.copy(img)
    height, width, channel = img.shape

    Z = img.reshape((-1, 3))
    Z = np.float32(Z)

    iterations = 10
    epsilon = 1.0

    criteria = (cv2.TERM_CRITERIA_EPS +
                cv2.TERM_CRITERIA_MAX_ITER, iterations, epsilon)
    K = 2
    ret, label, center = cv2.kmeans(
        Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))

	# Sort by grayScale
    # newCenter = center.reshape((1, -1, 3))
    # grayCenter = cv2.cvtColor(newCenter, cv2.COLOR_BGR2GRAY)
    # cloudPixel = center[np.argsort(grayCenter)[0][0]]

	# Take Cloud mean
    cloudMean = np.mean(center, axis=0)
    cloudPixel = cloudMean
    # print(cloudMean)

    return cloudPixel


def CloudThreshold(frame, threshold):

    img = np.copy(frame)
    # print(threshold)
    img[np.where((img >= threshold).all(axis=2))] = [0, 33, 166]

    return img

def TotalCloud(frame, threshold):

    total = frame[np.where((frame >= threshold).all(axis=2))].shape[0]
    return total