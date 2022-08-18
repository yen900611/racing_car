class MLPlay:
    def __init__(self,ai_name:str,*args,**kwargs):
        self.other_cars_position = []
        self.coins_pos = []
        self.ai_name = ai_name
        print("Initial ml script")
        print(ai_name)
        print(kwargs)

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
