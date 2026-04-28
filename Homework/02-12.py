# type: ignore
import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread("images/Mat01.jpg")
if img is None:
    print("无法读取图像")
    exit()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 傅里叶变换
f = np.fft.fft2(gray)
# 把低频移到图像中心（必须加，否则频谱看不清）
f_shift = np.fft.fftshift(f)

# 计算幅度谱（取对数让范围变小，方便显示）
magnitude_spectrum = 20 * np.log(np.abs(f_shift))

# 3. 傅里叶逆变换
# 逆中心化
f_ishift = np.fft.ifftshift(f_shift)
# 逆变换
img_back = np.fft.ifft2(f_ishift)
img_back = np.abs(img_back)

# ===================== 4. 显示结果 =====================
plt.figure(figsize=(12, 4))

# 显示原图
plt.subplot(1, 3, 1)
plt.imshow(img, cmap="gray")
plt.title("Original Image")
plt.axis("off")

# 显示频谱
plt.subplot(1, 3, 2)
plt.imshow(magnitude_spectrum, cmap="gray")
plt.title("Frequency Spectrum")
plt.axis("off")

# 显示逆变换后的图像
plt.subplot(1, 3, 3)
plt.imshow(img_back, cmap="gray")
plt.title("Restored Image")
plt.axis("off")

plt.show()
