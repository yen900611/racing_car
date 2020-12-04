from .car import *
from .highway import *
from .gameMode import GameMode
from .env import *
import pygame
import random

class PlayingMode(GameMode):
    def __init__(self, user_num: int, sound_controller):
        super(PlayingMode, self).__init__()
        self.frame = 0
        pygame.font.init()

        '''set groups'''
        self.users = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.computerCars = pygame.sprite.Group()
        self.lanes = pygame.sprite.Group()
        self.traffic_cones = pygame.sprite.Group()
        self.camera = Camera()

        '''sound'''
        self.sound_controller = sound_controller
        # pygame.mixer.init()
        # self.hit_sound = pygame.mixer.Sound(path.join(SOUND_DIR,"explosion.wav"))

        '''image'''
        self.bg_image = pygame.image.load(path.join(IMAGE_DIR, BACKGROUND_IMAGE[0])).convert()
        self.rank_image = pygame.image.load(path.join(IMAGE_DIR, RANKING_IMAGE[1])).convert_alpha()

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
        self.line = Line()
        self.lanes.add(self.line)
        self.background_x = 0
        self.bg_x = 0
        self.rel_x = 0
        self.end = False
        self.end_frame = 0
        self.car_lanes =[110, 160, 210, 260, 310, 360, 410, 460, 510]

    def update_sprite(self, command):
        '''update the model of game,call this fuction per frame'''
        self.frame += 1
        self.handle_event()
        self._revise_speed()

        if self.status == "START" and self.frame > FPS:
            self.status = "RUNNING"
            pass
        if self.status == "RUNNING":
            self.cars_info = []
            if self.frame > FPS*4:
                self._creat_computercar()
            self._is_game_end()

            self.camera.update(self.maxVel)
            self.user_distance = []

            '''update sprite'''
            self.line.update()
            self.computerCars.update(self.cars)
            self.lanes.update(self.camera.position)
            self.line.rect.left = self.line.distance - self.camera.position +500

            for car in self.users:
                # self.user_out__screen(car)
                self.user_distance.append(car.distance)
                # self.cars_info.append(car.get_info())
                car.update(command["ml_" + str(car.car_no+1) + "P"])

                '''是否通過終點'''
                self._is_car_arrive_end(car)

            for car in self.cars:
                '''偵測車子的狀態'''
                self._detect_car_status(car)
                self.cars_info.append(car.get_info())

                '''更新車子位置'''
                car.rect.left = car.distance - self.camera.position + 500

        elif self.status == "END" and self.close == False:
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
        super(PlayingMode,self).detect_collision()
        for car in self.cars:
            self.cars.remove(car)
            hits = pygame.sprite.spritecollide(car, self.cars, False)
            for hit in hits:
                if hit.status == True:
                    self.sound_controller.play_hit_sound()
                hit.status = False
                car.status = False
            self.cars.add(car)

    # def user_out__screen(self,car):
    #     if car.status:
    #             if car.rect.right < -100 or car.rect.bottom > 550 or car.rect.top < 100:
    #                 self.sound_controller.play_lose_sound()
    #                 car.status = False

    def _print_result(self):
        tem = []
        for user in self.winner:
            tem.append({"Player":str(user.car_no + 1) + "P",
                   "Distance":str(round(user.distance))+"m",
                   })
            print({"Player":str(user.car_no + 1) + "P",
                   "Distance":str(round(user.distance))+"m",
                   })
        self.winner = tem

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
                car.image = car.image_list[1]
                if car not in self.eliminated_user:
                    self.eliminated_user.append(car)
            else:
                car.image = car.image_list[1]

    def _is_game_end(self):
        if len(self.users)-1 == len(self.eliminated_user) and self.is_single == False:
            eliminated_user_distance = []
            for car in self.eliminated_user:
                eliminated_user_distance.append(car.distance)
            for car in self.users:
                if car not in self.eliminated_user and car.distance > max(eliminated_user_distance)+100:
                    self.eliminated_user.append(car)
                    self.status = "END"
                    return None
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
            self.status = "END"

    def _revise_speed(self):
        self.user_vel = []
        for car in self.users:
            self.user_vel.append(car.velocity)
        self.maxVel = max(self.user_vel)

    def draw_bg(self):
        '''show the background and imformation on screen,call this fuction per frame'''
        super(PlayingMode, self).draw_bg()
        self.rel_x = self.background_x % self.bg_image.get_rect().width
        self.bg_x = self.rel_x - self.bg_image.get_rect().width

        self.bg_img.blit(self.bg_image,(self.bg_x,0))
        if self.rel_x <= WIDTH:
            self.bg_img.blit(self.bg_image, (self.rel_x, 0))
        self.background_x -= self.maxVel

        self.bg_img.blit(self.rank_image,(WIDTH-315, 5))

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
                               (round(user.distance*(900/finish_line)),650+round(user.rect.top*(50/500))),4)
            if user.status == False:
                if user.car_no > 1:
                    pygame.draw.line(self.screen,RED,(700 + user.car_no*75,20),(700 + user.car_no*75 +20,70),2)
                    pygame.draw.line(self.screen, RED, (720 + user.car_no * 75, 20), (720 + user.car_no * 75 - 20, 70), 2)

                elif user.car_no <= 1:
                    pygame.draw.line(self.screen,RED,(700 + user.car_no*70,20),(700 + user.car_no*70 +20,70),2)
                    pygame.draw.line(self.screen, RED, (720 + user.car_no * 75, 20), (720 + user.car_no * 70 - 20, 70), 2)

        '''顯示玩家里程數'''
        for user in self.users:
            self.draw_information(self.screen, str(round(user.distance))+"m", 17, 730+user.car_no*78,45)

    def rank(self):
        while len(self.eliminated_user) > 0:
            for car in self.eliminated_user:
                if car.distance == min(self.user_distance):
                    self.winner.append(car)
                    self.user_distance.remove(car.distance)
                    self.eliminated_user.remove(car)
        self.winner.reverse()

