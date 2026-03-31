import cv2 
import numpy as np 

img = cv2.imread('images/image.png', 1)  # 读取原始图像
rows, cols = img.shape[:2]  # 返回原图像像素的行和列

# 定义旋转中心点
center = (cols // 2, rows // 2)

# 获取仿射变换矩阵
matRotate45 = cv2.getRotationMatrix2D(center, 45, 1)    # 中心旋转45°
matRotate90 = cv2.getRotationMatrix2D(center, 90, 1)    # 中心旋转90°
matRotate180 = cv2.getRotationMatrix2D(center, 180, 1)  # 中心旋转180°

# 进行仿射变换
dst = cv2.warpAffine(img, matRotate45, (cols, rows), borderValue=(255, 255, 255)) 
src = cv2.warpAffine(img, matRotate90, (cols, rows), borderValue=(255, 255, 255)) 
mat = cv2.warpAffine(img, matRotate180, (cols, rows), borderValue=(255, 255, 255)) 

cv2.imshow('origin_picture', img)       # 输出原始图像
cv2.imshow('new_picture1', dst)         # 输出中心旋转45°图像
cv2.imshow('new_picture2', src)         # 输出中心旋转90°图像
cv2.imshow('new_picture3', mat)         # 输出中心旋转180°图像
cv2.waitKey(0)
cv2.destroyAllWindows()
