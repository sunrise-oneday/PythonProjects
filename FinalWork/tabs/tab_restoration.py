"""图像复原 Tab"""
import gradio as gr
from ._builder import build_tab


TAB_KEY = "图像复原"


def create_tab():
    with gr.Tab(TAB_KEY):
        build_tab(TAB_KEY)
