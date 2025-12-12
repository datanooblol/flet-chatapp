import flet as ft
from design.tokens import Colors, Layout

def NavBar(title="Chat", on_refresh=None):
    controls = [ft.Text(title, color=Colors.TEXT_PRIMARY, size=16, weight=ft.FontWeight.BOLD)]
    
    if on_refresh:
        controls.append(
            ft.IconButton(
                icon=ft.Icons.REFRESH_ROUNDED,
                icon_color=Colors.TEXT_PRIMARY,
                on_click=on_refresh
            )
        )
    
    return ft.Container(
        height=Layout.NAV_HEIGHT,
        bgcolor=Colors.BACKGROUND,
        content=ft.Row(
            controls=controls,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.symmetric(horizontal=16)
    )
