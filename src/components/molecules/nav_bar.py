import flet as ft
from design.tokens import Colors, Layout

def NavBar(title="Chat"):
    return ft.Container(
        height=Layout.NAV_HEIGHT,
        bgcolor=Colors.BACKGROUND,
        content=ft.Row(
            controls=[
                ft.Text(title, color=Colors.TEXT_PRIMARY, size=16, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
