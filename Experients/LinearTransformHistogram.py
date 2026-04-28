import cv2
import numpy as np
from matplotlib import pyplot as plt

# ========== 1. 读取与灰度转换 ==========(实验指导书)
img = cv2.imread("images/Nikoniko.png")
if img is None:
    print("无法读取图像")
    exit()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 图像灰度转换


h, w = gray.shape
result = np.zeros((h, w), np.uint8)

for i in range(h):
    for j in range(w):
        # result[i, j] = np.clip((gray[i, j] - 100) * 1.2, 0, 255)
        if gray[i, j] < 100:
            result[i, j] = 0
        else:
            result[i, j] = np.clip((gray[i, j] - 100) * 1.2, 0, 255)

equalized = cv2.equalizeHist(gray)  # 均匀化


# 三张图像对比(AI)
cv2.imshow("Original", gray)
cv2.imshow("Linear Transform", result)
cv2.imshow("Histogram Equalized", equalized)


cv2.waitKey(1)  # 让OpenCV窗口渲染

# 三张直方图对比
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].hist(gray.ravel(), 256, [0, 256], color="gray")
axes[0].set_title("Original")
axes[1].hist(result.ravel(), 256, [0, 256], color="blue")
axes[1].set_title("Linear Transform")
axes[2].hist(equalized.ravel(), 256, [0, 256], color="green")
axes[2].set_title("Equalized")
plt.show()

cv2.destroyAllWindows()
