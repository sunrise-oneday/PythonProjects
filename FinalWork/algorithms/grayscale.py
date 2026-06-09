"""实验一：灰度变换与直方图"""

import numpy as np
import cv2
from .registry import register


@register("灰度变换", "线性变换")
def linear_transform(image: np.ndarray, alpha: float = 1.0, beta: int = 0) -> np.ndarray:
    """g(x,y) = alpha * f(x,y) + beta，自动截断 [0,255]"""
    img_f32 = image.astype(np.float32)
    result = np.clip(alpha * img_f32 + beta, 0, 255)
    return result.astype(np.uint8)


@register("灰度变换", "分段线性变换")
def piecewise_linear(image: np.ndarray, r1: int = 80, s1: int = 30, r2: int = 180, s2: int = 220) -> np.ndarray:
    """三段式分段线性变换"""
    img_f32 = image.astype(np.float32)
    result = np.zeros_like(img_f32)

    mask1 = img_f32 <= r1
    mask2 = (img_f32 > r1) & (img_f32 <= r2)
    mask3 = img_f32 > r2

    result[mask1] = (s1 / max(r1, 1)) * img_f32[mask1]
    result[mask2] = ((s2 - s1) / max(r2 - r1, 1)) * (img_f32[mask2] - r1) + s1
    result[mask3] = ((255 - s2) / max(255 - r2, 1)) * (img_f32[mask3] - r2) + s2

    return np.clip(result, 0, 255).astype(np.uint8)


@register("灰度变换", "直方图均衡化")
def histogram_equalization(image: np.ndarray) -> np.ndarray:
    """直方图均衡化（彩色图处理 Y 通道）"""
    if len(image.shape) == 2:
        return cv2.equalizeHist(image)
    else:
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)


@register("灰度变换", "CLAHE自适应均衡化")
def adaptive_equalization(image: np.ndarray, clip_limit: float = 2.0, grid_size: int = 8) -> np.ndarray:
    """限制对比度自适应直方图均衡化"""
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(grid_size, grid_size))
    if len(image.shape) == 2:
        return clahe.apply(image)
    else:
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
