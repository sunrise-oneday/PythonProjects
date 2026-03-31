import cv2  
import numpy as np  
import matplotlib.pyplot as plt  

def log(c, img):  
    output = c * np.log(1 + img)  
    output = np.uint8(output) 
    return output  

img = cv2.imread('images/image.png', 0)		# 读取原始图像 
output = log(40, img)		# 进行对数变换，c=40  
cv2.imshow('Output', output)		# 显示图像与直方图  
cv2.imshow('img', img)
plt.hist(output.ravel(), 256) 
plt.show()