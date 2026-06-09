"""Tab 构建工具：动态参数生成 + 通用处理函数"""

import inspect
import gradio as gr
from algorithms import ALGORITHMS
from utils.io_helper import to_opencv, to_gradio
from utils.control_meta import get_kwargs_defaults


def get_param_configs(algo_func):
    """获取算法函数的参数配置列表（排除 image）"""
    configs = []
    sig = inspect.signature(algo_func)
    for name, param in sig.parameters.items():
        if name == "image":
            continue
        annotation = param.annotation
        default = param.default
        if default is inspect.Parameter.empty:
            default = None
        cfg = get_kwargs_defaults(algo_func.__name__, name, annotation, default)
        cfg["name"] = name
        cfg["annotation"] = annotation
        configs.append(cfg)
    return configs


def build_tab(tab_key: str):
    """一站式构建 Tab：布局 + 动态参数面板 + 事件绑定"""
    from utils.layout_helper import create_standard_layout

    algo_choices = list(ALGORITHMS.get(tab_key, {}).keys())

    # 预先计算第一个算法的参数配置，用于初始滑块显示
    first_params = None
    if algo_choices:
        first_func = ALGORITHMS[tab_key][algo_choices[0]]
        first_params = get_param_configs(first_func)

    comp = create_standard_layout(tab_key, algo_choices, first_params)
    _safe_name = tab_key.replace(' ', '_').replace('-', '_')

    # ---- 更新参数滑块（算法切换时） ----
    def update_param_slots(algo_name):
        if algo_name is None or algo_name not in ALGORITHMS.get(tab_key, {}):
            return tuple(gr.update(visible=False) for _ in range(8))

        func = ALGORITHMS[tab_key][algo_name]
        configs = get_param_configs(func)
        num = len(configs)
        updates = []
        for i in range(8):
            if i < num:
                c = configs[i]
                updates.append(gr.update(
                    visible=True,
                    label=c.get("label", c["name"]),
                    minimum=c.get("minimum", 0),
                    maximum=c.get("maximum", 255),
                    step=c.get("step", 1),
                    value=c.get("value", None),
                ))
            else:
                updates.append(gr.update(visible=False))
        return tuple(updates)

    update_param_slots.__name__ = f"update_slots_{_safe_name}"
    update_param_slots.__qualname__ = f"UpdateSlots.{_safe_name}"

    # ---- 图像处理函数 ----
    def _process(img, algo_name, *slot_values):
        if img is None or algo_name is None:
            return None

        func = ALGORITHMS[tab_key][algo_name]
        configs = get_param_configs(func)

        args = []
        for i, c in enumerate(configs):
            val = slot_values[i] if i < len(slot_values) and slot_values[i] is not None else c.get("value", None)
            if c["annotation"] is int and val is not None:
                args.append(int(val))
            elif c["annotation"] is float and val is not None:
                args.append(float(val))
            else:
                args.append(val)

        try:
            bgr = to_opencv(img)
            result = func(bgr, *args)
            return to_gradio(result)
        except Exception as e:
            print(f"Error in {tab_key}/{algo_name}: {e}")
            return img

    _process.__name__ = f"process_{_safe_name}"
    _process.__qualname__ = f"ProcessTab.{_safe_name}"

    # ---- 事件绑定 ----
    inputs = [comp["img_input"], comp["algo_selector"]] + comp["param_slots"]
    outputs = [comp["img_output"]]

    # 切换算法 → 更新滑块（仅此而已，不触发处理）
    comp["algo_selector"].change(
        fn=update_param_slots,
        inputs=[comp["algo_selector"]],
        outputs=comp["param_slots"],
        api_name=f"update_slots_{_safe_name}",
    )

    # 点击按钮 → 执行处理
    comp["process_btn"].click(
        fn=_process,
        inputs=inputs,
        outputs=outputs,
        api_name=f"process_{_safe_name}",
    )

    # 上传图片 → 自动处理
    comp["img_input"].change(
        fn=_process,
        inputs=inputs,
        outputs=outputs,
        queue=False,
    )

    return comp, _process
