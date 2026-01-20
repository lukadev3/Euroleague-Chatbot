from euroleague_api.team_stats import TeamStats
from euroleague_api.player_stats import PlayerStats

team_stats = TeamStats()
player_stats = PlayerStats()

def get_all_games(season):
    global team_stats
    return team_stats.get_gamecodes_season(season)

def get_all_players_stats(season):
    global player_stats
    return player_stats.get_player_stats_single_season(season=season, endpoint="advanced")