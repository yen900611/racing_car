from os import path
'''screen size'''
WIDTH = 900
HEIGHT = 500
FPS = 30

'''color'''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GREY = (190,190,190)
BLUE = (3,28,252)

'''object size'''
car_size = (60,30)
coin_size = (20, 20)

'''keyboard command'''
LEFT_cmd = "MOVE_LEFT"
RIGHT_cmd = "MOVE_RIGHT"
SPEED_cmd = "SPEED"
BRAKE_cmd = "BRAKE"

user_lane = [105, 245, 385, 525]
lane_center = [35, 105, 175, 245, 315, 385, 455, 525, 595]
startLine = 2 * HEIGHT / 3
end_line = 20000
ceiling = 350
cars_num = 12

USER_IMAGE = ["使用者車.png", "使用者車2.png", "使用者車3.png", "使用者車4.png"]
USER_COLOR = ["white", "chartreuse", "pink", "azure"]
IMAGE_DIR = path.join(path.dirname(__file__), 'image')
SOUND_DIR = path.join(path.dirname(__file__), 'sound')
