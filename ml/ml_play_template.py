class MLPlay:
    def __init__(self):
        self.other_cars_position = []
        self.coins_pos = []
        print("Initial ml script")

    def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        """

        if scene_info.__contains__("coin"):
            self.coin_pos = scene_info["coin"]

        return ["SPEED"]

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass
