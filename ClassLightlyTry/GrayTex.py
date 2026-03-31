import cv2
import numpy as np
from matplotlib import pyplot as plt

# 1. 读取并处理图像
img = cv2.imread('images/zutomayo.jpg', 0)
processed_array = (img // 2).astype(np.uint8)

# 2. OpenCV 显示图像（非阻塞）
cv2.imshow("Processed", processed_array)
cv2.waitKey(1)  # ⚠️ 关键：给OpenCV窗口时间渲染，用1而不是0

# 3. Matplotlib 绘制直方图（阻塞式）
plt.title("Grayscale Histogram")
plt.hist(processed_array.ravel(), 256, [0, 256])
plt.show()  # ⚠️ 这会阻塞程序，直到关闭图表窗口

# 4. 关闭OpenCV窗口（plt.show()关闭后执行）
cv2.destroyAllWindows()