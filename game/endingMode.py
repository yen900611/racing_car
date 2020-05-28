import pygame
from .gameMode import GameMode
from .env import *

class EndMocde(GameMode):
    def __init__(self, winner_rank):
        super(EndMocde, self).__init__()
        self.running = True
        self.willChange = False
        self.winner_rank = winner_rank

    def draw_bg(self):
        super(EndMocde, self).draw_bg()
        self.bg_img.fill(BLACK)
        for user in self.winner_rank:
            self.draw_information(self.screen,
                                  "Rank"+str(len(self.winner_rank)-self.winner_rank.index(user))+" : Player "+str(user.car_no+1),
                                  25,
                                  300,
                                  300-self.winner_rank.index(user)*25)