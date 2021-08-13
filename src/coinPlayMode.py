from games.racing_car.src.coin import Coin
from .car import *
from .highway import *
from .gameMode import GameMode
from .env import *
import pygame
import random

class CoinMode(GameMode):
    def __init__(self, user_num: int, car_num, sound_controller):
        super(CoinMode, self).__init__()
        self.frame = 0
        pygame.font.init()
        self.cars_num = car_num

        '''set groups'''
        self.users = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.computerCars = pygame.sprite.Group()
        self.lanes = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.camera = Camera()
        '''sound'''
        self.sound_controller = sound_controller

        '''image'''
        self.bg_image = pygame.Surface((2000, HEIGHT))
        self.cars_info = []
        self.user_distance = []
        self.maxVel = 0
        self._init_lanes()
        # user數量
        for user in range(user_num):
            self._init_user(user)
        self.eliminated_user = []
        self.winner = []
        '''
        status incloud "GAME_ALIVE"、"GAME_PASS"、"GAME_OVER"
        '''
        self.status = "GAME_ALIVE"
        if user_num == 1:
            self.is_single = True
        else:
            self.is_single = False
        self.line = Line()
        self.background_x = 0
        self.bg_x = 0
        self.rel_x = 0
        self.lanes.add(self.line)
        self.end = False
        self.creat_coin_frame = 0
        self.end_frame = 0
        self.coin_lanes = [125, 175, 225, 275, 325, 375, 425, 475, 525]
        self.car_lanes = [110, 160, 210, 260, 310, 360, 410, 460, 510]
        for car in self.cars:
            self.cars_info.append(car.get_info())

    def update_sprite(self, command):
        '''update the model of src,call this fuction per frame'''
        self.count_bg()
        self.frame += 1
        self.handle_event()
        self._revise_speed()


        if self.status == "GAME_ALIVE":
            if self.frame > FPS*4:
                self._creat_computercar()
            if self.is_creat_coin():
                self.creat_coins()
            self.user_distance = []
            self.coin_num = []

            self.cars_info = []
            self.camera.update(self.maxVel)

            '''update sprite'''
            self.line.update()
            self.lanes.update(self.camera.position)
            self.line.rect.left = self.line.distance - self.camera.position +500
            self.coins.update()
            self.computerCars.update(self.cars)
            # self.background.update()

            for car in self.users:
                # self.user_out__screen(car)
                self.user_distance.append(car.distance)
                self.coin_num.append(car.coin_num)
                car.update(command["ml_" + str(car.car_no+1) + "P"])

            for car in self.cars:
                '''偵測車子的狀態'''
                self._detect_car_status(car)
                self.cars_info.append(car.get_info())

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
            pass

    # def user_out__screen(self,car):
    #     if car.status:
    #             if car.rect.right < -100 or car.rect.bottom > 550 or car.rect.top < 100:
    #                 self.sound_controller.play_lose_sound()
    #                 car.status = False

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

    def _init_user(self, user_no: int):
        self.car = UserCar((user_no)*100+160 , 0,user_no)
        self.users.add(self.car)
        self.cars.add(self.car)
        return None

    def _init_lanes(self):
        for i in range(8):
            for j in range(23):
                self.lane = Lane(i * 50+150, j * 50-150)
                self.lanes.add(self.lane)

    def _detect_car_status(self, car):
        if car.status:
            pass
        else:
            car.velocity = 0
            if car in self.users:
                car.image = car.image_list[1]
                if car not in self.eliminated_user:
                    self.eliminated_user.append(car)
            else:
                car.kill()


    def _is_game_end(self):
        if len(self.eliminated_user) == len(self.users):
            self.status = "GAME_OVER"
        if self.frame > FPS*60:
            self.status = "GAME_OVER"
        for car in self.users:
            if car.distance >= finish_line/2:
                self.status = "GAME_PASS"

    def _revise_speed(self):
        self.user_vel = []
        for car in self.users:
            self.user_vel.append(car.velocity)
        self.maxVel = max(self.user_vel)

    def count_bg(self):
        '''show the background and imformation on screen,call this fuction per frame'''
        super(CoinMode, self).count_bg()
        self.rel_x = self.background_x % self.bg_image.get_rect().width
        self.bg_x = self.rel_x - self.bg_image.get_rect().width
        self.background_x -= self.maxVel

    def _creat_computercar(self):
        if len(self.cars) < self.cars_num:
                x = random.choice([650,-700])
                y = random.choice(self.car_lanes)
                self.computerCar = ComputerCar(y,self.camera.position+x,x+500)
                self.computerCars.add(self.computerCar)
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

    def creat_coins(self):
        if self.frame - self.creat_coin_frame > FPS*2:
            coin = Coin(WIDTH,random.choice(self.coin_lanes))
            self.coin_lanes.remove(coin.rect.centery)
            self.all_sprites.add(coin)
            self.coins.add(coin)
            self.creat_coin_frame = self.frame
        if len(self.coin_lanes) == 0:
            self.coin_lanes = [125, 175, 225, 275, 325, 375, 425, 475, 525]
        else:
            pass

    def is_creat_coin(self):
        if self.maxVel >= 11:
            return True
        else:
            return False
