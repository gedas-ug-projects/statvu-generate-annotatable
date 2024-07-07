"""
Automation script for generating game and 2d postion image side-by-side. 

This script is written specifically for statvu dataset file structure and naming convention. 
"""

from ..Animate_img import animate_image
from ..Util import getTotalFrames
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-frame_inc",
    type=int,
    default=15,
    help="Number of frames between two consecutive sample.",
)

args = parser.parse_args()


def calcNumOfPeriods(game_path: str) -> int:
    num_files = len(os.listdir(f"./data/{game_name}"))
    """
    There's always a game_log file and a track file + video for each period...
    """
    return (num_files - 1) // 2


if __name__ == "__main__":
    games_dir = [
        name
        for name in os.listdir("./data")
        if os.path.isdir(os.path.join("./data", name))
    ]

    for game_name in games_dir:
        game_log_path = f"./data/{game_name}/{game_name}.json"

        if not os.path.exists(game_log_path):
            print(f"Game log path ({game_log_path}) does not exit. Aborting...")
            exit(0)

        for period_i in range(1, calcNumOfPeriods(f"./data/{game_name}") + 1):
            vid_path = f"./data/{game_name}/{game_name}.Q{period_i}.2D-POS.mp4"
            track_path = f"./data/{game_name}/{game_name}.Q{period_i}.2D-POS.json"

            if not os.path.exists(vid_path) and not os.path.exists(track_path):
                print(
                    f"Video path ({vid_path}) or track path ({track_path}) does not exist. Aborting..."
                )
                exit(0)

            total_frame = getTotalFrames(track_path)
            for frame_num in range(0, total_frame, args.frame_inc):
                animate_image(vid_path, track_path, game_log_path, frame_num)
