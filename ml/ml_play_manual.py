import pygame

LEFT_cmd = "MOVE_LEFT"
RIGHT_cmd = "MOVE_RIGHT"
SPEED_cmd = "SPEED"
BRAKE_cmd = "BRAKE"

class MLPlay:
    def __init__(self):
        self.other_cars_position = []
        self.coins_pos = []
        print("Initial ml script")

    def update(self, scene_info: dict, keyboard: list = [], *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        actions = []
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"
        if pygame.K_w in keyboard or pygame.K_UP in keyboard:
            actions.append("MOVE_LEFT")
        elif pygame.K_a in keyboard or pygame.K_LEFT in keyboard:
            actions.append("BRAKE")
        elif pygame.K_d in keyboard or pygame.K_RIGHT in keyboard:
            actions.append("SPEED")
        elif pygame.K_s in keyboard or pygame.K_DOWN in keyboard:
            actions.append("MOVE_RIGHT")
        else:
            return ["NONE"]

        return actions

    def reset(self):
        """
        Reset the status
        """
        # print("reset ml script")
        pass
