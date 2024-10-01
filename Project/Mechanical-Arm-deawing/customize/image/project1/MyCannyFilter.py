import cv2
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.ndimage import convolve
from scipy import misc
import numpy as np




#img_smoothed = None
#gradientMat = None
#thetaMat = None
#nonMaxImg = None
#thresholdImg = None
#weak_pixel = 75
#strong_pixel = 255
#sigma = 1
#kernel_size = 5
#lowThreshold = 0.05
#highThreshold = 0.15


def gaussian_kernel( size, sigma=1):
    size = int(size) // 2
    x, y = np.mgrid[-size:size + 1, -size:size + 1]
    normal = 1 / (2.0 * np.pi * sigma ** 2)
    g = np.exp(-((x ** 2 + y ** 2) / (2.0 * sigma ** 2))) * normal
    return g


def sobel_filters(img):
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
    Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)

    Ix = convolve(img, Kx)
    Iy = convolve(img, Ky)

    G = np.hypot(Ix, Iy)
    G = G / G.max() * 255
    theta = np.arctan2(Iy, Ix)
    return (G, theta)


def non_max_suppression(img, D):
    M, N = img.shape
    Z = np.zeros((M, N), dtype=np.int32)
    angle = D * 180. / np.pi
    angle[angle < 0] += 180

    for i in range(1, M - 1):
        for j in range(1, N - 1):
            try:
                q = 255
                r = 255

                # angle 0
                if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                    q = img[i, j + 1]
                    r = img[i, j - 1]
                # angle 45
                elif (22.5 <= angle[i, j] < 67.5):
                    q = img[i + 1, j - 1]
                    r = img[i - 1, j + 1]
                # angle 90
                elif (67.5 <= angle[i, j] < 112.5):
                    q = img[i + 1, j]
                    r = img[i - 1, j]
                # angle 135
                elif (112.5 <= angle[i, j] < 157.5):
                    q = img[i - 1, j - 1]
                    r = img[i + 1, j + 1]

                if (img[i, j] >= q) and (img[i, j] >= r):
                    Z[i, j] = img[i, j]
                else:
                    Z[i, j] = 0


            except IndexError as e:
                pass

    return Z



def threshold(img):
    lowThreshold = 0.01
    highThreshold = 0.1
    weak_pixel = 100
    strong_pixel = 255

    highThreshold = img.max() * highThreshold
    lowThreshold = highThreshold * lowThreshold

    M, N = img.shape
    res = np.zeros((M, N), dtype=np.int32)

    weak = np.int32(weak_pixel)
    strong = np.int32(strong_pixel)

    strong_i, strong_j = np.where(img >= highThreshold)
    zeros_i, zeros_j = np.where(img < lowThreshold)

    weak_i, weak_j = np.where((img <= highThreshold) & (img >= lowThreshold))

    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak

    return (res)


def hysteresis(img):
    weak_pixel = 75
    strong_pixel = 255

    M, N = img.shape
    weak = weak_pixel
    strong = strong_pixel

    for i in range(1, M - 1):
        for j in range(1, N - 1):
            if (img[i, j] == weak):
                try:
                    if ((img[i + 1, j - 1] == strong) or (img[i + 1, j] == strong) or (img[i + 1, j + 1] == strong)
                            or (img[i, j - 1] == strong) or (img[i, j + 1] == strong)
                            or (img[i - 1, j - 1] == strong) or (img[i - 1, j] == strong) or (
                                    img[i - 1, j + 1] == strong)):
                        img[i, j] = strong
                    else:
                        img[i, j] = 0
                except IndexError as e:
                    pass

    return img

if __name__ == '__main__':

    sigma = 1
    kernel_size = 5
    gradientMat = None
    thetaMat = None
    nonMaxImg = None
    thresholdImg = None

    img = cv2.imread('image/gail1.png', cv2.IMREAD_GRAYSCALE)


    img_smoothed = convolve(img, gaussian_kernel(kernel_size,sigma))
    gradientMat, thetaMat = sobel_filters(img_smoothed)
    nonMaxImg = non_max_suppression(gradientMat,thetaMat)
    thresholdImg = threshold(nonMaxImg)
    img_final = hysteresis(thresholdImg)
    edges = cv2.Canny(img, 100, 200)
    #plt.imshow(img_final, cmap='gray')
    cv2.imshow("cannny edge detection", img_final.astype(np.uint8))
    cv2.imshow("cannny edge detection opencv", edges.astype(np.uint8))
    cv2.waitKey(0)