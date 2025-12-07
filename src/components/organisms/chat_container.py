import flet as ft
from design.tokens import Colors, Spacing

def ChatContainer(chat_list):
    return ft.Container(
        content=chat_list,
        border_radius=Spacing.MD,
        expand=True,
        padding=Spacing.MD,
        bgcolor=Colors.BACKGROUND
    )
