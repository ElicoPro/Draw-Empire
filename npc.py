import pygame
from settings import *
from random import randrange
import math

MAX_DEPTH = 20

class Normal_Npc():
    def __init__(self, game, pos):
        self.game = game
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        self.alive = True
        self.x, self.y = pos
        self.npc_pos = [self.x * 100, self.y * 100]
        self.health = 100
        self.angle = 0
        self.speed = 0.017
        self.size = 20
        self.player_search = False
        self.mov_angle = math.radians(randrange(0, 360))
        

    def movement(self):
        if self.ray_cast_player_npc():
            self.player_search = True
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        if next_pos == self.map_pos:
            self.game.player.health -= 0.1
            if self.game.player.health <= 0:
                self.game.victory = False
                self.game.game_active = False
        next_x, next_y = next_pos


        # pygame.draw.rect(self.game.screen, 'blue', (100 * next_x, 100 * next_y, 100, 100))
        if next_pos not in self.game.object_handler.npc_positions:
            if self.player_search:
                self.mov_angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            else:
                self.mov_angle += math.radians(randrange(0, 20))
            dx = math.cos(self.mov_angle) * self.speed
            dy = math.sin(self.mov_angle) * self.speed
            self.check_wall_collision(dx, dy)

    
    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map


    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy
        self.npc_pos = [self.x * 100, self.y * 100]


    def check_hit(self):
        if self.alive:
            player_pos = [self.game.player.x, self.game.player.y]
            x_diff = (self.npc_pos[0] - player_pos[0] * 100)
            y_diff = (self.npc_pos[1] - player_pos[1] * 100)
            self.theta = math.atan2(y_diff, x_diff)
            if x_diff != 0:
                self.angle = math.degrees(math.atan2(y_diff, x_diff))
            diff = math.sqrt((math.pow(x_diff, 2) + math.pow(y_diff, 2)))
            if self.game.player.shot and self.ray_cast_player_npc():
                if diff < 200:
                    if self.angle < self.game.player.angle + 3 and self.angle > self.game.player.angle - 3:
                        self.health -= self.game.player.damage
                        if self.health <= 0:
                            self.alive = False
                elif diff >= 200 and diff <= 600:
                    if self.angle < self.game.player.angle + 2 and self.angle > self.game.player.angle - 2:
                        self.health -= self.game.player.damage
                        if self.health <= 0:
                            self.alive = False
                else:
                    if self.angle < self.game.player.angle + 1 and self.angle > self.game.player.angle - 1:
                        self.health -= self.game.player.damage
                        if self.health <= 0:
                            self.alive = False


    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
        if sin_a == 0:
            sin_a = 0.001
        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        if cos_a == 0:
            cos_a = 0.001
        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False


    def draw(self):
        if self.health > 50:
            pygame.draw.circle(self.game.screen, 'red', (self.x * 100, self.y * 100), 15)
        else:
            pygame.draw.circle(self.game.screen, 'orange', (self.x * 100, self.y * 100), 15)
        # if self.ray_cast_player_npc():
        #     pygame.draw.line(self.game.screen, 'white', (100 * self.game.player.x, 100 * self.game.player.y),
        #                 (100 * self.x, 100 * self.y), 2)
            
    
    def update(self):
        self.check_hit()
        self.movement()
        self.draw()


    @property
    def map_pos(self):
        return int(self.x), int(self.y)


class Big_Npc():
    def __init__(self, game, pos):
        self.game = game
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        self.alive = True
        self.x, self.y = pos
        self.npc_pos = [self.x * 100, self.y * 100]
        self.health = 3000
        self.angle = 0
        self.speed = 0.005
        self.size = 20
        self.player_search = False
        self.mov_angle = math.radians(randrange(0, 360))

        self.health_font = pygame.font.Font('Font/PublicPixel-z84yD.ttf', 20)

        self.Health_2 = self.health_font.render('BOSS HP', False, 'white')
        self.Health_rect_2 = self.Health_2.get_rect(center = (985, 35))
        

    def movement(self):
        if self.ray_cast_player_npc():
            self.player_search = True
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        if next_pos == self.map_pos:
            self.game.player.health -= 0.1
            if self.game.player.health <= 0:
                self.game.game_active = False
        next_x, next_y = next_pos

        # pygame.draw.rect(self.game.screen, 'blue', (100 * next_x, 100 * next_y, 100, 100))
        if next_pos not in self.game.object_handler.npc_positions:
            if self.player_search:
                self.mov_angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            else:
                self.mov_angle += math.radians(randrange(0, 20))
            dx = math.cos(self.mov_angle) * self.speed
            dy = math.sin(self.mov_angle) * self.speed
            self.check_wall_collision(dx, dy)

    
    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map


    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy
        self.npc_pos = [self.x * 100, self.y * 100]


    def check_hit(self):
        if self.alive:
            player_pos = [self.game.player.x, self.game.player.y]
            x_diff = (self.npc_pos[0] - player_pos[0] * 100)
            y_diff = (self.npc_pos[1] - player_pos[1] * 100)
            self.theta = math.atan2(y_diff, x_diff)
            if x_diff != 0:
                self.angle = math.degrees(math.atan2(y_diff, x_diff))
            diff = math.sqrt((math.pow(x_diff, 2) + math.pow(y_diff, 2)))
            if self.game.player.shot and self.ray_cast_player_npc():
                if diff < 200:
                    if self.angle < self.game.player.angle + 6 and self.angle > self.game.player.angle - 6:
                        self.health -= self.game.player.damage
                        if self.health <= 0:
                            self.alive = False
                elif diff >= 200 and diff <= 600:
                    if self.angle < self.game.player.angle + 4 and self.angle > self.game.player.angle - 4:
                        self.health -= self.game.player.damage
                        if self.health <= 0:
                            self.alive = False
                else:
                    if self.angle < self.game.player.angle + 2 and self.angle > self.game.player.angle - 2:
                        self.health -= self.game.player.damage
                        if self.health <= 0:
                            self.alive = False


    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
        if sin_a == 0:
            sin_a = 0.001
        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        if cos_a == 0:
            cos_a = 0.001
        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False


    def draw(self):
        if self.health > 50:
            pygame.draw.circle(self.game.screen, 'Red', (self.x * 100, self.y * 100), 30)
        else:
            pygame.draw.circle(self.game.screen, 'Orange', (self.x * 100, self.y * 100), 30)
        # if self.ray_cast_player_npc():
        #     pygame.draw.line(self.game.screen, 'white', (100 * self.game.player.x, 100 * self.game.player.y),
        #                  (100 * self.x, 100 * self.y), 2)
            
    
    def update(self):
        self.check_hit()
        self.movement()
        self.print_health()
        self.draw()
    

    def print_health(self):
        self.Health = self.health_font.render(str(format(self.health, ".0f")), False, 'white')
        self.Health_rect = self.Health.get_rect(center = (975, 65))
        self.game.screen.blit(self.Health, self.Health_rect)
        pygame.draw.rect(self.game.screen, 'black', (902, 2, 598, 96))
        self.game.screen.blit(self.Health, self.Health_rect)
        self.game.screen.blit(self.Health_2, self.Health_rect_2)
        pygame.draw.rect(self.game.screen, 'red', (1075, 40, 400, 20))
        pygame.draw.rect(self.game.screen, 'green', (1075, 40, self.health * 400 / 3000, 20))


    @property
    def map_pos(self):
        return int(self.x), int(self.y)
    