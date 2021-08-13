import abc

import pygame

class I_Commander(abc.ABC):
    @abc.abstractmethod
    def getControlDict(self) -> dict:
        pass

keyboardSet = [
    {"MOVE_LEFT": pygame.K_UP,
     "MOVE_RIGHT": pygame.K_DOWN,
     "SPEED": pygame.K_RIGHT,
     "BRAKE": pygame.K_LEFT},

    {"MOVE_LEFT": pygame.K_w,
     "MOVE_RIGHT": pygame.K_s,
     "SPEED": pygame.K_d,
     "BRAKE": pygame.K_a},


    {"MOVE_LEFT": pygame.K_SPACE,
     "MOVE_RIGHT": pygame.K_SPACE,
     "SPEED": pygame.K_SPACE,
     "BRAKE": pygame.K_SPACE},

    {"MOVE_LEFT": pygame.K_SPACE,
     "MOVE_RIGHT": pygame.K_SPACE,
     "SPEED": pygame.K_SPACE,
     "BRAKE": pygame.K_SPACE}

]

class KeyBoardCommander(I_Commander):
    def __init__(self, keyboard_no=0):
        self.no = keyboard_no
        self.speedKey = keyboardSet[keyboard_no]["SPEED"]
        self.brakeKey = keyboardSet[keyboard_no]["BRAKE"]
        self.moveLeftKey = keyboardSet[keyboard_no]["MOVE_LEFT"]
        self.moveRightKey = keyboardSet[keyboard_no]["MOVE_RIGHT"]

    def getControlDict(self):
        keys = pygame.key.get_pressed()
        control_list = []
        control_dic = {"LEFT": keys[self.moveLeftKey],
                       "RIGHT": keys[self.moveRightKey],
                       "SPEED_UP": keys[self.speedKey],
                       "BRAKEDOWN": keys[self.brakeKey]}
        if control_dic["LEFT"]:
            control_list.append("MOVE_LEFT")
        if control_dic["RIGHT"]:
            control_list.append("MOVE_RIGHT")
        if control_dic["SPEED_UP"]:
            control_list.append("SPEED")
        if control_dic["BRAKEDOWN"]:
            control_list.append("BRAKE")

        return control_list

