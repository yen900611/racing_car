from .playingMode import PlayingMode
from .env import *
from .coin import Coin
import pygame
import random
import time


class CoinPlayingMode(PlayingMode):
    def __init__(self, user_num):
        super(CoinPlayingMode, self).__init__(user_num)
        self.creat_coin_time = time.time()
        self.coins = pygame.sprite.Group()
        self.coin_lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]
        self.is_crear_coin = False

    def update_sprite(self, command: list):
        self.frame += 1
        self.handle_event()
        self.all_sprites.update()
        self.revise_speed_of_lane()
        self.creat_computercar()
        self.cars_info = []
        if self.is_creat_coin():
            self.creat_coins()

        if self.maxVel >= 13:
            if self.touch_ceiling:
                self.camera_vel = self.maxVel
            else:
                self.camera_vel = self.maxVel - 2
        elif self.maxVel == 0:
            self.camera_vel = 1
        else:
            self.revise_camera()
        self.touch_ceiling = False

        for car in self.user_cars:
            car.update(command[car.car_no])
            self.collide_coins(car)

            '''是否通過終點'''
            self.is_car_arrive_end(car)

            '''if user reach ceiling'''
            if car.rect.top <= self.ceiling:
                self.touch_ceiling = True

        for car in self.cars:
            '''碰撞偵測'''
            self.collide_with_cars(car)
            '''偵測車子的狀態'''
            self.detect_car_state(car)
            self.cars_info.append(car.get_info())

            '''更新車子位置'''
            car.rect.centery += self.camera_vel - car.velocity

        if len(self.user_cars) <= 1 and self.end == False:
            self.now_time = time.time()
            self.end = True
        if self.end and time.time() - self.now_time > 3 or len(self.user_cars) == 0:
            if len(self.user_cars) == 1:
                for car in self.user_cars:
                    car.state = False
                    self.detect_car_state(car)
            self.print_result()
            self.running = False
            self.status = "GAMEOVER"

    def creat_coins(self):
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
        pass

    def is_creat_coin(self):
        if self.maxVel >= 12:
            self.is_crear_coin = True
        return self.is_crear_coin

    def is_car_arrive_end(self, car):
        if car.distance > self.end_line:
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
            self.draw_information(self.screen, "Player" + str(car.car_no+1) +
                                  "("+USER_COLOR[car.car_no]+")", 17, 715, (car.car_no) * 120 + 10)
            self.draw_information(self.screen, "vel : " + str(round(car.velocity, 2)), 17, 715,
                                  (car.car_no) * 120 + 40)
            self.draw_information(self.screen, "distance : " + str(abs(round(car.distance, 2))), 17, 715,
                                  (car.car_no) * 120 + 70)
            self.draw_information(self.screen, "coins : " + str(car.coin_num), 17, 715,
                                  (car.car_no) * 120 + 100)
