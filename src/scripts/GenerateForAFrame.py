import argparse
from ..Animate_img import animate_image

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
    "--frame_num",
    type=int,
    nargs="?",
    help="Specify the frame number you wanted to animate.",
)

parser.add_argument(
    "--frame_range",
    type=str,
    nargs="?",
    help="Specify the range of frames you wanted to animate.\nAccepted Format: '[0-9]+-[0-9]+'",
)

parser.add_argument(
    "--video",
    type=bool,
    nargs="?",
    default=False,
    help="Whether you want video as output. NOTE: if set to True, frame_range must be specified.",
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
            "Syntax Error: argument \'--frame_range\' is not in specified format. Type '-h' for help."
        )
        exit(0)
else:
    if (args.frame_num == None):
        print("Invalid argument: '--frame_num' must be specified.")
    elif (args.vid_path == None): 
        print("Invalid argument: '--vid_path' must be specified.")
    else:
        animate_image(args.vid_path, args.pos_2d_path, args.game_log_path, args.frame_num)