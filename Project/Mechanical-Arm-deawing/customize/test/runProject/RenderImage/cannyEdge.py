import numpy as np
from scipy import ndimage
import cv2
import matplotlib.pyplot as plt
from imagePointer import get_edge_coordinates, save_edge_coordinates_to_json

def gaussian_kernel(size, sigma=1):
    size = int(size) // 2
    x, y = np.mgrid[-size:size+1, -size:size+1]
    normal = 1 / (2.0 * np.pi * sigma**2)
    g =  np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
    return g

def sobel_filters(img):
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
    Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)

    Ix = ndimage.convolve(img, Kx)  # แก้ไขจาก ndimage.filters.convolve เป็น ndimage.convolve
    Iy = ndimage.convolve(img, Ky)  # แก้ไขจาก ndimage.filters.convolve เป็น ndimage.convolve

    G = np.hypot(Ix, Iy)
    G = G / G.max() * 255
    theta = np.arctan2(Iy, Ix)

    return (G, theta)

def non_max_suppression(gradient_magnitude, gradient_direction):
    image_row, image_col = gradient_magnitude.shape

    output = np.zeros(gradient_magnitude.shape)

    PI = 180

    for row in range(1, image_row - 1):
        for col in range(1, image_col - 1):
            direction = gradient_direction[row, col]
            if (0 <= direction < PI / 8) or (15 * PI / 8 <= direction <= 2 * PI):
                before_pixel = gradient_magnitude[row, col - 1]
                after_pixel = gradient_magnitude[row, col + 1]

            elif (PI / 8 <= direction < 3 * PI / 8) or (9 * PI / 8 <= direction < 11 * PI / 8):
                before_pixel = gradient_magnitude[row + 1, col - 1]
                after_pixel = gradient_magnitude[row - 1, col + 1]

            elif (3 * PI / 8 <= direction < 5 * PI / 8) or (11 * PI / 8 <= direction < 13 * PI / 8):
                before_pixel = gradient_magnitude[row - 1, col]
                after_pixel = gradient_magnitude[row + 1, col]

            else:
                before_pixel = gradient_magnitude[row - 1, col - 1]
                after_pixel = gradient_magnitude[row + 1, col + 1]

            if gradient_magnitude[row, col] >= before_pixel and gradient_magnitude[row, col] >= after_pixel:
                output[row, col] = gradient_magnitude[row, col]

    # if verbose:
    #    plt.imshow(output, cmap='gray')
    #    plt.title("Non Max Suppression")
    #    plt.show()

    return output

def threshold(img, lowThresholdRatio=0.05, highThresholdRatio=0.09):
    highThreshold = img.max() * highThresholdRatio
    lowThreshold = highThreshold * lowThresholdRatio

    M, N = img.shape
    res = np.zeros((M, N), dtype=np.int32)

    weak = np.int32(25)
    strong = np.int32(255)

    strong_i, strong_j = np.where(img >= highThreshold)
    zeros_i, zeros_j = np.where(img < lowThreshold)

    weak_i, weak_j = np.where((img <= highThreshold) & (img >= lowThreshold))

    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak

    return (res, weak, strong)

def hysteresis(img, weak, strong=255):
    M, N = img.shape
    for i in range(1, M-1):
        for j in range(1, N-1):
            if (img[i,j] == weak):
                try:
                    if ((img[i+1, j-1] == strong) or (img[i+1, j] == strong) or (img[i+1, j+1] == strong)
                        or (img[i, j-1] == strong) or (img[i, j+1] == strong)
                        or (img[i-1, j-1] == strong) or (img[i-1, j] == strong) or (img[i-1, j+1] == strong)):
                        img[i, j] = strong
                    else:
                        img[i, j] = 0
                except IndexError as e:
                    pass
    return img

def canny_edge_detection(image, sigma=1, low_threshold_ratio=0.05, high_threshold_ratio=0.09):
    # 1. ลดสัญญาณรบกวนด้วย Gaussian filter
    kernel = gaussian_kernel(size=5, sigma=sigma)
    smoothed = ndimage.convolve(image, kernel)

    # 2. หา gradient
    gradient, theta = sobel_filters(smoothed)

    # 3. Non-maximum suppression
    nms = non_max_suppression(gradient, theta)

    # 4. Double thresholding
    thresholded, weak, strong = threshold(nms, low_threshold_ratio, high_threshold_ratio)

    # 5. Edge tracking by hysteresis
    final = hysteresis(thresholded, weak, strong)

    return final

# อ่านภาพ
image = cv2.imread("cat3.jpg")

# ตรวจสอบว่าอ่านภาพสำเร็จหรือไม่
if image is None:
    print("Unable to read image file. Please check file name and location.")
else:
    # แปลงภาพเป็นขาวดำ (Grayscale)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ใช้งาน Canny Edge Detection
    edges = canny_edge_detection(gray_image)

    # เก็บตำแหน่งจุดขอบ
    # edge_coords = get_edge_coordinates(edges)

    # บันทึกพิกัดจุดขอบลงในไฟล์ .json
    # save_edge_coordinates_to_json(edge_coords)

    # print(f"จำนวนจุดขอบที่พบ: {len(edge_coords)}")
    # print("ตัวอย่างพิกัดจุดขอบ 5 จุดแรก:")
    # print(edge_coords[:5])

    # แปลงภาพจาก BGR เป็น RGB สำหรับการแสดงผลด้วย matplotlib
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # แสดงผลลัพธ์
    plt.figure(figsize=(12, 6))

    plt.subplot(121)
    plt.imshow(image_rgb)
    plt.title('Original image')
    plt.axis('off')

    plt.subplot(122)
    plt.imshow(edges, cmap='gray')
    plt.title('Canny Edge Detection')
    plt.axis('off')

    plt.tight_layout()
    plt.show()
