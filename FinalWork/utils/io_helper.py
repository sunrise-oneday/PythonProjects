"""RGB ↔ BGR 格式转换工具（兼容 3/4 通道）"""

import numpy as np
import cv2


def to_opencv(img: np.ndarray) -> np.ndarray:
    """Gradio RGB → OpenCV BGR（兼容 RGBA → BGRA）

    Args:
        img: Gradio 传入的 numpy 数组，RGB 或 RGBA

    Returns:
        BGR 或 BGRA 格式，uint8
    """
    if len(img.shape) == 3:
        if img.shape[2] == 4:
            return cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)
        elif img.shape[2] == 3:
            return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


def to_gradio(img: np.ndarray) -> np.ndarray:
    """OpenCV BGR → Gradio RGB（兼容 BGRA → RGBA）

    Args:
        img: OpenCV 格式的 numpy 数组，BGR 或 BGRA

    Returns:
        RGB 或 RGBA 格式，uint8
    """
    if len(img.shape) == 3:
        if img.shape[2] == 4:
            return cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
        elif img.shape[2] == 3:
            return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img
