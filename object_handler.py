from random import randrange
from npc import *
import random


class Object():
    def __init__(self, game):
        self.game = game
        self.npc_list = []

        self.last_spawn = 0
        self.cooldown_spawn = 5000
        self.now_spawn = 5000

        # npc map
        if self.game.level == 1:
            self.add_npc(Normal_Npc(game, pos=(14.0, 4.5)))
        if self.game.level == 2:
            # self.add_npc(Normal_Npc(game, pos=(2.0, 4.0)))
            # self.add_npc(Normal_Npc(game, pos=(11.5, 4.5)))
            # self.add_npc(Normal_Npc(game, pos=(13.5, 6.5)))
            # self.add_npc(Normal_Npc(game, pos=(14.0, 2.0)))
            # self.add_npc(Normal_Npc(game, pos=(6.0, 3.0)))
            # self.add_npc(Normal_Npc(game, pos=(8.0, 5.5)))
            # self.add_npc(Normal_Npc(game, pos=(4.0, 2.0)))
            # self.add_npc(Normal_Npc(game, pos=(7.0, 1.0)))
            self.add_npc(Big_Npc(game, pos=(9.0, 1.0)))
    

    def add_npc(self, npc):
        self.npc_list.append(npc)
    

    def update(self):
        if self.game.level == 2:
            if self.last_spawn == 0:
                self.spawn_pos = (2.0, 4.0)
            self.now_spawn = pygame.time.get_ticks()
            if self.now_spawn - self.last_spawn >= self.cooldown_spawn:
                self.last_spawn = self.now_spawn
                self.add_npc(Normal_Npc(self.game, pos = self.spawn_pos))
                self.cooldown_spawn -= 10
                pos_list = [(2.0, 4.0), (11.5, 4.5), (13.5, 6.5), (14.0, 2.0), (6.0, 3.0), (8.0, 5.5), (4.0, 2.0), (7.0, 1.0), (9.0, 1.0)]
                self.spawn_pos = random.choice(pos_list)
            if self.now_spawn - self.last_spawn > self.cooldown_spawn - 2000:
                pygame.draw.rect(self.game.screen, 'darkblue', (100 * (self.spawn_pos[0] - 0.5) , 100 * (self.spawn_pos[1] - 0.5), 100, 100))

        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        for npc in self.npc_list:
            npc.update()
            if not npc.alive:
                self.npc_list.remove(npc)
            if len(self.npc_list) == 0:
                self.game.victory = True
                self.game.game_active = False
                self.game.new_game()
        self.game.player.shot = False

