from .I_Commander import *
from .car import *
from .highway import *
from .gameMode import GameMode
from .env import *
import pygame
import random
from .endingMode import EndMocde

class PlayingMode(GameMode):
    def __init__(self, user_num:int):
        super(PlayingMode, self).__init__()
        self.frame = 0
        '''音效初始化'''
        # pygame.mixer.init()
        # self.carCrash = pygame.mixer.Sound(path.join(SOUND_DIR,"Hit.wav"))

        pygame.font.init()

        '''建立User Group；Car Group'''
        self.user_cars = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.cars_info = []
        self.maxVel = 0
        self.create_lanes()
        self.startLine = 3 * HEIGHT / 4
        self.ceiling = HEIGHT / 4
        self.end_line = 20000
        self.camera_vel = 0
        self.cars_num = 10
        #user數量
        for user in range(user_num):
            car = self.create_user(user)
        self.winner = []
        self.status = "ALIVE"
        self.time = pygame.time.get_ticks()

    def update_sprite(self,command:list):
        self.frame += 1
        self.handle_event()
        self.all_sprites.update()

        self.cars_info = []

        for car in self.cars:
            '''碰撞偵測'''
            self.collide_with_cars(car)
            '''偵測車子的狀態'''
            self.detect_car_state(car)
            self.cars_info.append(car.get_info())

            '''更新車子位置'''
            car.rect.centery += self.camera_vel - car.velocity

        for car in self.user_cars:
            car.update(command[car.car_no])

            '''是否通過終點'''
            self.is_car_arrive_end(car)

            '''if user reach ceiling'''
            if car.rect.top <= self.ceiling and len(self.user_cars) > 1:
                self.camera_vel = self.maxVel
            else:
                self.revise_camera()

        if len(self.user_cars) == 0:
            self.print_result()
            self.running = False
            self.status = "GAMEOVER"

        self.revise_speed_of_lane()
        self.creat_computercar()

    def print_result(self):
        for user in self.winner:
            print("Rank" + str(len(self.winner) - self.winner.index(user)) + " : Player " + str(user.car_no + 1))

    def revise_camera(self):
        if self.camera_vel < self.maxVel:
            self.camera_vel += 0.5
        elif self.camera_vel > self.maxVel+1:
            self.camera_vel -= 0.5
        elif self.camera_vel == self.maxVel:
            self.camera_vel -= 3

    def create_user(self, user_no:int):
        self.car = UserCar(lane_center[user_no], self.startLine, user_no)
        self.user_cars.add(self.car)
        self.cars.add(self.car)
        return self.car

    def create_lanes(self):
        self.lanes = []
        for i in range(1, 6):
            for j in range(20):
                self.lane = Lane(i * 70, j * 60, self.maxVel)
                self.lanes.append(self.lane)
                self.all_sprites.add(self.lane)

    def detect_car_state(self, car):
        if car.state:
            pass
        else:
            car.velocity = 0
            if car in self.user_cars:
                self.winner.append(car)
            car.kill()

    def is_game_end(self):
        if 0 == len(self.user_cars):
            return True
        else:
            return False

    def collide_with_cars(self,car):
        self.cars.remove(car)
        hits = pygame.sprite.spritecollide(car, self.cars, False)
        for hit in hits:
            car.state = False
            hit.state = False
            # self.carCrash.play()
        self.cars.add(car)

    def is_car_arrive_end(self, car):
        if car.distance > self.end_line:
            for user in self.user_cars:
                user.state = False

    def revise_speed_of_lane(self):
        self.user_vel = []
        for car in self.user_cars:
            self.user_vel.append(car.velocity)
        if len(self.user_vel) != 0:
            self.maxVel = max(self.user_vel)
        self.user_cars.maxVel = self.maxVel
        for lane in self.lanes:
            lane.vel = self.maxVel

    def draw_bg(self):
        super(PlayingMode, self).draw_bg()
        self.bg_img.fill(GREY)
        pygame.draw.line(self.screen ,WHITE ,(420,0) ,(420,800) , 2)

        '''畫出每台車子的資訊'''
        self.draw_user_imformation()

        self.all_sprites.draw(self.screen)
        self.user_cars.draw(self.screen)

        '''顯示出已出局的玩家'''
        for car in self.winner:
            self.draw_information(self.screen, "Player"+str(car.car_no+1), 17, 510, 730-self.winner.index(car)*20)

    def creat_computercar(self):
        if len(self.cars) < self.cars_num:
            self.computerCar = ComputerCar(random.choice(lane_center), random.choice([HEIGHT + 40, -70]),self.cars)
            self.cars.add(self.computerCar)
            self.all_sprites.add(self.computerCar)

    def draw_user_imformation(self):
        for car in self.user_cars:
            self.draw_information(self.screen, "Player" + str(car.car_no+1), 17, 510, (car.car_no) * 120 + 10)
            self.draw_information(self.screen, "vel : " + str(round(car.velocity, 2)), 17, 510,
                                  (car.car_no) * 120 + 40)
            self.draw_information(self.screen, "distance : " + str(abs(round(car.distance, 2))), 17, 510,
                                  (car.car_no) * 120 + 70)
