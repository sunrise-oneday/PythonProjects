"""附加：抠图（GrabCut + rembg 双模式）"""

import numpy as np
import cv2
from .registry import register


@register("抠图", "GrabCut交互式抠图")
def grabcut_matting(image: np.ndarray, rect_x: int = 10, rect_y: int = 10,
                    rect_w: int = 100, rect_h: int = 100, iterations: int = 5) -> np.ndarray:
    """GrabCut 交互式抠图

    Args:
        image: BGR uint8
        rect_x, rect_y, rect_w, rect_h: 初始矩形框
        iterations: 迭代次数

    Returns:
        BGRA uint8，背景透明（A=0）
    """
    mask = np.zeros(image.shape[:2], np.uint8)
    bg_model = np.zeros((1, 65), np.float64)
    fg_model = np.zeros((1, 65), np.float64)

    rect = (rect_x, rect_y, rect_w, rect_h)

    cv2.grabCut(image, mask, rect, bg_model, fg_model, iterations, cv2.GC_INIT_WITH_RECT)

    # 前景保留，背景设为透明
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype(np.uint8)
    # 转为 BGRA
    bgra = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = mask2 * 255
    return bgra


@register("抠图", "rembg自动抠图")
def rembg_matting(image: np.ndarray) -> np.ndarray:
    """基于 U²-Net 的一键自动抠图

    pip install rembg 后可用，首次运行自动下载模型(~200MB)。

    Args:
        image: BGR uint8

    Returns:
        BGRA uint8，背景透明（A=0）
    """
    try:
        from rembg import remove

        # rembg 需要 RGB 输入
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result_rgba = remove(img_rgb)
        # 转回 BGRA 遵从 OpenCV 惯例
        return cv2.cvtColor(result_rgba, cv2.COLOR_RGBA2BGRA)
    except BaseException:
        # rembg 未安装或缺少 onnxruntime 时，在图片上叠提示文字
        overlay = image.copy()
        h, w = overlay.shape[:2]
        text = "rembg 不可用，请运行: pip install rembg[cpu]"
        font_scale = max(0.5, min(min(w, h) / 600.0, 2.0))
        thickness = max(1, int(font_scale * 2))
        (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
        x, y = (w - tw) // 2, h // 2
        cv2.rectangle(overlay, (x - 10, y - th - 10), (x + tw + 10, y + 10), (0, 0, 0), -1)
        cv2.putText(overlay, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
        bgra = cv2.cvtColor(overlay, cv2.COLOR_BGR2BGRA)
        bgra[:, :, 3] = 255
        return bgra
