# 数字图像处理系统 — UI 表现层设计

> 日期：2026-06-09
> 项目：FinalWork/ImageProcessingSystem
> 关联：主架构规范见 `2026-06-09-image-processing-system-design.md`

---

## 设计目标

打造产品级的优雅 UI，9 个 Tab 视觉高度统一、交互丝滑、具备现代 Web 应用的精致感（圆角、阴影、呼吸感间距）。

通过**自定义主题（Theme）**、**全局 CSS 注入**以及**标准化布局生成器**三大基石实现。

---

## 一、核心主题配置 — `utils/theme.py`

Gradio 4.x 支持深度定制主题。定义名为 **Soft-Blue** 的专业配色方案，替代默认的单调灰色。

```python
# utils/theme.py
import gradio as gr

def get_custom_theme():
    """
    定制 Soft-Blue 主题，专业现代外观。
    主色软蓝，辅色石板灰。
    """
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
    ).set(
        # 全局背景
        body_background_fill="#f8fafc",
        body_background_fill_dark="#0f172a",

        # 卡片容器
        block_background_fill="white",
        block_border_width="0px",
        block_shadow="0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
        block_radius="12px",

        # 按钮
        button_primary_background_fill="#2563eb",
        button_primary_text_color="white",
        button_primary_background_fill_hover="#1d4ed8",
        button_primary_border_color="#2563eb",

        # 输入框
        input_background_fill="#f1f5f9",
        input_border_color="#cbd5e1",
        input_border_width="1px",
        input_radius="8px",
    )
    return theme
```

| 维度 | 取值 |
|------|------|
| 主色调 | `primary_hue="blue"` → `#2563eb` |
| 次色调 | `secondary_hue="slate"`, `neutral_hue="slate"` |
| 字体 | Inter（Google Font）+ fallback 系统无衬线 |
| 背景 | `body_background_fill="#f8fafc"` |
| 卡片 | 白底、无边框、`12px` 圆角、微阴影 |
| 按钮 | 蓝色填充、hover 加深（`#1d4ed8`） |
| 输入框 | `#f1f5f9` 浅灰底、`8px` 圆角、Slate 边框 |

---

## 二、全局 CSS 注入 — `assets/style.css`

处理 Gradio 主题无法覆盖的细节：容器最大宽度、图片圆角阴影、Tab 导航栏美化、按钮动效。

```css
/* assets/style.css */

/* 1. 居中限制最大宽度，大屏上内容不被过度拉伸 */
.gradio-container {
    max-width: 1280px !important;
    margin: auto !important;
    padding: 2rem !important;
}

/* 2. 图片容器：圆角阴影，hover 时阴影加深 */
.image-wrapper {
    border-radius: 16px !important;
    overflow: hidden !important;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08),
                0 4px 6px -2px rgba(0, 0, 0, 0.04) !important;
    border: 1px solid #e2e8f0 !important;
    transition: box-shadow 0.3s ease !important;
}
.image-wrapper:hover {
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
                0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
}

/* 3. 主按钮：hover 上浮 + 阴影加深 */
.primary-btn {
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-weight: 600 !important;
    letter-spacing: 0.025em !important;
    box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2) !important;
}
.primary-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3) !important;
}

/* 4. Tab 导航栏：简约风格，选中项蓝色下划线 */
.tabs > .tab-nav > button {
    border: none !important;
    font-weight: 500 !important;
    color: #64748b !important;
    transition: all 0.2s !important;
    padding: 12px 20px !important;
}
.tabs > .tab-nav > button.selected {
    color: #2563eb !important;
    border-bottom: 2px solid #2563eb !important;
    background: transparent !important;
    font-weight: 600 !important;
}
.tabs > .tab-nav > button:hover {
    color: #1e293b !important;
}

/* 5. 滑块主题色 */
input[type="range"] {
    accent-color: #2563eb !important;
}
```

> **注意**：Tab 导航栏的 CSS 选择器 `.tabs > .tab-nav > button` 在 Gradio 不同版本中 DOM 结构可能有差异。实现阶段先用浏览器检查元素确认，必要时改用 `elem_classes` + 自定义类名。

---

## 三、标准化布局生成器 — `utils/layout_helper.py`

保证所有 Tab 采用相同结构，用户切换 Tab 时无"跳跃感"。

```python
# utils/layout_helper.py
import gradio as gr

def create_standard_layout(tab_title: str, algo_choices: list):
    """
    生成标准化的优雅布局。
    返回组件字典，供 tab 文件绑定事件。
    """
    with gr.Row(equal_height=True):
        # 左栏：输入与参数
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
                params_container = gr.Column()  # 动态控件容器

            with gr.Row():
                auto_preview = gr.Checkbox(
                    label="🔄 自动预览 (拖动滑块即时生效)",
                    value=True,
                    container=False,
                )
                process_btn = gr.Button(
                    "▶ 执行处理",
                    variant="primary",
                    elem_classes="primary-btn",
                )

        # 右栏：处理结果
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
        "params_container": params_container,
        "auto_preview": auto_preview,
        "process_btn": process_btn,
    }
```

### 布局结构示意

```
┌─────────────────────────────────────────────┐
│  ← 左栏（scale=1）    │  右栏（scale=1） →   │
│  📥 输入与参数         │  📤 处理结果          │
│  [图片上传·image-wrapper]│  [结果展示·image-wrapper]│
│  ⚙️ 算法参数设置        │                      │
│    ┌─ Accordion ──┐   │                      │
│    │ 算法下拉框     │   │                      │
│    │ 自动生成控件区  │   │                      │
│    └───────────────┘   │                      │
│  🔄 自动预览  [▶执行]  │                      │
└─────────────────────────────────────────────┘
```

| 特性 | 说明 |
|------|------|
| 分栏比例 | `scale=1:1` 等宽 |
| 最小宽度 | `min_width=450` 防止过窄 |
| 参数收纳 | `Accordion` 折叠，避免满屏滑块视觉混乱 |
| CSS 类 | 自动应用 `image-wrapper` 和 `primary-btn` |

---

## 四、在 app.py 中启用

```python
import gradio as gr
from utils.theme import get_custom_theme
# ... 导入各 Tab

css_path = "assets/style.css"

with gr.Blocks(
    title="数字图像处理实验系统",
    theme=get_custom_theme(),
    css=css_path,
    analytics_enabled=False,
) as demo:
    gr.Markdown(
        """
        # 🖼️ 数字图像处理实验系统
        ### 基于 OpenCV 与 Gradio 构建的现代化图像处理工作台
        """
    )
    # ... 注册各 Tab
```

---

## 五、设计要点总结

1. **视觉呼吸感**：`max-width: 1280px` 避免大屏过度拉伸
2. **一致性**：`layout_helper.py` 强制所有 Tab 相同结构，切换无跳跃感
3. **交互反馈**：按钮 hover 上浮、图片容器 hover 阴影加深，提供桌面级质感
4. **参数收纳**：`Accordion` 折叠参数面板，默认展开但可收拢，避免满屏滑块
