import arcade
from pyglet.graphics import Batch
from Assets.Scripts.Engine import InputSystem
from Assets.GC import SCORE_MULTIPLIER
from Assets.Sounds import WIN, DEATH


class GameResultView(arcade.View):
    """Окно результата"""
    def __init__(self, application, caption: str, result_message: str = "", gameplay_time: float = 0, is_win: bool=False):
        super().__init__(application.window)
        self.application = application
        self.is_win = is_win

        self.win_sound = arcade.load_sound(WIN)
        self.death_sound = arcade.load_sound(DEATH)
        self.texture = arcade.load_texture("Assets/Sprites/gameOverBG.jpg")
        self.to_menu_list = arcade.SpriteList()
        self.restart_list = arcade.SpriteList()

        self.score = int(SCORE_MULTIPLIER * gameplay_time)

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
        self.score_txt = arcade.Text(
            text=f"Счёт: {self.score}",
            color=arcade.color.WHITE,
            x=self.center_x,
            y=self.center_y,
            font_size=40,
            anchor_x="center",
            batch=self.batch
        )

    def on_show_view(self):
        """Настройка при показе меню"""
        self.to_menu_list.clear()
        self.restart_list.clear()

        y_offset = 100

        if not self.is_win:
            restart = arcade.Sprite("Assets/Sprites/gameOverRestartBtn.jpg", 0.5)
            restart.center_x = self.application.width // 2
            restart.center_y = self.application.height // 2 - y_offset
            self.restart_list.append(restart)

        to_menu = arcade.Sprite("Assets/Sprites/showMenuBtn.jpg", 0.5)
        to_menu.center_x = self.application.width // 2
        to_menu.center_y = self.application.height // 2 - 120 - y_offset
        self.to_menu_list.append(to_menu)

        self.sound_player = arcade.play_sound(self.win_sound if self.is_win else self.death_sound, loop=False,
                                        volume=float(self.application.volume) / 100)

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

    def on_update(self, delta_time):
        if InputSystem.on_key_down(InputSystem.Keys.R):
            self.restart()
        elif InputSystem.on_key_down(InputSystem.Keys.ESCAPE):
            self.application.show_menu()

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мышью"""
        if arcade.get_sprites_at_point((x, y), self.restart_list):
            self.restart()
            return

        if arcade.get_sprites_at_point((x, y), self.to_menu_list):
            self.application.show_menu()
            return