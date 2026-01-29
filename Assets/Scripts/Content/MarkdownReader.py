import arcade
import Assets.Scripts.Engine.InputSystem as InputSystem
from Assets.Sounds import UI_INTERACTION


SCROLL_SPEED = 20
SLIDER_WIDTH = 15


class MarkdownView(arcade.View):
    """Окно, в котором можно прочитать содержимое .md файла"""
    def __init__(self, app, filepath: str):
        super().__init__(app.window)
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.app = app
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        self.document = arcade.Text(
            content,
            x=20,
            y=self.app.height - 20,
            color=arcade.color.WHITE,
            font_size=14,
            width=self.app.width - 50,
            multiline=True,
            anchor_y="top"
        )
        
        # Вычисляем границы прокрутки
        # self.document.content_height — высота всего текста в пикселях
        self.max_scroll = max(0, self.document.content_height - self.app.height + 40)
        self.current_scroll = 0

    def on_draw(self):
        self.clear()
        
        # Сдвигаем текст вверх на величину скролла
        self.document.y = (self.app.height - 20) + self.current_scroll
        self.document.draw()


    def on_update(self, delta_time):
        if InputSystem.on_key_down(InputSystem.Keys.ESCAPE):
            self.app.show_menu()
            self.interact_sound = arcade.play_sound(arcade.load_sound(UI_INTERACTION), 
                                        volume=self.app.volume / 1000)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # scroll_y > 0 это прокрутка вверх (колесико от себя)
        self.current_scroll -= scroll_y * SCROLL_SPEED
        
        # Ограничиваем скролл
        if self.current_scroll < 0:
            self.current_scroll = 0
        elif self.current_scroll > self.max_scroll:
            self.current_scroll = self.max_scroll