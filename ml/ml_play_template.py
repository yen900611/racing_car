# TODO
class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0
        self.car_pos = ()

        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        self.car_pos = scene_info[self.player]
        # self.car_vel = scene_info["players_velocity"][self.player_no]

        if scene_info["status"] != "ALIVE":
            return "RESET"

        return {"frame": scene_info["frame"], "command": ["MOVE_LEFT","SPEED"]}


    def reset(self):
        """
        Reset the status
        """
        pass
