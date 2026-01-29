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
        
        # Отрисовка ползунка (Sidebar)
        self.draw_slider()

    def on_update(self, delta_time):
        if InputSystem.on_key_down(InputSystem.Keys.ESCAPE):
            self.app.show_menu()
            self.interact_sound = arcade.play_sound(arcade.load_sound(UI_INTERACTION), 
                                        volume=self.app.volume / 1000)

    def draw_slider(self):
        if self.max_scroll <= 0: return
        
        # Фон дорожки
        arcade.draw_lbwh_rectangle_filled(self.app.width - SLIDER_WIDTH / 2, self.app.height / 2, 
                                     SLIDER_WIDTH, self.app.height, (30, 30, 30))
        
        # Вычисляем размер и позицию ползунка
        view_ratio = self.app.height / (self.document.content_height + 40)
        slider_height = self.app.height * view_ratio
        
        scroll_percent = self.current_scroll / self.max_scroll
        slider_y = self.app.height - (scroll_percent * (self.app.height - slider_height)) - slider_height/2
        
        arcade.draw_lbwh_rectangle_filled(self.app.width - SLIDER_WIDTH / 2, slider_y, 
                                     SLIDER_WIDTH - 4, slider_height, arcade.color.GRAY)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # scroll_y > 0 это прокрутка вверх (колесико от себя)
        self.current_scroll -= scroll_y * SCROLL_SPEED
        
        # Ограничиваем скролл
        if self.current_scroll < 0:
            self.current_scroll = 0
        elif self.current_scroll > self.max_scroll:
            self.current_scroll = self.max_scroll