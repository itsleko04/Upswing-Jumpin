import arcade
from Assets.Scripts.Engine import InputSystem
from Assets.Scripts.Engine import Event
from Assets.Scripts.Content.Menu import MenuView
from Assets.Scripts.Content.Levels.TestLevel import TestLevel
from Assets.Scripts.Engine import Level
from Assets.GC import VOLUME


class Application:
    """Базовая реализация запуска игровой сессии"""
    def __init__(self, settings):
        self.settings = settings

        self.volume = VOLUME

        self.width = float(self.settings["Application"]["ScreenWidth"])
        self.height = float(self.settings["Application"]["ScreenHeight"])
        self.window = Window(self.width, self.height)
        self.window.on_close_event.connect(self.save_volume)
        self.show_menu()

        self.last_started_level = None
    
    def start_level(self, level: Level):
        """Запуск уровня"""
        self.last_started_level = level
        self.last_started_level.setup()
        self.window.show_view(self.last_started_level)

    def set_volume(self, volume: float):
        """Громкость от 0 до 1"""
        self.volume = volume

    def save_volume(self):
        ...

    def show_menu(self):
        self.window.show_view(MenuView(self))

    def run(self):
        """Запустить игру"""
        arcade.run()


class Window(arcade.Window):
    def __init__(self, width: int = 1280, height: int = 720):
        super().__init__(width, height)
        self.on_close_event = Event()

    def __translate_from_arcade_input_system__(self, button):
        buttons = {
            arcade.MOUSE_BUTTON_LEFT : InputSystem.MouseButton.LEFT,
            arcade.MOUSE_BUTTON_RIGHT : InputSystem.MouseButton.RIGHT,
            arcade.MOUSE_BUTTON_MIDDLE : InputSystem.MouseButton.MIDDLE
        }
        return buttons[button]

    def on_update(self, delta_time):
        for key in InputSystem.ALL_INPUT:
            if key.status == InputSystem.KeyPressStatus.PRESSED:
                key.status = InputSystem.KeyPressStatus.HOLDING
            elif key.status == InputSystem.KeyPressStatus.RELEASED:
                key.status = None
        return super().on_update(delta_time)

    def on_key_press(self, symbol, modifiers):
        InputSystem.__set_key_status__(symbol, InputSystem.KeyPressStatus.PRESSED)
        return super().on_key_press(symbol, modifiers)
    
    def on_key_release(self, symbol, modifiers):
        InputSystem.__set_key_status__(symbol, InputSystem.KeyPressStatus.RELEASED)
        return super().on_key_release(symbol, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        button = self.__translate_from_arcade_input_system__(button)
        InputSystem.__set_mouse_status__(button, InputSystem.KeyPressStatus.PRESSED)
        return super().on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        button = self.__translate_from_arcade_input_system__(button)
        InputSystem.__set_mouse_status__(button, InputSystem.KeyPressStatus.RELEASED)
        return super().on_mouse_release(x, y, button, modifiers)

    def on_close(self):
        self.on_close_event.invoke()
        return super().on_close()