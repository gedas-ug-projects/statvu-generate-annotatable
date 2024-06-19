import argparse
import os
from multiprocessing import Process
from ..DriveHandler import *


parser = argparse.ArgumentParser()

parser.add_argument(
    "-n", type=int, default=5, help="Number of games to fetch. Default: 5."
)

parser.add_argument(
    "-has_browser",
    type=bool,
    default=False,
    help="Whether the environment supports browser verification. Default: False.",
)

args = parser.parse_args()

if __name__ == "__main__":
    # With GUI: reset_Auth() will work
    # Without GUI: must transfer in the refresh token
    #     therefore, will need a token validation function

    if args.has_browser:
        reset_Auth()
    else:
        if not validate_Auth():
            print("No valid token.json file found. Aborting...")
            exit(0)

    game_log_list = query(f"'19PadFkgZA-Z5WF_lvI_fStQpfDdIMEtD' in parents")
    i = 0

    for game_log_name, game_log_id, size in game_log_list:
        if i > args.n:
            break
        i += 1

        game_id = game_log_name.split(".")[-1]
        videos_list = query(
            f"'1-0K7OsofHtGtXQon9kJIeqyyuYgQmhO9' in parents and name contains '{game_id}'"
        )
        track_list = query(
            f"'1OCxnK8ssQTlD_osH9b3OsFI39lCIFbms' in parents and name contains '{game_id}'"
        )
        game_log_json_name, game_log_json_id, game_log_json_size = query(
            f"'{game_log_id}' in parents"
        )[
            0
        ]  # implied that only one file is in the game log dir

        """
        Video and 2d track matching is basic. Sort the video and track files (done by query()) and they 
        will naturally match. The limitation of this is that the number of videos and tracks must match. 
        In the dataset, we are missing some track data. So, here the entire game is discarded. 

        If more data is required, we can utilize games with missing tracks with more sophisticated matching.
        """
        if len(videos_list) == len(track_list):
            # create a dir for game_id
            path = f"./data/{game_log_name}"
            if not os.path.exists(path):
                os.makedirs(path)

            procs = []
            # create process for downloading game_log
            game_log_id
            game_log_proc = Process(
                target=download_file,
                args=(game_log_json_id, f"{path}/{game_log_name}.json"),
            )
            procs.append(game_log_proc)

            # create process for downloading videos and tracks
            for i in range(0, len(videos_list)):
                vid_name, vid_id, track_size = videos_list[i]
                track_name, track_id, track_size = track_list[i]
                new_vid_name = ".".join([s for s in track_name.split(".")[:-1]])

                vid_proc = Process(
                    target=download_file, args=(vid_id, f"{path}/{new_vid_name}.mp4")
                )
                track_proc = Process(
                    target=download_file, args=(track_id, f"{path}/{track_name}")
                )
                procs += [vid_proc, track_proc]

            for proc in procs:
                proc.start()

            for proc in procs:
                proc.join()
