import flet as ft 
from package.llms.ollama import OllamaLlama
model = OllamaLlama()

WIDTH = 430
HEIGHT = 800

MESSAGES = []

SYSTEM_PROMPT = """\
You're the best bro, Andy who is always chill and supportive. Always reply in laid-back manner and always stick with bro-style.
""".strip()

class Message():
    def __init__(self, user_name:str, text:str, message_type:str):
        self.user_name = user_name
        self.text = text 
        self.message_type = message_type

# This is the app
def main(page: ft.Page):
    page.window.width = WIDTH
    page.window.height = HEIGHT
    page.window.resizable = False
    
    page.padding = 0
    page.spacing = 0
    
    # My Widgets
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
        padding=24,
    )

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            for file in e.files:
                print(f"Selected: {file.name}")
                print(f"Path: {file.path}")
                # Do something with the file
    
    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)
    
    # Button to trigger file picker
    def pick_file(e):
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "png", "pdf", "txt"]
        )

    new_message = ft.TextField(
        hint_text="Type a message...",
        border=ft.InputBorder.NONE,
        expand=True,
        multiline=True,
        content_padding=8,
        bgcolor=ft.Colors.GREY_100,
    )

    # Add the functionality
    def add_message(user_name:str, text:str, message_type:str):
        message = Message(user_name, text, message_type)
        horizontal_alignment = ft.CrossAxisAlignment.START
        if message_type == "assistant":
            text_color = ft.Colors.BLACK
            bg_color = ft.Colors.WHITE
        else:
            text_color = ft.Colors.BLACK
            bg_color = ft.Colors.GREY_200
            horizontal_alignment = ft.CrossAxisAlignment.END
        def pack_text(text, message_type):
            if message_type != "assistant":
                return ft.Text(text, selectable=True, color=text_color)
            return ft.Markdown(text, selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB) 
        # Add messages to my ListView
        chat.controls.append(
            ft.Column(
                controls=[
                    ft.Text(message.user_name, size=12, color=ft.Colors.GREY_700),
                    ft.Container(
                        content=pack_text(text, message_type),
                        border_radius=10,
                        padding=10,
                        bgcolor=bg_color
                    ),
                ],
                horizontal_alignment=horizontal_alignment
            )
        )
        page.update()

    # Send the messages
    def send_message(e):
        if not new_message.value:
            return 
        
        # Add messages to the chat
        user_message = new_message.value 
        add_message("You", user_message, "user")
        new_message.value = ""
        page.update()
        MESSAGES.append(dict(role="user", content=user_message)) 
        ai_res = model.run(system_prompt=SYSTEM_PROMPT, messages=MESSAGES)
        MESSAGES.append(dict(role="assistant", content=ai_res.content))
        add_message("Andy", ai_res.content, "assistant")

    # Building out the Container
    chat_container = ft.Container(
        content=chat,
        border_radius=10,
        expand=True,
        padding=10,
        bgcolor=ft.Colors.WHITE
    )
    
    input_row = ft.Container(
        height=60,
        bgcolor=ft.Colors.WHITE,
        padding=ft.padding.only(left=24, right=24),        
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ATTACH_FILE_ROUNDED,
                    icon_color=ft.Colors.BLACK,
                    on_click=pick_file
                ),
                new_message,
                ft.IconButton(
                    icon=ft.Icons.SEND_ROUNDED,
                    icon_color=ft.Colors.BLACK,
                    on_click=send_message,
                ),
            ]
        )
    )
    nav_bar = ft.Container(
        height=60,
        bgcolor=ft.Colors.WHITE,
        content=ft.Row(
            controls=[
                ft.Text("Chat", color=ft.Colors.BLACK),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    chat_area = ft.Container(
        bgcolor=ft.Colors.WHITE,
        expand=True,
        content=ft.Column(
            controls=[
                nav_bar,
                chat_container,
                input_row
            ],
            spacing=0,
        ),
        padding=ft.padding.only(bottom=24)
    )
    page.add(
        ft.Row(
            controls=[
                chat_area,
            ], expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir=".")