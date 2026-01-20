import pandas as pd
from extract import get_all_games, get_all_players_stats

def get_players(players_stats):
    players = players_stats[[
        "player.code", 
        "player.name", 
        "player.age"
    ]]
    players = players.rename(columns = {
        "player.code": "code",
        "player.name": "name",
        "player.age": "age"
    })
    return players

def get_players_average_stats(players_stats):
    players_average_stats = players_stats[[
        "player.code", 
        "gamesPlayed", 
        "minutesPlayed", 
        "offensiveReboundsPercentage", 
        "defensiveReboundsPercentage", 
        "reboundsPercentage", 
        "assistsRatio", 
        "turnoversRatio", 
        "twoPointAttemptsRatio", 
        "threePointAttemptsRatio",
        "freeThrowsRate"
    ]]

    players_average_stats = players_average_stats.rename(columns={
        "player.code": "player_code",
        "gamesPlayed": "games_played",
        "minutesPlayed": "minutes_played",
        "offensiveReboundsPercentage": "offensive_rebounds_percentage",
        "defensiveReboundsPercentage": "defensive_rebounds_percentage",
        "reboundsPercentage": "rebounds_percentage",
        "assistsRatio": "assists_ratio",
        "turnoversRatio": "turnovers_ratio",
        "twoPointAttemptsRatio": "two_point_attempts_ratio",
        "threePointAttemptsRatio": "three_point_attempts_ratio",
        "freeThrowsRate": "free_throws_rate"
    })

    return players_average_stats

def get_teams(games_stats):
    teams = games_stats[games_stats["Round"] == 1]
    teams_home = teams[["homecode", "hometeam"]].rename(columns={"homecode":"code", "hometeam":"team"})
    teams_away = teams[["awaycode", "awayteam"]].rename(columns={"awaycode":"code", "awayteam":"team"})
    teams_all = pd.concat([teams_home, teams_away], ignore_index=True)
    teams_all.rename(columns = {
        "team": "name"
    })
    return teams_all

def get_games(games_stats):
    games = games_stats[["Round", "group", "date", "time", "homecode", "homescore", "awaycode", "awayscore"]]
    games = games.rename(columns = {
        "Round": "round",
        "homecode": "home_team_code",
        "homescore": "home_team_score",
        "awaycode": "away_team_code",
        "awayscore": "away_team_score"
    })
    return games

def get_players_teams(players_stats):
    players_teams = players_stats[["player.code", "player.team.code"]]
    players_teams = players_teams.rename(columns = {
        "players.code": "player_code",
        "player.team.code": "team_code"
    })
    return players_teams

def transform_data(season):
    players_stats = get_all_players_stats(season)
    games_stats = get_all_games(season)
    players = get_players(players_stats)
    players_average_stats = get_players_average_stats(players_stats)
    teams = get_teams(games_stats)
    games = get_games(games_stats)
    players_teams = get_players_teams(players_stats)
    return players, players_average_stats, teams, games, players_teams
