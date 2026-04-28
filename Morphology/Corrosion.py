import cv2
import numpy as np

o = cv2.imread("images/Morph.png")  # 读取待处理图像
if o is None:
    print("无法读取图像")
    exit()
kernel = np.ones((3, 3), np.uint8)  # 构建5x5卷积核
erosion = cv2.erode(o, kernel, iterations=2)  # 使用erode函数处理，迭代2次
cv2.imshow("original", o)  # 输出原始图像
cv2.imshow("erosion", erosion)  # 输出结果图像
cv2.waitKey()
cv2.destroyAllWindows()
