"""实验四：边缘检测"""

import numpy as np
import cv2
from .registry import register


@register("边缘检测", "Canny边缘检测")
def canny_edge(image: np.ndarray, threshold1: int = 50, threshold2: int = 150) -> np.ndarray:
    """Canny 边缘检测"""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    edges = cv2.Canny(gray, threshold1, threshold2)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)


@register("边缘检测", "Sobel边缘检测")
def sobel_edge(image: np.ndarray, ksize: int = 3) -> np.ndarray:
    """Sobel 边缘检测"""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=ksize)
    grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=ksize)
    grad = cv2.magnitude(grad_x, grad_y)
    grad = np.clip(grad, 0, 255).astype(np.uint8)
    return cv2.cvtColor(grad, cv2.COLOR_GRAY2BGR)


@register("边缘检测", "Prewitt边缘检测")
def prewitt_edge(image: np.ndarray) -> np.ndarray:
    """Prewitt 边缘检测"""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
    kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)
    grad_x = cv2.filter2D(gray, cv2.CV_32F, kernel_x)
    grad_y = cv2.filter2D(gray, cv2.CV_32F, kernel_y)
    grad = cv2.magnitude(grad_x, grad_y)
    grad = np.clip(grad, 0, 255).astype(np.uint8)
    return cv2.cvtColor(grad, cv2.COLOR_GRAY2BGR)


@register("边缘检测", "Roberts边缘检测")
def roberts_edge(image: np.ndarray) -> np.ndarray:
    """Roberts 边缘检测（2x2 交叉算子）"""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    kernel_x = np.array([[1, 0], [0, -1]], dtype=np.float32)
    kernel_y = np.array([[0, 1], [-1, 0]], dtype=np.float32)
    grad_x = cv2.filter2D(gray, cv2.CV_32F, kernel_x)
    grad_y = cv2.filter2D(gray, cv2.CV_32F, kernel_y)
    grad = cv2.magnitude(grad_x, grad_y)
    grad = np.clip(grad, 0, 255).astype(np.uint8)
    return cv2.cvtColor(grad, cv2.COLOR_GRAY2BGR)
