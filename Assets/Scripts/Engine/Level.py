import arcade
import datetime
from Assets.Scripts.Engine import Event
from Assets.Scripts.Content.PlayerModes import PlayerCube
from Assets.Scripts.Content.GameResultView import GameResultView

from Assets.Scripts.Engine import InputSystem
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
        self.on_complete = Event()
        self.is_game_over = False
        self.on_game_over.connect(self.__on_game_over_flag)
        self.on_complete.connect(self.__on_level_finished)
        self.cell_size = 51.2

    def setup(self, tilemap_path):
        self.is_game_over = False
        self.player_list = arcade.SpriteList()
        self.player = PlayerCube(self.application.settings["Sprites"]["PlayerIdle"], 0.075)
        self.player.left = self.cell_size * 11
        self.player.bottom = self.cell_size * 11
        self.player.on_death.connect(self.on_game_over.invoke)
        self.player_list.append(self.player)
        
        self.world_camera = arcade.camera.Camera2D()
        self.world_camera.position = self.player.position

        self.tile_map = arcade.load_tilemap(tilemap_path, scaling=0.1)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.shapes_list = self.scene["shapes"]
        self.jump_points = self.scene["jump_points"]
        self.autojumpers = self.scene["autojumpers"]
        self.collision_list = self.scene["collision"]
        self.finish = self.scene["finish"]

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player, 
            walls=self.collision_list,
            gravity_constant=GRAVITY
        )

        self.gameplay_time = 0

    def on_update(self, delta_time):
        if self.is_game_over:
            return
        
        self.gameplay_time += delta_time
        
        jump_keys = (InputSystem.Keys.SPACE, InputSystem.Keys.MOUSE_LEFT)
        jumping = any([InputSystem.on_key_down(key) for key in jump_keys])
        if jumping:
            self.__try_to_jump()
        
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
                self.player.jump()

        if len(self.physics_engine.player_sprite.collides_with_list(self.shapes_list)) != 0:
            self.player.die()
            self.player = None
        
        if self.physics_engine.player_sprite.collides_with_list(self.finish):
            self.on_complete.invoke()
    
    def on_draw(self):
        self.clear()
        self.world_camera.use()
        for i in range(1, 20):
            rect = arcade.XYWH(self.window.rect.x * i, self.window.rect.y * 2, 
                               self.window.rect.width, self.window.rect.height)
            arcade.draw_texture_rect(self.bg, rect)
        self.scene.draw()
        self.player_list.draw()

    def __on_game_over_flag(self):
        self.is_game_over = True
        self.window.show_view(GameResultView(self.application, "Gameover", "Вы проиграли!", self.gameplay_time))

    def __on_level_finished(self):
        self.window.show_view(GameResultView(self.application, "VICTORY!!!", "Уровень пройден!", self.gameplay_time))

    def __try_to_jump(self):
        if self.physics_engine.can_jump(5) and self.player.change_y == 0 or self.player.can_double_jump:
            self.player.change_y = 0
            self.player.jump()
        if self.player.can_dash:
            self.player.dashing = True