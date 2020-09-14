from .car import *
from .highway import *
from .gameMode import GameMode
from .env import *
import pygame
import random
from .I_Commander import *

class PlayingMode(GameMode):
    def __init__(self, user_num: int):
        super(PlayingMode, self).__init__()
        self.cars = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.__init_user(user_num)

    def __init_user(self, user_num):
        l = []
        for i in range(user_num):
            l.append(i *2)
        for i in range(user_num):
            j = random.choice(l)
            self.user = UserCar(0,(j+1)*22.5,i)
            self.cars.add(self.user)
            self.all_sprites.add(self.user)
            l.remove(j)
        pass

    def __init_lanes(self):
        pass

    def update_sprite(self, command: list):
        self.frame += 1
        for car in self.cars:
            car.update(keyboardSet[car.car_no])
        pass

    def revise_camera(self):
        pass

    def end_ranking(self,user_info):

        pass

    def print_result(self):
        pass

    def detect_car_state(self, car):
        pass

    def is_game_end(self):
        pass

    def collide_with_cars(self, car):
        pass

    def is_car_arrive_end(self, car):
        pass

    def revise_speed_of_lane(self):
        pass

    def draw_bg(self):
        super(PlayingMode, self).draw_bg()
        self.screen.fill(GREY)
        for i in range(9):
            pygame.draw.line(self.screen,BLACK,(0,45*(i+1)),(900,45*(i+1)),2)

    def creat_computercar(self):
        for i in range(9):
            self.car = ComputerCar(0,(i+1)*22.5)
            self.cars.add(self.car)

        pass

    def draw_user_imformation(self):
        pass