import pygame

from .playingMode import PlayingMode

# TODO
'''need some fuction same as arkanoid which without dash in the name of fuction'''


class RacingCar:
    def __init__(self, user_num: int):
        self.game_mode = PlayingMode(user_num)


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
                # "players_velocity":self.game_mode.user_vel
                }

    def update(self, p1_cmd, p2_cmd=[], p3_cmd=[], p4_cmd=[]):
        commands = [p1_cmd, p2_cmd, p3_cmd, p4_cmd]
        self.game_mode.ticks()
        self.game_mode.handle_event()
        self.game_mode.detect_collision()
        self.game_mode.update_sprite(commands)
        if not self.isRunning():
            return "QUIT"
        self.draw()

        pass

    def reset(self):
        # self.game_mode.

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
        computer_cars_pos = []
        lanes_pos = []
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
        for lane in self.game_mode.lanes:
            lanes_pos.append(lane.rect.center)
        scene_info = {
            "frame": self.game_mode.frame,
            "status": self.game_mode.status,
            "computer_cars": computer_cars_pos,
            "lanes": lanes_pos,
            "player1": player_1_pos,
            "player2": player_2_pos,
            "player3": player_3_pos,
            "player4": player_4_pos
        }
        return scene_info

    def get_game_info(self):
        """
        Get the scene and object information for drawing on the web
        """
        return {
            "scene": {
                "size": [600, 800]
            },
            "game_object": [
                {"name": "lane", "size": [5, 30], "color": (255, 255, 255)},
                {"name": "computer_car", "size": [40, 60], "color": (0, 191, 255)},
                {"name": "player1_car", "size": [40, 60], "color": (255, 246, 143)},
                {"name": "player2_car", "size": [40, 60], "color": (0, 255, 127)},
                {"name": "player3_car", "size": [40, 60], "color": (255, 191, 203)},
                {"name": "player4_car", "size": [40, 60], "color": (171, 130, 255)},
            ]
        }

    def get_game_progress(self):
        """
        Get the position of game objects for drawing on the web
        """
        scene_info = self.get_scene_info()

        return {
            "game_object": {
                "lane": scene_info["lanes"],
                "computer_car": scene_info["computer_cars"],
                "player1_car": [scene_info["player1"]],
                "player2_car": [scene_info["player2"]],
                "player3_car": [scene_info["player3"]],
                "player4_car": [scene_info["player4"]],

            }
        }

    def get_game_result(self):
        """
        Get the game result for the web
        """
        scene_info = self.get_scene_info()

        return {
            "frame_used": scene_info["frame"],
            "result": [scene_info["status"]]
        }


if __name__ == '__main__':
    pygame.init()
    display = pygame.display.init()
    game = Game(4)

    while game.isRunning():
        game.update(commands)
        game.draw()
    pygame.quit()
