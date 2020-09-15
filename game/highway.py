import pygame
from .env import *

class Lane(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(lane_size)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = x ,y

    def update(self, velocity):
        if self.rect.right > WIDTH:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.right = WIDTH
        self.rect.centerx -= velocity*2