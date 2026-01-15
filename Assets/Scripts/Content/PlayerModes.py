from Assets.Scripts.Engine.Player import Player


class PlayerCube(Player):
    """Игрок в режиме куба"""
    def __init__(self, path_or_texture, scale=1, x=0, y=0):
        super().__init__(path_or_texture, scale, x=x, y=y)
        self.change_x = self.movement_speed
        self.can_double_jump = False
        self.can_dash = False
        self.dashing = False

    def update(self, delta_time = 1 / 60):
        super().update(delta_time)
        if self.dashing:
            self.change_y = 0
        if self.angle % 180 == 0:
            self.change_angle = 0
            self.angle = 0
    
    def jump(self):
        angle_speed = 5
        self.change_y += self.jump_force
        self.change_angle = angle_speed
        self.angle = angle_speed