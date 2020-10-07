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
        self.camera = Camera()

        self.cars_info = []
        self.user_distance = []
        self.maxVel = 0
        self._init_lanes()
        # user數量
        for user in range(user_num):
            self._init_user(user)
        self.eliminated_user = []
        '''
        status incloud "START"、"RUNNING"、"END"
        '''
        self.status = "START"
        if user_num == 1:
            self.is_single = True
        else:
            self.is_single = False
        self.line = Enviroment()
        self.lanes.add(self.line)
        self.end = False

    def update_sprite(self, command: list):
        '''update the model of game,call this fuction per frame'''
        self.frame += 1
        self.handle_event()

        if self.status == "START" and self.frame > FPS*3:
            self.status = "RUNNING"
            pass
        elif self.status == "RUNNING":
            self._revise_speed_of_lane()
            self._creat_computercar()
            self.cars_info = []
            self.camera.update(self.maxVel)

            '''update sprite'''
            self.line.update()
            self.lanes.update(self.camera.position)
            self.line.rect.centerx = self.line.distance - self.camera.position +450

            for car in self.users:
                self.computerCars.update(car)
                car.update(command[car.car_no])

                '''是否通過終點'''
                self._is_car_arrive_end(car)

            for car in self.cars:
                '''偵測車子的狀態'''
                self._detect_car_status(car)
                self.cars_info.append(car.get_info())
                if car.status:
                    self.user_distance.append(car.distance)

                '''更新車子位置'''
                car.rect.centerx = car.distance - self.camera.position + 450

            for car in self.eliminated_user:
                self.user_distance.append(car.distance)
            self._is_game_end()

        elif self.status == "END":
            self.rank()
            self._print_result()
            self.running = False
            pass
        else:
            pass

    def detect_collision(self):
        super(PlayingMode,self).detect_collision()
        for car in self.cars:
            self.cars.remove(car)
            hits = pygame.sprite.spritecollide(car, self.cars, False)
            for hit in hits:
                hit.status = False
                car.status = False
            self.cars.add(car)

    def _print_result(self):
        self.eliminated_user.reverse()
        for user in self.eliminated_user:
            print("Rank" + str(self.eliminated_user.index(user) + 1) +
                  " : Player " + str(user.car_no + 1))

    def _init_user(self, user_no: int):
        self.car = UserCar((user_no)*100+60 , 0,user_no)
        self.users.add(self.car)
        self.cars.add(self.car)
        return None

    def _init_lanes(self):
        for i in range(9):
            for j in range(20):
                self.lane = Lane(i * 50, j * 50-150)
                self.lanes.add(self.lane)

    def _detect_car_status(self, car):
        if car.status:
            pass
        else:
            car.velocity = 0
            if car in self.users:
                i = 2
                car.image = pygame.transform.scale(pygame.image.load(
                        path.join(IMAGE_DIR, USER_IMAGE[car.car_no][i])), car_size)
                if car not in self.eliminated_user:
                    self.eliminated_user.append(car)
            else:
                i = 1
                car.image = pygame.transform.scale(pygame.image.load(
                        path.join(IMAGE_DIR, COMPUTER_CAR_IMAGE[i])), car_size)

    def _is_game_end(self):
        if len(self.users)-1 == len(self.eliminated_user) and self.is_single == False:
            for user in self.eliminated_user:
                self.user_distance.append(user.distance)
            for car in self.users:
                if car not in self.eliminated_user and car.distance >max(self.user_distance):
                    self.eliminated_user.append(car)
                    self.user_distance.append(car.distance)
                    self.status = "END"
                    break
                else:
                    pass
            else:
                pass
        elif len(self.eliminated_user) == len(self.users):
            self.status = "END"
        else:
            pass

    def _is_car_arrive_end(self, car):
        if car.distance > finish_line:
            for user in self.users:
                if user not in self.eliminated_user:
                    self.eliminated_user.append(user)
            for user in self.eliminated_user:
                self.user_distance.append(user.distance)
            self.status = "END"

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

    def drawAllSprites(self):
        '''show all cars and lanes on screen,call this fuction per frame'''
        super(PlayingMode,self).drawAllSprites()
        self.lanes.draw(self.screen)
        self.cars.draw(self.screen)

    def _creat_computercar(self):
        if len(self.cars) < cars_num:
            for i in range(2):
                x = random.choice([550,-500])
                y = random.randint(0,8)
                self.computerCar = ComputerCar(y * 50 +10,self.camera.position+x,x+420)
                self.computerCars.add(self.computerCar)
                self.cars.add(self.computerCar)

    def _draw_user_imformation(self):
        '''全縮圖'''
        pygame.draw.rect(self.screen,BLACK,pygame.Rect(0,450,900,150))
        for user in self.users:
            pygame.draw.circle(self.screen,USER_COLOR[user.car_no],
                               (round(user.distance*(900/finish_line)),450+round(user.rect.centery*(150/450))),4)
        '''線縮圖'''
        # pygame.draw.line(self.screen,BLACK,(0,450),(900,450),10)
        # for user in self.users:
        #     pygame.draw.circle(self.screen,USER_COLOR[user.car_no],(round(user.distance*(900/finish_line)),450),4)

    def rank(self):
        for car in self.eliminated_user:
            if car.distance == min(self.user_distance):
                self.eliminated_user.append(car)
                self.user_distance.remove(car.distance)
                self.eliminated_user.remove(car)
