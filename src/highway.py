import pygame
from .env import *

class Lane(pygame.sprite.Sprite):
    def __init__(self,y,distance):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, lane_size[0], lane_size[1])
        self.rect.center = distance+150,y
        self.distance = distance

    def update(self, camera):
        if self.rect.right < 0:
            self.distance += 1150
        self.rect.centerx = self.distance-camera+450

    def get_asset_info(self):
        return {
            "type": "rect",
            "name": "lane",
            "color": WHITE,
            "x": self.rect.x,
            "y": self.rect.y,
            "width": lane_size[0],
            "height": lane_size[1],
            "angle": 0
        }

class Line(pygame.sprite.Sprite):
    def __init__(self, length):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(80, 100, 45, 428)
        self.type = "start_line"
        self.distance = 60
        self.end_distance = length

    def update(self, camera):
        if self.rect.right < 0:
            self.distance = self.end_distance
            self.type = "start_line"
        else:
            pass
        self.rect.left = self.distance - camera + 520

    def get_asset_info(self):
        return {
            "type": "image",
            "x": self.rect.x,
            "y": self.rect.y,
            "width": 45,
            "height": 428,
            "image_id": self.type,
            "angle": 0
        }