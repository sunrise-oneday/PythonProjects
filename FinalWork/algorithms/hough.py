"""实验七：Hough 变换"""

import numpy as np
import cv2
from .registry import register


def _get_edge(image):
    """转灰度 + Canny 边缘检测"""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    return cv2.Canny(gray, 50, 150)


@register("Hough变换", "Hough直线检测")
def hough_lines(image: np.ndarray, threshold: int = 100) -> np.ndarray:
    """标准 Hough 直线检测，在原图上绘制结果"""
    edges = _get_edge(image)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold)

    result = image.copy()
    if lines is not None:
        for rho, theta in lines[:, 0]:
            a, b = np.cos(theta), np.sin(theta)
            x0, y0 = a * rho, b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * a))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * a))
            cv2.line(result, pt1, pt2, (0, 0, 255), 2)
    return result


@register("Hough变换", "Hough圆检测")
def hough_circles(image: np.ndarray, min_dist: int = 50, param1: int = 100, param2: int = 30,
                   min_radius: int = 10, max_radius: int = 100) -> np.ndarray:
    """Hough 梯度法圆检测"""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    gray_blur = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(gray_blur, cv2.HOUGH_GRADIENT, 1, min_dist,
                               param1=param1, param2=param2,
                               minRadius=min_radius, maxRadius=max_radius)

    result = image.copy()
    if circles is not None:
        circles = np.round(circles[0]).astype(int)
        for x, y, r in circles:
            cv2.circle(result, (x, y), r, (0, 255, 0), 2)
            cv2.circle(result, (x, y), 2, (0, 0, 255), 3)
    return result
