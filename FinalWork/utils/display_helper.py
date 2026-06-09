"""图像对比展示工具"""

import numpy as np
import cv2


def side_by_side(
    original: np.ndarray,
    processed: np.ndarray,
    titles: tuple = ("原图", "处理后"),
) -> np.ndarray:
    """将原图和结果水平拼接，方便对比

    Args:
        original: 原图 (H, W, C)
        processed: 处理后图片 (H, W, C)
        titles: 标签文字

    Returns:
        水平拼接后的图像
    """
    if original is None or processed is None:
        return processed if processed is not None else original

    # 统一高度
    h = max(original.shape[0], processed.shape[0])

    def _resize(img, height):
        scale = height / img.shape[0]
        new_w = int(img.shape[1] * scale)
        return cv2.resize(img, (new_w, height), interpolation=cv2.INTER_AREA)

    left = _resize(original, h)
    right = _resize(processed, h)

    return np.hstack([left, right])


def overlay_mask(image: np.ndarray, mask: np.ndarray, color: tuple = (0, 255, 0), alpha: float = 0.3):
    """将二值 mask 半透明叠加到原图上

    Args:
        image: BGR 原图
        mask: 单通道二值 mask (0/255)
        color: 叠加颜色 BGR
        alpha: 透明度

    Returns:
        叠加后的图像
    """
    overlay = image.copy()
    colored = np.zeros_like(image)
    colored[:] = color
    overlay = np.where(mask[:, :, np.newaxis] > 0, colored, overlay)
    return cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
