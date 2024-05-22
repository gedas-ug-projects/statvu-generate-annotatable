import argparse
from ..Animate_img import animate_image
from ..Util import getTotalFrames

parser = argparse.ArgumentParser()

parser.add_argument("--vid_path", type=str, help="Path to game video.")

parser.add_argument(
    "--pos_2d_path",
    type=str,
    help="Path to 2D positional tracking file.\nAccepted Format: JSON",
)

parser.add_argument(
    "--game_log_path", type=str, help="Path to StatVU game log.\n Accepted Format: JSON"
)

parser.add_argument(
    "--video",
    type=bool,
    nargs="?",
    default=False,
    help="Whether you want video as output. NOTE: if set to True, frame_range must be specified.",
)

parser.add_argument(
    "--frame_range",
    type=str,
    nargs="?",
    help="Specify the range of frames you wanted to animate.\nAccepted Format: '[0-9]+-[0-9]+'",
)

parser.add_argument(
    "--frame_inc",
    type=int,
    nargs="?",
    default=1,
    help="Number of frames to increment by. Defaults to 1.",
)

args = parser.parse_args()

if args.video:
    # validate frame_range
    try:
        start_fr, stop_fr = args.frame_range.split("-")
        print("Video generation not yet supported :)")
        exit(0)
        # TODO add animate video later....
    except Exception as error:
        print(
            "Syntax Error: argument '--frame_range' is not in specified format. Type '-h' for help."
        )
        exit(0)
else:
    if (args.vid_path == None): 
        print("Invalid argument: '--vid_path' must be specified.")
    else:
        total_frame = getTotalFrames(args.pos_2d_path)
        for frame_num in range(3500, 3600, args.frame_inc):
            animate_image(args.vid_path, args.pos_2d_path, args.game_log_path, frame_num)
