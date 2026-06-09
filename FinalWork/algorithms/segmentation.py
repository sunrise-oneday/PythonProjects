"""实验六：图像分割"""

import numpy as np
import cv2
from .registry import register


@register("图像分割", "Otsu大津法阈值分割")
def threshold_otsu(image: np.ndarray) -> np.ndarray:
    """大津法自动阈值分割"""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)


@register("图像分割", "自适应阈值分割")
def adaptive_threshold(image: np.ndarray, block_size: int = 11, c: int = 2) -> np.ndarray:
    """自适应阈值分割"""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, block_size, c)
    return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)


@register("图像分割", "区域生长")
def region_growing(image: np.ndarray, seed_x: int = 100, seed_y: int = 100, threshold: int = 10) -> np.ndarray:
    """简易区域生长分割（基于灰度差）"""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    h, w = gray.shape
    seed = (min(seed_y, h - 1), min(seed_x, w - 1))
    seed_val = int(gray[seed])
    visited = np.zeros((h, w), np.uint8)
    output = np.zeros((h, w), np.uint8)

    stack = [seed]
    visited[seed] = 1

    while stack:
        y, x = stack.pop()
        output[y, x] = 255
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                if abs(int(gray[ny, nx]) - seed_val) <= threshold:
                    visited[ny, nx] = 1
                    stack.append((ny, nx))

    return cv2.cvtColor(output, cv2.COLOR_GRAY2BGR)
