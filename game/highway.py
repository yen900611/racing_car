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

class Enviroment(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,600))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (250,300)
        self.status = "START"
        pass

    def update(self,vel):
        if self.status == "START":
            self.rect.centerx -= vel
            if self.rect.right < 0:
                self.status = "FINISH"
                self.rect.centerx = finish_line
        else:
            self.rect.centerx -= vel

        pass
