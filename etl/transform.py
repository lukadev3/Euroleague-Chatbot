import pandas as pd
from extract import get_all_games, get_advanced_players_stats, get_scoring_players_stats

def get_teams(games_stats):
    teams = games_stats[games_stats["Round"] == 1].copy()
    teams_home = teams[["homecode", "hometeam"]].rename(columns={"homecode":"code", "hometeam":"team"})
    teams_away = teams[["awaycode", "awayteam"]].rename(columns={"awaycode":"code", "awayteam":"team"})
    teams_all = pd.concat([teams_home, teams_away], ignore_index=True)
    teams_all = teams_all.rename(columns = {
        "team": "name"
    })
    return teams_all

def get_games(games_stats):
    games = games_stats[[
        "Round", 
        "group", 
        "date", 
        "time", 
        "homecode", 
        "homescore", 
        "awaycode", 
        "awayscore"
    ]].copy()
    games = games.rename(columns = {
        "Round": "round",
        "group": "type",
        "homecode": "home_team_code",
        "homescore": "home_team_score",
        "awaycode": "away_team_code",
        "awayscore": "away_team_score"
    })
    return games

def get_players(players_advanced_stats):
    players = players_advanced_stats[[
        "player.code", 
        "player.name", 
        "player.age"
    ]].copy()
    players = players.rename(columns = {
        "player.code": "code",
        "player.name": "name",
        "player.age": "age"
    })
    return players


def get_players_teams(players_advanced_stats):
    players_teams = players_advanced_stats[[
        "player.code", 
        "player.team.code"
    ]].copy()
    players_teams = players_teams.rename(columns = {
        "player.code": "player_code",
        "player.team.code": "team_code"
    })
    return players_teams

def get_players_average_stats(players_advanced_stats, players_scoring_stats):
    advanced = players_advanced_stats[[
        "player.code", 
        "gamesPlayed", 
        "minutesPlayed", 
        "offensiveReboundsPercentage", 
        "defensiveReboundsPercentage", 
        "reboundsPercentage", 
        "assistsRatio", 
        "turnoversRatio"
    ]].copy()
    advanced = advanced.rename(columns={
        "player.code": "player_code",
        "gamesPlayed": "games_played",
        "minutesPlayed": "minutes_played",
        "offensiveReboundsPercentage": "offensive_rebounds_percentage",
        "defensiveReboundsPercentage": "defensive_rebounds_percentage",
        "reboundsPercentage": "rebounds_percentage",
        "assistsRatio": "assists_ratio",
        "turnoversRatio": "turnovers_ratio"
    })
    scoring = players_scoring_stats[[
        "player.code",
        "twoPointAttemptsShare",
        "threePointAttemptsShare",
        "freeThrowsAttemptsShare",
        "twoPointersMadeShare", 
        "threePointersMadeShare", 
        "freeThrowsMadeShare",
        "twoPointRate",
        "threePointRate",
        "pointsFromTwoPointersPercentage",
        "pointsFromThreePointersPercentage",
        "pointsFromFreeThrowsPercentage"
    ]].copy()
    scoring = scoring.rename(columns={
        "player.code": "player_code",
        "twoPointAttemptsShare": "two_point_attempts_share",
        "threePointAttemptsShare": "three_point_attempts_share",
        "freeThrowsAttemptsShare": "free_throws_attempts_share",
        "twoPointersMadeShare": "two_point_made_share", 
        "threePointersMadeShare": "three_point_made_share", 
        "freeThrowsMadeShare": "free_throws_made_share",
        "twoPointRate": "two_point_rate",
        "threePointRate": "three_point_rate",
        "pointsFromTwoPointersPercentage": "points_from_two_percentage",
        "pointsFromThreePointersPercentage": "points_from_three_percentage",
        "pointsFromFreeThrowsPercentage": "points_from_free_throws_percentage"
    })
    players_average_stats = advanced.merge(
        scoring,
        on="player_code",
        how="inner"
    )
    return players_average_stats

def transform_data(season):
    players_advanced_stats = get_advanced_players_stats(season)
    players_scoring_stats = get_scoring_players_stats(season)
    games_stats = get_all_games(season)
    teams = get_teams(games_stats)
    games = get_games(games_stats)
    players = get_players(players_advanced_stats)
    players_teams = get_players_teams(players_advanced_stats)
    players_average_stats = get_players_average_stats(players_advanced_stats, players_scoring_stats)
    return players, players_average_stats, teams, games, players_teams
