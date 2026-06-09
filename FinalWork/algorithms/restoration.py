"""实验八：图像复原（噪声建模与去噪）"""

import numpy as np
import cv2
from .registry import register


@register("图像复原", "高斯噪声")
def gaussian_noise(image: np.ndarray, mean: float = 0.0, sigma: float = 25.0) -> np.ndarray:
    """添加高斯噪声"""
    noise = np.random.normal(mean, sigma, image.shape).astype(np.float32)
    result = image.astype(np.float32) + noise
    return np.clip(result, 0, 255).astype(np.uint8)


@register("图像复原", "椒盐噪声")
def salt_pepper_noise(image: np.ndarray, prob: float = 0.02) -> np.ndarray:
    """添加椒盐噪声"""
    result = image.copy()
    # 椒噪声（黑）
    salt_mask = np.random.random(result.shape[:2]) < prob / 2
    if len(result.shape) == 3:
        result[salt_mask] = [0, 0, 0]
    else:
        result[salt_mask] = 0
    # 盐噪声（白）
    pepper_mask = np.random.random(result.shape[:2]) < prob / 2
    if len(result.shape) == 3:
        result[pepper_mask] = [255, 255, 255]
    else:
        result[pepper_mask] = 255
    return result


@register("图像复原", "非局部均值去噪")
def nlm_denoise(image: np.ndarray, h: float = 10.0) -> np.ndarray:
    """非局部均值去噪（对高斯噪声效果好）"""
    return cv2.fastNlMeansDenoisingColored(image, None, h, h, 7, 21)


@register("图像复原", "双边滤波")
def bilateral_filter(image: np.ndarray, d: int = 9, sigma_color: float = 75.0,
                     sigma_space: float = 75.0) -> np.ndarray:
    """双边滤波（保边去噪）"""
    return cv2.bilateralFilter(image, d, sigma_color, sigma_space)
