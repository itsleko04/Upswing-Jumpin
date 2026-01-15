import arcade


class DashArrow(arcade.Sprite):
    def __init__(self, position):
        super().__init__(x=position[0], y=position[1])