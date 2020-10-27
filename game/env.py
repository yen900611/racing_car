from os import path
import pygame
'''width and height'''
WIDTH = 1000
HEIGHT = 700

'''environment data'''
FPS = 30
ceiling = 600
finish_line = 20000
cars_num = 15

'''color'''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GREY = (140,140,140)
BLUE = (3,28,252)

'''object size'''
car_size = (60, 30)
coin_size = (24,25)
lane_size = (20,3)

'''command'''
LEFT_cmd = "MOVE_LEFT"
RIGHT_cmd = "MOVE_RIGHT"
SPEED_cmd = "SPEED"
BRAKE_cmd = "BRAKE"

'''data path'''
BACKGROUND_IMAGE = ["ground1.jpg", "ground2.jpg", "ground3.jpg"]
RANKING_IMAGE = ["info_coin.png", "info_km.png"]
START_LINE_IMAGE = ["start.png", "finish.png"]
USER_IMAGE = [["car1.png","撞擊.png","car1-bad.png"],["car2.png","撞擊.png","car2-bad.png"],
              ["car3.png","撞擊.png","car3-bad.png"], ["car4.png","撞擊.png","car4-bad.png"]]
COMPUTER_CAR_IMAGE = ["computer_car.png","角錐.png"]
USER_COLOR = [WHITE, YELLOW, BLUE, RED]
IMAGE_DIR = path.join(path.dirname(__file__), 'image')
SOUND_DIR = path.join(path.dirname(__file__), 'sound')

# # pygame.mixer.init()
# pygame.mixer.music.load(path.join(SOUND_DIR,"BGM.mp3"))
# pygame.mixer.music.set_volume(0.4)
