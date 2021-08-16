# from argparse import ArgumentTypeError

# test to push
# test to push again
# test to push and build
# test to push , build and run
# def positive_int(string):
#     value = int(string)
#     if value < 1:
#         raise ArgumentTypeError()
#     return value
from .src.RacingCar import RacingCar
import pygame
from os import path
from mlgame.utils.parse_config import read_json_file, parse_config
from argparse import ArgumentTypeError

GAME_SETUP = {
    "game": RacingCar,

    "ml_clients":RacingCar.ai_clients(),
    "dynamic_ml_clients":True
}

# test to push
# test to push again
# test to push and build
# test to push , build and run
# def positive_int(string):
#     value = int(string)
#     if value < 1:
#         raise ArgumentTypeError()
#     return value

config_file = path.join(path.dirname(__file__), "game_config.json")

config_data = read_json_file(config_file)
GAME_VERSION = config_data["version"]
GAME_PARAMS = parse_config(config_data)

