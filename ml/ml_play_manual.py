import pygame


class MLPlay:
    def __init__(self,*args,**kwargs):
        self.other_cars_position = []
        self.coins_pos = []
        print("Initial ml script")

    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        # print(scene_info)
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        command = []
        if pygame.K_LEFT in keyboard:
            command.append("BRAKE")
        if pygame.K_RIGHT in keyboard:
            command.append("SPEED")
        if pygame.K_UP in keyboard:
            command.append("MOVE_LEFT")
        if pygame.K_DOWN in keyboard:
            command.append("MOVE_RIGHT")

        return command
    def reset(self):
        """
        Reset the status
        """
        # print("reset ml script")
        pass
