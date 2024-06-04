import pygame

class Uiv:
    def __init__(self, game):
        self.game = game

        self.Blaster = pygame.image.load('Sprites/Blaster.png')
        self.Blaster_rect = self.Blaster.get_rect(center = (200, 850))

        self.Machine_gun = pygame.image.load('Sprites/Machine_gun.png')
        self.Machine_gun_rect = self.Machine_gun.get_rect(center = (400, 850))

        self.Sniper = pygame.image.load('Sprites/Sniper.png')
        self.Sniper_rect = self.Sniper.get_rect(center = (600, 850))


    def draw(self):
        if self.game.player.switcher == 1:
            pygame.draw.rect(self.game.screen, 'green', (100, 800, 200, 100))
        else:
            pygame.draw.rect(self.game.screen, 'red', (100, 800, 200, 100))
        if self.game.player.switcher == 2:
            pygame.draw.rect(self.game.screen, 'green', (300, 800, 200, 100))
        else:
            pygame.draw.rect(self.game.screen, 'red', (300, 800, 200, 100))
        if self.game.player.switcher == 3:
            pygame.draw.rect(self.game.screen, 'green', (500, 800, 200, 100))
        else:
            pygame.draw.rect(self.game.screen, 'red', (500, 800, 200, 100))
        self.game.screen.blit(self.Blaster, self.Blaster_rect)
        self.game.screen.blit(self.Machine_gun, self.Machine_gun_rect)
        self.game.screen.blit(self.Sniper, self.Sniper_rect)

