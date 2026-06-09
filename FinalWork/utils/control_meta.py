"""参数元数据覆盖 —— 处理特殊算法参数的范围、步长、选项"""

PARAM_OVERRIDES = {
    # === 空间滤波 ===
    "mean_filter": {
        "kernel_size": {"minimum": 1, "maximum": 31, "step": 2, "label": "核大小 (奇数)"},
    },
    "gaussian_blur": {
        "sigma": {"minimum": 0.1, "maximum": 10.0, "step": 0.1},
    },
    "median_filter": {
        "kernel_size": {"minimum": 1, "maximum": 31, "step": 2, "label": "核大小 (奇数)"},
    },
    # === 边缘检测 ===
    "canny_edge": {
        "threshold1": {"minimum": 0, "maximum": 255, "label": "低阈值"},
        "threshold2": {"minimum": 0, "maximum": 255, "label": "高阈值"},
    },
    # === 形态学 ===
    "erode": {
        "kernel_size": {"minimum": 1, "maximum": 31, "step": 2, "label": "结构元大小"},
    },
    "dilate": {
        "kernel_size": {"minimum": 1, "maximum": 31, "step": 2, "label": "结构元大小"},
    },
    # === Hough ===
    "hough_lines": {
        "threshold": {"minimum": 1, "maximum": 300, "step": 1, "label": "累加器阈值"},
    },
    "hough_circles": {
        "min_dist": {"minimum": 1, "maximum": 100, "step": 1, "label": "圆心最小距离"},
    },
    # === 抠图 ===
    "grabcut_matting": {
        "rect_x": {"minimum": 0, "maximum": 500, "step": 1, "label": "矩形框左上角 X"},
        "rect_y": {"minimum": 0, "maximum": 500, "step": 1, "label": "矩形框左上角 Y"},
        "rect_w": {"minimum": 1, "maximum": 800, "step": 1, "label": "矩形框宽度"},
        "rect_h": {"minimum": 1, "maximum": 800, "step": 1, "label": "矩形框高度"},
        "iterations": {"minimum": 1, "maximum": 20, "step": 1, "label": "迭代次数"},
    },
}


def get_kwargs_defaults(func_name: str, param_name: str, param_type, param_default):
    """获取参数控件的配置（优先读取覆盖，否则使用默认规则）

    Args:
        func_name: 函数名（用于查 PARAM_OVERRIDES）
        param_name: 参数名
        param_type: 类型注解（int/float/bool/str）
        param_default: 默认值

    Returns:
        dict: 传给 Gradio 控件的参数字典
    """
    override = PARAM_OVERRIDES.get(func_name, {}).get(param_name, {})

    if override:
        return {
            "minimum": override.get("minimum", 0),
            "maximum": override.get("maximum", 255),
            "step": override.get("step", 1),
            "label": override.get("label", param_name),
            "value": param_default,
        }

    # 默认规则
    if param_type is bool:
        return {"label": param_name, "value": bool(param_default) if param_default is not None else False}
    elif param_type is int:
        return {"minimum": 0, "maximum": 255, "step": 1, "label": param_name, "value": param_default}
    elif param_type is float:
        return {"minimum": 0.0, "maximum": 1.0, "step": 0.01, "label": param_name, "value": param_default}

    return {"label": param_name, "value": param_default}
