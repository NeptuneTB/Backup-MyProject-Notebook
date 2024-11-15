import numpy as np
import cv2
# import argparse

import project.sobel as sobel
import project.gaussian_smoothing as gaussian

import matplotlib.pyplot as plt


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

# อ่านภาพตัวอย่าง
img = cv2.imread('lena_square_half.png', 0)

# ขั้นตอนการใช้ Sobel Filter เพื่อตรวจจับขอบ
blurred = cv2.GaussianBlur(img, (5, 5), 1.4)
gradient, theta = sobel.sobel_edge_detection()
nms_img = non_max_suppression(gradient, theta)
threshold_img, weak, strong = threshold(nms_img)
final_img = hysteresis(threshold_img, weak, strong)

# แสดงภาพก่อนและหลังการแปลงภาพเป็นเส้น
plt.figure(figsize=(10,5))
plt.subplot(1, 2, 1)
plt.imshow(img, cmap='gray')
plt.title('Original Image')

plt.subplot(1, 2, 2)
plt.imshow(final_img, cmap='gray')
plt.title('Edge Detected Image')

plt.show()


# if __name__ == '__main__':
#     # ap = argparse.ArgumentParser()
#     # ap.add_argument("-i", "--image", required=True, help="Path to the image")
#     # ap.add_argument("-v", "--verbose", type=bool, default=False, help="Path to the image")
#     # args = vars(ap.parse_args())
#
#     # image = cv2.imread(args["image"])
#     image = cv2.imread("Image/8910.jpg")
#     print(image.shape)
#     resize = cv2.resize(image, (115, 110), cv2.INTER_CUBIC)
#     cv2.imshow("Resized Image", resize)
#
#     plt.imshow(image, cmap='gray')
#     plt.title("Original Image")
#     plt.show()
#
#     blurred_image = gaussian_blur(image, kernel_size=9, verbose=False)
#
#     edge_filter = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
#
#     # gradient_magnitude, gradient_direction = sobel_edge_detection(blurred_image, edge_filter, convert_to_degree=True,
#     #                                                              verbose=args["verbose"])
#     gradient_magnitude, gradient_direction = sobel_edge_detection(blurred_image, edge_filter, convert_to_degree=True)
#
#     # new_image = non_max_suppression(gradient_magnitude, gradient_direction, verbose=args["verbose"])
#     new_image = non_max_suppression(gradient_magnitude, gradient_direction)
#
#     weak = 50
#
#     # new_image = threshold(new_image, 5, 20, weak=weak, verbose=args["verbose"])
#     new_image = threshold(new_image, 5, 20, weak=weak)
#     new_image = hysteresis(new_image, weak)
#
#     cv2.imshow('Resize edge image', cv2.resize(new_image, (115, 100), cv2.INTER_CUBIC))  # INTER_NEAREST
#     cv2.imwrite('sizeOutput1.png', new_image, (115, 100))
#     plt.imshow(new_image, cmap='gray')
#     plt.title("Canny Edge Detector")
#     plt.show()
