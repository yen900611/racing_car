from os import path

WIDTH = 900
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GREY = (190,190,190)
BLUE = (3,28,252)
FPS = 30
car_size = (60, 30)
LEFT_cmd = "MOVE_LEFT"
RIGHT_cmd = "MOVE_RIGHT"
SPEED_cmd = "SPEED"
BRAKE_cmd = "BRAKE"
USER_IMAGE = ["使用者車.png", "使用者車2.png", "使用者車3.png", "使用者車4.png"]
USER_COLOR = ["white", "chartreuse", "pink", "azure"]
IMAGE_DIR = path.join(path.dirname(__file__), 'image')
SOUND_DIR = path.join(path.dirname(__file__), 'sound')
