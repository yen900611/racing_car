"""
This is a base class for different mode in src.
"""
import pygame
from .env import *
from .car import Camera, UserCar, ComputerCar
from .highway import Lane, Line
import random
from mlgame.gamedev.game_interface import GameResultState, GameStatus

class GameMode(object):
    def __init__(self, user_num: int, car_num, sound_controller):
        self.bg_rect = pygame.Rect(0, 0, 2000, HEIGHT)
        self.running = True
        self.frame = 0
        '''sound'''
        self.sound_controller = sound_controller

        '''groups'''
        self.users = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.computerCars = pygame.sprite.Group()
        self.lanes = pygame.sprite.Group()
        self.camera = Camera()

        '''data set'''
        self.cars_num = car_num
        self.background_x = 0
        self.rel_x = 0
        self.bg_x = 0
        self.maxVel = 0
        self.user_distance = []
        self.eliminated_user = []
        self.winner = []
        if user_num == 1:
            self.is_single = True
        else:
            self.is_single = False

        '''initial object'''
        for user in range(user_num):
            self._init_user(user)
        self._init_lanes()
        self.line = Line()
        self.lanes.add(self.line)

        '''state include GameResultState.FINISH、GameResultState.FAIL"'''
        self.state = GameResultState.FAIL

    def handle_event(self):
        """ Handle the event from window , mouse or button.
        :return: None
        """
        pass

    def detect_collision(self):
        """ Detect the collision event between sprites.
        :return: None
        """
        pass

    def update(self, command):
        """ This function should update every sprite in games.
        :return: None
        """
        pass

    def count_bg(self):
        """  Draw a background on screen.
        :return:None
        """
        self.rel_x = self.background_x % self.bg_rect.width
        self.bg_x = self.rel_x - self.bg_rect.width
        self.background_x -= self.maxVel

    def isRunning(self) -> bool:
        return self.running

    def _init_user(self, user_no: int):
        self.car = UserCar(userCar_init_position[user_no], 0, user_no)
        self.users.add(self.car)
        self.cars.add(self.car)

    def _init_lanes(self):
        for i in range(8):
            for j in range(23):
                self.lane = Lane(i * 50+150, j * 50-150)
                self.lanes.add(self.lane)

    def _creat_computercar(self):
        if len(self.cars) < self.cars_num:
            for i in range(2):
                x, y = random.choice(computerCar_init_position)
                computerCar = ComputerCar(y, self.camera.position + x, x + 500)
                self.computerCars.add(computerCar)
                self.cars.add(computerCar)
            # x = random.choice([650, -700])
            # y = random.choice(self.car_lanes)

    def user_out_screen(self,car):
        if car.state:
            if car.rect.right < -100 or car.rect.bottom > 550 or car.rect.top < 100:
                self.sound_controller.play_lose_sound()
                car.state = False

    def _detect_car_status(self, car):
        if car.state:
            pass
        else:
            car.velocity = 0
            if car in self.users:
                if car not in self.eliminated_user:
                    car.status = GameStatus.GAME_OVER
                    self.eliminated_user.append(car)
                    self.user_distance.append(car.distance)
            else:
                car.kill()

    def _revise_speed(self):
        self.user_vel = []
        for car in self.users:
            self.user_vel.append(car.velocity)
        self.maxVel = max(self.user_vel)
