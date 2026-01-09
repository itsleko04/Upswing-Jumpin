import arcade
from Assets.GC import PLAYER_SPEED, PLAYER_JUMP_FORCE
from Assets.Scripts.Engine import Event


class Player(arcade.Sprite):
    """Базовая реализация игрока"""
    def __init__(self, path_or_texture, scale=1, x=0, y=0):
        super().__init__(path_or_texture, scale, center_x=x, center_y=y)
        self.is_freeze = False
        self.movement_speed = PLAYER_SPEED
        self.jump_force = PLAYER_JUMP_FORCE
        
        self.on_death = Event()

    def update(self, delta_time: float = 1 / 60):
        if self.is_freeze:
            self.change_x = 0
            self.change_y = 0
        if self.center_y <= -5:
            self.die()

    def freeze(self):
        self.is_freeze = True
    
    def unfreeze(self):
        self.is_freeze = False
    
    def on_jump_input(self):
        """Выполняется, когда пользователь вводит клавишу прыжка"""
        pass

    def die(self):
        """Вызывает событие on_death и удаляет из всех списков"""
        self.on_death.invoke()
        self.remove_from_sprite_lists()