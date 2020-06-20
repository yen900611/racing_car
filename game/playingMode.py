
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
        self.startLine = 2 * HEIGHT / 3
        self.ceiling = 350
        self.end_line = 20000
        self.camera_vel = 0
        self.cars_num = 15
        # user數量
        for user in range(user_num):
            car = self.create_user(user)
        self.winner = []
        self.status = "ALIVE"
        self.creat_computerCar_time = pygame.time.get_ticks()
        self.lane_center = [35, 105, 175, 245, 315, 385, 455, 525, 595]
        self.touch_ceiling = False
        self.now_time = 0
        self.end = False

    def update_sprite(self, command: list):
        self.frame += 1
        self.handle_event()
        self.all_sprites.update()
        self.revise_speed_of_lane()
        self.creat_computercar()
        self.cars_info = []

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

            '''是否通過終點'''
            self.is_car_arrive_end(car)

            '''if user reach ceiling'''
            if car.rect.top <= self.ceiling :
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
        if self.end and time.time() - self.now_time > 3:
            if len(self.user_cars)==1:
                for car in self.user_cars:
                    car.state = False
                    self.detect_car_state(car)
            self.print_result()
            self.running = False
            self.status = "GAMEOVER"

    def print_result(self):
        self.winner.reverse()
        for user in self.winner:
            print("Rank" + str(self.winner.index(user)+1) +
                  " : Player " + str(user.car_no + 1))

    def revise_camera(self):
        if self.camera_vel < self.maxVel:
            self.camera_vel += 0.7
        elif self.camera_vel > self.maxVel+1:
            self.camera_vel -= 0.7
        else:
            pass

    def create_user(self, user_no: int):
        rect_x = random.choice(lane_center)
        lane_center.remove(rect_x)
        self.car = UserCar(rect_x, self.startLine, user_no)
        self.user_cars.add(self.car)
        self.cars.add(self.car)
        return self.car

    def create_lanes(self):
        self.lanes = []
        for i in range(1, 9):
            for j in range(30):
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

    def collide_with_cars(self, car):
        self.cars.remove(car)
        hits = pygame.sprite.spritecollide(car, self.cars, False)
        for hit in hits:
            if hit.distance > car.distance:
                car.state = False
                self.detect_car_state(car)
                hit.state = False
            else:
                hit.state = False
                self.detect_car_state(hit)
                car.state = False
            # self.carCrash.play()
        self.cars.add(car)

    def is_car_arrive_end(self, car):
        if car.distance > self.end_line:
            user_distance = []
            for user in self.user_cars:
                user_distance.append(user.distance)
            for user in self.user_cars:
                if user.distance == min(user_distance):
                    user_distance.remove(user.distance)
                    user.state = False
                    self.detect_car_state(user)

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
        pygame.draw.line(self.screen, WHITE, (630, 0), (630, 1000), 10)
        pygame.draw.line(self.screen, WHITE, (0, 0), (0, 1000), 10)

        '''畫出每台車子的資訊'''
        self.draw_user_imformation()

        self.all_sprites.draw(self.screen)
        self.user_cars.draw(self.screen)

        '''顯示出已出局的玩家'''
        for car in self.winner:
            self.draw_information(
                self.screen, "Player"+str(car.car_no+1), 17, 715, 730-self.winner.index(car)*20)

    def creat_computercar(self):
        if pygame.time.get_ticks() - self.creat_computerCar_time > 1200 and len(self.cars) < self.cars_num:
            for i in range(3):
                self.computerCar = ComputerCar(random.choice(
                    self.lane_center[i*3:i*3+3]), random.choice([HEIGHT + 120, -200]), self.cars)
                self.cars.add(self.computerCar)
                self.all_sprites.add(self.computerCar)
                self.creat_computerCar_time = pygame.time.get_ticks()

    def draw_user_imformation(self):
        for car in self.user_cars:
            self.draw_information(self.screen, "Player" + str(car.car_no+1) +
                                  "("+USER_COLOR[car.car_no]+")", 17, 715, (car.car_no) * 120 + 10)
            self.draw_information(self.screen, "vel : " + str(round(car.velocity, 2)), 17, 715,
                                  (car.car_no) * 120 + 40)
            self.draw_information(self.screen, "distance : " + str(abs(round(car.distance, 2))), 17, 715,
                                  (car.car_no) * 120 + 70)
