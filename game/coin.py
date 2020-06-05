import pygame
from .env import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y , maxVel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(path.join(IMAGE_DIR,"金幣.png")),(20,20))
        self.rect = self.image.get_rect()
        self.rect.center = x ,y
        self.vel = maxVel/2

    def update(self, *args):
        self.rect.centery += self.vel
        if self.rect.centery > HEIGHT:
            self.kill()