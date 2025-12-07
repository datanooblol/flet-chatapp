import flet as ft
from design.tokens import Colors

def IconButton(icon, on_click, color=None):
    return ft.IconButton(
        icon=icon,
        icon_color=color or Colors.TEXT_PRIMARY,
        on_click=on_click,
    )
