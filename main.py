import pygame

from game import playingMode,I_Commander,coinPlayMode,sound_controller


if __name__ == '__main__':
    pygame.init()
    display = pygame.display.init()

    sound_controller = sound_controller.SoundController("off")
    game = coinPlayMode.CoinMode(4,sound_controller)
    # game = playingMode.PlayingMode(4,sound_controller)
    sound_controller.play_music()

    while game.isRunning():
        commands = {}
        for i in range(4):
            commands["ml_" + str(i+1) + "P"] = I_Commander.KeyBoardCommander(i).getControlDict()

        game.ticks()
        game.handle_event()
        game.detect_collision()
        game.update_sprite(commands)
        game.draw_bg()
        game.drawAllSprites()
        game.flip()

    pygame.quit()
