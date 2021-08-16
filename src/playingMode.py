from .car import *
from .highway import *
from .gameMode import GameMode
from .env import *
import pygame
import random


class PlayingMode(GameMode):
    def __init__(self, user_num: int, car_num, sound_controller):
        super(PlayingMode, self).__init__(user_num, car_num, sound_controller)


        # self.line = Line() # TODO
        # self.lanes.add(self.line)
        self.end_frame = 0
        self.car_lanes = [110, 160, 210, 260, 310, 360, 410, 460, 510] # TODO

    def update(self, command):
        '''update the model of src,call this fuction per frame'''
        self.count_bg()
        self.frame += 1
        self.handle_event()
        self._revise_speed()

        if self.status == "GAME_ALIVE":
            if self.frame > FPS * 4:
                self._creat_computercar()
            self._is_game_end()

            self.camera.update(self.maxVel)
            self.user_distance = []

            '''update sprite'''
            # self.line.update()
            self.computerCars.update(self.cars)
            self.lanes.update(self.camera.position)
            # self.line.rect.left = self.line.distance - self.camera.position + 500

            for car in self.users:
                # self.user_out__screen(car)
                self.user_distance.append(car.distance)
                car.update(command[str(car.car_no + 1) + "P"])

                '''是否通過終點'''
                self._is_car_arrive_end(car)

            for car in self.cars:
                '''偵測車子的狀態'''
                self._detect_car_status(car)

                '''更新車子位置'''
                car.rect.left = car.distance - self.camera.position + 500

        elif self.status == ("GAME_PASS" or "GAME_OVER") and self.close == False:
            self.user_distance = []
            for user in self.users:
                self.user_distance.append(user.distance)
            self.rank()
            self._print_result()
            self.close = True
            # self.running = False
            pass
        else:
            if self.frame - self.end_frame > FPS * 3:
                self.running = False

    def detect_collision(self):
        super(PlayingMode, self).detect_collision()
        for car in self.cars:
            self.cars.remove(car)
            hits = pygame.sprite.spritecollide(car, self.cars, False)
            for hit in hits:
                if (hit.status == True and 0 < hit.rect.centerx < WIDTH):
                    self.sound_controller.play_hit_sound()
                hit.status = False
                car.status = False
            self.cars.add(car)

    def _print_result(self):
        tem = []
        for user in self.winner:
            tem.append({"player": str(user.car_no + 1) + "P",
                        "distance": str(round(user.distance)) + "m",
                        "rank": self.winner.index(user) + 1
                        })
            print({"player": str(user.car_no + 1) + "P",
                   "distance": str(round(user.distance)) + "m",
                   "rank":self.winner.index(user)+1
                   })
        self.winner = tem

    def _is_game_end(self):
        if len(self.users) - 1 == len(self.eliminated_user) and self.is_single == False:
            eliminated_user_distance = []
            for car in self.eliminated_user:
                eliminated_user_distance.append(car.distance)
            for car in self.users:
                if car not in self.eliminated_user and car.distance > max(eliminated_user_distance) + 100:
                    self.eliminated_user.append(car)
                    self.status = "GAME_PASS"
                    return None
                else:
                    pass
        elif len(self.eliminated_user) == len(self.users):
            self.status = "GAME_OVER"
        else:
            pass

    def _is_car_arrive_end(self, car):
        if car.distance > finish_line:
            for user in self.users:
                if user not in self.eliminated_user:
                    self.eliminated_user.append(user)
            self.status = "GAME_PASS"

    def _creat_computercar(self): #TODO
        # print(self.cars_num)
        if len(self.cars) < self.cars_num:
            x = random.choice([650, -700])
            y = random.choice(self.car_lanes)
            computerCar = ComputerCar(y, self.camera.position + x, x + 500)
            self.computerCars.add(computerCar)
            self.cars.add(computerCar)


    def rank(self):
        while len(self.eliminated_user) > 0:
            for car in self.eliminated_user:
                if car.distance == min(self.user_distance):
                    self.winner.append(car)
                    self.user_distance.remove(car.distance)
                    self.eliminated_user.remove(car)
        self.winner.reverse()
