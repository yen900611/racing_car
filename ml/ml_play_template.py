class MLPlay:
    def __init__(self,*args,**kwargs):
        self.other_cars_position = []
        self.coins_pos = []
        print("Initial ml script")

    def update(self, scene_info: dict,*args,**kwargs):
        """
        Generate the command according to the received scene information
        """
        # print(scene_info)
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        return ["SPEED"]

    def reset(self):
        """
        Reset the status
        """
        # print("reset ml script")
        pass
