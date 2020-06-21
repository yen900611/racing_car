def normal_game_progress(scene_info: dict):
    return {"game_object": {
        "lane": scene_info["lanes"],
        "computer_car": scene_info["computer_cars"],
        "player1_car": [scene_info["player1_pos"]],
        "player2_car": [scene_info["player2_pos"]],
        "player3_car": [scene_info["player3_pos"]],
        "player4_car": [scene_info["player4_pos"]],
        "player1_car_icon": [(730, 395)],
        "player2_car_icon": [(730, 430)],
        "player3_car_icon": [(730, 465)],
        "player4_car_icon": [(730, 500)],
    },
        "status": {
        "player_1_distance": scene_info["player_1_distance"],
        "player_1_velocity": scene_info["player_1_velocity"],
        "player_2_distance": scene_info["player_2_distance"],
        "player_2_velocity": scene_info["player_2_velocity"],
        "player_3_distance": scene_info["player_3_distance"],
        "player_3_velocity": scene_info["player_3_velocity"],
        "player_4_distance": scene_info["player_4_distance"],
        "player_4_velocity": scene_info["player_4_velocity"], }
    }


def coin_game_progress(scene_info: dict):
    return {"game_object": {
        "lane": scene_info["lanes"],
        "coin": scene_info["coin"],
        "computer_car": scene_info["computer_cars"],
        "player1_car": [scene_info["player1_pos"]],
        "player2_car": [scene_info["player2_pos"]],
        "player3_car": [scene_info["player3_pos"]],
        "player4_car": [scene_info["player4_pos"]],
        "player1_car_icon": [(730, 395)],
        "player2_car_icon": [(730, 430)],
        "player3_car_icon": [(730, 465)],
        "player4_car_icon": [(730, 500)],
    },
        "status": {
        "player_1_distance": scene_info["player_1_distance"],
        "player_1_velocity": scene_info["player_1_velocity"],
        "player_1_coin": scene_info["player_1_coin"],
        "player_2_distance": scene_info["player_2_distance"],
        "player_2_velocity": scene_info["player_2_velocity"],
        "player_2_coin": scene_info["player_2_coin"],
        "player_3_distance": scene_info["player_3_distance"],
        "player_3_velocity": scene_info["player_3_velocity"],
        "player_3_coin": scene_info["player_3_coin"],
        "player_4_distance": scene_info["player_4_distance"],
        "player_4_velocity": scene_info["player_4_velocity"],
        "player_4_coin": scene_info["player_4_coin"], }
    }
