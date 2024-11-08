import cv2
import numpy as np
from matplotlib import pyplot as plt
from cannyEdge import sobel_filters, non_max_suppression, threshold, hysteresis

# โหลดภาพและแปลงเป็นขาวดำ (Grayscale)
img = cv2.imread('')

# เรียกฟังก์ชัน Sobel Filter เพื่อคำนวณขอบภาพ
G, theta = sobel_filters(img)

# เรียกฟังก์ชัน Non-Max Suppression เพื่อทำการยับยั้งค่าที่ไม่ใช่ค่าขอบ
non_max_img = non_max_suppression(G, theta)

# เรียกฟังก์ชัน Threshold เพื่อแปลงภาพเป็นระดับสีตามเงื่อนไข
threshold_img, weak, strong = threshold(non_max_img)

# เรียกฟังก์ชัน Hysteresis เพื่อทำการต่อเชื่อมขอบที่อ่อนแอให้เป็นขอบที่แข็งแรง
final_img = hysteresis(threshold_img, weak, strong)

# แสดงภาพผลลัพธ์
plt.figure(figsize=(10,10))

plt.subplot(1, 2, 1)
plt.imshow(img, cmap='gray')
plt.title('Original Image')

plt.subplot(1, 2, 2)
plt.imshow(final_img, cmap='gray')
plt.title('Final Edge Detection')

plt.show()
