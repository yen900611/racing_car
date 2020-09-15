import pygame
from .env import *

class Lane(pygame.sprite.Sprite):
    def __init__(self,x,y,Vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,3))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = x ,y
        self.vel = Vel

    def update(self):
        if self.rect.right > WIDTH:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.right = WIDTH
        self.rect.centerx -= self.vel*2