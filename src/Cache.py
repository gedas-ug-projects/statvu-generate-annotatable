class Cache:
    prev_pos_2d_path = ""
    prev_game_log_path = ""
    prev_track_data = {}
    prev_player_data = {}

    @staticmethod
    def isSameGame(pos_2d_path: str, game_log_path: str) -> bool:
        return pos_2d_path == Cache.prev_pos_2d_path and game_log_path == Cache.prev_game_log_path
    
    @staticmethod
    def refreshCache(pos_2d_path: str, game_log_path: str, track_data, player_data):
        Cache.prev_pos_2d_path = pos_2d_path
        Cache.prev_game_log_path = game_log_path
        Cache.prev_track_data = track_data
        Cache.prev_player_data = player_data
