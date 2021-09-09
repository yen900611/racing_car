import pygame
from os import path
from .env import *

class SoundController():
    def __init__(self, is_sound_on):
        if is_sound_on == "on":
            self.is_sound_on = True
            try:
                pygame.mixer.init()
                self.hit_sound = pygame.mixer.Sound(path.join(SOUND_DIR, "explosion.wav"))
                self.coin_sound = pygame.mixer.Sound(path.join(SOUND_DIR, "coin.wav"))
                self.lose_sound = pygame.mixer.Sound(path.join(SOUND_DIR,"Powerup3.wav"))
                pygame.mixer.music.load(path.join(SOUND_DIR, "BGM.mp3"))
                pygame.mixer.music.set_volume(0.4)
            except Exception:
                self.is_sound_on = False

        else:
            self.is_sound_on = False

    def play_music(self):
        if self.is_sound_on:
            pygame.mixer.music.play(-1)
        else:
            pass

    def play_hit_sound(self):
        if self.is_sound_on:
            self.hit_sound.play()
        else:
            pass

    def play_coin_sound(self):
        if self.is_sound_on:
            self.coin_sound.play()
        else:
            pass

    def play_lose_sound(self):
        if self.is_sound_on:
            self.lose_sound.play()
        else:
            pass
