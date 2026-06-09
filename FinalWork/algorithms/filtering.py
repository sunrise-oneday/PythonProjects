"""实验二：空间滤波（平滑与锐化）"""

import numpy as np
import cv2
from .registry import register


@register("空间滤波", "均值滤波")
def mean_filter(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """均值平滑"""
    return cv2.blur(image, (kernel_size, kernel_size))


@register("空间滤波", "高斯滤波")
def gaussian_blur(image: np.ndarray, kernel_size: int = 3, sigma: float = 1.0) -> np.ndarray:
    """高斯平滑"""
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)


@register("空间滤波", "中值滤波")
def median_filter(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """中值滤波（对椒盐噪声效果极佳）"""
    return cv2.medianBlur(image, kernel_size)


@register("空间滤波", "拉普拉斯锐化")
def laplacian_sharpen(image: np.ndarray, strength: float = 1.0) -> np.ndarray:
    """拉普拉斯算子锐化"""
    lap = cv2.Laplacian(image, cv2.CV_32F)
    img_f32 = image.astype(np.float32)
    result = img_f32 - strength * lap
    return np.clip(result, 0, 255).astype(np.uint8)


@register("空间滤波", "Sobel锐化")
def sobel_sharpen(image: np.ndarray) -> np.ndarray:
    """Sobel 梯度锐化"""
    grad_x = cv2.Sobel(image, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(image, cv2.CV_32F, 0, 1, ksize=3)
    grad = np.abs(grad_x) + np.abs(grad_y)
    img_f32 = image.astype(np.float32)
    result = img_f32 + grad
    return np.clip(result, 0, 255).astype(np.uint8)
