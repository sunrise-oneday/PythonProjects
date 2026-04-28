import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("images/image.png", 0)
if img is None:
    print("无法读取图像")
    exit()
equal = cv2.equalizeHist(img)  # 直方图均衡化
hist = cv2.calcHist([equal], [0], None, [256], [0, 256])
cv2.imshow("equal", equal)
plt.hist(equal.ravel(), 256)
plt.show()
