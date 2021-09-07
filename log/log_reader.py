import pickle
from os import path
import json

if __name__ == "__main__":

    log_file = path.join(path.dirname(__file__),
                         'log_template.pickle')
    with open(log_file, 'rb') as fp:
        data = pickle.load(fp)

    # Data structure in log file
    print("# Data structure")
    print(data.keys())
    print("")

    # Data structure of scene_info in single frame
    print("# Single Frame Info")
    single_scene = data['scene_info'][200]
    # print(single_scene)
    print(json.dumps(single_scene))
    print("")

    # Data structure of command in single frame
    print("# Single Commands Info")
    single_frame_commands = data['command'][200]
    print(single_frame_commands)
    P1_commands = single_frame_commands[0]
    P2_commands = single_frame_commands[1]
    print("Player 1 Commands = ", P1_commands)
    print("Player 2 Commands = ", P2_commands)
    print("")

    for i in range(0, len(data)):
        single_scene = data['scene_info'][i]
        single_frame_commands = data['command'][i]
