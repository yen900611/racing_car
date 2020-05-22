# TODO
class MLPlay:
    def __init__(self, player_no):
        self.player_no = player_no

        self.car_pos = ()

        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        self.car_pos = scene_info[self.player_no]


        if scene_info["status"] != "ALIVE":
            return "RESET"

        return {"frame": scene_info["frame"], "command": ["MOVE_LEFT","SPEED"]}


    def reset(self):
        """
        Reset the status
        """
        pass
