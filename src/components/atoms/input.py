import flet as ft
from design.tokens import Colors, Spacing

def TextField(hint_text="Type a message...", on_submit=None):
    return ft.TextField(
        hint_text=hint_text,
        border=ft.InputBorder.NONE,
        expand=True,
        multiline=True,
        content_padding=Spacing.SM,
        bgcolor=Colors.SURFACE,
        on_submit=on_submit,
        shift_enter=True,
    )
