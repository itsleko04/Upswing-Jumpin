import arcade
from Assets.Scripts.Engine.Level import Level
from Assets.Sounds.OST import LEVEL1OST


class TestLevel(Level):
    """Первый, пока что тестовый уровень. Непроходимый."""
    def __init__(self, application):
        super().__init__(application)
        self.application = application

        self.theme_music = arcade.load_sound(LEVEL1OST)
        self.on_game_over.connect(lambda: self.theme_music_player.delete())
        self.bg = arcade.load_texture(application.settings["Sprites"]["LevelsBG"])

    def setup(self):
        """Настраиваем игру здесь. Вызывается при старте и при рестарте"""
        super().setup(self.application.settings["Tilemap"]["TestLevel"])
        self.theme_music_player = arcade.play_sound(self.theme_music, loop=True, volume=float(self.application.volume))
        self.window.set_caption("Test Level")