import arcade
from pyglet.graphics import Batch
from Assets.Scripts.Engine import InputSystem


class GameResultView(arcade.View):
    """Окно результата"""
    def __init__(self, application, caption: str, result_message: str = ""):
        super().__init__(application.window)
        self.application = application
        self.texture = arcade.load_texture("Assets/Sprites/menuBG.jpg")
        self.settings_list = arcade.SpriteList()
        self.escape_list = arcade.SpriteList()
        self.play_list = arcade.SpriteList()

        self.gui_camera = arcade.camera.Camera2D()
        
        self.window.set_caption(caption)
        self.batch = Batch()
        self.restart_info = arcade.Text(
            text=result_message,
            color=arcade.color.WHITE,
            x=self.center_x,
            y=self.center_y,
            font_size=24,
            anchor_x="center",
            batch=self.batch
        )

    def on_draw(self):
        self.clear()
        self.gui_camera.use()
        self.batch.draw()

    def on_show_view(self):
        """Настройка при показе меню"""
        self.settings_list.clear()
        self.escape_list.clear()
        self.play_list.clear()

        # Кнопка Play
        play = arcade.Sprite("Assets/Sprites/playBtn.jpg", 0.5)
        play.center_x = self.application.width // 2
        play.center_y = 380
        self.play_list.append(play)

        # Кнопка Escape
        escape = arcade.Sprite("Assets/Sprites/exitBtn.jpg", 0.5)
        escape.center_x = self.application.width // 2
        escape.center_y = 130
        self.escape_list.append(escape)

    def restart(self):
        self.application.start_level(self.application.last_started_level)

    def on_draw(self):
        self.clear()
        # Рисуем фон
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.application.width // 2,
                self.application.height // 2, self.application.width, self.application.height))
        # Рисуем кнопки
        self.settings_list.draw()
        self.escape_list.draw()
        self.play_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мышью"""
        # Проверяем нажатие на Play
        if arcade.get_sprites_at_point((x, y), self.play_list):
            self.restart()
            return

        # Проверяем нажатие на Escape (выход)
        if arcade.get_sprites_at_point((x, y), self.escape_list):
            arcade.exit()
            return