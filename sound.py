import pygame

class Sound():
    def __init__(self, game):
        self.game = game
        pygame.mixer.init()
        self.laser = pygame.mixer.Sound('Sounds/Laser.wav')
        self.sniper = pygame.mixer.Sound('Sounds/Sniper.mp3')
        self.gun = pygame.mixer.Sound('Sounds/Machine-gun.wav')