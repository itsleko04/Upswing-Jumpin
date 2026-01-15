import arcade
from pyglet.graphics import Batch

from Assets.Scripts.Engine import InputSystem


class GameOverView(arcade.View):
    """Окно смерти"""
    def __init__(self, application):
        super().__init__(application.window)

        self.gui_camera = arcade.camera.Camera2D()
        
        self.window.set_caption("Gameover")
        self.application = application
        self.batch = Batch()
        self.restart_info = arcade.Text(
            text="Нажмите R, чтобы перезапустить уровень.",
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
    
    def on_update(self, delta_time):
        if InputSystem.on_key_down(InputSystem.Keys.R):
            self.restart()
    
    def restart(self):
        """Перезапуск последнего запущенного уровня"""
        self.application.start_level(self.application.last_started_level)