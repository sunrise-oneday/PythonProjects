"""标准化的优雅布局 —— 保证 9 个 Tab 视觉统一"""

import gradio as gr


def create_standard_layout(tab_title: str, algo_choices: list, first_params=None):
    """生成标准化的优雅布局

    Args:
        tab_title: Tab 标题
        algo_choices: 算法名称列表
        first_params: 第一个算法的参数配置列表，用于初始显示滑块

    Returns:
        dict: 组件字典
    """
    with gr.Row(equal_height=True):
        with gr.Column(scale=1, min_width=450):
            gr.Markdown(f"### 📥 {tab_title} · 输入与参数")

            img_input = gr.Image(
                label="上传原图",
                type="numpy",
                elem_classes="image-wrapper",
                height=400,
            )

            with gr.Accordion("⚙️ 算法参数设置", open=True):
                algo_selector = gr.Dropdown(
                    choices=algo_choices,
                    label="选择算法",
                    value=algo_choices[0] if algo_choices else None,
                    interactive=True,
                )
                # 参数滑块：根据 first_params 决定初始显示哪些
                param_slots = []
                if first_params:
                    for i in range(8):
                        if i < len(first_params):
                            c = first_params[i]
                            s = gr.Slider(
                                minimum=c.get("minimum", 0),
                                maximum=c.get("maximum", 255),
                                step=c.get("step", 1),
                                label=c.get("label", c.get("name", f"参数{i+1}")),
                                value=c.get("value", None),
                                visible=True,
                                interactive=True,
                            )
                        else:
                            s = gr.Slider(
                                minimum=0, maximum=255, step=1,
                                label=f"参数{i+1}",
                                visible=False,
                                interactive=True,
                            )
                        param_slots.append(s)
                else:
                    for i in range(8):
                        s = gr.Slider(
                            minimum=0, maximum=255, step=1,
                            label=f"参数{i+1}",
                            visible=False,
                            interactive=True,
                        )
                        param_slots.append(s)

            with gr.Row():
                auto_preview = gr.Checkbox(
                    label="自动预览 (拖动滑块即时生效)",
                    value=True,
                    container=False,
                )
                process_btn = gr.Button(
                    "执行处理",
                    variant="primary",
                    elem_classes="primary-btn",
                )

        with gr.Column(scale=1, min_width=450):
            gr.Markdown(f"### 📤 {tab_title} · 处理结果")
            img_output = gr.Image(
                label="处理结果",
                type="numpy",
                elem_classes="image-wrapper",
                height=400,
                interactive=False,
            )

    return {
        "img_input": img_input,
        "img_output": img_output,
        "algo_selector": algo_selector,
        "param_slots": param_slots,
        "auto_preview": auto_preview,
        "process_btn": process_btn,
    }
