"""
Automation script for generating game and 2d postion image side-by-side. 

This script is written specifically for statvu dataset file structure and naming convention. 
"""

from ..Constant import Constant
from ..Animate_img import animate_image
from ..Util import getTotalFrames
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--frame_inc",
    type=int,
    default=15,
    help="Number of frames between two consecutive sample.",
)

args = parser.parse_args()

if __name__ == "__main__":
    game_log_names = [
        name
        for name in os.listdir(Constant.DATA_DIR + Constant.GAME_LOGS)
        if os.path.isdir(Constant.DATA_DIR + Constant.GAME_LOGS + f"/{name}")
    ]

    for game_log_name in game_log_names:
        # get game id
        game_id = game_log_name.split(".").pop()

        # game log access setup
        abs_game_log_dir = f"{Constant.DATA_DIR}{Constant.GAME_LOGS}{game_log_name}/"
        game_logs = [f"{abs_game_log_dir}/{log_name}" for log_name in os.listdir(abs_game_log_dir)]

        if (len(game_logs) == 0):
            print(f"Could not read game_log in {abs_game_log_dir}")
            continue

        game_log_pth = game_logs.pop()

        # 2d player position access setup
        track_names = [
            file_name
            for file_name in os.listdir(
                f"{Constant.DATA_DIR}{Constant.PLAYER_2D_POSITION}"
            )
            if game_id in file_name
        ]

        track_names = sorted(track_names)

        player_2d_tracks_pths = [
            f"{Constant.DATA_DIR}{Constant.PLAYER_2D_POSITION}{track_name}"
            for track_name in track_names
        ]

        # game replay access setup
        replay_names = [
            file_name
            for file_name in os.listdir(
                f"{Constant.DATA_DIR}{Constant.GAME_REPLAYS}"
            )
            if game_id in file_name
        ]
        
        replay_names = sorted(replay_names)

        game_replays_pths = [
            f"{Constant.DATA_DIR}{Constant.GAME_REPLAYS}{replay_name}"
            for replay_name in replay_names
        ]

        # For now, if there's different number of game periods in player tracks and game replays, the game will be skipped        
        if len(player_2d_tracks_pths) != len(game_replays_pths):
            print(f"Skipping game with id of '{game_id}' has different number of periods for player-2d-tracks and game-replays")
            continue

        for period in range(1, len(player_2d_tracks_pths) + 1):
            vid_pth = game_replays_pths[period]
            track_pth = player_2d_tracks_pths[period]

            # validae that there video and track files exist
            if not os.path.exists(vid_pth) and not os.path.exists(track_pth):
                print(
                    f"Video path ({vid_pth}) or track path ({track_pth}) does not exist. Skipping..."
                )
                continue

            total_frame = getTotalFrames(track_pth)
            for frame_num in range(0, total_frame, args.frame_inc):
                animate_image(vid_pth, track_pth, game_log_pth, frame_num)