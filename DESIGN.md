# Design System Documentation

## Overview

This project implements **Atomic Design** methodology combined with **Design Tokens** to create a scalable, maintainable, and consistent UI architecture for the Flet chat application.

## Design Tokens

Design tokens are the visual design atoms of the design system — specifically, they are named entities that store visual design attributes. They act as a single source of truth for design decisions.

### Location: `src/design/tokens.py`

```python
class Colors:
    PRIMARY = ft.Colors.BLUE
    BACKGROUND = ft.Colors.WHITE
    SURFACE = ft.Colors.GREY_100
    TEXT_PRIMARY = ft.Colors.BLACK
    TEXT_SECONDARY = ft.Colors.GREY_700
    USER_BUBBLE = ft.Colors.GREY_200
    AI_BUBBLE = ft.Colors.WHITE

class Spacing:
    XS = 4
    SM = 8
    MD = 10
    LG = 24
    XL = 32

class Typography:
    BODY_SIZE = 14
    CAPTION_SIZE = 12
    
class Layout:
    WIDTH = 430
    HEIGHT = 800
    NAV_HEIGHT = 60
    INPUT_HEIGHT = 60
```

### Why Design Tokens?

**Before (Hardcoded values):**
```python
ft.Container(
    bgcolor=ft.Colors.WHITE,
    padding=24,
    border_radius=10
)
```

**After (Design Tokens):**
```python
ft.Container(
    bgcolor=Colors.BACKGROUND,
    padding=Spacing.LG,
    border_radius=Spacing.MD
)
```

**Benefits:**
- **Consistency**: All components use the same spacing/colors
- **Easy theming**: Change `Colors.BACKGROUND` once, updates everywhere
- **Maintainability**: No magic numbers scattered across codebase
- **Scalability**: Add dark mode by swapping token values

---

## Atomic Design

Atomic Design is a methodology for creating design systems with five distinct levels: Atoms, Molecules, Organisms, Templates, and Pages.

### 1. Atoms (`src/components/atoms/`)

**Definition**: Basic building blocks that can't be broken down further.

**Examples:**
- `button.py` - IconButton
- `input.py` - TextField

```python
# atoms/button.py
def IconButton(icon, on_click, color=None):
    return ft.IconButton(
        icon=icon,
        icon_color=color or Colors.TEXT_PRIMARY,
        on_click=on_click,
    )
```

**Why separate?**
- Reusable across entire app
- Single place to update button styling
- Easy to test in isolation

---

### 2. Molecules (`src/components/molecules/`)

**Definition**: Groups of atoms functioning together as a unit.

**Examples:**
- `message_bubble.py` - User name + message container
- `chat_input.py` - Attach button + TextField + Send button
- `nav_bar.py` - Container + Text

```python
# molecules/message_bubble.py
def MessageBubble(user_name: str, text: str, message_type: str):
    return ft.Column(
        controls=[
            ft.Text(user_name, size=Typography.CAPTION_SIZE),  # Atom
            ft.Container(                                       # Atom
                content=ft.Text(text),                          # Atom
                border_radius=Spacing.MD,
                padding=Spacing.MD,
            ),
        ],
    )
```

**Why separate?**
- Message bubble logic in one place
- Can reuse in different contexts (chat, notifications)
- Easier to modify bubble appearance

**Example: Before vs After**

**Before (Monolithic):**
```python
# Everything in main.py
chat.controls.append(
    ft.Column(
        controls=[
            ft.Text(message.user_name, size=12, color=ft.Colors.GREY_700),
            ft.Container(
                content=ft.Text(message.text, selectable=True, color=text_color),
                border_radius=10,
                padding=10,
                bgcolor=bg_color
            ),
        ],
    )
)
```

**After (Atomic):**
```python
# In main.py
chat.controls.append(MessageBubble(user_name, text, message_type))

# In molecules/message_bubble.py - reusable component
def MessageBubble(user_name, text, message_type):
    # ... implementation
```

---

### 3. Organisms (`src/components/organisms/`)

**Definition**: Complex UI components composed of molecules and/or atoms.

**Examples:**
- `chat_list.py` - ListView with configured spacing/padding
- `chat_container.py` - Container wrapping chat list

```python
# organisms/chat_list.py
def ChatList():
    return ft.ListView(
        expand=True,
        spacing=Spacing.MD,
        auto_scroll=True,
        padding=Spacing.LG,
    )
```

**Why separate?**
- Encapsulates complex behavior (auto-scroll, expand)
- Can swap implementations (ListView → Column)
- Consistent configuration across app

---

### 4. Templates (`src/components/templates/`)

**Definition**: Page-level layouts that combine organisms, molecules, and atoms.

**Example:**
- `chat_layout.py` - Full chat interface layout

```python
# templates/chat_layout.py
def ChatLayout(page, model):
    chat_list = ChatList()              # Organism
    chat_state = ChatState(...)         # Hook
    
    message_input = TextField()         # Atom
    chat_container = ChatContainer(chat_list)  # Organism
    input_row = ChatInput(message_input, on_send, on_attach)  # Molecule
    nav_bar = NavBar("Chat")            # Molecule
    
    return ft.Container(
        content=ft.Column(
            controls=[nav_bar, chat_container, input_row],
        ),
    )
```

**Why separate?**
- Defines page structure
- Easy to create new layouts (settings page, profile page)
- Separates layout from business logic

---

## Hooks (`src/hooks/`)

**Definition**: Encapsulated business logic and state management (inspired by React hooks).

**Example:**
- `use_chat.py` - Chat state and message handling

```python
# hooks/use_chat.py
class ChatState:
    def __init__(self, page, chat_list, model):
        self.page = page
        self.chat_list = chat_list
        self.model = model
        self.messages = []
    
    def send_message(self, text):
        self.add_message("You", text, "user")
        self.messages.append({"role": "user", "content": text})
        
        response = self.model.run(messages=self.messages)
        self.messages.append({"role": "assistant", "content": response.content})
        self.add_message("Andy", response.content, "assistant")
```

**Why separate?**
- Business logic separated from UI
- Easier to test (no UI dependencies)
- Can reuse logic in different contexts
- State management in one place

---

## File Structure

```
src/
├── design/
│   └── tokens.py              # Design tokens (single source of truth)
├── components/
│   ├── atoms/                 # Basic building blocks
│   │   ├── button.py
│   │   └── input.py
│   ├── molecules/             # Simple combinations
│   │   ├── message_bubble.py
│   │   ├── chat_input.py
│   │   └── nav_bar.py
│   ├── organisms/             # Complex components
│   │   ├── chat_list.py
│   │   └── chat_container.py
│   └── templates/             # Page layouts
│       └── chat_layout.py
├── hooks/                     # Business logic
│   └── use_chat.py
└── main.py                    # App entry point
```

---

## Real-World Example: Adding Dark Mode

**With Atomic Design + Design Tokens:**

1. Update tokens:
```python
# design/tokens.py
class Colors:
    BACKGROUND = ft.Colors.BLACK  # Changed from WHITE
    TEXT_PRIMARY = ft.Colors.WHITE  # Changed from BLACK
    # ... other colors
```

2. Done! All components automatically use new colors.

**Without this structure:**
- Search entire codebase for `ft.Colors.WHITE`
- Manually update 50+ locations
- Risk missing some instances
- Inconsistent results

---

## Real-World Example: Reusing Components

**Scenario**: Add a settings page with similar input fields.

**With Atomic Design:**
```python
# New file: templates/settings_layout.py
from components.atoms.input import TextField
from components.molecules.nav_bar import NavBar

def SettingsLayout(page):
    username_input = TextField(hint_text="Username")
    email_input = TextField(hint_text="Email")
    nav_bar = NavBar("Settings")
    
    return ft.Container(
        content=ft.Column(
            controls=[nav_bar, username_input, email_input],
        ),
    )
```

**Benefits:**
- Reused TextField atom (same styling)
- Reused NavBar molecule (consistent header)
- 10 lines of code vs 50+ without reuse

---

## Comparison: Before vs After

### Before (Monolithic `main.py`)

```python
# 170+ lines in one file
def main(page):
    # All UI code here
    # All business logic here
    # All styling here
    # Hard to maintain
    # Hard to test
    # Hard to reuse
```

**Problems:**
- Can't reuse message bubble in notifications
- Can't test chat logic without UI
- Changing button color requires finding all buttons
- Adding dark mode = nightmare

### After (Atomic Design)

```python
# main.py - 20 lines
def main(page):
    page.add(ChatLayout(page, model))

# Components are reusable
# Logic is testable
# Styling is consistent
# Easy to maintain
```

**Benefits:**
- Message bubble reusable anywhere
- Chat logic testable independently
- Change button color in one place
- Dark mode = update tokens

---

## Best Practices

1. **Always use design tokens** - Never hardcode colors/spacing
2. **Keep atoms simple** - Single responsibility
3. **Molecules should be reusable** - Not page-specific
4. **Organisms can be complex** - But still reusable
5. **Templates define layout** - Not business logic
6. **Hooks manage state** - Separate from UI

---

## Adding New Components

### Example: Add a "Typing Indicator"

1. **Create Atom** (if needed):
```python
# atoms/dot.py
def Dot(color):
    return ft.Container(width=8, height=8, bgcolor=color, border_radius=4)
```

2. **Create Molecule**:
```python
# molecules/typing_indicator.py
from components.atoms.dot import Dot
from design.tokens import Colors, Spacing

def TypingIndicator():
    return ft.Row(
        controls=[
            Dot(Colors.TEXT_SECONDARY),
            Dot(Colors.TEXT_SECONDARY),
            Dot(Colors.TEXT_SECONDARY),
        ],
        spacing=Spacing.XS,
    )
```

3. **Use in Template**:
```python
# templates/chat_layout.py
from components.molecules.typing_indicator import TypingIndicator

# Add to chat when AI is typing
chat_list.controls.append(TypingIndicator())
```

---

## Conclusion

This design system provides:
- **Consistency** through design tokens
- **Reusability** through atomic components
- **Maintainability** through separation of concerns
- **Scalability** through modular architecture
- **Testability** through isolated components

The initial setup takes more time, but pays off as the app grows.
