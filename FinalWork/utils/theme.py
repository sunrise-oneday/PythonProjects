"""Soft-Blue 自定义 Gradio 主题"""

import gradio as gr


def get_custom_theme():
    """返回 Soft-Blue 专业配色方案"""
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
    ).set(
        body_background_fill="#f8fafc",
        body_background_fill_dark="#0f172a",
        block_background_fill="white",
        block_border_width="0px",
        block_shadow="0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
        block_radius="12px",
        button_primary_background_fill="#2563eb",
        button_primary_text_color="white",
        button_primary_background_fill_hover="#1d4ed8",
        button_primary_border_color="#2563eb",
        input_background_fill="#f1f5f9",
        input_border_color="#cbd5e1",
        input_border_width="1px",
        input_radius="8px",
    )
    return theme
