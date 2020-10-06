import pygame
import time

from game import playingMode,I_Commander,coinPlayMode

if __name__ == '__main__':
    pygame.init()
    display = pygame.display.init()
    # game = coinPlayMode.CoinMode(4)
    game = playingMode.PlayingMode(4)

    while game.isRunning():
        commands = []
        for i in range(4):
            commands.append(I_Commander.KeyBoardCommander(i).getControlDict())
        game.ticks()
        game.handle_event()
        game.detect_collision()
        game.update_sprite(commands)
        game.draw_bg()
        game.drawAllSprites()
        game.flip()

    pygame.quit()
