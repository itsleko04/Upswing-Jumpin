import arcade
from Assets.Scripts.Engine import InputSystem
from Assets.Scripts.Content.MarkdownReader import MarkdownView
from Assets.Scripts.Content.Levels.FirstLevel import FirstLevel
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UISlider
from Assets.Scripts.Content.UIButton import UIButton
from Assets.Sounds import UI_INTERACTION


class MenuView(arcade.View):
    """Стартовое меню"""

    def __init__(self, application):
        super().__init__()
        self.application = application
        self.texture = arcade.load_texture("Assets/Sprites/menuBG.jpg")
        self.ui_buttons = arcade.SpriteList()

    def on_show_view(self):
        """Настройка при показе меню"""
        self.ui_buttons.clear()

        # Настройки кнопки
        settings = UIButton("Assets/Sprites/settingsBtn.jpg", 0.5, self.application.width // 2, 250)
        settings.on_click.connect(lambda: self.window.show_view(SettingsView(self.application)))
        self.ui_buttons.append(settings)

        # Кнопка Play
        play = UIButton("Assets/Sprites/playBtn.jpg", 0.5, self.application.width // 2, 380)
        play.on_click.connect(lambda: self.window.show_view(PlayView(self.application)))
        self.ui_buttons.append(play)

        # Кнопка Escape
        escape = UIButton("Assets/Sprites/exitBtn.jpg", 0.5, self.application.width // 2, 130)
        escape.on_click.connect(lambda: self.application.exit())
        self.ui_buttons.append(escape)

        #Кнопка Tutorial
        tutorial = UIButton("Assets/Sprites/openTutorialBtn.png", 0.3, self.application.width - 100, 130)
        tutorial.on_click.connect(lambda: self.open_tutorial())
        self.ui_buttons.append(tutorial)

    def on_draw(self):
        self.clear()
        # Рисуем фон
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.application.width // 2,
                self.application.height // 2, self.application.width, self.application.height))
        # Рисуем кнопки
        self.ui_buttons.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мышью"""
        for button in self.ui_buttons:
            list = arcade.SpriteList()
            list.append(button)
            if arcade.get_sprites_at_point((x, y), list):
                button.click()
    
    def open_tutorial(self):
        file_path = self.application.settings["Application"]["Tutorial"]
        mdView = MarkdownView(self.application, filepath=file_path)
        self.application.window.show_view(mdView)


class SettingsView(arcade.View):
    """Экран настроек"""

    def __init__(self, application):
        super().__init__()
        self.application = application
        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.interact_sound = arcade.play_sound(arcade.load_sound(UI_INTERACTION), 
                                        volume=self.application.volume / 1000)
        self.interact_sound.pause()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        def set_volume_value(self, val):
            self.application.volume = val

        slider = UISlider(
            y=self.application.height - 100,
            width=200, 
            height=45, 
            min_value=0, 
            max_value=100, 
            value=self.application.volume
        )
        slider.on_change = lambda e: set_volume_value(self, e.new_value)
        slider.on_click = lambda e: self.interact_sound.play()
        self.box_layout.add(slider)

    def on_draw(self):
        self.clear()
        arcade.set_background_color((126, 100, 145, 255))
        arcade.draw_text(
            text="Настройки",
            x=self.application.width / 2,
            y=self.application.height - 90,
            color=arcade.color.WHITE,
            font_size=60,
            anchor_x="center"
        )
        arcade.draw_text(
            text="Громкость",
            x=self.application.width / 2,
            y=self.application.height / 2 + 60,
            color=arcade.color.WHITE,
            font_size=32,
            anchor_x="center"
        )
        arcade.draw_text("Нажмите ESC для возврата", 500, 50, (255, 255, 255, 80), 20, anchor_x="center")
        self.manager.draw()

    def on_update(self, delta_time):
        if InputSystem.on_key_down(InputSystem.Keys.ESCAPE):
            menu_view = MenuView(self.application)
            self.window.show_view(menu_view)
            self.interact_sound.play()

    def on_hide_view(self):
        self.manager.clear()

class PlayView(arcade.View):
    """Экран игры"""
    def __init__(self, application):
        super().__init__()
        self.application = application
        self.level1 = arcade.SpriteList()
        button_size = (200, 200)
        button_color = (173, 168, 175, 255)
        level1 = arcade.SpriteSolidColor(button_size[0], button_size[1], 300, 450, button_color)
        self.level1.append(level1)
        self.level2 = arcade.SpriteList()
        level2 = arcade.SpriteSolidColor(button_size[0], button_size[1], 700, 450, button_color)
        self.level2.append(level2)

        self.interact_sound = arcade.play_sound(arcade.load_sound(UI_INTERACTION), 
                                        volume=self.application.volume / 1000)
        self.interact_sound.pause()

    def on_draw(self):
        """Отрисовка меню выбора уровней"""
        self.clear()
        bg_color = (96, 117, 102, 255)
        arcade.set_background_color(bg_color)
        arcade.draw_text("Выберите уровень", 500, 700, arcade.color.WHITE, 50, anchor_x="center")
        arcade.draw_text("Нажмите ESC для возврата", 500, 50, (255, 255, 255, 80), 20, anchor_x="center")
        arcade.draw_text("1 уровень", 300, 280, arcade.color.WHITE, 40, anchor_x="center")
        arcade.draw_text("В разработке", 700, 280, arcade.color.RED, 40, anchor_x="center")
        self.level1.draw()
        self.level2.draw()

    def on_update(self, delta_time):
        if InputSystem.on_key_down(InputSystem.Keys.ESCAPE):
            menu_view = MenuView(self.application)
            self.window.show_view(menu_view)
            self.interact_sound.play()

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мышью"""
        # Уровень 1
        if arcade.get_sprites_at_point((x, y), self.level1):
            self.application.start_level(FirstLevel(self.application))
            self.interact_sound.play()
            return

        # Уровень 2
        if arcade.get_sprites_at_point((x, y), self.level2):
            self.interact_sound.play()
            return