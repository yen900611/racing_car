from os import path

WIDTH = 800
HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (3,28,252)
FPS = 30
lane_center = [105, 245, 385, 525]
car_size = (40, 80)
LEFT_cmd = "MOVE_LEFT"
RIGHT_cmd = "MOVE_RIGHT"
SPEED_cmd = "SPEED"
BRAKE_cmd = "BRAKE"
USER_IMAGE = ["使用者車.png", "使用者車2.png", "使用者車3.png", "使用者車4.png"]
USER_COLOR = ["white", "chartreuse", "pink", "azure"]
IMAGE_DIR = path.join(path.dirname(__file__), 'image')
SOUND_DIR = path.join(path.dirname(__file__), 'sound')
