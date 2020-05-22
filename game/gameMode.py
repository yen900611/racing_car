"""
This is a base class for different mode in game.
"""
import pygame
from .env import *


class GameMode(object):
    def __init__(self, pygame_screen=pygame.display.set_mode((WIDTH, HEIGHT)), bg_img=pygame.Surface((WIDTH, HEIGHT))):
        self.screen = pygame_screen
        self.bg_img = bg_img
        self.bg_rect = bg_img.get_rect()
        self.clock = pygame.time.Clock()
        self.running = True
        self.willChange = False
        self.nextMode = None
        self.all_sprites = pygame.sprite.Group()

    def ticks(self, fps=FPS):
        """This method should be called once per frame.
        It will compute how many milliseconds have passed since the previous call.
        :param fps: frame per second 每秒的繪圖次數
        :return: None
        """
        self.clock.tick(fps)

    def handle_event(self):
        """ Handle the event from window , mouse or button.

        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False

    def detect_collision(self):
        """ Detect the collision event between sprites.
        :return: None
        """
        pass

    def update_sprite(self, command):
        """ This function should update every sprite in games.
        :return: None
        """
        self.all_sprites.update()
        pass

    def draw_bg(self):
        """  Draw a background on screen.
        :return:None
        """
        self.screen.blit(self.bg_img, self.bg_rect)

    def drawAllSprites(self):
        """  This function should draw every sprite on specific surface.
        :return: None
        """
        self.all_sprites.draw(self.screen)

    def flip(self):
        """Update the full display Surface to the screen
        :return:None
        """
        pygame.display.flip()

    def isRunning(self) -> bool:
        return self.running

    def getNextMode(self):
        """
         :return: gameMode
        """
        if self.willChange:
            if self.nextMode:
                self.willChange = False
                return self.nextMode
        return self

    def draw_information(self,surf,text,size,x,y):
        font = pygame.font.Font(pygame.font.match_font("arial"), size)
        text_surface = font.render(text , True , WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surf.blit(text_surface , text_rect)