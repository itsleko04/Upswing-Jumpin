from Assets.Scripts.Engine.InputSystem.Keys import ALL_KEYBOARD_KEYS, ALL_MOUSE_BUTTONS, KeyPressStatus, Key, MouseButton


def __set_key_status__(key_index: int, status: KeyPressStatus | None) -> None:
    changing_key = None
    for key in ALL_KEYBOARD_KEYS:
        if key_index == key.index:
            changing_key = key
    if changing_key:
        changing_key.status = status

def __set_mouse_status__(mouse_index: MouseButton, status: KeyPressStatus | None) -> None:
    changing_mouse_button = None
    for button in ALL_MOUSE_BUTTONS:
        if mouse_index == button.index:
            changing_mouse_button = button
    if changing_mouse_button:
        changing_mouse_button.status = status

def on_key_down(key: Key) -> bool:
    """Проверить, была ли только что нажата клавиша"""
    return key.status == KeyPressStatus.PRESSED

def on_key_up(key: Key) -> bool:
    """Проверить, была ли только что отжата клавиша"""
    return key.status == KeyPressStatus.RELEASED

def on_key(key: Key) -> bool:
    """Проверить, нажата ли клавиша до сих пор"""
    return key.status == KeyPressStatus.HOLDING

def on_mouse_down(button: Key) -> bool:
    """Проверить, была ли только что нажата кнопка мыши"""
    return button.status == KeyPressStatus.PRESSED

def on_mouse_up(button: Key) -> bool:
    """Проверить, была ли только что отжата кнопка мыши"""
    return button.status == KeyPressStatus.RELEASED

def on_mouse_holding(button: Key) -> bool:
    """Проверить, нажата ли кнопка мыши до сих пор"""
    return button.status == KeyPressStatus.HOLDING