import arcade
from configparser import ConfigParser
from Assets.Scripts.Levels.test_level import TestLevel

from pyglet.graphics import Batch


class Application:
    def __init__(self, settings_path: str):
        self.settings = ConfigParser()
        self.settings.read(settings_path)
        self.width = float(self.settings["Application"]["ScreenWidth"])
        self.height = float(self.settings["Application"]["ScreenHeight"])
        self.start_window = TestLevel(self, "Test")
        self.start_window.setup()
    
    def run(self):
        arcade.run()


def main():
    app = Application("settings.ini")
    app.run()


if __name__ == "__main__":
    main()