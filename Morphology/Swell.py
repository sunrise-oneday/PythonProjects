import cv2
import numpy as np

o = cv2.imread("images/Tangle.png")  # 读取待处理图像
if o is None:
    print("无法读取图像")
    exit()

kernel = np.ones((9, 9), np.uint8)  # 构建5x5卷积核
dilation = cv2.dilate(o, kernel, iterations=5)  # 使用dilate函数处理，迭代5次
cv2.imshow("original", o)  # 输出原始图像
cv2.imshow("dilation", dilation)  # 输出结果图像
cv2.waitKey()
cv2.destroyAllWindows()
