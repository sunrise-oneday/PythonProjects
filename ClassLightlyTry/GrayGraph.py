import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread(r"C:\Users\77496\Pictures\MySQL001.jpg", 0)
if img is None:
    print("无法读取图像")
    exit()

cv2.imshow("Gray", img)  # 显示img中读取的灰度图片
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
plt.title(
    "Grayscale Histogram"
)  # 图像的标题  plt.hist(img.ravel(),256)		#画出灰度直方图
plt.show()
