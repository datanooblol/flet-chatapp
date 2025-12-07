import flet as ft
from design.tokens import Colors, Spacing, Typography

def MessageBubble(user_name: str, text: str, message_type: str):
    is_assistant = message_type == "assistant"
    
    content = (
        ft.Markdown(text, selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB)
        if is_assistant
        else ft.Text(text, selectable=True, color=Colors.TEXT_PRIMARY)
    )
    
    return ft.Column(
        controls=[
            ft.Text(user_name, size=Typography.CAPTION_SIZE, color=Colors.TEXT_SECONDARY),
            ft.Container(
                content=content,
                border_radius=Spacing.MD,
                padding=Spacing.MD,
                bgcolor=Colors.AI_BUBBLE if is_assistant else Colors.USER_BUBBLE,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.START if is_assistant else ft.CrossAxisAlignment.END,
    )
