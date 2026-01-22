import os
import arcade
import subprocess
from Assets.GC import TITLE
from Assets.Scripts.Engine import InputSystem
from Assets.Scripts.Content.Levels.TestLevel import TestLevel


class MenuView(arcade.View):
    """Стартовое меню"""

    def __init__(self, application):
        super().__init__()
        self.application = application
        self.texture = arcade.load_texture("Assets/Sprites/menuBG.jpg")
        self.settings_list = arcade.SpriteList()
        self.escape_list = arcade.SpriteList()
        self.play_list = arcade.SpriteList()
        self.tutorial_list = arcade.SpriteList()

    def on_show_view(self):
        """Настройка при показе меню"""
        self.settings_list.clear()
        self.escape_list.clear()
        self.play_list.clear()
        self.tutorial_list.clear()

        # Настройки кнопки
        settings = arcade.Sprite("Assets/Sprites/settingsBtn.jpg", 0.5, self.application.width // 2, 250)
        self.settings_list.append(settings)

        # Кнопка Play
        play = arcade.Sprite("Assets/Sprites/playBtn.jpg", 0.5, self.application.width // 2, 380)
        self.play_list.append(play)

        # Кнопка Escape
        escape = arcade.Sprite("Assets/Sprites/exitBtn.jpg", 0.5, self.application.width // 2, 130)
        self.escape_list.append(escape)

        #Кнопка Tutorial
        tutorial = arcade.Sprite("Assets/Sprites/openTutorialBtn.png", 0.3, self.application.width - 100, 130)
        self.tutorial_list.append(tutorial)

    def on_draw(self):
        self.clear()
        # Рисуем фон
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.application.width // 2,
                self.application.height // 2, self.application.width, self.application.height))
        # Рисуем кнопки
        self.settings_list.draw()
        self.escape_list.draw()
        self.play_list.draw()
        self.tutorial_list.draw()
        # Заголовок
        arcade.draw_text(TITLE, self.application.width // 2,
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
        
        if arcade.get_sprites_at_point((x, y), self.tutorial_list):
            self.open_tutorial()
            return
    
    def open_tutorial(self):
        try:
            file_path = self.application.settings["Application"]["Tutorial"]
            with open(file_path, 'r'):
                pass
            subprocess.run(['start', '', file_path], shell=True)
        except FileNotFoundError:
            pass


class SettingsView(arcade.View):
    """Экран настроек"""

    def __init__(self, application):
        super().__init__()
        self.application = application

    def on_draw(self):
        self.clear()
        arcade.set_background_color((126, 100, 145, 255))
        arcade.draw_text(
            text="Настройки",
            x=self.application.width // 2,
            y=self.application.height // 2,
            color=arcade.color.WHITE,
            font_size=50,
            anchor_x="center"
        )
        arcade.draw_text(
            text="Нажмите ESC для возврата",
            x=self.application.width // 2,
            y=self.application.height // 2 - 100,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center"
        )

    def on_update(self, delta_time):
        if InputSystem.on_key_down(InputSystem.Keys.ESCAPE):
            menu_view = MenuView(self.application)
            self.window.show_view(menu_view)


class PlayView(arcade.View):
    """Экран игры"""
    def __init__(self, application):
        super().__init__()
        self.application = application
        self.level1 = arcade.SpriteList()
        level1 = arcade.SpriteSolidColor(200, 200, 300, 450, (90, 0, 176, 255))
        self.level1.append(level1)
        self.level2 = arcade.SpriteList()
        level2 = arcade.SpriteSolidColor(200, 200, 700, 450, (90, 0, 176, 255))
        self.level2.append(level2)

    def on_draw(self):
        """Отрисовка меню выбора уровней"""
        self.clear()
        arcade.set_background_color((0, 126, 35, 0))
        arcade.draw_text("Выберите уровень", 500, 700, arcade.color.WHITE, 50, anchor_x="center")
        arcade.draw_text("Нажмите ESC для возврата", 500, 50, (255, 255, 255, 80), 20, anchor_x="center")
        arcade.draw_text("1 уровень", 300, 280, arcade.color.WHITE, 40, anchor_x="center")
        arcade.draw_text("Недоступно", 700, 280, arcade.color.RED, 40, anchor_x="center")
        self.level1.draw()
        self.level2.draw()

    def on_update(self, delta_time):
        if InputSystem.on_key_down(InputSystem.Keys.ESCAPE):
            menu_view = MenuView(self.application)
            self.window.show_view(menu_view)

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мышью"""
        # Уровень 1
        if arcade.get_sprites_at_point((x, y), self.level1):
            self.application.start_level(TestLevel(self.application))
            return

        # Уровень 2
        if arcade.get_sprites_at_point((x, y), self.level2):
            return