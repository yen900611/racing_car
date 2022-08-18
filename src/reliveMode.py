from .car import *
from .highway import *
from .gameMode import GameMode
from .env import *
import pygame
import random
from mlgame.game.paia_game import GameResultState, GameStatus


class ReliveMode(GameMode):
    def __init__(self, user_num: int, car_num, length, sound_controller):
        super(ReliveMode, self).__init__(user_num, car_num, length, sound_controller)
        self.car_arrived = 0
        self.user_frames = [] # 使用者抵達終點所使用的時間
        self.limit_frame = length/1000 * 300

    def update(self, command):
        '''update the model of src,call this fuction per frame'''
        self.count_bg()
        self.frame += 1
        self.handle_event()
        self._revise_speed() # get the velocity of user, and revise max_vel

        if self.frame > FPS:
            if self.frame > FPS * 4:
                self._creat_computercar()

            self.camera.update(self.maxVel)

            '''update sprite'''
            self.lanes.update(self.camera.position)

            for car in self.users:
                self.user_out_screen(car)
                car.update(command[str(car.car_no + 1) + "P"])

            for car in self.cars:
                '''偵測車子的狀態'''
                self._detect_car_status(car)
                '''更新車子位置'''
                car.rect.left = car.distance - self.camera.position + 520
            self.computerCars.update(self.cars)

        if self._is_game_end(self.car_arrived):
            self.rank()
            self._print_result()
            self.running = False

    def _detect_car_status(self, car):
        super(ReliveMode, self)._detect_car_status(car)
        if car.state:
            pass
        else:
            if car in self.users:
                car.velocity = 0
            else:
                car.kill()

    def detect_collision(self):
        super(ReliveMode, self).detect_collision()
        for car in self.cars:
            self.cars.remove(car) # 如果sprite本身也在要偵測的group裡面就會被偵測到
            hits = pygame.sprite.spritecollide(car, self.cars, False)
            for hit in hits:
                if (hit.state and 0 < hit.rect.centerx < WIDTH):
                    self.sound_controller.play_hit_sound()
                if car in self.users:
                    if self.frame - car.cash_frame > 3*FPS:
                        car.velocity = 0
                        car.cash_frame = self.frame
                    # car.status = GameStatus.GAME_OVER
                else:
                    car.state = False
                if hit in self.users:
                    if self.frame - hit.cash_frame > 3*FPS:
                        hit.velocity = 0
                        hit.cash_frame = self.frame
                    # hit.status = GameStatus.GAME_OVER
                else:
                    hit.state = False
            self.cars.add(car)

    def _print_result(self):
        '''
        依照排名順序印出玩家遊戲結果，以字典形式顯示，包含以下項目：
        'player':標示玩家代號，顯示為1P、2P等
        'distance':記錄家此局所行走的距離
        'rank':顯示完家此局排名
        :return:None
        '''
        tem = []
        for user in self.winner:
            tem.append({"player": str(user.car_no + 1) + "P",
                        "distance": str(round(user.distance)) + "m",
                        "used_frames": str(user.used_frame)+" frames",
                        "single_rank": self.winner.index(user) + 1
                        })
            print({"player": str(user.car_no + 1) + "P",
                   "distance": str(round(user.distance)) + "m",
                    "used_frames": str(user.used_frame)+" frames",
                   "single_rank":self.winner.index(user)+1
                   })
        self.winner = tem

    def _is_game_end(self, car_arrived:int):
        '''
        判斷遊戲是否結束，遊戲結束的條件如下：
        1. 所有玩家皆抵達終點
        2. 首位玩家通過終點後再1000 frames
        :return:Bool
        '''
        end = True
        if self.frame >= self.limit_frame:
            return True
        if car_arrived == 0: # 尚未有車子通過終點
            for car in self.users:
                if self._is_car_arrive_end(car):
                    self.car_arrived = self.frame
        else:
            if self.frame - car_arrived > 1000:# 有玩家通過終點且已經過1000 frames
                return True
            else:
                for car in self.users:
                    if not self._is_car_arrive_end(car):
                        end = False
                if end:
                    return True
                else:
                    return False


    def _is_car_arrive_end(self, car):
        '''
        :param car: User
        :return: Bool
        '''
        if car.distance >= self.length:
            car.distance = self.length
            car.state = False
            return True
        return False

    def rank(self):
        '''
        如果玩家有通過終點則標示為GAME_PASS，反之為GAME_OVER
        排名先依據抵達終點所費之時間，若未抵達終點則以行進距離較遠者排名靠前
        '''
        self.user_distance = []
        for user in self.users:
            if user.distance >= self.length:
                user.status = GameStatus.GAME_PASS
                self.user_frames.append(user.used_frame)
            else:
                user.status = GameStatus.GAME_OVER
                self.user_distance.append(user.distance)
        while len(self.user_frames) > 0:
            for car in self.users:
                if self.user_frames:
                    if car.used_frame == min(self.user_frames):
                        self.winner.append(car)
                        self.user_frames.remove(car.used_frame)
        while len(self.user_distance) > 0:
            for car in self.users:
                if self.user_distance:
                    if car.distance == max(self.user_distance):
                        self.winner.append(car)
                        self.user_distance.remove(car.distance)
        # self.winner.reverse()

    def user_out_screen(self,car):
        if car.state:
            if car.rect.bottom > 540:
                if self.frame - car.cash_frame > 3 * FPS:
                    car.cash_frame = self.frame
                    car.velocity = 0
                car.rect.bottom = 540
            elif car.rect.top < 100:
                if self.frame - car.cash_frame > 3 * FPS:
                    car.velocity = 0
                    car.cash_frame = self.frame
                car.rect.top = 100


