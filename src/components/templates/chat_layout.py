import flet as ft
from design.tokens import Colors, Spacing
from components.molecules.nav_bar import NavBar
from components.molecules.chat_input import ChatInput
from components.organisms.chat_list import ChatList
from components.organisms.chat_container import ChatContainer
from hooks.use_chat import ChatState
from components.atoms.input import TextField

def ChatLayout(page, model):
    chat_list = ChatList()
    chat_state = ChatState(page, chat_list, model)
    
    message_input = TextField()
    
    def on_send(e):
        if message_input.value:
            text = message_input.value
            message_input.value = ""
            page.update()
            chat_state.send_message(text)
    
    message_input.on_submit = on_send
    
    def on_attach(e):
        chat_state.pick_file()
    
    def on_refresh(e):
        chat_state.clear_messages()
    
    chat_container = ChatContainer(chat_list)
    input_row = ChatInput(message_input, on_send, on_attach)
    nav_bar = NavBar("Chat", on_refresh=on_refresh)
    
    return ft.Container(
        bgcolor=Colors.BACKGROUND,
        expand=True,
        content=ft.Column(
            controls=[nav_bar, chat_container, input_row],
            spacing=0,
        ),
        padding=ft.padding.only(bottom=Spacing.LG)
    )
