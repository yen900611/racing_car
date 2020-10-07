import pygame
import time
from .env import *
import random

class Car(pygame.sprite.Sprite):
    def __init__(self, y,distance):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(car_size)
        self.rect = self.image.get_rect()
        self.rect.centerx,self.rect.top = distance+150, y
        self.status = True
        self.velocity = 0
        self.distance = distance
        self.car_no = 0
        self.car_info = {}
        self.coin_num = 0
        self.max_vel = random.randrange(10, 14)

    def speedUp(self):
        self.velocity += 0.01*(self.velocity**0.6)+0.04

    def brakeDown(self):
        self.velocity -= 0.1

    def slowDown(self):
        if self.velocity > 1:
            self.velocity -= 0.3
        elif 0 <= self.velocity < 0.9:
            self.velocity += 0.3

    def moveRight(self):
        self.rect.centery += 4

    def moveLeft(self):
        self.rect.centery -= 4

    def keep_in_screen(self):
        if self.rect.left < -200 or self.rect.right > 1200 or self.rect.top < 0:
            self.kill()

    def get_info(self):
        self.car_info = {"id": self.car_no,
                         "pos": (self.rect.left, self.rect.top),
                         "distance": self.distance,
                         "velocity": self.velocity,
                         "coin_num": self.coin_num}
        return self.car_info

class UserCar(Car):
    def __init__(self, y,distance,user_no):
        Car.__init__(self, y,distance)
        self.car_no = user_no
        self.image = pygame.transform.scale(pygame.image.load(
            path.join(IMAGE_DIR, USER_IMAGE[self.car_no][0])), car_size)
        self.image = self.image.convert_alpha()
        self.lastUpdateTime = time.time()
        self.coin_num = 0
        self.max_vel = 15

    def update(self, control_list):
        if self.status:
            self.handleKeyEvent(control_list)
            self.distance += self.velocity
        else:
            pass
        self.keep_in_screen()

    def keep_in_screen(self):
        if self.rect.right < -100 or self.rect.bottom > 450 or self.rect.top < 0:
            self.status = False
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

        if RIGHT_cmd in control_list:
            self.moveRight()
            self.max_vel = 14.5
        if LEFT_cmd not in control_list and RIGHT_cmd not in control_list:
            self.max_vel = 15
        if SPEED_cmd in control_list:
            self.speedUp()
        elif BRAKE_cmd in control_list:
            self.brakeDown()
        else:
            self.slowDown()

class ComputerCar(Car):
    def __init__(self, y,distance):
        Car.__init__(self,y,distance)
        self.image = pygame.transform.scale(pygame.image.load(
            path.join(IMAGE_DIR, COMPUTER_CAR_IMAGE[0])), car_size)
        self.image = self.image.convert_alpha()
        self.velocity = random.randrange(10, 14)
        self.car_no = random.randrange(101, 200)
        self.distance = distance

    def update(self,car):
        if self.status:
            self.detect_other_cars(car)
            self.speedUp()
            if self.velocity < 0:
                self.velocity = 0
            if self.velocity > self.max_vel:
                self.velocity = self.max_vel
            pass
        else:
            pass
        self.keep_in_screen()

    def detect_other_cars(self, car):
        if abs(self.rect.centery - car.rect.centery) < 40:
            distance = car.rect.centerx - self.rect.centerx
            if 300 > distance > 0:
                self.brakeDown()
            else:
                pass

class Camera():
    def __init__(self):
        self.position = 300
        self.velocity = 0

    def update(self,car_velocity):
        self.revise_velocity(car_velocity)
        self.position += self.velocity

    def revise_velocity(self,car_velocity):
        if car_velocity >= 13:
            self.velocity = car_velocity-1

        elif car_velocity == 0:
            self.velocity = 1
        else:
            if self.velocity < car_velocity:
                self.velocity += 0.1
            elif self.velocity > car_velocity+1:
                self.velocity -= 0.1
            else:
                pass