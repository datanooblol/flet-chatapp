import flet as ft
from design.tokens import Colors, Spacing, Layout
from components.atoms.button import IconButton
from components.atoms.input import TextField

def ChatInput(message_input, on_send, on_attach):
    return ft.Container(
        height=Layout.INPUT_HEIGHT,
        bgcolor=Colors.BACKGROUND,
        padding=ft.padding.only(left=Spacing.LG, right=Spacing.LG),
        content=ft.Row(
            controls=[
                IconButton(icon=ft.Icons.ATTACH_FILE_ROUNDED, on_click=on_attach),
                message_input,
                IconButton(icon=ft.Icons.SEND_ROUNDED, on_click=on_send),
            ]
        )
    )
