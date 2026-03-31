import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('images/image.png',0)
img1 = np.power(img/float(np.max(img)), 1/2)        #γ=0.5
img2 = np.power(img/float(np.max(img)), 2)         # γ=2
cv2.imshow('original',img)
cv2.imshow('r=1/2',img1)
cv2.imshow('r=2',img2)
plt.hist(img.ravel(),256)
plt.hist(img1.ravel(),256)
plt.hist(img2.ravel(),256)
plt.show()
