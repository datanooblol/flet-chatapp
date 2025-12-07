import flet as ft
from design.tokens import Spacing

def ChatList():
    return ft.ListView(
        expand=True,
        spacing=Spacing.MD,
        auto_scroll=True,
        padding=Spacing.LG,
    )
