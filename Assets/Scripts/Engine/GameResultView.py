import arcade
from pyglet.graphics import Batch
from Assets.Scripts.Engine import InputSystem


class GameResultView(arcade.View):
    """Окно результата"""
    def __init__(self, application, caption: str, result_message: str = ""):
        super().__init__(application.window)
        self.application = application
        self.texture = arcade.load_texture("Assets/Sprites/gameOverBG.jpg")
        self.to_menu_list = arcade.SpriteList()
        self.restart_list = arcade.SpriteList()

        self.gui_camera = arcade.camera.Camera2D()
        
        self.window.set_caption(caption)
        self.batch = Batch()
        self.result_info = arcade.Text(
            text=result_message,
            color=(96, 117, 102),
            x=self.center_x,
            y=self.center_y + self.center_y * 2 / 3,
            font_size=48,
            anchor_x="center",
            batch=self.batch
        )

    def on_show_view(self):
        """Настройка при показе меню"""
        self.to_menu_list.clear()
        self.restart_list.clear()

        y_offset = 100

        restart = arcade.Sprite("Assets/Sprites/gameOverRestartBtn.jpg", 0.5)
        restart.center_x = self.application.width // 2
        restart.center_y = self.application.height // 2 - y_offset
        self.restart_list.append(restart)

        to_menu = arcade.Sprite("Assets/Sprites/showMenuBtn.jpg", 0.5)
        to_menu.center_x = self.application.width // 2
        to_menu.center_y = self.application.height // 2 - 120 - y_offset
        self.to_menu_list.append(to_menu)

    def restart(self):
        self.application.start_level(self.application.last_started_level)

    def on_draw(self):
        self.clear()
        self.gui_camera.use()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.application.width // 2,
                self.application.height // 2, self.application.width, self.application.height))
        self.to_menu_list.draw()
        self.restart_list.draw()
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мышью"""
        if arcade.get_sprites_at_point((x, y), self.restart_list):
            self.restart()
            return

        if arcade.get_sprites_at_point((x, y), self.to_menu_list):
            self.application.show_menu()
            return