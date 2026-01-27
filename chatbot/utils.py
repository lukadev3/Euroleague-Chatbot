from llama_index.core.objects import SQLTableSchema
from sqlalchemy import text

def load_teams_and_players_from_engine(engine):
    with engine.connect() as conn:
        teams_result = conn.execute(
            text("SELECT DISTINCT name FROM teams ORDER BY name")
        )
        teams = [row[0] for row in teams_result.fetchall()]

        players_result = conn.execute(
            text("SELECT DISTINCT name FROM players ORDER BY name")
        )
        players = [row[0] for row in players_result.fetchall()]
    return teams, players

def get_table_schema_obj(teams, players):
    return [
        SQLTableSchema(
            table_name="games",
            context_str="""
                Table games stores information about EuroLeague matches.
                Each row represents one game.

                Column format:
                - round: integer (e.g. 1, 2, 15)
                - type: text (e.g. "Regular Season", "Playoffs")
                - date: text (format: 'Mon DD, YYYY')
                - time: text (24h format: 'HH:MM')
                - home_team_code: text (3-letter uppercase team code, FK → teams.code)
                - home_team_score: integer
                - away_team_code: text (3-letter uppercase team code, FK → teams.code)
                - away_team_score: integer

                Use this table for questions about matches, scores, rounds, and schedules.
                Do not use this table for questions about players stats.
                Join with teams when team names are required.
            """
        ),
        SQLTableSchema(
            table_name="players",
            context_str=f"""
                Table players contains basic player information.
                Each row represents one player.
                Players names: {players}

                Column format:
                - code: text (unique player identifier, e.g. '004512')
                - name: text (format: 'LASTNAME, FIRSTNAME', uppercase, e.g. 'VILDOZA, LUCA', 'DOBRIC, OGNJEN', 'KALAITZAKIS, PANAGIOTIS')
                - age: integer

                Use this table when questions involve player identities or ages.
                Join with players_average_stats for performance data.
                Join with players_teams to determine the player's team.
            """
        ),
        SQLTableSchema(
            table_name="players_average_stats",
            context_str="""
                Table players_average_stats contains season-level average player statistics.
                Each row represents one player.

                Column format:
                - player_code: text (FK → players.code)
                - games_played: integer
                - minutes_played: float (average minutes per game)
                - offensive_rebounds_percentage: numeric percentage
                - defensive_rebounds_percentage: numeric percentage
                - rebounds_percentage: numeric percentage
                - assists_ratio: numeric percentage
                - turnovers_ratio: numeric percentage
                - two_point_attempts_share: numeric percentage
                - three_point_attempts_share: numeric percentage
                - free_throws_attempts_share: numeric percentage
                - two_point_made_share: numeric percentage
                - three_point_made_share: numeric percentage
                - free_throws_made_share: numeric percentage
                - two_point_rate: numeric percentage
                - three_point_rate: numeric percentage
                - points_from_two_percentage: numeric percentage
                - points_from_three_percentage: numeric percentage
                - points_from_free_throws_percentage: numeric percentage

                Use this table for questions about players stats, efficiency, and scoring profile.
                Always JOIN with players to retrieve player names.
                Join with players_teams and teams to retrieve the player's team.
                Percentages may be stored as numbers or strings; cast to numeric if needed.
            """
        ),
        SQLTableSchema(
            table_name="players_teams",
            context_str="""
                Table players_teams defines the relationship between players and teams.
                This is a mapping table used for JOIN operations.

                Column format:
                - player_code: text (FK → players.code)
                - team_code: text (3-letter uppercase team code, FK → teams.code)

                Use this table ONLY to connect players with teams.
                Typical JOIN path:
                players → players_teams → teams
            """
        ),
        SQLTableSchema(
            table_name="teams",
            context_str=f"""
                Table teams contains team information.
                Each row represents one team.
                Teams names: {teams}

                Column format:
                - code: text (3-letter uppercase team code, PRIMARY KEY)
                - name: text (full team name, uppercase)

                Use this table when questions involve teams or team names.
                Join with games for match results.
                Join with players_teams for team rosters.
            """
        ),
    ]
