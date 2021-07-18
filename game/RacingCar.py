import pygame

from .playingMode import PlayingMode
from .coinPlayMode import CoinMode
from mlgame.view.test_decorator import check_game_progress
from mlgame.view.view_model import create_text_view_data, create_asset_init_data, create_image_view_data, \
    create_line_view_data, Scene, create_polygon_view_data, create_rect_view_data
from mlgame.gamedev.game_interface import PaiaGame

from .env import *
from .sound_controller import *

'''need some fuction same as arkanoid which without dash in the name of fuction'''

class RacingCar(PaiaGame):
    def __init__(self, user_num: int, difficulty,sound):
        super().__init__()
        self.is_sound = sound
        self.sound_controller = SoundController(self.is_sound)
        if difficulty == "NORMAL":
            self.game_mode = PlayingMode(user_num,self.sound_controller)
            self.game_type = "NORMAL"
        elif difficulty == "COIN":
            self.game_mode = CoinMode(user_num,self.sound_controller)
            self.game_type = "COIN"

        self.user_num = user_num
        self.scene = Scene(WIDTH, HEIGHT, "#000000")

    def game_to_player_data(self) -> dict:
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
        # self.draw()
        if not self.isRunning():
            return "QUIT"

    def reset(self):
        self.__init__(self.user_num,self.game_type,self.is_sound)

    def isRunning(self):
        return self.game_mode.isRunning()

    def get_scene_init_data(self) -> dict:
        """
        Get the scene and object information for drawing on the web
        """
        game_info = {"scene": self.scene.__dict__,
                     "assets":[]}
        sys_car_path = path.join(IMAGE_DIR, COMPUTER_CAR_IMAGE[0])
        game_info["assets"].append(create_asset_init_data("computer_car", car_size[0], coin_size[1], sys_car_path, COMPUTER_CAR_URL))
        for i in range(self.user_num):
            game_info["assets"].append(
                create_asset_init_data("player" + str(i+1) + "_car", car_size[0], coin_size[1], path.join(IMAGE_DIR, USER_IMAGE[i][0]), USER_CAR_URL[i]))
        game_info["assets"].append(create_asset_init_data("background", 2000, HEIGHT, path.join(IMAGE_DIR, BACKGROUND_IMAGE), BACKGROUND_URL))
        game_info["assets"].append(create_asset_init_data("coin", coin_size[0], coin_size[1], path.join(IMAGE_DIR, COIN_IMAGE), COIN_URL))

        # game_info = {
        #     "scene": {
        #         "size": [WIDTH, HEIGHT]
        #     },
        #     "game_object": [
        #         {"name": "background", "size": (2000, HEIGHT), "color": BLACK, "image": "ground0.jpg"},
        #         {"name": "lane", "size": lane_size, "color": WHITE},
        #         {"name": "coin", "size": coin_size, "color": YELLOW, "image":"logo.png"},
        #         {"name": "computer_car", "size": car_size, "color": LIGHT_BLUE, "image": "computer_car.png"},
        #         {"name": "player1_car", "size": car_size, "color": WHITE, "image": "car1.png"},
        #         {"name": "player2_car", "size": car_size, "color": YELLOW, "image": "car2.png"},
        #         {"name": "player3_car", "size": car_size, "color": BLUE, "image": "car3.png"},
        #         {"name": "player4_car", "size": car_size, "color": RED, "image": "car4.png"},
        #         {"name": "line", "size": (45,450), "color": WHITE, "image": "start.png"},
        #         {"name": "icon", "size": (319,80), "color": BLACK, "image": "info_km.png"},
        #     ],
        #     "images": ["car1.png", "car2.png", "car3.png", "car4.png", "computer_car.png",
        #               "car1-bad.png", "car2-bad.png", "car3-bad.png", "car4-bad.png", "computer_die.png",
        #               "start.png", "finish.png", "info_coin.png", "info_km.png",
        #               "logo.png", "ground0.jpg"
        #               ]
        # }

        # if self.game_type == "COIN":
        #     game_info["game_object"][9]={"name": "icon", "size": (319,80), "color": BLACK, "image": "info_coin.png"}

        return game_info

    @check_game_progress
    def get_scene_progress_data(self) -> dict:
        """
        Get the position of game objects for drawing on the web
        """
        game_progress = {
            "background": [],
            "object_list": [],
            "toggle": [],
            "foreground": [],
            "user_info": [],
            "game_sys_info": {}
        }
        bg = create_image_view_data("background", )
        # scene_info = self.get_scene_info
        # game_progress = {"game_object": {
        # "background" : [self._progress_dict(scene_info["background"][0][0], scene_info["background"][0][1]),
        #                 self._progress_dict(scene_info["background"][1][0], scene_info["background"][1][1])],
        # "icon": [self._progress_dict(WIDTH-315, 5)],
        # "line":[self._progress_dict(scene_info["line"][0][0], scene_info["line"][0][1])],
        # },
        # "game_user_information":[]}
        #
        # if self.game_mode.status == "RUNNING":
        #     for user in self.game_mode.users:
        #         user_info = {}
        #         user_info["distance"] = round(user.distance)
        #         if self.game_type == "COIN":
        #             user_info["coin"] = user.coin_num
        #         game_progress["game_user_information"].append(user_info)
        #
        #         if user.status  == False:
        #             game_progress["game_object"]["player"+str(user.car_no+1) + "_car"] = [{"pos":scene_info["player_" + str(user.car_no) + "_pos"],
        #                                                                                    "image":"car" + str(user.car_no+1) + "-bad.png"}]
        #         else:
        #             game_progress["game_object"]["player"+str(user.car_no+1) + "_car"] = [{"pos":scene_info["player_" + str(user.car_no) + "_pos"]}]
        #
        # lane_pos = []
        # for lane in scene_info["lanes"]:
        #     lane_pos.append(self._progress_dict(lane[0], lane[1]))
        # game_progress["game_object"]["lane"] = lane_pos
        #
        # computer_car_pos = []
        # for computer in scene_info["computer_cars"]:
        #     computer_car_pos.append(self._progress_dict(computer[0], computer[1]))
        # game_progress["game_object"]["computer_car"] = computer_car_pos
        #
        # if self.game_type == "COIN":
        #     coin_pos = []
        #     for coin in scene_info["coin"]:
        #         coin_pos.append(self._progress_dict(coin[0], coin[1]))
        #     game_progress["game_object"]["coin"] = coin_pos
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
