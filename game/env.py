from os import path

WIDTH = 800
HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GREY = (190, 190, 190)
FPS = 30
lane_center = [105,245,385,525]
user_image = ["使用者車.png", "使用者車2.png", "使用者車3.png", "使用者車4.png", ["white", "chartreuse", "pink", "azure"]]
IMAGE_DIR = path.join(path.dirname(__file__),'image')
SOUND_DIR = path.join(path.dirname(__file__),'sound')
