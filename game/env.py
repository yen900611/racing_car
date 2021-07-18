from os import path

'''width and height'''
WIDTH = 1000
HEIGHT = 700

'''environment data'''
FPS = 30
ceiling = 600
finish_line = 20000
cars_num = 22

'''color'''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GREY = (140,140,140)
BLUE = (3,28,252)
LIGHT_BLUE = (33, 161, 241)

'''object size'''
car_size = (60, 30)
coin_size = (30,31)
lane_size = (20,3)

'''command'''
LEFT_cmd = "MOVE_LEFT"
RIGHT_cmd = "MOVE_RIGHT"
SPEED_cmd = "SPEED"
BRAKE_cmd = "BRAKE"

'''data path'''
IMAGE_DIR = path.join(path.dirname(__file__), 'image')
SOUND_DIR = path.join(path.dirname(__file__), 'sound')
BACKGROUND_IMAGE = ["ground0.jpg"]
COIN_IMAGE = "log.png"
RANKING_IMAGE = ["info_coin.png", "info_km.png"]

START_LINE_IMAGE = "start.png"
FINISH_LINE_IMAGE = "finish.png"
USER_IMAGE = [["car1.png","car1-bad.png"],["car2.png","car2-bad.png"],
              ["car3.png","car3-bad.png"], ["car4.png","car4-bad.png"]]
COMPUTER_CAR_IMAGE = ["computer_car.png","computer_die.png"]
USER_COLOR = [WHITE, YELLOW, BLUE, RED]

'''image url'''
COMPUTER_CAR_URL = "https://raw.githubusercontent.com/yen900611/RacingCar/master/game/image/computer_car.png"
USER_CAR_URL = ["https://github.com/yen900611/RacingCar/blob/master/game/image/car1.png?raw=true",
                "https://github.com/yen900611/RacingCar/blob/master/game/image/car2.png?raw=true",
                "https://github.com/yen900611/RacingCar/blob/master/game/image/car3.png?raw=true",
                "https://github.com/yen900611/RacingCar/blob/master/game/image/car4.png?raw=true"]
BACKGROUND_URL = "https://github.com/yen900611/RacingCar/blob/master/game/image/ground0.jpg?raw=true"
INFO_COIN_URL = "https://github.com/yen900611/RacingCar/blob/master/game/image/info_coin.png?raw=true"
INFO_KM_URL = "https://github.com/yen900611/RacingCar/blob/master/game/image/info_km.png?raw=true"
FINISH_URL = "https://github.com/yen900611/RacingCar/blob/master/game/image/finish.png?raw=true"
START_URL = "https://github.com/yen900611/RacingCar/blob/master/game/image/start.png?raw=true"
COIN_URL = "https://github.com/yen900611/RacingCar/blob/master/game/image/logo.png?raw=true"



