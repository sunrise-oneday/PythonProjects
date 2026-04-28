import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread("images/image.png")
if img is None:
    print("无法读取图像")
    exit()
grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 图像灰度转换
height = grayImage.shape[0]  # 获取图像高度
width = grayImage.shape[1]  # 获取图像宽度
result = np.zeros((height, width), np.uint8)  # 创建一幅图像
for i in range(height):
    for j in range(width):
        if int(grayImage[i, j] * 2) > 255:
            gray = 255  # 防溢出判断
        else:
            gray = int(grayImage[i, j] + 50)  # 每个像素点的灰度值增加50
        result[i, j] = np.uint8(gray)
        cv2.imshow("Result", result)
plt.hist(grayImage.ravel(), 256)
plt.show()
