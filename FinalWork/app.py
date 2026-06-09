"""数字图像处理实验系统 — 入口"""

import gradio as gr

from utils.theme import get_custom_theme
from tabs.tab_grayscale import create_tab as create_grayscale
from tabs.tab_filtering import create_tab as create_filtering
from tabs.tab_frequency import create_tab as create_frequency
from tabs.tab_edge import create_tab as create_edge
from tabs.tab_morphology import create_tab as create_morphology
from tabs.tab_segmentation import create_tab as create_segmentation
from tabs.tab_hough import create_tab as create_hough
from tabs.tab_restoration import create_tab as create_restoration
from tabs.tab_matting import create_tab as create_matting

CSS_PATH = "assets/style.css"

with gr.Blocks(
    title="数字图像处理实验系统",
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
    create_frequency()
    create_edge()
    create_morphology()
    create_segmentation()
    create_hough()
    create_restoration()
    create_matting()

if __name__ == "__main__":
    demo.launch(theme=get_custom_theme(), css=CSS_PATH, show_error=True)
