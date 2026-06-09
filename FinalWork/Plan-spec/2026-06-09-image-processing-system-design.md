# 数字图像处理系统 — 架构设计规范

> 日期：2026-06-09
> 项目：FinalWork/ImageProcessingSystem

---

## 一、技术选型

| 维度 | 选择 | 理由 |
|------|------|------|
| 框架 | **Gradio** | 对 OpenCV numpy 原生支持，代码量约为 PyQt 的 1/5，天然支持滑块联动与自动刷新 |
| 核心库 | OpenCV + NumPy | 标准的图像处理栈 |
| 可视化 | Matplotlib | 直方图、频域谱等辅助展示 |
| 抠图 | OpenCV GrabCut + rembg | 双模式：交互式手动 + 深度学习自动 |

---

## 二、目录结构

```
FinalWork/
├── app.py                      # 入口，组装 Gradio 应用
├── requirements.txt            # 依赖清单
│
├── algorithms/                 # 算法层（纯函数，无 UI 依赖）
│   ├── __init__.py
│   ├── registry.py             # @register 装饰器 + 全局 ALGORITHMS 字典
│   ├── grayscale.py            # 灰度变换 + 直方图
│   ├── filtering.py            # 空间滤波（平滑/锐化）
│   ├── frequency.py            # 频率域滤波
│   ├── edge_detection.py       # 边缘检测
│   ├── morphology.py           # 形态学处理
│   ├── segmentation.py         # 图像分割
│   ├── hough.py                # Hough 变换
│   ├── restoration.py          # 图像复原
│   └── matting.py              # 抠图（GrabCut + rembg）
│
├── tabs/                       # UI 层（每个 Tab 一个独立文件）
│   ├── __init__.py
│   ├── tab_grayscale.py
│   ├── tab_filtering.py
│   ├── tab_frequency.py
│   ├── tab_edge.py
│   ├── tab_morphology.py
│   ├── tab_segmentation.py
│   ├── tab_hough.py
│   ├── tab_restoration.py
│   └── tab_matting.py
│
├── assets/
│   └── style.css              # 全局 CSS：阴影、圆角、Tab 导航、按钮动效
│
└── utils/                      # 工具层
    ├── __init__.py
    ├── io_helper.py            # RGB ↔ BGR 转换（兼容 3/4 通道）
    ├── theme.py                # Soft-Blue 自定义 Gradio 主题
    ├── layout_helper.py        # 标准化布局生成器（保证 9 个 Tab 视觉统一）
    ├── control_meta.py         # 参数元数据覆盖（PARAM_OVERRIDES）
    └── display_helper.py       # 原图 vs 结果对比展示
```

---

## 三、算法层（algorithms/）契约

### 3.1 统一函数签名

```python
def algorithm_name(image: np.ndarray, param1: type, param2: type = default) -> np.ndarray:
```

- **输入**：`uint8`，BGR（3通道）或灰度（单通道）
- **输出**：与输入同格式同尺寸，`uint8`
- **例外**：抠图算法允许返回 BGRA（4通道），由工具层统一兼容
- **纯函数原则**：不读写文件、不弹窗、不 print

### 3.2 内部精度控制

```
uint8 输入 → 转为 float32 [0,1] → 高精度计算 → clip[0,1] → 转回 uint8
```

### 3.3 装饰器注册模式（registry.py）

```python
ALGORITHMS = {}

def register(tab_name: str, algo_name: str):
    def decorator(func):
        if tab_name not in ALGORITHMS:
            ALGORITHMS[tab_name] = {}
        ALGORITHMS[tab_name][algo_name] = func
        return func
    return decorator
```

用法：在算法函数上标注 `@register("灰度变换", "线性变换")` 即可自动注册。

---

## 四、UI 层（tabs/）设计

### 4.1 全局布局

```
Gradio App
├── 标题 + 说明
├── Tab 1: 灰度变换
├── Tab 2: 空间滤波
├── Tab 3: 频率域滤波
├── Tab 4: 边缘检测
├── Tab 5: 形态学处理
├── Tab 6: 图像分割
├── Tab 7: Hough 变换
├── Tab 8: 图像复原
└── Tab 9: 抠图
```

### 4.2 每个 Tab 的通用结构

```
┌─────────────────────────────────────┐
│  左：输入图像       右：处理结果      │
│  [上传/拖拽]        [显示区]         │
│                                     │
│  算法选择：[下拉框]                  │
│  参数区：[自动生成控件]              │
│                                     │
│  ☐ 自动预览  [▶ 执行处理]           │
└─────────────────────────────────────┘
```

### 4.3 控件自动生成 + 元数据覆盖

利用 `inspect` 读取算法函数显式参数的类型注解自动生成 Gradio 控件：

| 类型 | 默认控件 | 说明 |
|------|---------|------|
| `int` | `gr.Slider(0, 255, step=1)` | 整数滑块 |
| `float` | `gr.Slider(0.0, 1.0, step=0.01)` | 浮点滑块 |
| `bool` | `gr.Checkbox` | 复选框 |
| `str` | `gr.Dropdown` | 需从元数据提供 choices |

**参数覆盖机制（control_meta.py）**：

```python
PARAM_OVERRIDES = {
    "mean_filter": {
        "kernel_size": {"minimum": 1, "maximum": 31, "step": 2, "label": "核大小 (奇数)"}
    },
    "gaussian_blur": {
        "sigma": {"minimum": 0.1, "maximum": 10.0, "step": 0.1}
    },
}
```

优先读取覆盖配置，未配置的走默认规则。

### 4.4 实时预览与性能

- 增加 **"自动预览 (Auto Preview)"** Checkbox
- 勾选时：轻量级操作绑定滑块 `change` 事件，实时刷新
- 取消勾选时：必须点击"执行处理"按钮，确保复杂算法不卡死

---

## 五、颜色通道契约（io_helper.py）

### 数据流

```
Gradio (RGB) → to_opencv() → 算法层 (BGR) → to_gradio() → Gradio (RGB)
```

### 兼容通道数

```python
def to_opencv(img):
    if 4通道: RGB?A → BGRA
    if 3通道: RGB  → BGR
    if 灰度: 不变

def to_gradio(img):
    if 4通道: BGRA → RGBA
    if 3通道: BGR  → RGB
    if 灰度: 不变
```

---

## 六、抠图模块（matting.py）详细设计

### 6.1 GrabCut 交互式抠图

- 用户上传图片后用鼠标框选目标区域
- OpenCV 内置 `cv2.grabCut()`，无需额外模型
- 提供矩形框绘制工具（`gr.Image` 的 `tool="sketch"` 模式）

### 6.2 rembg 自动抠图

- 基于 U²-Net 深度学习模型，全自动
- `pip install rembg` 即用，首次运行时自动下载模型（~200MB）
- **关键陷阱已处理**：
  - 输入：BGR → 转为 RGB 再传给 rembg（否则模型色盲）
  - 输出：rembg 返回 RGBA → 转为 BGRA 返回

---

## 七、入口文件（app.py）

```python
import gradio as gr
from utils.theme import get_custom_theme
from tabs.tab_grayscale import create_tab as create_grayscale
from tabs.tab_filtering import create_tab as create_filtering
# ... 导入所有 Tab

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
    create_grayscale()
    create_filtering()
    # ... 注册所有 Tab

if __name__ == "__main__":
    demo.launch()
```

预计不超过 30 行。

---

> **UI 表现层设计（主题、CSS、布局生成器）已拆分到独立文档：**
> [`2026-06-09-image-processing-system-ui-design.md`](./2026-06-09-image-processing-system-ui-design.md)

---

## 八、依赖清单（requirements.txt）

```
opencv-python>=4.8.0
numpy>=1.24.0
gradio>=4.0.0
matplotlib>=3.7.0
rembg>=0.1.0
onnxruntime>=1.15.0
Pillow>=10.0.0
scipy>=1.10.0
```

> 除 `rembg` 外的依赖通过 `pip install rembg` 自动拉取。`rembg` 在模块内采用延迟导入（函数内 `import`），防止未安装时影响其他 Tab。

---

## 九、实施路线图

### Phase 1：骨架搭建（预计 0.5 天）

1. 创建完整目录结构
2. 实现 `registry.py`、`io_helper.py`、`control_meta.py`
3. 实现第一个 Tab（灰度变换）验证全链路通
4. app.py 启动可访问

### Phase 2：算法填充（预计 1-2 天）

按顺序实现并逐个验证：
1. 空间滤波 → 边缘检测 → 形态学
2. 频率域滤波 → 图像分割 → Hough 变换 → 图像复原
3. 每个算法实现后立即对应 Tab 验证

### Phase 3：抠图 + 收尾（预计 0.5 天）

1. GrabCut + rembg 双模式 Tab
2. display_helper 对比展示
3. 全局联调
4. README 文档

### 开发原则

- 写一个算法，测一个 Tab，不积攒未验证的代码
- 算法层严格纯函数，不耦合任何 UI/IO
- 参数特殊范围优先加 `control_meta.py`，不破坏通用规则
- 每个 Tab 验证通过后做一次 git commit

---

## 十、架构总览图

```
┌──────────────────────────────────────────────────────────┐
│                   app.py                                 │
│    theme=get_custom_theme() + css="assets/style.css"     │
│                gr.Blocks() 组装                          │
├──────────┬──────────┬──────────┬──────────┬──────────────┤
│ Tab 1    │ Tab 2    │ Tab 3    │  ...     │ Tab 9        │
│ 灰度变换  │ 空间滤波  │ 频率域    │          │ 抠图          │
├──────────┴──────────┴──────────┴──────────┴──────────────┤
│                    utils/ 工具层                          │
│  io_helper(RGB/BGR转换)  control_meta(参数覆盖)          │
│  theme.py(Soft-Blue主题)  layout_helper(标准化布局)      │
│  display_helper(对比展示)                                 │
├──────────────────────────────────────────────────────────┤
│                  algorithms/ 算法层                        │
│  纯函数 · uint8进出 · float32内部 · @register注册          │
└──────────────────────────────────────────────────────────┘
```

---

## 十一、设计决策记录

| # | 决策 | 备选 | 结论理由 |
|---|------|------|----------|
| 1 | Gradio 而非 PyQt | PyQt/Tkinter | 代码量 1/5，天然滑块联动 |
| 2 | 每个 Tab 独立文件 | 单文件统一 | 避免文件超千行，解耦 |
| 3 | 装饰器注册而非手写字典 | 手动维护 ALGORITHMS | 新增算法无需改其他地方 |
| 4 | 显式参数 + inspect 自动控件 | 手写所有控件 | 减少 UI 层硬编码量 |
| 5 | PARAM_OVERRIDES 覆盖 | 统一默认规则 | 解决奇数核/特殊范围等问题 |
| 6 | io_helper 统一转换 | 各 Tab 各自转换 | 避免 BGR/RGB 混乱 |
| 7 | rembg 允许 4 通道输出 | 强制转 3 通道 | 保留透明背景，不丢失信息 |
| 8 | 自动预览 Checkbox 开关 | 全量绑定 change | 防止复杂算法卡死 Gradio |

> UI 表现层相关决策（主题、布局生成器、CSS、Accordion 等）见独立文档：
> [`2026-06-09-image-processing-system-ui-design.md`](./2026-06-09-image-processing-system-ui-design.md)
