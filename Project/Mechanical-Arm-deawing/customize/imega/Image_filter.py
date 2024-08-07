import cv2
import numpy as np

# โหลดภาพและแปลงเป็นภาพสีเทา
image = cv2.imread('lena_square_half.png', 0)

# ใช้ Canny Edge Detector
edges = cv2.Canny(image, 100, 200)

# ค้นหา Contours
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# วาด Contours ลงบนภาพต้นฉบับ
contour_image = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 2)

# แสดงภาพที่ได้
cv2.imshow('Contours', contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# จัดเก็บพิกัดของ Contours
contour_points = [contour.reshape(-1, 2) for contour in contours]

print(contour_points)
