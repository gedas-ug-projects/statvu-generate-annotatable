import json
import csv
import cv2
import matplotlib.pyplot as plt
import numpy as np
import traceback
import os
from .Constant import Constant
from .Player import Player
from .Team import Team
from .Util import parseFileName
from .Cache import Cache

def extract_player_tracking(path: str):
    """
    Extract data from 2D position data file
    """

    # Opening JSON file
    file = open(path)
    
    # returns JSON object as 
    # a dictionary
    data = json.load(file)

    return data

def extract_player_info(path: str) -> dict[int, Player]:
    """
    Extract team information from original statvu log file
    """

    file = open(path)
    data = json.load(file)
    visitor_data = data["events"][0]["visitor"]
    visit_player_list = []

    visitor: Team = Team(visitor_data["teamid"], True)

    for player_data in visitor_data["players"]:
        player = Player(
            player_data["playerid"],
            player_data["firstname"],
            player_data["lastname"],
            player_data["jersey"],
            visitor
        )

        visit_player_list.append(player)

    home_data = data["events"][0]["home"]
    home_player_list = []

    home: Team = Team(home_data["teamid"], False)

    for player_data in home_data["players"]:
        player = Player(
            player_data["playerid"],
            player_data["firstname"],
            player_data["lastname"],
            player_data["jersey"],
            home
        )

        home_player_list.append(player)

    player_dict = {}

    for player in home_player_list + visit_player_list:
        player_dict[player.id] = player

    return player_dict

def get_player_on_court(track_data, player_dict: dict[int, Player], frame):
    try:
        player_on_court = {}
        track_data_frame = track_data[str(frame)]
        for player in track_data_frame["moment"]["player_positions"][1:]:
            player_on_court[player["player_id"]] = player_dict[player["player_id"]]

        return player_on_court
    except Exception: 
        traceback.print_exc()
        exit(1)

def get_img_player_w_court(title: str, frame_num: int, track_data, player_dict: dict[int, Player]):
    """
    just drawing
    """

    # pyplot configs
    fig,ax = plt.subplots(1)
    plt.title(f'{title}.frame-{frame_num}')
    ax.set_aspect('equal')
    ax.axis('off')

    player_circles = []
    team_circles = []

    track_data_frame = track_data[str(frame_num)]

    for player in track_data_frame["moment"]["player_positions"][1:]:
        player_info = player_dict.get(player["player_id"])
        x = player["x_position"]
        y = player["y_position"]
        t_circle = plt.Circle((x, y), Constant.TEAM_CIRCLE_SIZE, color=player_info.team.color)
        team_circles.append(t_circle)

    for index, player in enumerate(track_data_frame["moment"]["player_positions"][1:]):
        x = player["x_position"]
        y = player["y_position"]
        p_circle = plt.Circle((x, y), Constant.PLAYER_CIRCLE_SIZE, color='#FFFFFF')
        player_circles.append(p_circle)
        # Add text on top of the circle
        text = ax.text(x, y, chr(ord('A') + index), color='black', ha='center', va='center')

    court = plt.imread("./resources/court.png")
    plt.imshow(court, zorder=0, extent=[Constant.X_MIN, Constant.X_MAX, Constant.Y_MAX, Constant.Y_MIN])

    # Now, loop through coord arrays, and create a circle at each x,y pair
    for p_circle, t_circle in zip(player_circles, team_circles):
        ax.add_patch(t_circle)
        ax.add_patch(p_circle)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # A small hack to covert matplotlib image to cv2 compatible image
    fig.canvas.draw()
    b = fig.axes[0].get_window_extent()
    img = np.array(fig.canvas.buffer_rgba())
    img = img[int(b.y0):int(b.y1),int(b.x0):int(b.x1),:]
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)
    img = img[:,:,:3]  # remove alpha channel
    img = np.ascontiguousarray(img)
    img = write_frame_num(img, frame_num)
    return img

def create_csv_id_jersey(title: str, write_path: str, frame: int, track_data, player_dict: dict[int, Player]): 
    row: list[str] = []
    track_data_frame = track_data[str(frame)]

    row.append(title + '.frame-' + str(frame))

    for index, player_json in enumerate(track_data_frame["moment"]["player_positions"][1:]):
        player_id: int = player_json["player_id"]
        player = player_dict[player_id]
        row.append(chr(ord('A') + index))
        row.append(player.jersey)
    
    file = open(write_path, "a+", newline='')
    csv_writer = csv.writer(file, delimiter=",")
    csv_writer.writerow(row)

def get_player_position(title: str, track_data, player_dict, frame_num: int):
    player_on_court = get_player_on_court(track_data, player_dict, frame_num)
    create_csv_id_jersey(title, f"./output/{title}.csv", frame_num, track_data, player_on_court)
    return get_img_player_w_court(title, frame_num, track_data, player_on_court)

def concat_img(img1, img2, output_path: str):
    img = hconcat_resize([img1, img2]) 
    cv2.imwrite(output_path, img)

def getFrame(frame_num: int, vid_path: str):
    cap = cv2.VideoCapture(vid_path)

    # get total number of frames
    totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # check for valid frame number
    if frame_num >= 0 & frame_num <= totalFrames:
        # set frame position
        cap.set(cv2.CAP_PROP_POS_FRAMES,frame_num)

        ret, frame = cap.read()
        frame = write_frame_num(frame, frame_num)
        return frame

def hconcat_resize(img_list, interpolation = cv2.INTER_CUBIC): 
    # take minimum hights 
    h_min = min(img.shape[0] for img in img_list) 
      
    # image resizing  
    im_list_resize = [cv2.resize(img, (int(img.shape[1] * h_min / img.shape[0]), h_min), interpolation = interpolation) for img in img_list] 
    # return final image 
    return cv2.hconcat(im_list_resize) 

def write_frame_num(img, frame_num: int):
    # Write some Text

    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10, 50)
    fontScale              = 1
    fontColor              = (255,255,255)
    thickness              = 2
    lineType               = 2

    cv2.putText(img, str(frame_num), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        thickness,
        lineType)
    
    return img

def animate_image(vid_path: str, track_path: str, game_log_path: str, frame_number: int):
    # Frame compensation: due to inaccuracy in the dataset, some frame compensation may be required
    frame_compensation = 0  # used to offset a fix number of frames to compensate for inaccuracy. 0 means no offset
    title = parseFileName(track_path)
    if not os.path.exists(f'./output/{title}'): os.mkdir(f'./output/{title}')
    # extract information from 2d-position json and game-log json
    if Cache.isSameGame(track_path, game_log_path):
        track_data = Cache.prev_track_data
        player_dict = Cache.prev_player_data
    else:
        track_data = extract_player_tracking(track_path)
        player_dict = extract_player_info(game_log_path)
        Cache.refreshCache(track_path, game_log_path, track_data, player_dict)
    
    try:
        pos_2d = get_player_position(title, track_data, player_dict, frame_number)
        vid_frame = getFrame(frame_number + frame_compensation, vid_path)
        result_path = f'./output/{title}/{title}.frame-{frame_number}.png'
        concat_img(vid_frame, pos_2d, result_path)  # for now don't save image
        plt.close('all')
    except Exception as error:
        print(f'Encountered and Handled Error for frame {frame_number}: {error}')
        print('INFO: check if tracks for this frame is NULL; check if file path is correct')
        plt.close('all')
        traceback.print_exc()


# TODO remove script code after testing
if __name__ == "__main__":
    title = '01-14-2016.SAC.NOP.17647.Q2.2D-POS'
    track_file_path = f'./data/{title}.json'
    game_log_path = './data/01-14-2016.SAC.NOP.17647.json'
    # extract information from 2d-position json and game-log json
    track_data = extract_player_tracking(track_file_path)
    player_dict = extract_player_info(game_log_path)
    video = None
    frame_number = 3000

    try:
        pos_2d = get_player_position(title, track_data, player_dict, frame_number)
        vid_frame = getFrame(frame_number, './data/17647_01-14-2016_3225_Sacramento Kings_3279_New Orleans Pelicans_period2.mp4')
        result_path = f'./output/{title}.frame-{frame_number}.png'
        concat_img(vid_frame, pos_2d, result_path)  # for now don't save image
        plt.close('all')
    except Exception as error:
        print(f'Encountered Error: {error}')
        plt.close('all')