import arcade


class Player(arcade.Sprite):
    def __init__(self, path_or_texture, scale=1, x=0, y=0):
        super().__init__(path_or_texture, scale, center_x=x, center_y=y)