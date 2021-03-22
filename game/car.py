import pygame
import time
from .env import *
import random

class Car(pygame.sprite.Sprite):
    def __init__(self, y,distance):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(car_size)
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = distance, y
        self.status = True
        self.velocity = 0
        self.distance = distance
        self.car_no = 0
        self.car_info = {}
        self.coin_num = 0
        self.max_vel = random.randint(10, 16)

    def speedUp(self):
        self.velocity += 0.01*(self.velocity**0.6)+0.04

    def brakeDown(self):
        self.velocity -= 0.2

    def slowDown(self):
        if self.velocity > 1:
            self.velocity -= 0.05
        elif 0 <= self.velocity < 0.9:
            self.velocity += 0.3
    def moveRight(self):
        self.rect.centery += 3

    def moveLeft(self):
        self.rect.centery -= 3

    def keep_in_screen(self):
        if self.rect.left < -250 or self.rect.right > 1300 or self.rect.top < 100:
            self.status = False

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
        self.image_list = [pygame.transform.scale(pygame.image.load(
            path.join(IMAGE_DIR, USER_IMAGE[self.car_no][0])), car_size), pygame.transform.scale(pygame.image.load(
            path.join(IMAGE_DIR, USER_IMAGE[self.car_no][1])), car_size)]

        self.image = self.image_list[0]
        self.image = self.image.convert_alpha()
        self.lastUpdateTime = time.time()
        self.coin_num = 0
        self.max_vel = 15

    def update(self, control_list):
        if self.status:
            self.handleKeyEvent(control_list)
            self.distance += self.velocity
            self.keep_in_screen()
        else:
            pass


    def keep_in_screen(self):
        if self.rect.top < 100 or self.rect.bottom > 550:
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
    def __init__(self, y,distance,x):
        Car.__init__(self,y,distance)
        self.image_list = [pygame.transform.scale(pygame.image.load(
            path.join(IMAGE_DIR, COMPUTER_CAR_IMAGE[0])), car_size),pygame.transform.scale(pygame.image.load(
            path.join(IMAGE_DIR, COMPUTER_CAR_IMAGE[1])), (32,40))]
        self.image = self.image_list[0]
        self.rect.left, self.rect.top = x, y
        self.image = self.image.convert_alpha()
        self.velocity = random.randint(8,12)
        self.car_no = random.randrange(101, 200)
        self.distance = distance
        self.action = None

    def update(self,cars):
        if self.status:
            for car in cars:
                if abs(self.rect.centery - car.rect.centery) < 40:
                    self.detect_other_cars(car)
                else:
                    continue
                if self.action == "stop":
                    self.brakeDown()
                    break
                elif self.action == "continue":
                    self.speedUp()
                else:
                    pass
            self.distance += self.velocity
            if self.velocity < 0:
                self.velocity = 0
            if self.velocity > self.max_vel:
                self.velocity = self.max_vel
            pass
        else:
            pass
        self.keep_in_screen()

    def detect_other_cars(self, car):
        distance = car.rect.centerx - self.rect.centerx
        if 400 > distance > 0:
            self.action = "stop"
        else:
            self.action = "continue"

    def re_create(self, distance):
        self.distance = distance

class Camera():
    def __init__(self):
        self.position = 500
        self.velocity = 0

    def update(self,car_velocity):
        self.revise_velocity(car_velocity)
        self.position += self.velocity

    def revise_velocity(self,car_velocity):
        if car_velocity >= 13:
            self.velocity = car_velocity-0.5

        elif car_velocity == 0:
            self.velocity = 1
        else:
            if self.velocity < car_velocity:
                self.velocity += 0.05
            elif self.velocity > car_velocity+1:
                self.velocity -= 0.05
            else:
                pass