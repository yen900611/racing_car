from .coin import Coin
from .car import *
from .highway import *
from .gameMode import GameMode
from .env import *
import pygame
import random
from mlgame.game.paia_game import GameResultState, GameStatus


class CoinMode(GameMode):
    def __init__(self, user_num: int, car_num, length, sound_controller):
        super(CoinMode, self).__init__(user_num, car_num, length, sound_controller)
        self.coins = pygame.sprite.Group()
        self.is_arrive = False

        '''image'''
        self.create_coin_frame = 0
        self.coin_lanes = [125, 175, 225, 275, 325, 375, 425, 475, 525]

    def update(self, command):
        '''update the model of src,call this fuction per frame'''
        self.count_bg()
        self.frame += 1
        self.handle_event()
        self._revise_speed()

        if self.frame > FPS:
            if self.frame > FPS * 3:
                self._creat_computercar()
            if self.is_create_coin():
                self.create_coins()
            self.user_distance = []
            self.coin_num = []

            self.camera.update(self.maxVel)

            '''update sprite'''
            self.lanes.update(self.camera.position)
            self.coins.update()
            self.computerCars.update(self.cars)

            for car in self.users:
                self.user_out_screen(car)
                self.coin_num.append(car.coin_num)
                car.update(command[str(car.car_no + 1) + "P"])
                if self._is_car_arrive_end(car):
                    self.is_arrive = True
                    self.eliminated_user.append(car)
                    self.user_distance.append(car.distance)
                    break # 任一玩家通過終點則結束遊戲

            for car in self.cars:
                '''偵測車子的狀態'''
                self._detect_car_status(car)

                '''更新車子位置'''
                car.rect.left = car.distance - self.camera.position + 520

            if self._is_game_end(self.is_arrive):
                self.rank()
                self._print_result()
                self.running = False

    def detect_collision(self):
        super(CoinMode, self).detect_collision()
        for car in self.cars:
            self.cars.remove(car)  # 如果sprite本身也在要偵測的group裡面就會被偵測到
            hits = pygame.sprite.spritecollide(car, self.cars, False)
            for hit in hits:
                if (hit.state and 0 < hit.rect.centerx < WIDTH):
                    self.sound_controller.play_hit_sound()
                hit.state = False
                car.state = False
            self.cars.add(car)
        for car in self.users:
            hits = pygame.sprite.spritecollide(car, self.coins, True)
            for hit in hits:
                self.sound_controller.play_coin_sound()
                car.coin_num += 1

    def _print_result(self):
        '''
        依照排名順序印出玩家遊戲結果，以字典形式顯示，包含以下項目：
        'player':標示玩家代號，顯示為1P、2P等
        'coin':記錄玩家此局獲得的金幣數量
        'distance':記錄家此局所行走的距離
        'rank':顯示完家此局排名
        :return:None
        '''
        tem = []
        for user in self.winner:
            tem.append({
                "player": str(user.car_no + 1) + "P",
                "coin": str(user.coin_num),
                "used_frames": str(user.used_frame)+" frames",
                "distance": str(round(user.distance)) + "m",
                "single_rank": self.winner.index(user) + 1
            })
            print({
                "player": str(user.car_no + 1) + "P",
                "coin": str(user.coin_num),
                "used_frames": str(user.used_frame)+" frames",
                "distance": str(round(user.distance)) + "m",
                "single_rank": self.winner.index(user) + 1
            })
        self.winner = tem

    def _is_game_end(self, is_arrive:bool):
        '''
        判斷遊戲是否結束，遊戲結束的條件如下：
        單人模式：抵達終點，或是玩家出局(FAIL)
        多人模式：一名或以上玩家抵達終點，或市場上僅餘一名玩家
        :return:Bool
        '''
        if is_arrive:
            self.state = GameResultState.FINISH
            return True
        if self.is_single:
            if len(self.eliminated_user) == 1:
                self.state = GameResultState.FAIL
                return True
            return False
        else:
            if len(self.users) <= len(self.eliminated_user):
                self.state = GameResultState.FINISH
                return True
            else:
                return False

    def _is_car_arrive_end(self, car):
        '''
        :param car: User
        :return: Bool
        '''
        if car.distance > self.length:
            car.status = GameStatus.GAME_PASS
            return True
        return False

    def rank(self):
        user_value = []
        for car in self.users:
            if car not in self.eliminated_user:
                car.status = GameStatus.GAME_PASS
                self.eliminated_user.append(car)
            user_value.append(car.coin_num * 100000 + car.distance)
        while len(self.eliminated_user) != 0:
            for car in self.eliminated_user:
                car_value = car.coin_num * 100000 + car.distance
                if car_value == max(user_value):
                    self.winner.append(car)
                    user_value.remove(car_value)
                    self.eliminated_user.remove(car)

    def create_coins(self):
        if self.frame - self.create_coin_frame > FPS * 1.5:
            coin = Coin(WIDTH, random.choice(self.coin_lanes))
            self.coin_lanes.remove(coin.rect.centery)
            self.coins.add(coin)
            self.create_coin_frame = self.frame
        if len(self.coin_lanes) == 0:
            self.coin_lanes = [125, 175, 225, 275, 325, 375, 425, 475, 525]
        else:
            pass

    def is_create_coin(self):
        if self.maxVel >= 8:
            return True
        else:
            return False
