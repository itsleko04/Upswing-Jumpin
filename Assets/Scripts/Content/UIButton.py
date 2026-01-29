import arcade
from Assets.Scripts.Engine import Event
from Assets.Sounds import UI_INTERACTION


class UIButton(arcade.Sprite):
    """
    Кнопка для работы с UI без UIManager\n
    Чтобы работать через UIButton создаёте SpriteList(ui_buttons) и в on_mouse_press проверяете на arcade.get_sprites_at_point \n
    У каждой кнопки вызываете click \n
    ```
    def on_mouse_press(self, x, y, button, modifiers):
        for button in self.ui_buttons:
            list = arcade.SpriteList()
            list.append(button)
            if arcade.get_sprites_at_point((x, y), list):
                button.click()
    ```
    """
    def __init__(self, path: str, scale: float = 1, x: float = 0, y: float = 0, click_volume: float = 1):
        super().__init__(path)
        self.on_click = Event()
        self.scale = scale
        self.center_x = x
        self.center_y = y
        self.volume = click_volume
        self.sound = arcade.load_sound(UI_INTERACTION)

    def click(self):
        self.player = arcade.play_sound(self.sound, volume=self.volume / 10)
        self.on_click.invoke()