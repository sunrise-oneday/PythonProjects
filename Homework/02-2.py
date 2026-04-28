# type: ignore
import cv2
import matplotlib.pyplot as plt
import numpy as np

# 1. 读取灰度图
img = cv2.imread("images/Mat02.jpg", 0)
if img is None:
    print("无法读取图像")
    exit()
h, w = img.shape

# 2. 傅里叶变换 + 中心化
f = np.fft.fft2(img)
f_shift = np.fft.fftshift(f)

# 3. 构造滤波器掩模
# 中心坐标
cx, cy = w // 2, h // 2


# 理想低通滤波器 (LPF)：保留中心低频
def ideal_low_pass(radius=50):
    mask = np.zeros((h, w), np.float32)
    for x in range(w):
        for y in range(h):
            if np.hypot(x - cx, y - cy) <= radius:
                mask[y, x] = 1
    return mask


# 理想高通滤波器 (HPF)：保留高频边缘
def ideal_high_pass(radius=50):
    return 1 - ideal_low_pass(radius)


# 带阻滤波器 (BSF)：阻止某一频段
def band_stop(r1=20, r2=80):
    mask = np.ones((h, w), np.float32)
    for x in range(w):
        for y in range(h):
            d = np.hypot(x - cx, y - cy)
            if r1 <= d <= r2:
                mask[y, x] = 0
    return mask


# 带通滤波器 (BPF)：只保留某一频段
def band_pass(r1=20, r2=80):
    return 1 - band_stop(r1, r2)


# 4. 选择滤波器
mask = ideal_low_pass(50)  # 低通
mask = ideal_high_pass(30)  # 高通
mask = band_pass(20, 80)  # 带通
mask = band_stop(20, 80)  # 带阻

# 5. 频域滤波
f_filtered = f_shift * mask

# 6. 逆傅里叶变换
f_ishift = np.fft.ifftshift(f_filtered)
img_filtered = np.fft.ifft2(f_ishift)
img_filtered = np.abs(img_filtered)

# 7. 显示结果
plt.figure(figsize=(12, 8))

plt.subplot(221)
plt.imshow(img, cmap="gray")
plt.title("Original")
plt.axis("off")

plt.subplot(222)
plt.imshow(20 * np.log(np.abs(f_shift) + 1), cmap="gray")
plt.title("FFT Spectrum")
plt.axis("off")

plt.subplot(223)
plt.imshow(mask, cmap="gray")
plt.title("Filter Mask")
plt.axis("off")

plt.subplot(224)
plt.imshow(img_filtered, cmap="gray")
plt.title("Filtered Image")
plt.axis("off")

plt.show()
