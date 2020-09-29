from games.RacingCar.game.coin import Coin
from .car import *
from .highway import *
from .gameMode import GameMode
from .env import *
import pygame
import random

class CoinMode(GameMode):
    def __init__(self, user_num: int):
        super(CoinMode, self).__init__()
        self.frame = 0
        pygame.font.init()
        '''set groups'''
        self.users = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.computerCars = pygame.sprite.Group()
        self.lanes = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.camera = Camera()

        self.cars_info = []
        self.all_distance = []
        self.maxVel = 0
        self._init_lanes()
        # user數量
        for user in range(user_num):
            self._init_user(user)
        self.winner = []
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
        self.touch_ceiling = False
        self.end = False
        self.creat_coin_frame = 0
        self.coin_lanes = [25, 75, 125, 175, 225, 275, 325, 375, 425]

    def update_sprite(self, command: list):
        '''update the model of game,call this fuction per frame'''
        self.frame += 1
        self.handle_event()

        if self.status == "START" and self.frame > FPS*3:
            self.status = "RUNNING"
            pass
        elif self.status == "RUNNING":
            if self.is_creat_coin():
                self.creat_coins()
            self.all_distance = []
            self._revise_speed_of_lane()
            self._creat_computercar()
            self.cars_info = []
            self.camera.update(self.maxVel, self.touch_ceiling)

            self.touch_ceiling = False
            '''update sprite'''
            self.line.update(self.maxVel)
            self.lanes.update(self.maxVel)
            self.coins.update()

            for car in self.users:
                self.computerCars.update(car)
                car.update(command[car.car_no])

                '''是否通過終點'''
                self._is_car_arrive_end(car)


                '''if user reach ceiling'''
                if car.rect.right >= ceiling:
                    self.touch_ceiling = True

            for car in self.cars:
                '''偵測車子的狀態'''
                self._detect_car_state(car)
                self.cars_info.append(car.get_info())
                if car.state:
                    self.all_distance.append(car.distance)

                '''更新車子位置'''
                car.rect.centerx -= self.camera.velocity - car.velocity
            for car in self.winner:
                self.all_distance.append(car.distance)
            self._is_game_end()

        elif self.status == "END":
            self.rank()
            self._print_result()
            self.running = False
            pass
        else:
            pass

    def detect_collision(self):
        super(CoinMode,self).detect_collision()
        for car in self.cars:
            self.cars.remove(car)
            hits = pygame.sprite.spritecollide(car, self.cars, False)
            for hit in hits:
                hit.state = False
                car.state = False
            self.cars.add(car)
        for car in self.users:
            hits = pygame.sprite.spritecollide(car, self.coins, True)
            for hit in hits:
                car.coin_num += 1
            pass

    def _print_result(self):
        self.winner.reverse()
        for user in self.winner:
            print("Rank" + str(self.winner.index(user)+1) +
                  " : Player " + str(user.car_no + 1))

    def _init_user(self, user_no: int):
        self.car = UserCar(startLine,(user_no)*100+60 , user_no)
        self.users.add(self.car)
        self.cars.add(self.car)
        return None

    def _init_lanes(self):
        for i in range(9):
            for j in range(50):
                self.lane = Lane(j * 60, i * 50)
                self.lanes.add(self.lane)

    def _detect_car_state(self, car):
        if car.state:
            pass
        else:
            car.velocity = 0
            if car in self.users:
                i = 2
                car.image = pygame.transform.scale(pygame.image.load(
                        path.join(IMAGE_DIR, USER_IMAGE[car.car_no][i])), car_size)
            else:
                i = 1
                car.image = pygame.transform.scale(pygame.image.load(
                        path.join(IMAGE_DIR, COMPUTER_CAR_IMAGE[i])), car_size)

    def _is_game_end(self):
        if 1 == len(self.users) and self.is_single == False:
            self.status = "END"

        elif 0 == len(self.users):
            self.status = "END"
        else:
            pass

    def _is_car_arrive_end(self, car):
        if self.frame > FPS*60:
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
        super(CoinMode, self).draw_bg()
        self.bg_img.fill(GREY)
        pygame.draw.line(self.screen, WHITE, (0, 450), (WIDTH, 450), 5)

        '''畫出每台車子的資訊'''
        self._draw_user_imformation()

        self.all_sprites.draw(self.screen)
        self.users.draw(self.screen)

    def drawAllSprites(self):
        '''show all cars and lanes on screen,call this fuction per frame'''
        super(CoinMode,self).drawAllSprites()
        self.lanes.draw(self.screen)
        self.cars.draw(self.screen)

    def _creat_computercar(self):
        if len(self.cars) < cars_num:
            for i in range(3):
                x = random.randint(0,8)
                self.computerCar = ComputerCar(random.choice([WIDTH + 100, -200]), x * 50 +10)
                self.computerCars.add(self.computerCar)
                self.cars.add(self.computerCar)

    def _draw_user_imformation(self):
        for car in self.users:
            self.draw_information(self.screen, "Player" + str(car.car_no+1), 17, (car.car_no*200)+20,450 +10)
            self.draw_information(self.screen, "vel : " + str(round(car.velocity, 2)), 17, (car.car_no*200)+20,450 +40)
            self.draw_information(self.screen, "distance : " + str(abs(round(car.distance, 2))), 17, (car.car_no*200)+20,450 +70)
            self.draw_information(self.screen, "coins : " + str(car.coin_num), 17, (car.car_no*200)+20,450 + 100)

    def rank(self):
        coin_num = []
        for car in self.users:
            coin_num.append(car.coin_num)
        for car in self.users:
            if car.coin_num == min(coin_num):
                self.winner.append(car)
                coin_num.remove(car.coin_num)

    def creat_coins(self):
        if self.frame - self.creat_coin_frame > FPS*2:
            coin = Coin(WIDTH,random.choice(self.coin_lanes))
            self.coin_lanes.remove(coin.rect.centery)
            self.all_sprites.add(coin)
            self.coins.add(coin)
            self.creat_coin_frame = self.frame
        if len(self.coin_lanes) == 0:
            self.coin_lanes = [25, 75, 125, 175, 225, 275, 325, 375, 425]
        else:
            pass

    def is_creat_coin(self):
        if self.maxVel >= 11:
            return True
        else:
            return False
