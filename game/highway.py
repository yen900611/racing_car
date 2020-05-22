import pygame
from .env import *
# class HightWay():
#     def __init__(self):
#         # lanes is collection of lane and lane is a rect with white color
#         self.lanes = []
#         pass
#
#     def draw(self,screen):
#         # TODO　screen blit way here
#         pass
#
#     def update(self,car):
#         # TODO　update infomation you need here
#         # if lanes is out of screen , they will be reset their position
#         # according velocity of car , revise the position of car
#         pass

class Lane(pygame.sprite.Sprite):
    def __init__(self,x,y,maxVel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = x ,y
        self.vel = maxVel

    def update(self):
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        self.rect.centery += self.vel*2