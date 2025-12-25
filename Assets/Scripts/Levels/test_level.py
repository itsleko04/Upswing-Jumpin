import arcade
from Assets.Scripts.Player import Player


class TestLevel(arcade.Window):
    def __init__(self, application, title):
        super().__init__(application.width, application.height, title)
        self.application = application
        self.bg = arcade.load_texture(application.settings["Sprites"]["LevelsBG"])

    def setup(self):
        """Настраиваем игру здесь. Вызывается при старте и при рестарте"""
        # Инициализируем списки спрайтов
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()  # Сюда попадёт слой Collision!

        tile_map = arcade.load_tilemap(self.application.settings["Tilemap"]["TestLevel"], scaling=0.1)

        # --- Достаём слои из карты как спрайт-листы ---
        # Слой "walls" (стены) — просто для отрисовки
        self.ground_list = tile_map.sprite_lists["ground"]
        # Слой "chests" (сундуки) — красота!
        self.shapes_list = tile_map.sprite_lists["shapes"]
        # САМЫЙ ГЛАВНЫЙ СЛОЙ: "Collision" — наши стены и платформы для физики!
        self.collision_list = tile_map.sprite_lists["collision"]
        self.player_sprite = Player(self.application.settings["Sprites"]["PlayerIdle"],
                                    0.075)
        self.player_sprite.left = 103  # Примерные координаты
        self.player_sprite.bottom = 52  # Примерные координаты
        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.collision_list
        )

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.bg, self.rect)
        self.ground_list.draw()
        self.shapes_list.draw()
        arcade.draw_sprite(self.player_sprite)