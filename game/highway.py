import pygame
from .env import *

class Lane(pygame.sprite.Sprite):
    def __init__(self,y,distance):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(lane_size)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = distance+150,y
        self.distance = distance

    def update(self, camera):
        if self.rect.right < 0:
            self.distance += 1000
        self.rect.centerx = self.distance-camera+450
        # if self.rect.right > WIDTH:
        #     self.rect.left = 0
        # if self.rect.left < 0:
        #     self.rect.right = WIDTH
        # self.rect.centerx -= velocity*2

class Enviroment(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,450))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = 250,225
        self.distance = 100
        self.end_distance = finish_line

    def update(self, *args):
        if self.rect.right < 0:
            self.distance = self.end_distance
            self.image.fill(RED)
        else:
            pass