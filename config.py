GAME_VERSION = "1.1"

from argparse import ArgumentTypeError

# test to push
# test to push again
# test to push and build
def positive_int(string):
    value = int(string)
    if value < 1:
        raise ArgumentTypeError()
    return value


GAME_PARAMS = {
    "()": {
        "prog": "RacingCar",
        "game_usage": "%(prog)s [user_num]"
    },
    # "difficulty": {
    #     "choices": ("EASY", "NORMAL", "HARD"),
    #     "metavar": "difficulty",
    #     "help": "Specify the game style. Choices: %(choices)s"
    # },
    "user_num": {
        "type": positive_int,
        "nargs": "?",
        "default": 3,
        "help": ("[Optional] The score that the game will be exited "
                 "when either side reaches it.[default: %(default)s]")
    }
}

from .game.RacingCar import RacingCar
import pygame

GAME_SETUP = {
    "game": RacingCar,
    "keyboards": [
        {pygame.K_LEFT: "MOVE_LEFT",
         pygame.K_RIGHT: "MOVE_RIGHT",
         pygame.K_UP: "SPEED",
         pygame.K_DOWN: "BRAKE"},

        {pygame.K_a: "MOVE_LEFT",
         pygame.K_d: "MOVE_RIGHT",
         pygame.K_w: "SPEED",
         pygame.K_s: "BRAKE"},

        # {pygame.K_SPACE:"MOVE_LEFT" ,
        #  pygame.K_SPACE:"MOVE_RIGHT" ,
        #  pygame.K_SPACE:"SPEED" ,
        #  pygame.K_SPACE:"BRAKE" },
        #
        # {"MOVE_LEFT": pygame.K_SPACE,
        #  "MOVE_RIGHT": pygame.K_SPACE,
        #  "SPEED": pygame.K_SPACE,
        #  "BRAKE": pygame.K_SPACE}

    ],
    "ml_clients": [
        {"name": "ml_1P", "args": ("player1",)},
        {"name": "ml_2P", "args": ("player2",)},
        {"name": "ml_3P", "args": ("player3",)},
        {"name": "ml_4P", "args": ("player4",)}
    ]
}
