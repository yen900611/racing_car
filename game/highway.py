import pygame
from .env import *

class Lane(pygame.sprite.Sprite):
    def __init__(self,x,y,Vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = x ,y
        self.vel = Vel

    def update(self):
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        self.move()

    def move(self):
        self.rect.centery += self.vel * 2