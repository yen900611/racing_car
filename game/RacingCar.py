import pygame

from .playingMode import PlayingMode
from .coinPlayMode import CoinMode
from .env import *
from .sound_controller import *

'''need some fuction same as arkanoid which without dash in the name of fuction'''

class RacingCar:
    def __init__(self, user_num: int, difficulty,sound):
        self.is_sound = sound
        self.sound_controller = SoundController(self.is_sound)
        if difficulty == "NORMAL":
            self.game_mode = PlayingMode(user_num,self.sound_controller)
            self.game_type = "NORMAL"
        elif difficulty == "COIN":
            self.game_mode = CoinMode(user_num,self.sound_controller)
            self.game_type = "COIN"

        self.user_num = user_num

    def get_player_scene_info(self) -> dict:
        scene_info = self.get_scene_info
        return {
            "ml_1P" : scene_info,
            "ml_2P" : scene_info,
            "ml_3P" : scene_info,
            "ml_4P" : scene_info
        }

    def update(self, commands):
        self.game_mode.handle_event()
        self.game_mode.detect_collision()
        self.game_mode.update_sprite(commands)
        self.draw()
        if not self.isRunning():
            return "QUIT"


    def reset(self):
        self.__init__(self.user_num,self.game_type,self.is_sound)
        pass

    def isRunning(self):
        return self.game_mode.isRunning()
        pass

    def draw(self):
        self.game_mode.draw_bg()
        self.game_mode.drawAllSprites()
        self.game_mode.flip()

    @property
    def get_scene_info(self) -> dict:
        """
        Get the scene information
        """

        cars_pos = []
        computer_cars_pos = []
        lanes_pos = []

        scene_info = {
            "frame": self.game_mode.frame,
            "status": self.game_mode.status,
            "background": self.game_mode.bg_x,
            "line":[(self.game_mode.line.rect.left,self.game_mode.line.rect.top)]}

        for car in self.game_mode.cars_info:
            cars_pos.append(car["pos"])
            if car["id"] <= 4:
                scene_info["player_"+str(car["id"])+"_pos"] = car["pos"]
            elif car["id"] > 100:
                computer_cars_pos.append(car["pos"])
        scene_info["computer_cars"] = computer_cars_pos
        scene_info["cars_pos"] = cars_pos

        for lane in self.game_mode.lanes:
            lanes_pos.append((lane.rect.left, lane.rect.top))
        scene_info["lanes"] = lanes_pos

        if self.game_type == "COIN":
            coin_pos = []
            for coin in self.game_mode.coins:
                coin_pos.append(coin.get_position())
            scene_info["coin"] = coin_pos

        scene_info["game_result"] = self.game_mode.winner
        return scene_info

    def get_game_info(self):
        """
        Get the scene and object information for drawing on the web
        """
        game_info = {

            "scene": {
                "size": [WIDTH, HEIGHT]
            },
            "game_object": [
                {"name": "background", "size": (WIDTH, HEIGHT), "color": BLACK, "image": "ground0.jpg"},
                {"name": "lane", "size": lane_size, "color": WHITE},
                {"name": "coin", "size": coin_size, "color": YELLOW, "image":"logo,png"},
                {"name": "computer_car", "size": car_size, "color": LIGHT_BLUE, "image": "computer_car.png"},
                {"name": "player1_car", "size": car_size, "color": WHITE, "image": "car1.png"},
                {"name": "player2_car", "size": car_size, "color": YELLOW, "image": "car2.png"},
                {"name": "player3_car", "size": car_size, "color": BLUE, "image": "car3.png"},
                {"name": "player4_car", "size": car_size, "color": RED, "image": "car4.png"},
                {"name": "line", "size": (5,450), "color": WHITE, "image": "start.png"},
                {"name": "icon", "size": (319,80), "color": BLACK, "image": "info_km.png"},
            ],
            "image": ["car1.png", "car2.png", "car3.png", "car4.png", "computer_car.png",
                      "car1-bad.png", "car2-bad.png", "car3-bad.png", "car4-bad.png", "computer_die.png",
                      "start.png", "finish.png", "info_coin.png", "info_km.png",
                      "logo.png", "ground0.jpg"
                      ]
        }

        if self.game_type == "COIN":
            game_info["game_object"][9]={"name": "icon", "size": (319,80), "color": BLACK, "image": "info_coin.png"}

        return game_info
    def get_game_progress(self):
        """
        Get the position of game objects for drawing on the web
        """
        scene_info = self.get_scene_info
        game_progress = {"game_object": {
        "background" :scene_info["background"],
        "lane": scene_info["lanes"],
        "icon": (WIDTH-315, 5),
        "line":scene_info["line"],
        "computer_car": scene_info["computer_cars"],
        }}

        if scene_info["status"] == "RUNNING":
            for user in self.game_mode.users:
                if user.status  == False:
                    game_progress["game_object"]["player"+str(user.car_no+1) + "_car"] = [{"pos":scene_info["player_" + str(user.car_no) + "_pos"],
                                                                                           "image":"car" + str(user.car_no+1) + "-bad.png"}]
                else:
                    game_progress["game_object"]["player"+str(user.car_no+1) + "_car"] = [{"pos":scene_info["player_" + str(user.car_no) + "_pos"]}]

        if self.game_type == "COIN":
            game_progress["game_object"]["coin"] = scene_info["coin"]
        return game_progress

    def get_game_result(self):
        """
        Get the game result for the web
        """
        scene_info = self.get_scene_info
        result = []
        for user in scene_info["game_result"]:
            result.append("GAME_DRAW")

        return {
            "frame_used": scene_info["frame"],
            "result": result,
            "ranking": scene_info["game_result"]
        }

    def get_keyboard_command(self):
        """
        Get the command according to the pressed keys
        """
        key_pressed_list = pygame.key.get_pressed()
        cmd_1P = []
        cmd_2P = []

        if key_pressed_list[pygame.K_LEFT]: cmd_1P.append(BRAKE_cmd)
        if key_pressed_list[pygame.K_RIGHT]:cmd_1P.append(SPEED_cmd)
        if key_pressed_list[pygame.K_UP]:cmd_1P.append(LEFT_cmd)
        if key_pressed_list[pygame.K_DOWN]:cmd_1P.append(RIGHT_cmd)

        if key_pressed_list[pygame.K_a]: cmd_2P.append(BRAKE_cmd)
        if key_pressed_list[pygame.K_d]:cmd_2P.append(SPEED_cmd)
        if key_pressed_list[pygame.K_w]:cmd_2P.append(LEFT_cmd)
        if key_pressed_list[pygame.K_s]:cmd_2P.append(RIGHT_cmd)

        return {"ml_1P":cmd_1P,
                "ml_2P":cmd_2P}

# if __name__ == '__main__':
#     pygame.init()
#     display = pygame.display.init()
#     game = Game(4)
#
#     while game.isRunning():
#         game.update(commands)
#         game.draw()
#
#     pygame.quit()
