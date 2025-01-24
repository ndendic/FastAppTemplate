from fasthtml.components import Uk_theme_switcher
from fasthtml.common import *


def theme_switcher():
    return Uk_theme_switcher(
        custom_palette="""[
            {"background": "#10b981", "key": "uk-theme-emerald", "text": "Custom"},
            {"background": "#0099AD", "key": "uk-theme-lightsky", "text": "Light Sky"},
            {"background": "#E74D3C", "key": "uk-theme-mandarino", "text": "Mandarino"},
            {"background": "#364049", "key": "uk-theme-calm", "text": "Calm"},
            ]"""
    )


def dark_mode_style_toggle():
    """
    This is a helper function when 'dark:' tailwind modifier is not working correctly.
    """
    return Style("""
            .theme-image-light { display: flex; }
            .theme-image-dark { display: none; }
            :root[class~="dark"] .theme-image-light { display: none; }
            :root[class~="dark"] .theme-image-dark { display: flex; }
            """)
