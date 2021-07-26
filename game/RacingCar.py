import pygame

from .playingMode import PlayingMode
from .coinPlayMode import CoinMode
from mlgame.view.test_decorator import check_game_progress, check_game_result
from mlgame.view.view_model import create_text_view_data, create_asset_init_data, create_image_view_data, \
    create_line_view_data, Scene, create_polygon_view_data, create_rect_view_data
from mlgame.gamedev.game_interface import PaiaGame, GameResultState

from .env import *
from .sound_controller import *

'''need some fuction same as arkanoid which without dash in the name of fuction'''

class RacingCar(PaiaGame):
    def __init__(self, user_num: int, difficulty, car_num, sound):
        super().__init__()
        self.is_sound = sound
        cars_num = car_num
        self.sound_controller = SoundController(self.is_sound)
        if difficulty == "NORMAL":
            self.game_mode = PlayingMode(user_num,cars_num, self.sound_controller)
            self.game_type = "NORMAL"
        elif difficulty == "COIN":
            self.game_mode = CoinMode(user_num,cars_num, self.sound_controller)
            self.game_type = "COIN"

        self.user_num = user_num
        self.scene = Scene(WIDTH, HEIGHT, "#000000")

    def game_to_player_data(self) -> dict:
        scene_info = self.get_scene_info
        to_player_data = {}
        for car in self.game_mode.cars_info:
            player_data = {}
            player_data["frame"] = self.game_mode.frame
            player_data["x"] = car["pos"][0]
            player_data["y"] = car["pos"][1]
            player_data["distance"] = car["distance"]
            player_data["velocity"] = car["velocity"]
            player_data["cars_pos"] = scene_info["cars_pos"]
            if self.game_mode == "COIN":
                player_data["coin"] = scene_info["coin"]
                player_data["coin_num"] = car["coin_num"]
            to_player_data["ml_" + str(car["id"]+1) + "P"] = player_data
        if to_player_data:
            return to_player_data
        else:
            return {
                "ml_1P" : scene_info,
                "ml_2P" : scene_info,
                "ml_3P" : scene_info,
                "ml_4P" : scene_info
            }

    @property
    def get_scene_info(self):
        """
        Get the scene information
        """
        cars_pos = []
        computer_cars_pos = []
        lanes_pos = []

        scene_info = {
            "frame": self.game_mode.frame,
            "status": self.game_mode.status,
            "background": [(self.game_mode.bg_x,0),(self.game_mode.rel_x,0)],}

        for car in self.game_mode.cars_info:
            cars_pos.append(car["pos"])
            if car["id"] <= 4:
                scene_info["player_"+str(car["id"])+"_pos"] = car["pos"]
            elif car["id"] > 100:
                computer_cars_pos.append(car["pos"])
        scene_info["computer_cars"] = computer_cars_pos
        scene_info["cars_pos"] = cars_pos

        if self.game_type == "COIN":
            coin_pos = []
            for coin in self.game_mode.coins:
                coin_pos.append(coin.get_position())
            scene_info["coin"] = coin_pos

        scene_info["game_result"] = self.game_mode.winner
        return scene_info

    def update(self, commands):
        self.frame_count += 1
        self.game_mode.handle_event()
        self.game_mode.detect_collision()
        self.game_mode.update_sprite(commands)
        if self.game_mode.status == "FINISH":
            self.game_result_state = GameResultState.FINISH
        # self.draw()
        if not self.isRunning():
            return "QUIT"

    def reset(self):
        pass

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
        game_info["assets"].append(create_asset_init_data("background", 2000, HEIGHT, path.join(IMAGE_DIR, BACKGROUND_IMAGE[0]), BACKGROUND_URL))
        game_info["assets"].append(create_asset_init_data("start_line", 45, 450, path.join(IMAGE_DIR, START_LINE_IMAGE[0]), START_URL))
        game_info["assets"].append(create_asset_init_data("finish_line", 45, 450, path.join(IMAGE_DIR, START_LINE_IMAGE[1]), FINISH_URL))
        if self.game_type == "COIN":
            game_info["assets"].append(create_asset_init_data("coin", coin_size[0], coin_size[1], path.join(IMAGE_DIR, COIN_IMAGE), COIN_URL))
            game_info["assets"].append(create_asset_init_data("info_coin", 319, 80, path.join(IMAGE_DIR, RANKING_IMAGE[0]), INFO_COIN_URL))
        else:
            game_info["assets"].append(create_asset_init_data("info_km", 319, 80, path.join(IMAGE_DIR, RANKING_IMAGE[1]), INFO_KM_URL))

        return game_info

    @check_game_progress
    def get_scene_progress_data(self) -> dict:
        """
        Get the position of game objects for drawing on the web
        """
        scene_info = self.get_scene_info
        game_progress = {
            "background": [],
            "object_list": [],
            "toggle": [],
            "foreground": [],
            "user_info": [],
            "game_sys_info": {}
        }
        if self.game_type == "COIN":
            info_board = create_image_view_data("info_coin", WIDTH -315, 5, 319, 80)
        else:
            info_board = create_image_view_data("info_km", WIDTH -315, 5, 319, 80)
        game_progress["foreground"].append(info_board)
        bg1 = create_image_view_data("background", self.game_mode.bg_x, 0, 2000, HEIGHT)
        bg2 = create_image_view_data("background", self.game_mode.rel_x, 0, 2000, HEIGHT)
        game_progress["object_list"].append(bg1)

        if self.game_mode.rel_x <= WIDTH:
            game_progress["object_list"].append(bg2)
        # 縮圖
        block = create_rect_view_data("block", 0, 650, 1000, 50, BLACK)
        game_progress["foreground"].append(block)
        # computer car
        for car in scene_info["computer_cars"]:
            car_image = create_image_view_data("computer_car", car[0], car[1], car_size[0], car_size[1])
            game_progress["object_list"].append(car_image)
        # user
        for lane in self.game_mode.lanes:
            lane_surface = create_rect_view_data("lane", lane.rect[0], lane.rect[1], lane_size[0], lane_size[1], WHITE)
            game_progress["object_list"].append(lane_surface)
        for user in self.game_mode.users:
            user_image = create_image_view_data("player" + str(user.car_no+1) + "_car", user.rect[0], user.rect[1], car_size[0], car_size[1])
            game_progress["object_list"].append(user_image)
            point = create_rect_view_data("user", round(user.distance * (900 / finish_line)), 650 + round(user.rect.top * (50 / 500)),
                                          4, 4, USER_COLOR[user.car_no])
            game_progress["foreground"].append(point)
        # score
        if self.game_type == "COIN":
            for user in self.game_mode.users:
                score = create_text_view_data(str(user.coin_num), 730 + user.car_no * 77, 45, WHITE, "20px Arial")
                game_progress["foreground"].append(score)
        else:
            for user in self.game_mode.users:
                score = create_text_view_data(str(round(user.distance)) + "m", 730 + user.car_no * 77, 45, WHITE, "20px Arial")
                game_progress["foreground"].append(score)
        # coin
        if self.game_type == "COIN":
            for coin in scene_info["coin"]:
                coin_image = create_image_view_data("coin", coin[0], coin[1], coin_size[0], coin_size[1])
                game_progress["object_list"].append(coin_image)
        return game_progress

    # @check_game_result
    def get_game_result(self):
        """
        Get the game result for the web
        """
        scene_info = self.get_scene_info
        result = []
        for user in scene_info["game_result"]:
            result.append("GAME_DRAW")
        ranking = scene_info["game_result"]

        return {"frame_used": self.frame_count,
                "state": self.game_result_state,
                "attachment": ranking,
                }

    def get_keyboard_command(self):
        """
        Get the command according to the pressed keys
        """
        key_pressed_list = pygame.key.get_pressed()
        cmd_1P = []
        cmd_2P = []
        cmd_3P = []
        cmd_4P = []

        if key_pressed_list[pygame.K_LEFT]: cmd_1P.append(BRAKE_cmd)
        if key_pressed_list[pygame.K_RIGHT]:cmd_1P.append(SPEED_cmd)
        if key_pressed_list[pygame.K_UP]:cmd_1P.append(LEFT_cmd)
        if key_pressed_list[pygame.K_DOWN]:cmd_1P.append(RIGHT_cmd)

        if key_pressed_list[pygame.K_a]: cmd_2P.append(BRAKE_cmd)
        if key_pressed_list[pygame.K_d]:cmd_2P.append(SPEED_cmd)
        if key_pressed_list[pygame.K_w]:cmd_2P.append(LEFT_cmd)
        if key_pressed_list[pygame.K_s]:cmd_2P.append(RIGHT_cmd)

        return {"ml_1P":cmd_1P,
                "ml_2P":cmd_2P,
                "ml_3P":cmd_3P,
                "ml_4P":cmd_4P,
                }
