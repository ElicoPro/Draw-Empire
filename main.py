import pygame
import sys
from settings import *
from map import * 
from player import *
from sound import *
from npc import *
from object_handler import *
from pathfinding import * 
from UIV import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()

        self.Font = pygame.font.Font('Font/PublicPixel-z84yD.ttf', 70)
        self.Text = self.Font.render('Draw empire', False, 'white')
        self.Text_rect = self.Text.get_rect(center = (800, 400))

        self.Info_font = pygame.font.Font('Font/PublicPixel-z84yD.ttf', 20)

        self.Secondary_font = pygame.font.Font('Font/PublicPixel-z84yD.ttf', 25)
        self.Text_bottom = self.Secondary_font.render('Press space to start', False, 'grey')
        self.Text_bottom_rect = self.Text_bottom.get_rect(center = (800, 600))
 
        self.Victory_text = self.Font.render('VICTORY', False, 'green')
        self.Victory_text_rect = self.Victory_text.get_rect(center = (800, 400))

        self.Lost_text = self.Font.render('YOU LOST', False, 'red')
        self.Lost_text_rect = self.Lost_text.get_rect(center = (800, 400))

        self.Green_ball = pygame.image.load('Sprites/Green_ball.png')
        self.Green_ball_rect = self.Green_ball.get_rect(center = (200, 200))

        self.Red_ball_1 = pygame.image.load('Sprites/Red_ball1.png')
        self.Red_ball_1_rect = self.Red_ball_1.get_rect(center = (1400, 600))

        self.level = 0
        self.delta_time = 0
        self.game_active = False

        self.level_text = self.Font.render('LEVEL ' + str(self.level + 1), False, 'white')
        self.level_text_rect = self.level_text.get_rect(center = (800, 400))

        self.victory = False
        self.info = False


    def new_game(self):
        self.sound = Sound(self)
        self.map = Map(self)
        self.uiv = Uiv(self)
        self.player = Player(self)
        self.object_handler = Object(self)
        self.pathfinding = PathFinding(self)


    def update(self):
        self.player.update()
        self.object_handler.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')


    def draw(self):
        self.screen.fill('black')
        self.map.draw()
        self.uiv.draw()
        self.player.draw()
    

    def check_events_active(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            self.player.single_shot_event(event)

    
    def check_events_disactive(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.level += 1
                self.new_game()
                self.game_active = True
            
            if self.level == 0:
                if not self.info:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                        self.new_game()
                        self.info = True
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                        self.info = False


    def home_screen(self):
        if self.level != 2:
            self.screen.blit(self.Text, self.Text_rect)
            self.screen.blit(self.Text_bottom, self.Text_bottom_rect)
            self.screen.blit(self.Green_ball, self.Green_ball_rect)
            self.screen.blit(self.Red_ball_1, self.Red_ball_1_rect)
        elif self.level == 2:
            if self.victory:
                self.screen.blit(self.Victory_text, self.Victory_text_rect)
            elif not self.victory:
                self.screen.blit(self.Lost_text, self.Lost_text_rect)


    def info_page(self):
        self.Info_text = self.Info_font.render('1. Aim with your mouse', False, 'grey')
        self.Info_text_rect = self.Text_bottom.get_rect(center = (1000, 150))
        self.screen.blit(self.Info_text, self.Info_text_rect)
        self.Info_text = self.Info_font.render('2. Shoot with right click', False, 'grey')
        self.Info_text_rect = self.Text_bottom.get_rect(center = (1000, 300))
        self.screen.blit(self.Info_text, self.Info_text_rect)
        self.Info_text = self.Info_font.render('3. Move with WASD', False, 'grey')
        self.Info_text_rect = self.Text_bottom.get_rect(center = (1000, 450))
        self.screen.blit(self.Info_text, self.Info_text_rect)
        self.Info_text = self.Info_font.render('4. Change weapon with Q and E', False, 'grey')
        self.Info_text_rect = self.Text_bottom.get_rect(center = (1000, 600))
        self.screen.blit(self.Info_text, self.Info_text_rect)
 
            

    def run(self):
        while True:
            if self.game_active:
                self.check_events_active()
                self.update()
                self.draw()
            else:
                if self.info:
                    self.info_page()
                    self.check_events_active()
                    self.update()
                    self.draw()              
                else:
                    self.screen.fill('black')
                    self.home_screen()
                self.check_events_disactive()
                pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()