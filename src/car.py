import pygame
import time
from .env import *
import random
from mlgame.game.paia_game import GameStatus

class Car(pygame.sprite.Sprite):
    def __init__(self, y,distance):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(distance+20, y, car_size[0],car_size[1])
        self.state = True
        self.status = None
        self.velocity = 0
        self.distance = distance
        self.car_no = 0
        self.car_info = {}
        self.coin_num = 0
        self.max_vel = random.randint(10, 14)

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
        if self.rect.left < -500 or self.rect.right > 1500 or self.rect.top < 100:
            self.state = False

    def get_info(self):
        self.car_info = {"id": self.car_no,
                         "x":self.rect.x,
                         "y":self.rect.y,
                         "status":self.status,
                         "distance": self.distance,
                         "velocity": self.velocity,
                         "coin_num": self.coin_num}
        return self.car_info

class UserCar(Car):
    def __init__(self, y,distance,user_no):
        Car.__init__(self, y,distance)
        self.car_no = user_no
        self.status = GameStatus.GAME_ALIVE
        self.coin_num = 0
        self.max_vel = 15
        self.cash_frame = 0
        self.used_frame = 0

    def update(self, control_list):
        if self.state:
            self.used_frame += 1
            self.handleKeyEvent(control_list)
            self.distance += self.velocity
            self.keep_in_screen()
        else:
            pass

    def keep_in_screen(self):
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
        self.rect.left, self.rect.top = x, y
        self.velocity = random.randint(8,12)
        self.car_no = random.randrange(101, 200)
        self.distance = distance
        self.action = None

    def update(self,cars):
        if self.state:
            for car in cars:
                if abs(self.rect.centery - car.rect.centery) < 40:
                    self.detect_other_cars(car)
                else:
                    continue
                if self.action == "stop":
                    self.brakeDown()
                    break
                else:
                    self.speedUp()
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
        if 200 > distance > 0:
            self.action = "stop"
        else:
            self.action = "continue"

class Camera():
    def __init__(self, length):
        self.position = 500
        self.velocity = 0
        self.length = length

    def update(self,car_velocity):
        self.revise_velocity(car_velocity)
        self.position += self.velocity
        # if self.position > self.length:
        #     self.position = self.length

    def revise_velocity(self,car_velocity):
        if self.position > self.length:
            self.velocity = 0
            return None
        elif self.position > 20000:
            self.velocity = car_velocity+0.1
            return None

        if car_velocity >= 13.5:
            self.velocity = car_velocity-0.5

        elif car_velocity == 0:
            self.velocity = 0.01
        else:
            if self.velocity < car_velocity:
                self.velocity += 0.07
            elif self.velocity > car_velocity+1:
                self.velocity -= 0.07
            else:
                pass
