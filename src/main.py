import flet as ft

WIDTH = 430
HEIGHT = 800
SIDEBAR_WIDTH = 50  # Width for hamburger icon

def main(page: ft.Page):
    page.window.width = WIDTH
    page.window.height = HEIGHT
    page.window.resizable = False
    page.padding = 0
    page.spacing = 0
    page.bgcolor = ft.Colors.WHITE
    side_bar = ft.Column(
        controls=[
            ft.IconButton(
                icon=ft.Icons.MENU,
                icon_color=ft.Colors.BLACK,
            ),
        ],
    )
    chat_box = ft.Container(
        width=WIDTH - SIDEBAR_WIDTH,
        height=HEIGHT,
        bgcolor=ft.Colors.GREY_100
    )
    chat_container = ft.Column(
        controls=[
            chat_box
        ]
    )
    main_container = ft.Row([
        side_bar,
        chat_container
    ])
    page.add(main_container)
ft.app(main)
