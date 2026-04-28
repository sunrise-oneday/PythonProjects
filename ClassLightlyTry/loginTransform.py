import cv2
import matplotlib.pyplot as plt
import numpy as np


def log(c, img):
    output = c * np.log(1 + img)
    output = output.astype(np.uint8)
    return output


img = cv2.imread("images/image.png", 0)  # 读取原始图像
if img is None:
    raise FileNotFoundError("无法读取图片，请检查文件路径是否正确！")

output = log(40, img)  # 进行对数变换，c=40
cv2.imshow("Output", output)  # 显示图像与直方图
cv2.imshow("img", img)
plt.hist(output.ravel(), 256)
plt.show()
