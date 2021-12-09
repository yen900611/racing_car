import pygame
from .env import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, coin_size[0], coin_size[1])
        self.rect.center = x ,y
        self.vel = 5

    def update(self, *args):
        self.rect.centerx -= self.vel
        if self.rect.centerx < -500:
            self.kill()

    def move(self):
        self.rect.centery += self.vel

    def get_position(self):
        return (self.rect.left, self.rect.top)
