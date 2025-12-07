import flet as ft
from design.tokens import Layout
from components.templates.chat_layout import ChatLayout
from package.llms.ollama import OllamaLlama

model = OllamaLlama()

def main(page: ft.Page):
    page.window.width = Layout.WIDTH
    page.window.height = Layout.HEIGHT
    page.window.resizable = False
    page.padding = 0
    page.spacing = 0
    
    page.add(
        ft.Row(
            controls=[ChatLayout(page, model)],
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir=".")
