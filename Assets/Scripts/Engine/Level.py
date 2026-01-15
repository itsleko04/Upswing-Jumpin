import arcade
from Assets.Scripts.Engine import Event
from Assets.Scripts.Content.PlayerModes import PlayerCube
from Assets.Scripts.Engine.GameOverView import GameOverView

from Assets.GC import GRAVITY, CAMERA_LERP


class Level(arcade.View):
    """
    Базовая реализация уровня в игре: \n
    Камера, игрок и тайлмап прогруженный с физическим движком
    """
    def __init__(self, application):
        super().__init__(application.window)
        self.application = application

        self.on_game_over = Event()
        self.is_game_over = False
        self.on_game_over.connect(self.__on_game_over_flag)
        self.cell_size = 51.2

    def setup(self, tilemap_path):
        self.is_game_over = False
        self.player_list = arcade.SpriteList()
        self.world_camera = arcade.camera.Camera2D()
        self.player = PlayerCube(self.application.settings["Sprites"]["PlayerIdle"], 0.075)
        self.player.left = self.cell_size * 11
        self.player.bottom = self.cell_size * 11
        self.player.on_death.connect(self.on_game_over.invoke)
        self.player_list.append(self.player)

        self.tile_map = arcade.load_tilemap(tilemap_path, scaling=0.1)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.shapes_list = self.scene["shapes"]
        self.jump_points = self.scene["jump_points"]
        self.autojumpers = self.scene["autojumpers"]
        #self.dash_arrows = self.scene["dash_arrows"]
        self.dash_arrows = []
        self.collision_list = self.scene["collision"]

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player, 
            walls=self.collision_list,
            gravity_constant=GRAVITY
        )

    def on_update(self, delta_time):
        if self.is_game_over:
            return
        self.player_list.update(delta_time)
        self.physics_engine.update()

        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            self.player.position,
            CAMERA_LERP
        )
                
        if len(self.jump_points) != 0:
            collided_jump_points_count = len(self.physics_engine.player_sprite.collides_with_list(self.jump_points))
            self.player.can_double_jump = collided_jump_points_count != 0

        if len(self.autojumpers) != 0:
            collided_autojumpers_count = len(self.physics_engine.player_sprite.collides_with_list(self.autojumpers))
            if collided_autojumpers_count != 0:
                self.player.change_y = 0
                self.player.on_jump_input()
        
        if len(self.dash_arrows) != 0:
            collided_dash_arrows_count = len(self.physics_engine.player_sprite.collides_with_list(self.dash_arrows))
            self.player.can_dash = collided_dash_arrows_count != 0

        if len(self.physics_engine.player_sprite.collides_with_list(self.shapes_list)) != 0:
            self.player.die()
            self.player = None
    
    def on_draw(self):
        self.clear()
        self.world_camera.use()
        for i in range(1, 20):
            rect = arcade.XYWH(self.window.rect.x * i, self.window.rect.y * 3, 
                               self.window.rect.width, self.window.rect.height)
            arcade.draw_texture_rect(self.bg, rect)
        self.scene.draw()
        self.player_list.draw()

    def __on_game_over_flag(self):
        self.is_game_over = True
        self.window.show_view(GameOverView(self.application))

    def __on_jump_input(self):
        if self.physics_engine.can_jump(5) and self.player.change_y == 0 or self.player.can_double_jump:
            self.player.change_y = 0
            self.player.on_jump_input()
        if self.player.can_dash:
            self.player.dashing = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.__on_jump_input()
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.player.dashing = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.__on_jump_input()

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player.dashing = False