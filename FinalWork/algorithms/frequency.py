"""实验三：频率域滤波"""

import numpy as np
import cv2
from .registry import register


def _dft_shift(image: np.ndarray) -> tuple:
    """计算 FFT 并移位到中心"""
    h, w = image.shape[:2]
    # 处理彩色图先转灰度
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    img_f32 = np.float32(gray)
    dft = cv2.dft(img_f32, flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    return dft_shift, (h, w)


@register("频率域滤波", "理想低通滤波")
def ideal_lowpass(image: np.ndarray, radius: int = 50) -> np.ndarray:
    """理想低通滤波"""
    dft_shift, (h, w) = _dft_shift(image)
    crow, ccol = h // 2, w // 2

    mask = np.zeros((h, w, 2), np.uint8)
    cv2.circle(mask, (ccol, crow), radius, (1, 1), -1)

    fshift = dft_shift * mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])
    return np.clip(img_back, 0, 255).astype(np.uint8)


@register("频率域滤波", "巴特沃斯低通滤波")
def butterworth_lowpass(image: np.ndarray, radius: int = 50, order: int = 2) -> np.ndarray:
    """巴特沃斯低通滤波"""
    dft_shift, (h, w) = _dft_shift(image)
    crow, ccol = h // 2, w // 2

    y, x = np.ogrid[:h, :w]
    dist = np.sqrt((x - ccol) ** 2 + (y - crow) ** 2)
    mask = 1 / (1 + (dist / max(radius, 1)) ** (2 * order))
    mask = np.stack([mask] * 2, axis=-1)

    fshift = dft_shift * mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])
    return np.clip(img_back, 0, 255).astype(np.uint8)
