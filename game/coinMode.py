from .gameMode import GameMode
from .env import *
from .coin import Coin
import pygame
import random
import time


class CoinPlayingMode(GameMode):
    def __init__(self, user_num):
        super(CoinPlayingMode, self).__init__(user_num)

    def create_coins(self):
        if time.time() - self.creat_coin_time > 1.6:
            coin = Coin(random.choice(self.coin_lanes), 0)
            self.coin_lanes.remove(coin.rect.centerx)
            self.all_sprites.add(coin)
            self.coins.add(coin)
            self.creat_coin_time = time.time()
        if len(self.coin_lanes) == 0:
            self.coin_lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]
        else:
            pass

    def collide_coins(self, car):
        hits = pygame.sprite.spritecollide(car, self.coins, True)
        for hit in hits:
            car.coin_num += 1

    def is_create_coin(self):
        if self.maxVel >= 12:
            self.is_crear_coin = True
        return self.is_crear_coin

    def is_car_arrive_end(self, car):
        if car.distance > end_line:
            user_coins = []
            for user in self.user_cars:
                user_coins.append(user.coin_num)
            for user in self.user_cars:
                if user.coin_num == min(user_coins):
                    user_coins.remove(user.coin_num)
                    user.state = False
                    self.detect_car_state(user)

    def draw_user_imformation(self):
        for car in self.user_cars:
            self.__draw_information(self.screen, "Player" + str(car.car_no + 1) +
                                  "(" + USER_COLOR[car.car_no] +")", 17, 715, (car.car_no) * 120 + 10)
            self.__draw_information(self.screen, "vel : " + str(round(car.velocity, 2)), 17, 715,
                                    (car.car_no) * 120 + 40)
            self.__draw_information(self.screen, "distance : " + str(abs(round(car.distance, 2))), 17, 715,
                                    (car.car_no) * 120 + 70)
            self.__draw_information(self.screen, "coins : " + str(car.coin_num), 17, 715,
                                    (car.car_no) * 120 + 100)
