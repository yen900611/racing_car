import pygame
import time
from .I_Commander import I_Commander
from .env import *
import random

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(car_size)
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = x, y
        self.state = True
        self.velocity = 0
        self.distance = 0
        self.car_no = 0
        self.car_info = {}
        self.coin_num = 0
        self.max_vel = random.randrange(10, 14)

    def speedUp(self):
        self.velocity += 0.3

    def brakeDown(self):
        self.velocity -= 1.7

    def slowDown(self):
        if self.velocity > 1:
            self.velocity -= 0.3
        elif 0 <= self.velocity < 0.9:
            self.velocity += 0.3

    def moveRight(self):
        self.rect.centery += 3

    def moveLeft(self):
        self.rect.centery -= 3

    def keep_in_screen(self):
        if self.rect.left < 0 or self.rect.right > 630 or self.rect.centery > HEIGHT+200:
            self.velocity = 0
            self.state = False

    def get_info(self):
        self.car_info = {"id": self.car_no,
                         "pos": (self.rect.left, self.rect.top),
                         "distance": self.distance,
                         "velocity": self.velocity,
                         "coin_num": self.coin_num}
        return self.car_info


class UserCar(Car):
    def __init__(self, x, y, user_no):
        Car.__init__(self, x, y)
        self.car_no = user_no
        self.image = pygame.transform.scale(pygame.image.load(
            path.join(IMAGE_DIR, USER_IMAGE[self.car_no])), car_size)
        self.image = self.image.convert_alpha()
        self.lastUpdateTime = time.time()
        self.coin_num = 0
        self.max_vel = 15

    def update(self, control_list):
        self.handleKeyEvent(control_list)
        self.keep_in_screen()
        self.distance += self.velocity

    def keep_in_screen(self):
        if self.rect.left < -100 or self.rect.right > WIDTH+200 or self.rect.centery > 405 or self.rect.centery < 0:
            self.velocity = 0
            print("not in screen")
            self.state = False
        if self.rect.centerx > HEIGHT-100:
            self.rect.centerx = HEIGHT-100
        if self.velocity > self.max_vel:
            self.velocity = self.max_vel
        elif self.velocity < 0:
            self.velocity = 0

    def handleKeyEvent(self, control_list: list):
        if control_list == None:
            return True
        if LEFT_cmd in control_list:
            self.moveLeft()
            self.max_vel = 14.5
        elif RIGHT_cmd in control_list:
            self.moveRight()
            self.max_vel = 14.5
        else:
            self.max_vel = 15
        if time.time() - self.lastUpdateTime > 0.150:
            if SPEED_cmd in control_list:
                self.speedUp()
            elif BRAKE_cmd in control_list:
                self.brakeDown()
            else:
                self.slowDown()
            self.lastUpdateTime = time.time()


class ComputerCar(Car):
    def __init__(self, x, y, other_cars):
        Car.__init__(self, x, y)
        self.image = pygame.transform.scale(pygame.image.load(
            path.join(IMAGE_DIR, "電腦車2.png")), car_size)
        self.image = self.image.convert_alpha()
        self.other_cars = other_cars
        self.velocity = random.randrange(8, 14)
        self.car_no = random.randrange(101, 200)
        self.start_rect = x

    def update(self, *args):
        self.keep_in_screen()
        self.detect_other_cars(self.other_cars)
        self.speedUp()
        i = random.randint(0, 20)
        if i < 2:
            self.moveLeft()
        elif i > 18:
            self.moveRight()
        else:
            pass

        if self.rect.centerx < -210:
            self.state = False
        if self.velocity < 0:
            self.velocity = 0
        if self.velocity > self.max_vel:
            self.velocity = self.max_vel

    def detect_other_cars(self, other_cars):
        for each_car in other_cars:
            if abs(self.rect.centerx - each_car.rect.centerx) < 50:
                distance = self.rect.centery - each_car.rect.centery
                if 160 > distance > 0:
                    self.brakeDown()
            else:
                pass
