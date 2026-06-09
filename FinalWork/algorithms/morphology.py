"""实验五：形态学处理"""

import numpy as np
import cv2
from .registry import register


def _get_kernel(kernel_size: int, shape: str = "rect") -> np.ndarray:
    """生成结构元"""
    if shape == "ellipse":
        return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    elif shape == "cross":
        return cv2.getStructuringElement(cv2.MORPH_CROSS, (kernel_size, kernel_size))
    else:
        return cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))


@register("形态学处理", "腐蚀")
def erode(image: np.ndarray, kernel_size: int = 3, iterations: int = 1) -> np.ndarray:
    """腐蚀操作"""
    kernel = _get_kernel(kernel_size)
    return cv2.erode(image, kernel, iterations=iterations)


@register("形态学处理", "膨胀")
def dilate(image: np.ndarray, kernel_size: int = 3, iterations: int = 1) -> np.ndarray:
    """膨胀操作"""
    kernel = _get_kernel(kernel_size)
    return cv2.dilate(image, kernel, iterations=iterations)


@register("形态学处理", "开运算")
def opening(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """开运算（先腐蚀后膨胀，去噪点）"""
    kernel = _get_kernel(kernel_size)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


@register("形态学处理", "闭运算")
def closing(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """闭运算（先膨胀后腐蚀，填补空洞）"""
    kernel = _get_kernel(kernel_size)
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
