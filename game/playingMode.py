from .car import *
from .highway import *
from .gameMode import GameMode
from .env import *
import pygame
import random

class PlayingMode(GameMode):
    def __init__(self, user_num: int):
        super(PlayingMode, self).__init__()
        self.frame = 0
        pygame.font.init()

        '''set groups'''
        self.users = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.computerCars = pygame.sprite.Group()
        self.lanes = pygame.sprite.Group()

        self.cars_info = []
        self.maxVel = 0
        self._init_lanes()
        self.camera_vel = 0
        # user數量
        for user in range(user_num):
            self._init_user(user)
        self.winner = []
        self.status = "ALIVE"
        self.touch_ceiling = False
        self.now_time = 0
        self.end = False

    def update_sprite(self, command: list):
        '''update the model of game,call this fuction per frame'''
        self.frame += 1
        self.handle_event()
        self.lanes.update(self.maxVel)
        self._revise_speed_of_lane()
        self._creat_computercar()
        self.cars_info = []

        if self.maxVel >= 13:
            if self.touch_ceiling:
                self.camera_vel = self.maxVel
            else:
                self.camera_vel = self.maxVel - 2

        elif self.maxVel == 0:
            self.camera_vel = 1
        else:
            self._revise_camera()
        self.touch_ceiling = False

        for car in self.users:
            car.update(command[car.car_no])

            '''是否通過終點'''
            self._is_car_arrive_end(car)

            '''if user reach ceiling'''
            if car.rect.top <= ceiling:
                self.touch_ceiling = True

        for car in self.cars:

            '''偵測車子的狀態'''
            self._detect_car_state(car)
            self.cars_info.append(car.get_info())

            '''更新車子位置'''
            car.rect.centerx += self.camera_vel - car.velocity

        if len(self.users) <= 1 and self.end == False:
            self.now_time = time.time()
            self.end = True
        if self.end and time.time() - self.now_time > 3 or len(self.users) == 0:
            if len(self.users) == 1:
                for car in self.users:
                    car.state = False
                    self._detect_car_state(car)
            self._print_result()
            self.running = False
            self.status = "GAMEOVER"

    def detect_collision(self):
        super(PlayingMode,self).detect_collision()
        for car in self.cars:
            self.cars.remove(car)
            hits = pygame.sprite.spritecollide(car, self.cars, True)
            for hit in hits:
                car.state = False
            self.cars.add(car)

    def _print_result(self):
        self.winner.reverse()
        for user in self.winner:
            print("Rank" + str(self.winner.index(user)+1) +
                  " : Player " + str(user.car_no + 1))

    def _revise_camera(self):
        if self.camera_vel < self.maxVel:
            self.camera_vel += 0.7
        elif self.camera_vel > self.maxVel+1:
            self.camera_vel -= 0.7

        else:
            pass

    def _init_user(self, user_no: int):
        self.car = UserCar(startLine,(user_no)*100+60 , user_no)
        self.users.add(self.car)
        self.cars.add(self.car)
        return None

    def _init_lanes(self):
        for i in range(1, 9):
            for j in range(50):
                self.lane = Lane(j * 60, i * 50)
                self.lanes.add(self.lane)

    def _detect_car_state(self, car):
        if car.state:
            pass
        else:
            car.velocity = 0
            if car in self.users:
                self.winner.append(car)
            car.kill()

    def _is_game_end(self):
        if 0 == len(self.users):
            return True
        else:
            return False

    def _is_car_arrive_end(self, car):
        if car.distance > end_line:
            user_distance = []
            for user in self.users:
                user_distance.append(user.distance)
            for user in self.users:
                if user.distance == min(user_distance):
                    user_distance.remove(user.distance)
                    user.state = False
                    self._detect_car_state(user)

    def _revise_speed_of_lane(self):
        self.user_vel = []
        for car in self.users:
            self.user_vel.append(car.velocity)
        if len(self.user_vel) != 0:
            self.maxVel = max(self.user_vel)
        self.users.maxVel = self.maxVel
        for lane in self.lanes:
            lane.vel = self.maxVel

    def draw_bg(self):
        '''show the background and imformation on screen,call this fuction per frame'''
        super(PlayingMode, self).draw_bg()
        self.bg_img.fill(GREY)
        pygame.draw.line(self.screen, WHITE, (0, 450), (WIDTH, 450), 5)

        '''畫出每台車子的資訊'''
        self._draw_user_imformation()

        self.all_sprites.draw(self.screen)
        self.users.draw(self.screen)

        '''顯示出已出局的玩家'''
        # for car in self.winner:
        #     self.draw_information(
        #         self.screen, "Player"+str(car.car_no+1), 17, 715, 730-self.winner.index(car)*20)

    def drawAllSprites(self):
        '''show all cars and lanes on screen,call this fuction per frame'''
        super(PlayingMode,self).drawAllSprites()
        self.lanes.draw(self.screen)
        self.cars.draw(self.screen)

    def _creat_computercar(self):
        if len(self.cars) < cars_num:
            for i in range(3):
                x = random.randint(0,8)
                self.computerCars = ComputerCar(random.choice([WIDTH + 120, -200]), x * 50 +10, self.cars)
                self.cars.add(self.computerCars)
                self.creat_computerCar_time = pygame.time.get_ticks()

    def _draw_user_imformation(self):
        pass
        # for car in self.user_cars:
        #     self.draw_information(self.screen, "Player" + str(car.car_no+1) +
        #                           "("+USER_COLOR[car.car_no]+")", 17, 715, (car.car_no) * 120 + 10)
        #     self.draw_information(self.screen, "vel : " + str(round(car.velocity, 2)), 17, 715,
        #                           (car.car_no) * 120 + 40)
        #     self.draw_information(self.screen, "distance : " + str(abs(round(car.distance, 2))), 17, 715,
        #                           (car.car_no) * 120 + 70)
