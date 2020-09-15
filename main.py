import pygame
import time

from game import playingMode,I_Commander,coinPlayMode

if __name__ == '__main__':
    pygame.init()
    display = pygame.display.init()
    # game = coinPlayMode.CoinPlayingMode(4)
    game = playingMode.PlayingMode(3)

    while game.isRunning():
        commands = []
        for i in range(3):
            commands.append(I_Commander.KeyBoardCommander(i).getControlDict())
        game.ticks()
        game.handle_event()
        game.detect_collision()
        game.update_sprite(commands)
        game.draw_bg()
        game.flip()

    pygame.quit()
