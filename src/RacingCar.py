import pygame

from .playingMode import PlayingMode
from .coinPlayMode import CoinMode
from .reliveMode import ReliveMode
from mlgame.view.decorator import check_game_progress, check_game_result
from mlgame.view.view_model import create_text_view_data, create_asset_init_data, create_image_view_data, \
    create_line_view_data, Scene, create_polygon_view_data, create_rect_view_data
from mlgame.game.paia_game import PaiaGame, GameResultState

from .env import *
from .sound_controller import *

'''need some fuction same as arkanoid which without dash in the name of fuction'''


class RacingCar(PaiaGame):
    def __init__(self, user_num: int, game_type, car_num, racetrack_length=15000, rounds=1, sound="off"):
        super().__init__(user_num=user_num)
        self.game_times_goal = rounds
        self.game_times = 1
        self.score = []  # 用於計算積分
        self.is_sound = sound
        self.cars_num = car_num
        self.sound_controller = SoundController(self.is_sound)
        self.game_type = game_type
        self.user_num = user_num
        self.length = racetrack_length
        self.game_mode = self.set_game_mode()
        self.game_mode.sound_controller.play_music()
        self.scene = Scene(WIDTH, HEIGHT, BLACK)
        self.attachements = []

    def get_data_from_game_to_player(self) -> dict:
        scene_info = self.get_scene_info
        to_player_data = {}
        for user in self.game_mode.users:
            player_data = user.get_info()
            player_data["all_cars_pos"] = scene_info["cars_pos"]
            player_data["frame"] = scene_info["frame"]
            # player_data["status"] = scene_info["status"]
            if self.game_type == "COIN":
                player_data["coin"] = scene_info["coin"]
            else:
                player_data["coin"] = []
            to_player_data[str(player_data["id"] + 1) + "P"] = player_data

        if to_player_data:
            return to_player_data
        else:
            return {
                "1P": scene_info,
                "2P": scene_info,
                "3P": scene_info,
                "4P": scene_info
            }

    @property
    def get_scene_info(self):
        """
        Get the scene information
        """
        cars_pos = []
        computer_cars_pos = []

        scene_info = {
            "frame": self.game_mode.frame,
            "status": self.game_mode.state,
            "background": [(self.game_mode.bg_x, 0), (self.game_mode.rel_x, 0)], }

        for user in self.game_mode.cars:
            car_info = user.get_info()
            cars_pos.append((car_info["x"], car_info["y"]))
            if car_info["id"] <= 4:
                scene_info["player_" + str(car_info["id"]) + "_pos"] = (car_info["x"], car_info["y"])
            elif car_info["id"] > 100:
                computer_cars_pos.append((car_info["x"], car_info["y"]))
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
        self.game_mode.update(commands)
        self.game_result_state = self.game_mode.state
        if not self.isRunning():
            # collect game rank
            game_result = self.game_mode.winner.copy()
            if len(self.attachements) == 0:
                """ fisrt time end"""
                self.attachements = game_result
                for user in self.attachements:
                    user["accumulated_score"] = 5 - user["single_rank"]

            else:
                for user in self.attachements:
                    for single_rank in game_result:
                        if single_rank['player'] == user['player']:
                            match_single_rank = single_rank
                    user["accumulated_score"] += (5 - match_single_rank["single_rank"])
                    user["single_rank"] = match_single_rank["single_rank"]
            if self.game_times < self.game_times_goal:
                self.game_times += 1
                return "RESET"
            else:
                return "QUIT"

    def reset(self):
        self.frame_count = 0
        self.game_mode = self.set_game_mode()
        self.game_mode.sound_controller.play_music()
        userCar_init_position = [160, 260, 360, 460]

    def isRunning(self):
        return self.game_mode.isRunning()

    def get_scene_init_data(self) -> dict:
        """
        Get the scene and object information for drawing on the web
        """
        game_info = {"scene": self.scene.__dict__,
                     "assets": []}
        sys_car_path = path.join(ASSET_IMAGE_DIR, COMPUTER_CAR_IMAGE[0])
        game_info["assets"].append(
            create_asset_init_data("computer_car", car_size[0], coin_size[1], sys_car_path, COMPUTER_CAR_URL))
        for i in range(self.user_num):
            game_info["assets"].append(
                create_asset_init_data("player" + str(i + 1) + "_car", car_size[0], coin_size[1],
                                       path.join(ASSET_IMAGE_DIR, USER_IMAGE[i][0]), USER_CAR_URL[i]))
        game_info["assets"].append(
            create_asset_init_data("background", 2000, HEIGHT, path.join(ASSET_IMAGE_DIR, BACKGROUND_IMAGE[0]),
                                   BACKGROUND_URL))
        game_info["assets"].append(
            create_asset_init_data("start_line", 45, 450, path.join(ASSET_IMAGE_DIR, START_LINE_IMAGE[0]), START_URL))
        game_info["assets"].append(
            create_asset_init_data("finish_line", 45, 450, path.join(ASSET_IMAGE_DIR, START_LINE_IMAGE[1]), FINISH_URL))
        if self.game_type == "COIN":
            game_info["assets"].append(
                create_asset_init_data("coin", coin_size[0], coin_size[1], path.join(ASSET_IMAGE_DIR, COIN_IMAGE),
                                       COIN_URL))
            game_info["assets"].append(
                create_asset_init_data("info_coin", 319, 80, path.join(ASSET_IMAGE_DIR, RANKING_IMAGE[0]),
                                       INFO_COIN_URL))
        else:
            game_info["assets"].append(
                create_asset_init_data("info_km", 319, 80, path.join(ASSET_IMAGE_DIR, RANKING_IMAGE[1]), INFO_KM_URL))

        return game_info

    @check_game_progress
    def get_scene_progress_data(self) -> dict:
        """
        Get the position of src objects for drawing on the web
        """
        scene_info = self.get_scene_info
        game_progress = {
            "frame": self.frame_count,
            "background": [],
            "object_list": [],
            "toggle_with_bias": [],
            "toggle": [],
            "foreground": [],
            "user_info": [],
            "game_sys_info": {}
        }
        if self.game_type == "COIN":
            info_board = create_image_view_data("info_coin", WIDTH - 315, 5, 319, 80)
        else:
            info_board = create_image_view_data("info_km", WIDTH - 315, 5, 319, 80)
        game_progress["foreground"].append(info_board)
        bg1 = create_image_view_data("background", self.game_mode.bg_x, 0, 2000, HEIGHT)
        bg2 = create_image_view_data("background", self.game_mode.rel_x, 0, 2000, HEIGHT)
        game_progress["object_list"].append(bg1)

        if self.game_mode.rel_x <= WIDTH:
            game_progress["object_list"].append(bg2)
        # 縮圖
        block = create_rect_view_data("block", 0, 650, 1000, 50, BLACK)
        game_progress["foreground"].append(block)
        # line and lane
        game_progress["object_list"].append(self.game_mode.line.get_asset_info())
        for lane in self.game_mode.lanes:
            game_progress["object_list"].append(lane.get_asset_info())
        # user
        for user in self.game_mode.users:
            user_image = create_image_view_data("player" + str(user.car_no + 1) + "_car", user.rect[0], user.rect[1],
                                                car_size[0], car_size[1])
            game_progress["object_list"].append(user_image)
            point = create_rect_view_data("user", round(user.distance * (900 / self.length)),
                                          650 + round(user.rect.top * (50 / 500)),
                                          4, 4, USER_COLOR[user.car_no])
            game_progress["foreground"].append(point)
        # score
        if self.game_type == "COIN":
            for coin in scene_info["coin"]:
                coin_image = create_image_view_data("coin", coin[0], coin[1], coin_size[0], coin_size[1])
                game_progress["object_list"].append(coin_image)
            for user in self.game_mode.users:
                score = create_text_view_data(str(user.coin_num), 740 + user.car_no * 77, 45, WHITE, "16px Arial")
                game_progress["foreground"].append(score)
        else:
            for user in self.game_mode.users:
                score = create_text_view_data(str(round(user.distance)) + "m", 725 + user.car_no * 77, 45, WHITE,
                                              "16px Arial")
                game_progress["foreground"].append(score)
        # computer car
        for car in scene_info["computer_cars"]:
            car_image = create_image_view_data("computer_car", car[0], car[1], car_size[0], car_size[1])
            game_progress["object_list"].append(car_image)
        return game_progress

    @check_game_result
    def get_game_result(self):
        """
        Get the src result for the web
        """

        return {"frame_used": self.frame_count,
                "state": self.game_result_state,
                "attachment": self.rank()
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
        if key_pressed_list[pygame.K_RIGHT]: cmd_1P.append(SPEED_cmd)
        if key_pressed_list[pygame.K_UP]: cmd_1P.append(LEFT_cmd)
        if key_pressed_list[pygame.K_DOWN]: cmd_1P.append(RIGHT_cmd)

        if key_pressed_list[pygame.K_a]: cmd_2P.append(BRAKE_cmd)
        if key_pressed_list[pygame.K_d]: cmd_2P.append(SPEED_cmd)
        if key_pressed_list[pygame.K_w]: cmd_2P.append(LEFT_cmd)
        if key_pressed_list[pygame.K_s]: cmd_2P.append(RIGHT_cmd)

        if not self.isRunning():
            return {"1P": "RESET",
                    "2P": "RESET",
                    "3P": "RESET",
                    "4P": "RESET",
                    }

        return {"1P": cmd_1P,
                "2P": cmd_2P,
                "3P": cmd_3P,
                "4P": cmd_4P,
                }

    @staticmethod
    def ai_clients():
        """
        let MLGame know how to parse your ai,
        you can also use this names to get different cmd and send different data to each ai client
        """
        return [
            {"name": "1P"},
            {"name": "2P"},
            {"name": "3P"},
            {"name": "4P"}
        ]

    def set_game_mode(self):
        if self.game_type == "NORMAL":
            game_mode = PlayingMode(self.user_num, self.cars_num, self.length, self.sound_controller)
        elif self.game_type == "COIN":
            game_mode = CoinMode(self.user_num, self.cars_num, self.length, self.sound_controller)
        elif self.game_type == "RELIVE":
            game_mode = ReliveMode(self.user_num, self.cars_num, self.length, self.sound_controller)

        return game_mode

    def rank(self):
        # game_result = self.get_scene_info["game_result"]
        # TODO refactor
        # if len(self.attachements)==0:
        #     self.attachements = game_result
        #     for user in self.attachements:
        #         user["accumulated_score"] = 5 - user["single_rank"]
        #     return self.attachements
        #
        # for user in self.attachements:
        #     for single_rank in game_result:
        #         if single_rank['player'] == user['player']:
        #             match_single_rank = single_rank
        #     user["accumulated_score"] += (5 - match_single_rank["single_rank"])
        # if self.score:
        #     for user in self.score:
        #         user["accumulated_score"] += (5 - user["single_rank"])
        # else:
        #     self.score = single_game_result
        #     for user in self.score:
        #         user["accumulated_score"] = 5 - user["single_rank"]

        return self.attachements
