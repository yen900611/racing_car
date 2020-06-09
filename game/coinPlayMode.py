from .playingMode import PlayingMode
from .env import *
from .coin import Coin
import pygame
import random

class CoinPlayingMode(PlayingMode):
    def __init__(self, user_num):
        super(CoinPlayingMode, self).__init__(user_num)
        self.creat_coin_time = pygame.time.get_ticks()

    def update_sprite(self,command:list):
        self.frame += 1
        self.handle_event()
        self.all_sprites.update()
        self.revise_speed_of_lane()
        self.creat_computercar()
        self.cars_info = []
        self.creat_coins()

        for car in self.user_cars:
            car.update(command[car.car_no])

            '''是否通過終點'''
            self.is_car_arrive_end(car)

            '''if user reach ceiling'''
            if car.rect.top <= self.ceiling and len(self.user_cars) > 1:
                self.camera_vel = self.maxVel
            else:
                self.revise_camera()

        for car in self.cars:
            '''碰撞偵測'''
            self.collide_with_cars(car)
            '''偵測車子的狀態'''
            self.detect_car_state(car)
            self.cars_info.append(car.get_info())

            '''更新車子位置'''
            car.rect.centery += self.camera_vel - car.velocity

        if len(self.user_cars) == 0:
            self.print_result()
            self.running = False
            self.status = "GAMEOVER"

    def creat_coins(self):
        if pygame.time.get_ticks() - self.creat_coin_time > 5000:
            coin = Coin(random.choice(self.lane_center), 0, self.maxVel)
            self.all_sprites.add(coin)
            self.creat_coin_time = pygame.time.get_ticks()
        pass

    def collide_coins(self,car):
        pass