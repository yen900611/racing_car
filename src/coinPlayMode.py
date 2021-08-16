from .coin import Coin
from .car import *
from .highway import *
from .gameMode import GameMode
from .env import *
import pygame
import random

class CoinMode(GameMode):
    def __init__(self, user_num: int, car_num, sound_controller):
        super(CoinMode, self).__init__(user_num, car_num, sound_controller)
        self.coins = pygame.sprite.Group()

        '''image'''
        # self.line = Line() # TODO
        # self.lanes.add(self.line)
        self.create_coin_frame = 0
        self.end_frame = 0
        self.coin_lanes = [125, 175, 225, 275, 325, 375, 425, 475, 525] # TODO
        self.car_lanes = [110, 160, 210, 260, 310, 360, 410, 460, 510] # TODO

    def update(self, command):
        '''update the model of src,call this fuction per frame'''
        self.count_bg()
        self.frame += 1
        self.handle_event()
        self._revise_speed()


        if self.status == "GAME_ALIVE":
            if self.frame > FPS*4:
                self._creat_computercar()
            if self.is_create_coin():
                self.create_coins()
            self.user_distance = []
            self.coin_num = []

            self.camera.update(self.maxVel)

            '''update sprite'''
            # self.line.update()
            self.lanes.update(self.camera.position)
            # self.line.rect.left = self.line.distance - self.camera.position +500
            self.coins.update()
            self.computerCars.update(self.cars)
            # self.background.update()

            for car in self.users:
                # self.user_out__screen(car)
                self.user_distance.append(car.distance)
                self.coin_num.append(car.coin_num)
                car.update(command[str(car.car_no+1) + "P"])

            for car in self.cars:
                '''偵測車子的狀態'''
                self._detect_car_status(car)

                '''更新車子位置'''
                car.rect.left = car.distance - self.camera.position + 500

            self._is_game_end()

        elif self.status == ("GAME_PASS" or "GAME_OVER") and self.close == False:
            self.rank()
            self._print_result()
            self.close = True
            self.end_frame = self.frame
            pass
        else:
            if self.frame - self.end_frame > FPS:
                self.running = False
            pass

    def detect_collision(self):
        super(CoinMode,self).detect_collision()
        for car in self.cars:
            self.cars.remove(car)
            hits = pygame.sprite.spritecollide(car, self.cars, False)
            for hit in hits:
                if (hit.status == True and 0 < hit.rect.centerx < WIDTH):
                    self.sound_controller.play_hit_sound()
                hit.status = False
                car.status = False
            self.cars.add(car)
        for car in self.users:
            hits = pygame.sprite.spritecollide(car, self.coins, True)
            for hit in hits:
                self.sound_controller.play_coin_sound()
                car.coin_num += 1

    def _print_result(self):
        tem = []
        for user in self.winner:
            tem.append({"player":str(user.car_no + 1) + "P",
                   "coin":str(user.coin_num),
                   "distance":str(round(user.distance))+"m",
                    "rank": self.winner.index(user) + 1
                   })
            print({"player":str(user.car_no + 1) + "P",
                   "coin":str(user.coin_num),
                   "distance":str(round(user.distance))+"m",
                   })
        self.winner = tem

    def _is_game_end(self):
        if len(self.eliminated_user) == len(self.users):
            self.status = "GAME_OVER"
        if self.frame > FPS*60:
            self.status = "GAME_OVER"
        for car in self.users:
            if car.distance >= finish_line/2:
                self.status = "GAME_PASS"


    def _creat_computercar(self): #TODO
        if len(self.cars) < self.cars_num:
                x = random.choice([650,-700])
                y = random.choice(self.car_lanes)
                computerCar = ComputerCar(y,self.camera.position+x,x+500)
                self.computerCars.add(computerCar)
                self.cars.add(self.computerCar)
                self.car_lanes.remove(y)
        if len(self.car_lanes) == 0:
            self.car_lanes = [110, 160, 210, 260, 310, 360, 410, 460, 510]

    def rank(self):
        user_value = []
        for car in self.users:
            user_value.append(car.coin_num * 100000 + car.distance)
        while len(self.eliminated_user) != 0:
            for car in self.eliminated_user:
                car_value = car.coin_num * 100000 + car.distance
                if car_value == max(user_value):
                    self.winner.append(car)
                    user_value.remove(car_value)
                    self.eliminated_user.remove(car)

    def create_coins(self):
        if self.frame - self.create_coin_frame > FPS*2:
            coin = Coin(WIDTH,random.choice(self.coin_lanes))
            self.coin_lanes.remove(coin.rect.centery)
            self.coins.add(coin)
            self.create_coin_frame = self.frame
        if len(self.coin_lanes) == 0:
            self.coin_lanes = [125, 175, 225, 275, 325, 375, 425, 475, 525]
        else:
            pass

    def is_create_coin(self):
        if self.maxVel >= 11:
            return True
        else:
            return False
