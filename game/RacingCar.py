import time

import pygame

from .playingMode import PlayingMode
from .coinPlayMode import CoinPlayingMode
from .env import *

# TODO
'''need some fuction same as arkanoid which without dash in the name of fuction'''


class RacingCar:
    def __init__(self, user_num: int, difficulty):
        if difficulty == "NORMAL":
            self.game_mode = PlayingMode(user_num)
            self.game_type = "NORMAL"
        elif difficulty == "COIN":
            self.game_mode = CoinPlayingMode(user_num)
            self.game_type = "COIN"
        pass

    def get_player_scene_info(self) -> dict:
        computer_cars_pos = []
        player_1_pos = ()
        player_2_pos = ()
        player_3_pos = ()
        player_4_pos = ()

        for car in self.game_mode.cars_info:
            if car["id"] >= 101:
                computer_cars_pos.append(car["pos"])
            elif car["id"] == 0:
                player_1_pos = car["pos"]
            elif car["id"] == 1:
                player_2_pos = car["pos"]
            elif car["id"] == 2:
                player_3_pos = car["pos"]
            elif car["id"] == 3:
                player_4_pos = car["pos"]

        return {"frame": self.game_mode.frame,
                "status": self.game_mode.status,
                "computer_cars": computer_cars_pos,
                "player1": player_1_pos,
                "player2": player_2_pos,
                "player3": player_3_pos,
                "player4": player_4_pos,
                "cars_info": self.game_mode.cars_info
                }

    def update(self, commands):
        self.game_mode.handle_event()
        self.game_mode.detect_collision()
        self.game_mode.update_sprite(commands)
        if not self.isRunning():
            return "QUIT"
        self.draw()


    def reset(self):

        pass

    def isRunning(self):
        return self.game_mode.isRunning()
        pass

    def draw(self):
        self.game_mode.draw_bg()
        self.game_mode.flip()

    def get_scene_info(self) -> dict:
        """
        Get the scene information
        """
        coin_pos = []
        computer_cars_pos = []
        lanes_pos = []
        player_1_pos = ()
        player_2_pos = ()
        player_3_pos = ()
        player_4_pos = ()
        player_1 = []
        player_2 = []
        player_3 = []
        player_4 = []

        for car in self.game_mode.cars_info:
            if car["id"] >= 101:
                computer_cars_pos.append((car["pos"][0]-20,car["pos"][1]-40))
            elif car["id"] == 0:
                player_1_pos = (car["pos"][0]-20,car["pos"][1]-40)
                player_1 = car
            elif car["id"] == 1:
                player_2_pos = (car["pos"][0]-20,car["pos"][1]-40)
                player_2 = car
            elif car["id"] == 2:
                player_3_pos = (car["pos"][0]-20,car["pos"][1]-40)
                player_3 = car
            elif car["id"] == 3:
                player_4_pos = (car["pos"][0]-20,car["pos"][1]-40)
                player_4 = car
        for lane in self.game_mode.lanes:
            lanes_pos.append((lane.rect.left, lane.rect.top))

        if self.game_type == "NORMAL":
            scene_info = {
                "frame": self.game_mode.frame,
                "status": self.game_mode.status,
                "computer_cars": computer_cars_pos,
                "lanes": lanes_pos,
                "player1_pos": player_1_pos,
                "player2_pos": player_2_pos,
                "player3_pos": player_3_pos,
                "player4_pos": player_4_pos,
                "player1": player_1,
                "player2": player_2,
                "player3": player_3,
                "player4": player_4,
                "game_result": self.game_mode.winner}

        elif self.game_type == "COIN":
            for coin in self.game_mode.coins:
                coin_pos.append(coin.get_position())
            scene_info = {
                "frame": self.game_mode.frame,
                "status": self.game_mode.status,
                "computer_cars": computer_cars_pos,
                "lanes": lanes_pos,
                "player1_pos": player_1_pos,
                "player2_pos": player_2_pos,
                "player3_pos": player_3_pos,
                "player4_pos": player_4_pos,
                "player1": player_1,
                "player2": player_2,
                "player3": player_3,
                "player4": player_4,
                "coins":coin_pos,
                "game_result": self.game_mode.winner}

        return scene_info

    def get_game_info(self):
        """
        Get the scene and object information for drawing on the web
        """
        scene_info = self.get_scene_info()

        return {
            "scene": {
                "size": [WIDTH, HEIGHT]
            },
            "game_object": [
                {"name": "lane", "size": [5, 30], "color": WHITE},
                {"name": "computer_car", "size": [40, 60], "color": (0, 191, 255)},
                {"name": "player1_car", "size": [40, 60], "color": RED},
                {"name": "player2_car", "size": [40, 60], "color": YELLOW},
                {"name": "player3_car", "size": [40, 60], "color": GREEN},
                {"name": "player4_car", "size": [40, 60], "color": BLUE},
                {"name":"coins", "size":[20,20], "color":(255, 193, 37)}
            ],
            "status": [
                {"player_1_distance":str(scene_info["player1"]["distance"]),
                 "player_1_velocity":str(scene_info["player1"]["velocity"]),
                 "player_1_coin":str(scene_info["player1"]["coin"]),
                 "player_2_distance": str(scene_info["player2"]["distance"]),
                 "player_2_velocity": str(scene_info["player2"]["velocity"]),
                 "player_2_coin": str(scene_info["player2"]["coin"]),
                 "player_3_distance": str(scene_info["player3"]["distance"]),
                 "player_3_velocity": str(scene_info["player3"]["velocity"]),
                 "player_3_coin": str(scene_info["player3"]["coin"]),
                 "player_4_distance": str(scene_info["player4"]["distance"]),
                 "player_4_velocity": str(scene_info["player4"]["velocity"]),
                 "player_4_coin": str(scene_info["player4"]["coin"]),
                 }
            ]
        }

    def get_game_progress(self):
        """
        Get the position of game objects for drawing on the web
        """
        scene_info = self.get_scene_info()
        if self.game_type == "NORMAL":
            return {
                "game_object": {
                    "lane": scene_info["lanes"],
                    "computer_car": scene_info["computer_cars"],
                    "player1_car": [scene_info["player1_pos"]],
                    "player2_car": [scene_info["player2_pos"]],
                    "player3_car": [scene_info["player3_pos"]],
                    "player4_car": [scene_info["player4_pos"]],}
                    }

        elif self.game_type == "COIN":
            return {
                "game_object": {
                    "lane": scene_info["lanes"],
                    "coins":scene_info["coins"],
                    "computer_car": scene_info["computer_cars"],
                    "player1_car": [scene_info["player1_pos"]],
                    "player2_car": [scene_info["player2_pos"]],
                    "player3_car": [scene_info["player3_pos"]],
                    "player4_car": [scene_info["player4_pos"]],}
                    }

    def get_game_result(self):
        """
        Get the game result for the web
        """
        scene_info = self.get_scene_info()
        result = []
        ranking = []
        for user in scene_info["game_result"]:
            result.append("GAME_DRAW")
            ranking.append(str(user.car_no + 1) + "P")

        return {
            "frame_used": scene_info["frame"],
            "result": result,
            "ranking": ranking
        }

    def get_keyboard_command(self):
        """
        Get the command according to the pressed keys
        """
        key_pressed_list = pygame.key.get_pressed()
        cmd_1P = []
        cmd_2P = []

        if key_pressed_list[pygame.K_LEFT]: cmd_1P.append("MOVE_LEFT")
        if key_pressed_list[pygame.K_RIGHT]:cmd_1P.append("MOVE_RIGHT")
        if key_pressed_list[pygame.K_UP]:cmd_1P.append("SPEED")
        if key_pressed_list[pygame.K_DOWN]:cmd_1P.append("BREAK")

        if key_pressed_list[pygame.K_a]: cmd_2P.append("MOVE_LEFT")
        if key_pressed_list[pygame.K_d]:cmd_2P.append("MOVE_RIGHT")
        if key_pressed_list[pygame.K_w]:cmd_2P.append("SPEED")
        if key_pressed_list[pygame.K_s]:cmd_2P.append("BREAK")

        return [cmd_1P, cmd_2P]


if __name__ == '__main__':
    pygame.init()
    display = pygame.display.init()
    game = Game(4)

    while game.isRunning():
        game.update(commands)
        game.draw()

    pygame.quit()
