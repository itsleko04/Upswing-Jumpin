import arcade
from configparser import ConfigParser

from Assets.Scripts.Engine import Event
from Assets.Scripts.Content.Levels.TestLevel import TestLevel
from Assets.Scripts.Engine import Level


class Window(arcade.Window):
    def __init__(self, width: int = 1280, height: int = 720):
        super().__init__(width, height)
        self.on_close_event = Event()
    
    def on_close(self):
        self.on_close_event.invoke()
        return super().on_close()


class Application:
    """Базовая реализация запуска игровой сессии"""
    def __init__(self, settings_path: str):
        self.settings_path = settings_path
        self.settings = ConfigParser()
        self.settings.read(self.settings_path)

        self.volume = float(self.settings["Application"]["Volume"])

        self.width = float(self.settings["Application"]["ScreenWidth"])
        self.height = float(self.settings["Application"]["ScreenHeight"])
        self.window = Window(self.width, self.height)
        self.window.on_close_event.connect(self.save_volume)

        self.last_started_level = None
        self.start_level(TestLevel(self))
    
    def start_level(self, level: Level):
        """Запуск уровня"""
        self.last_started_level = level
        self.last_started_level.setup()
        self.window.show_view(self.last_started_level)

    def set_volume(self, volume: float):
        """Громкость от 0 до 1"""
        self.volume = volume

    def save_volume(self):
        self.settings["Application"]["Volume"] = str(self.volume)
        with open(self.settings_path, "w") as settings_file:
            self.settings.write(settings_file)

    def run(self):
        """Запустить игру"""
        arcade.run()