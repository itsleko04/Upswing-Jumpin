import arcade
from Assets.GC import TITLE


class MenuView(arcade.View):
    """Стартовое меню"""

    def __init__(self, application):
        super().__init__()
        self.application = application
        self.texture = arcade.load_texture("Assets/Sprites/menuBG.jpg")
        self.settings_list = arcade.SpriteList()
        self.escape_list = arcade.SpriteList()
        self.play_list = arcade.SpriteList()

    def on_show_view(self):
        """Настройка при показе меню"""
        self.settings_list.clear()
        self.escape_list.clear()
        self.play_list.clear()

        # Настройки кнопки
        settings = arcade.Sprite("Assets/Sprites/settingsBtn.jpg", 0.5)
        settings.center_x = self.application.width // 2
        settings.center_y = 250
        self.settings_list.append(settings)

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

    def on_draw(self):
        self.clear()
        # Рисуем фон
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.application.width // 2,
                self.application.height // 2, self.application.width, self.application.height))
        # Рисуем кнопки
        self.settings_list.draw()
        self.escape_list.draw()
        self.play_list.draw()
        # Заголовок
        arcade.draw_text(TITLE, self.application.width,
            self.application.height - 100, arcade.color.WHITE, 50, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мышью"""
        # Проверяем нажатие на Settings
        if arcade.get_sprites_at_point((x, y), self.settings_list):
            settings_view = SettingsView(self.application)
            self.window.show_view(settings_view)
            return

        # Проверяем нажатие на Play
        if arcade.get_sprites_at_point((x, y), self.play_list):
            play_view = PlayView(self.application)
            self.window.show_view(play_view)
            return

        # Проверяем нажатие на Escape (выход)
        if arcade.get_sprites_at_point((x, y), self.escape_list):
            arcade.exit()
            return


class SettingsView(arcade.View):
    """Экран настроек"""

    def __init__(self, application):
        super().__init__()
        self.application = application

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        arcade.draw_text("Настройки", self.application.width // 2,
            self.application.height // 2, arcade.color.WHITE, 50, anchor_x="center")
        arcade.draw_text("Нажмите ESC для возврата", self.application.width // 2,
            self.application.height // 2 - 100, arcade.color.WHITE,
            20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = MenuView(self.application)
            self.window.show_view(menu_view)


class PlayView(arcade.View):
    """Экран игры"""

    def __init__(self, application):
        super().__init__()
        self.application = application

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.DARK_GREEN)
        arcade.draw_text("Игра", self.application.width // 2,
            self.application.height // 2, arcade.color.WHITE, 50, anchor_x="center")
        arcade.draw_text("Нажмите ESC для возврата", self.application.width // 2,
            self.application.height // 2 - 100, arcade.color.WHITE,
            20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = MenuView(self.application)
            self.window.show_view(menu_view)