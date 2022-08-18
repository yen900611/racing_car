import pygame
from src import RacingCar

from src.env import FPS
from mlgame.view.view import PygameView
from mlgame.game.generic import quit_or_esc

if __name__ == '__main__':
    pygame.init()
    # game = RacingCar.RacingCar(user_num=2, game_mode="NORMAL", car_num=50, racetrack_length=10000, game_times=1, sound="off")
    game = RacingCar.RacingCar(user_num=1, game_mode="RELIVE", car_num=20, racetrack_length=30000, game_times=1, sound="off")
    # game = RacingCar.RacingCar(2, "COIN", 30, 1000, 1, "off")
    scene_init_info_dict = game.get_scene_init_data()
    game_view = PygameView(scene_init_info_dict)
    frame_count = 0
    while game.isRunning() and not quit_or_esc():
        pygame.time.Clock().tick_busy_loop(FPS)
        game.update(game.get_keyboard_command())
        game_progress_data = game.get_scene_progress_data()
        game_view.draw(game_progress_data)
        frame_count += 1

    pygame.quit()
