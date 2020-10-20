from games.RacingCar.game.coin import Coin
from .car import *
from .highway import *
from .gameMode import GameMode
from .env import *
import pygame
import random

class CoinMode(GameMode):
    def __init__(self, user_num: int, sound_controller):
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
        '''sound'''
        self.sound_controller = sound_controller
        # pygame.mixer.init()
        # self.hit_sound = pygame.mixer.Sound(path.join(SOUND_DIR,"explosion.wav"))
        # self.coin_sound = pygame.mixer.Sound(path.join(SOUND_DIR,"coin.wav"))

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
        self.creat_coin_frame = 0
        self.coin_lanes = [125, 175, 225, 275, 325, 375, 425, 475, 525]
        self.car_lanes = [110, 160, 210, 260, 310, 360, 410, 460, 510]

    def update_sprite(self, command: list):
        '''update the model of game,call this fuction per frame'''
        self.frame += 1
        self.handle_event()

        if self.status == "START" and self.frame > FPS*3:
            self.status = "RUNNING"
            pass
        elif self.status == "RUNNING":
            if self.frame > FPS*7:
                self._creat_computercar()
            if self.is_creat_coin():
                self.creat_coins()
            self.user_distance = []
            self.coin_num = []
            self._revise_speed()
            self.cars_info = []
            self.camera.update(self.maxVel)

            '''update sprite'''
            self.line.update()
            self.lanes.update(self.camera.position)
            self.line.rect.left = self.line.distance - self.camera.position +500
            self.coins.update()
            self.computerCars.update(self.cars)

            for car in self.users:
                self.user_distance.append(car.distance)
                self.coin_num.append(car.coin_num)
                car.update(command[car.car_no])

            for car in self.cars:
                '''偵測車子的狀態'''
                self._detect_car_status(car)
                self.cars_info.append(car.get_info())

                '''更新車子位置'''
                car.rect.left = car.distance - self.camera.position + 500

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
                if hit.status:
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

    def _print_result(self):
        #TODO
        self.eliminated_user.reverse()
        for user in self.eliminated_user:
            print("Rank" + str(self.eliminated_user.index(user)+1) +
                  " : Player " + str(user.car_no + 1))

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
        if len(self.eliminated_user) == len(self.users):
            self.status = "END"
        if self.frame > FPS*60:
            self.status = "END"

    def _revise_speed(self):
        self.user_vel = []
        for car in self.users:
            self.user_vel.append(car.velocity)
        self.maxVel = max(self.user_vel)

    def draw_bg(self):
        '''show the background and imformation on screen,call this fuction per frame'''
        super(CoinMode, self).draw_bg()
        bg_image = pygame.image.load(path.join(IMAGE_DIR, BACKGROUND_IMAGE[0]))
        bg_image = bg_image.convert_alpha()
        self.bg_img.blit(bg_image,(0,0))

        rank_image = pygame.image.load(path.join(IMAGE_DIR, RANKING_IMAGE[0])).convert_alpha()
        self.bg_img.blit(rank_image,(WIDTH-325, 5))

        '''畫出每台車子的資訊'''
        self._draw_user_imformation()
        '''顯示玩家金幣數'''
        for user in self.users:
            self.draw_information(self.screen,str(user.coin_num), 17, 730+user.car_no*78,45)

        self.all_sprites.draw(self.screen)
        self.users.draw(self.screen)

    def drawAllSprites(self):
        '''show all cars and lanes on screen,call this fuction per frame'''
        super(CoinMode,self).drawAllSprites()
        self.lanes.draw(self.screen)
        self.cars.draw(self.screen)

    def _creat_computercar(self):
        if len(self.cars) < cars_num:
            x = random.choice([650,-700])
            y = random.choice(self.car_lanes)
            self.computerCar = ComputerCar(y,self.camera.position+x,x+500)
            self.computerCars.add(self.computerCar)
            self.cars.add(self.computerCar)
            self.car_lanes.remove(y)
        if len(self.car_lanes) == 0:
            self.car_lanes = [110, 160, 210, 260, 310, 360, 410, 460, 510]

    def _draw_user_imformation(self):
        '''全縮圖'''
        pygame.draw.rect(self.screen,BLACK,pygame.Rect(0,650,1000,50))
        for user in self.users:
            pygame.draw.circle(self.screen,USER_COLOR[user.car_no],
                               (round(user.distance*(1000/finish_line)),650+round(user.rect.top*(50/500))),4)

    def rank(self):
        user_coin = []
        for user in self.users:
            user_coin.append(user.coin_num)
        while len(self.users) != 0:
            for user in self.users:
                if user.coin_num == min(user_coin):
                    self.winner.append(user)
                    user_coin.remove(user.coin_num)
                    user.kill()

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
