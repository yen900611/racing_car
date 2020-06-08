import pygame

from .I_Commander import I_Commander
from .env import *
import random

class Car(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 80))
        self.rect = self.image.get_rect()
        self.rect.center = x ,y
        self.state = True
        self.velocity = 0
        self.distance = 0
        self.car_no = 0
        self.car_info ={}
        self.coin_num = 0

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

    def keep_in_screen(self):
        if self.rect.left < 0 or self.rect.right > 420 or self.rect.centery > HEIGHT+80:
            self.velocity = 0
            self.state = False

    def get_velocity(self):
        return self.velocity

    def get_position(self):
        return (self.rect.left, self.rect.top)

    def get_coin_num(self):
        return self.coin_num

    def get_info(self):
        self.car_info = {"id":self.car_no,
                         "pos":(self.rect.centerx,self.rect.centery),
                         "velocity":self.get_velocity(),
                         "coin_num":self.get_coin_num()}
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
        if self.rect.left < 0 or self.rect.right > 420 or self.rect.centery > HEIGHT+50:
            self.velocity = 0
            self.state = False
        if self.rect.centery <200:
            self.rect.centery = 200
        if self.velocity > 15:
            self.velocity = 15
        elif self.velocity < 0:
            self.velocity = 0

    def handleKeyEvent(self,control_list:list):
        if control_list == None:
            return True
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
        self.velocity = random.randrange(8,14)
        self.car_no = random.randrange(101,200)
        self.max_vel = random.randrange(10,14)

    def update(self, *args):
        self.keep_in_screen()
        self.detect_other_cars(self.other_cars)
        self.speedUp()
        if self.rect.centery < -150:
            self.state = False
        if self.velocity < 0:
            self.velocity = 0
        if self.velocity > self.max_vel:
            self.velocity = self.max_vel

    def detect_other_cars(self,other_cars):
        for each_car in other_cars:
            if abs(self.rect.centerx - each_car.rect.centerx) < 50:
                distance = self.rect.centery - each_car.rect.centery
                if 130 > distance > 0:
                    self.brakeDown()
            else:pass