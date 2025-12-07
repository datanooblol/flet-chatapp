import flet as ft
from components.molecules.message_bubble import MessageBubble

SYSTEM_PROMPT = """\
You're the best bro, Andy who is always chill and supportive. Always reply in laid-back manner and always stick with bro-style.
""".strip()

class ChatState:
    def __init__(self, page:ft.Page, chat_list:ft.ListView, model):
        self.page = page
        self.chat_list = chat_list
        self.model = model
        self.messages = []
        self.file_picker = ft.FilePicker(on_result=self.on_file_picked)
        page.overlay.append(self.file_picker)
    
    def add_message(self, user_name, text, message_type):
        self.chat_list.controls.append(MessageBubble(user_name, text, message_type))
        self.page.update()
    
    def send_message(self, text):
        self.add_message("You", text, "user")
        self.messages.append({"role": "user", "content": text})
        
        response = self.model.run(system_prompt=SYSTEM_PROMPT, messages=self.messages)
        self.messages.append({"role": "assistant", "content": response.content})
        self.add_message("Andy", response.content, "assistant")
    
    def pick_file(self):
        self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "png", "pdf", "txt"]
        )
    
    def on_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            for file in e.files:
                print(f"Selected: {file.name}")
                print(f"Path: {file.path}")
