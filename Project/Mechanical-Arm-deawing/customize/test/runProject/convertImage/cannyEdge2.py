import numpy as np
from scipy import ndimage
import cv2
import matplotlib.pyplot as plt
from imagePointer import get_edge_coordinates, save_edge_coordinates_to_json
from gaussian_smoothing import gaussian_blur
from sobel import sobel_edge_detection


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


def threshold(image, low, high, weak, verbose=False):
    output = np.zeros(image.shape)

    strong = 255

    strong_row, strong_col = np.where(image >= high)
    weak_row, weak_col = np.where((image <= high) & (image >= low))

    output[strong_row, strong_col] = strong
    output[weak_row, weak_col] = weak

    if verbose:
        plt.imshow(output, cmap='gray')
        plt.title("threshold")
        plt.show()

    return output


def hysteresis(image, weak):
    image_row, image_col = image.shape

    top_to_bottom = image.copy()

    for row in range(1, image_row):
        for col in range(1, image_col):
            if top_to_bottom[row, col] == weak:
                if top_to_bottom[row, col + 1] == 255 or top_to_bottom[row, col - 1] == 255 or top_to_bottom[
                    row - 1, col] == 255 or top_to_bottom[
                    row + 1, col] == 255 or top_to_bottom[
                    row - 1, col - 1] == 255 or top_to_bottom[row + 1, col - 1] == 255 or top_to_bottom[
                    row - 1, col + 1] == 255 or top_to_bottom[
                    row + 1, col + 1] == 255:
                    top_to_bottom[row, col] = 255
                else:
                    top_to_bottom[row, col] = 0

    bottom_to_top = image.copy()

    for row in range(image_row - 1, 0, -1):
        for col in range(image_col - 1, 0, -1):
            if bottom_to_top[row, col] == weak:
                if bottom_to_top[row, col + 1] == 255 or bottom_to_top[row, col - 1] == 255 or bottom_to_top[
                    row - 1, col] == 255 or bottom_to_top[
                    row + 1, col] == 255 or bottom_to_top[
                    row - 1, col - 1] == 255 or bottom_to_top[row + 1, col - 1] == 255 or bottom_to_top[
                    row - 1, col + 1] == 255 or bottom_to_top[
                    row + 1, col + 1] == 255:
                    bottom_to_top[row, col] = 255
                else:
                    bottom_to_top[row, col] = 0

    right_to_left = image.copy()

    for row in range(1, image_row):
        for col in range(image_col - 1, 0, -1):
            if right_to_left[row, col] == weak:
                if right_to_left[row, col + 1] == 255 or right_to_left[row, col - 1] == 255 or right_to_left[
                    row - 1, col] == 255 or right_to_left[
                    row + 1, col] == 255 or right_to_left[
                    row - 1, col - 1] == 255 or right_to_left[row + 1, col - 1] == 255 or right_to_left[
                    row - 1, col + 1] == 255 or right_to_left[
                    row + 1, col + 1] == 255:
                    right_to_left[row, col] = 255
                else:
                    right_to_left[row, col] = 0

    left_to_right = image.copy()

    for row in range(image_row - 1, 0, -1):
        for col in range(1, image_col):
            if left_to_right[row, col] == weak:
                if left_to_right[row, col + 1] == 255 or left_to_right[row, col - 1] == 255 or left_to_right[
                    row - 1, col] == 255 or left_to_right[
                    row + 1, col] == 255 or left_to_right[
                    row - 1, col - 1] == 255 or left_to_right[row + 1, col - 1] == 255 or left_to_right[
                    row - 1, col + 1] == 255 or left_to_right[
                    row + 1, col + 1] == 255:
                    left_to_right[row, col] = 255
                else:
                    left_to_right[row, col] = 0

    final_image = top_to_bottom + bottom_to_top + right_to_left + left_to_right

    final_image[final_image > 255] = 255

    return final_image

# def canny_edge_detection(image, sigma=1, low_threshold_ratio=0.05, high_threshold_ratio=0.09):
#     """ทำ Canny Edge Detection"""
#     # 1. ลดสัญญาณรบกวนด้วย Gaussian filter
#     kernel = gaussian_kernel(size=5, sigma=sigma)
#     smoothed = ndimage.convolve(image, kernel)
#
#     # 2. หา gradient
#     gradient, theta = sobel_filters(smoothed)
#
#     # 3. Non-maximum suppression
#     nms = non_max_suppression(gradient, theta)
#
#     # 4. Double thresholding
#     thresholded, weak, strong = threshold(nms, low_threshold_ratio, high_threshold_ratio)
#
#     # 5. Edge tracking by hysteresis
#     final = hysteresis(thresholded, weak, strong)
#
#     return final


# อ่านภาพ
image = cv2.imread("lena01.png")

# ตรวจสอบว่าอ่านภาพสำเร็จหรือไม่
if image is None:
    print("Unable to read image file. Please check file name and location.")
else:
    cv2.imshow("Original Image", image)
    resize = np.array(image)

    blurred_image = gaussian_blur(resize, kernel_size=9, verbose=False)

    edge_filter = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

    gradient_magnitude, gradient_direction = sobel_edge_detection(blurred_image, edge_filter, convert_to_degree=True)

    new_image = non_max_suppression(gradient_magnitude, gradient_direction)

    weak = 50

    new_image = threshold(new_image, 5, 20, weak=weak)
    new_image = hysteresis(new_image, weak)

    cv2.imshow('Resize edge image', new_image)

    cv2.waitKey(0)

    edge_coords = get_edge_coordinates(new_image)
    save_edge_coordinates_to_json(edge_coords)

    # # แปลงภาพเป็นขาวดำ (Grayscale)
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #
    # # ใช้งาน Canny Edge Detection
    # edges = canny_edge_detection(gray_image)
    #
    # # เก็บตำแหน่งจุดขอบ (ถ้าต้องการ)
    # # edge_coords = get_edge_coordinates(edges)
    #
    # # บันทึกพิกัดจุดขอบลงในไฟล์ .json (ถ้าต้องการ)
    # # save_edge_coordinates_to_json(edge_coords)
    #
    # # แปลงภาพจาก BGR เป็น RGB สำหรับการแสดงผลด้วย matplotlib
    # image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #
    # # แสดงผลลัพธ์
    # plt.figure(figsize=(12, 6))
    #
    # plt.subplot(121)
    # plt.imshow(image_rgb)
    # plt.title('Original Image')
    # plt.axis('off')
    #
    # plt.subplot(122)
    # plt.imshow(edges, cmap='gray')
    # plt.title('Canny Edge Detection')
    # plt.axis('off')
    #
    # plt.tight_layout()
    # plt.show()
