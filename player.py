from settings import *
import pygame
import math


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.diag_move_corr = 1 / math.sqrt(2)
        self.map = [self.x, self.y]
        self.mouse_pos = pygame.mouse.get_pos()
        self.shot = False
        self.last = 0
        self.health = 100
        self.health_font = pygame.font.Font('Font/PublicPixel-z84yD.ttf', 20)

        self.Health_2 = self.health_font.render('HP', False, 'white')
        self.Health_rect_2 = self.Health_2.get_rect(center = (175, 35))

        self.switcher = 1

    
    def single_shot_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot:
                self.fire()
        if self.switcher == 2:
            now = pygame.time.get_ticks()
            self.cooldown = 50
            if now - self.last >= self.cooldown:
                mouse = pygame.mouse.get_pressed()
                if mouse[0]:
                    self.long_shot()
                    self.last = now
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.switcher += 1
            if self.switcher > 3:
                self.switcher = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self.switcher -= 1
            if self.switcher < 1:
                self.switcher = 3
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            self.switcher = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            self.switcher = 2
        if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            self.switcher = 3


    def long_shot(self):
        self.damage = 2
        self.shot = True
        self.game.sound.gun.play()
    

    def fire(self):
        now = pygame.time.get_ticks()

        if self.switcher == 1:
            self.cooldown = 500
            self.damage = 34
            if now - self.last >= self.cooldown:
                self.shot = True
                self.last = now
                self.game.sound.laser.play()

        # elif self.switcher == 2:
        #     self.cooldown = 50
        #     self.damage = 5
        #     if now - self.last >= self.cooldown:
        #         self.shot = True
        #         self.last = now
        #         self.game.sound.laser.play()
        
        elif self.switcher == 3:
            self.cooldown = 2500
            self.damage = 200
            if now - self.last >= self.cooldown:
                self.shot = True
                self.last = now
                self.game.sound.sniper.play()
                
 
    # Movement of the player
    def movement(self):
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time

        keys = pygame.key.get_pressed()
        num_key_pressed = -1
        if keys[pygame.K_w]:
            num_key_pressed += 1
            dy += -speed
        if keys[pygame.K_s]:
            num_key_pressed += 1
            dy += speed
        if keys[pygame.K_a]:
            num_key_pressed += 1
            dx += -speed
        if keys[pygame.K_d]:
            num_key_pressed += 1
            dx += speed

        # Diagonal movement correction
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

 
        self.check_wall_collision(dx, dy)

        # Make the line continous
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = list(self.mouse_pos)
        self.my_pos = [self.x * 100, self.y * 100]
        x_diff = (self.mouse_pos[0] - self.my_pos[0])
        y_diff = (self.mouse_pos[1] - self.my_pos[1])
        if x_diff != 0:
            if x_diff < 0:
                self.angle = math.degrees(math.atan2(y_diff, x_diff))
            else:
                self.angle = math.degrees(math.atan2(y_diff, x_diff))
        x_diff *= 100
        y_diff *= 100
        self.mouse_pos[0] += x_diff
        self.mouse_pos[1] += y_diff


    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy


    def draw(self):
        pygame.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                    self.mouse_pos, 2)
        pygame.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)


    def update(self):
        self.print_health()
        self.movement()
        

    
    def print_health(self):
        self.Health = self.health_font.render(str(format(self.health, ".0f")), False, 'white')
        self.Health_rect = self.Health.get_rect(center = (175, 65))
        pygame.draw.rect(self.game.screen, 'black', (102, 2, 598, 96))
        self.game.screen.blit(self.Health, self.Health_rect)
        self.game.screen.blit(self.Health_2, self.Health_rect_2)
        pygame.draw.rect(self.game.screen, 'red', (225, 40, 400, 20))
        pygame.draw.rect(self.game.screen, 'green', (225, 40, self.health * 4, 20))


    @property
    def pos(self):
        return self.x, self.y
 
    
    @property
    def map_pos(self):
        return int(self.x), int(self.y)