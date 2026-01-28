import arcade
import random
from arcade.particles import Emitter, EmitMaintainCount, FadeParticle
from Assets.Scripts.Engine import Event
from Assets.Scripts.Content.PlayerModes import PlayerCube
from Assets.Scripts.Content.GameResultView import GameResultView

from Assets.Scripts.Engine import InputSystem
from Assets.GC import GRAVITY, CAMERA_LERP


#region Система частиц
SPARK_TEX = [
    arcade.make_soft_circle_texture(20, arcade.color.ASH_GREY),
    arcade.make_soft_circle_texture(20, arcade.color.COOL_GREY),
    arcade.make_soft_circle_texture(20, arcade.color.BLUE_GRAY),
    arcade.make_soft_circle_texture(20, arcade.color.DARK_GRAY),
]


def make_trail(attached_sprite, maintain=60):
    # «След за объектом»: поддерживаем постоянное число частиц
    emit = Emitter(
        center_xy=(attached_sprite.center_x, attached_sprite.center_y),
        emit_controller=EmitMaintainCount(maintain),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=random.choice(SPARK_TEX),
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 1.6),
            lifetime=random.uniform(0.25, 0.45),
            start_alpha=220, end_alpha=0,
            scale=random.uniform(0.25, 0.4),
        ),
    )
    # Хитрость: каждое обновление будем прижимать центр к спрайту (см. ниже)
    emit._attached = attached_sprite
    return emit
#endregion


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
        self.player_trail = make_trail(self.player)
        
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

        self.player_tail_timer = 0
        self.gameplay_time = 0

    def on_update(self, delta_time):
        if self.is_game_over:
            return

        self.player_tail_timer += delta_time
        self.gameplay_time += delta_time
        
        jump_keys = (InputSystem.Keys.SPACE, InputSystem.Keys.MOUSE_LEFT)
        jumping = any([InputSystem.on_key(key) for key in jump_keys])
        if jumping:
            self.__try_to_jump()
        
        self.player_list.update(delta_time)
        self.physics_engine.update()

        if self.player_trail:
            self.player_trail.center_x = self.player.center_x
            self.player_trail.center_y = self.player.bottom + 5
            self.player_trail.update(delta_time)

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
        for i in range(1, 40):
            for j in range(1, 3):
                rect = arcade.XYWH(self.window.rect.x * i, self.window.rect.y * 2 * j, 
                               self.window.rect.width, self.window.rect.height)
                arcade.draw_texture_rect(self.bg, rect)
        self.scene.draw()
        if self.physics_engine.can_jump() and self.player_tail_timer > 0.75:
            self.player_trail.draw()
        self.player_list.draw()

    def __on_game_over_flag(self):
        self.is_game_over = True
        self.window.show_view(GameResultView(self.application, "Gameover",
                                            "Вы проиграли!", self.gameplay_time, is_win=False))

    def __on_level_finished(self):
        self.window.show_view(GameResultView(self.application, "VICTORY!!!",
                                            "Уровень пройден!", self.gameplay_time, is_win=True))

    def __try_to_jump(self):
        if self.physics_engine.can_jump() and self.player.change_y == 0 or self.player.can_double_jump:
            self.player.change_y = 0
            self.player.jump()
            self.player_tail_timer = 0
        if self.player.can_dash:
            self.player.dashing = True