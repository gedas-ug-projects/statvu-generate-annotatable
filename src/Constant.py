class Constant:
    """A class for handling constants"""
    NORMALIZATION_COEF = 7
    PLAYER_CIRCLE_SIZE = 12 / NORMALIZATION_COEF
    TEAM_CIRCLE_SIZE = 17 / NORMALIZATION_COEF
    INTERVAL = 10
    DIFF = 6
    X_MIN = 0
    X_MAX = 100
    Y_MIN = 0
    Y_MAX = 50
    COL_WIDTH = 0.3
    SCALE = 1.65
    FONTSIZE = 6
    X_CENTER = X_MAX / 2 - DIFF / 1.5 + 0.10
    Y_CENTER = Y_MAX - DIFF / 1.5 - 0.35
    MESSAGE = 'You can rerun the script and choose any event from 0 to '


# class Constant:
#     """A class for handling constants"""
#     NORMALIZATION_COEF = 7
#     PLAYER_CIRCLE_SIZE = 12 / NORMALIZATION_COEF
#     TEAM_CIRCLE_SIZE = 17 / NORMALIZATION_COEF
#     INTERVAL = 10
#     # DIFF = 6
#     X_MIN = 15
#     X_MAX = 92
#     Y_MIN = 11
#     Y_MAX = 51
#     COL_WIDTH = 0.3
#     SCALE = 1.65
#     FONTSIZE = 6
#     # X_CENTER = X_MAX / 2 - DIFF / 1.5 + 0.10
#     # Y_CENTER = Y_MAX - DIFF / 1.5 - 0.35
#     MESSAGE = 'You can rerun the script and choose any event from 0 to '

    # Pre-written query for google drive api
   
    QUERY_ID_OF_720 = "mimeType='application/vnd.google-apps.folder' and name='720'"
    """ID of dir 720 which store all Statvu videos"""
    QUERY_ALL_VIDS = "1-0K7OsofHtGtXQon9kJIeqyyuYgQmhO9' in parents"
    """All videos in 720 (hardcoded dir id). NOTE append to this query to filter videos"""
    QUERY_VIDS_ID_OF_17725 = QUERY_ALL_VIDS + " and name contains '17725'"
    """Example for appending queries"""
    QUERY_ALL_GAME_LOG = "'19PadFkgZA-Z5WF_lvI_fStQpfDdIMEtD' in parents"
    """Query all game logs in statvu-gmae-logs"""
    QUERY_ALL_2D_TRACKS = "'1OCxnK8ssQTlD_osH9b3OsFI39lCIFbms' in parents"
    """Query all 2d player position by frame"""