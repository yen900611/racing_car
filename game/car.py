import pygame

from .I_Commander import I_Commander
from .env import *
import random

class Car(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 60))
        self.rect = self.image.get_rect()
        self.rect.center = x ,y
        self.state = True
        self.velocity = 0
        self.distance = 0
        self.car_no = 0
        self.car_info ={}

    def speedUp(self):
        self.velocity += 0.3

    def brakeDown(self):
        self.velocity -= 1.5

    def slowDown(self):
        if self.velocity > 1:
            self.velocity -= 0.3
        elif 0 <= self.velocity < 0.9:
            self.velocity += 0.3

    def moveRight(self):
        self.rect.centerx += 2

    def moveLeft(self):
        self.rect.centerx -= 2

    def get_velocity(self):
        return self.velocity

    def get_position(self):
        return self.rect.center

    def get_info(self):
        self.car_info = {"id":self.car_no,
                         "pos":self.get_position(),
                         "velocity":self.get_velocity()}
        return self.car_info

class UserCar(Car):
    def __init__(self, x, y, user_no):
        Car.__init__(self,x ,y)
        self.car_no = user_no
        self.image = pygame.transform.scale(pygame.image.load(path.join(IMAGE_DIR,user_image[self.car_no])), (40, 80))
        self.lastUpdateTime = pygame.time.get_ticks()

    def update(self,control_dic):
        self.handleKeyEvent(control_dic)
        self.keep_in_screen()
        self.distance +=self.velocity

    def keep_in_screen(self):
        if self.rect.left < 0 or self.rect.right > 420 or self.rect.centery > HEIGHT+35:
            self.velocity = 0
            self.state = False
        if self.rect.centery <200:
            self.rect.centery = 200
        if self.velocity > 15:
            self.velocity = 15
        elif self.velocity < 0:
            self.velocity = 0

    def handleKeyEvent(self,control_list:list):
        if "MOVE_LEFT" in control_list:
            self.moveLeft()
        if "MOVE_RIGHT" in control_list:
            self.moveRight()
        if pygame.time.get_ticks() - self.lastUpdateTime > 150:
            if "SPEED" in control_list:
                self.speedUp()
            elif "BRAKE" in control_list:
                self.brakeDown()
            else:
                self.slowDown()
            self.lastUpdateTime = pygame.time.get_ticks()

class ComputerCar(Car):
    def __init__(self,x,y,other_cars):
        Car.__init__(self ,x ,y)
        self.image = pygame.transform.scale(pygame.image.load(path.join(IMAGE_DIR,"電腦車2.png")),(40,80))
        self.other_cars = other_cars
        self.velocity = 0
        self.car_no = random.randrange(101,200)

    def update(self, *args):
        self.detect_other_cars(self.other_cars)
        self.rect.centery -= self.velocity
        self.speedUp()
        if self.rect.top >= HEIGHT+70 or self.rect.bottom < -70:
            self.state = False
        if self.velocity < 0:
            self.velocity = 0
        if self.velocity > 14:
            self.velocity = 14

    def detect_other_cars(self,other_cars):
        for each_car in other_cars:
            if abs(self.rect.centerx - each_car.rect.centerx) < 50:
                distance = self.rect.centery - each_car.rect.centery
                if 170 > distance > 0:
                    self.brakeDown()
            else:pass