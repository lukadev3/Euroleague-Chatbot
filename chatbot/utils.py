from llama_index.core.objects import SQLTableSchema

table_schema_objs = [

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
        context_str="""
            Table players contains basic player information.
            Each row represents one player.

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
            Table players_average_stats contains season-level average statistics per player.
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
            - two_point_attempts_ratio: numeric percentage
            - three_point_attempts_ratio: numeric percentage
            - free_throws_rate: numeric percentage

            Use this table for questions about players stats.
            Percentages may be stored as numbers or strings; cast to numeric if needed.
            Always JOIN with players to retrieve player names.
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
        context_str="""
            Table teams contains team information.
            Each row represents one team.
            List of teams names: ALBA BERLIN, AS MONACO, ZALGIRIS KAUNAS, BASKONIA VITORIA-GASTEIZ, FC BAYERN MUNICH, MACCABI PLAYTIKA TEL AVIV,
                                 FENERBAHCE BEKO ISTANBUL, PARIS BASKETBALL, VIRTUS SEGAFREDO BOLOGNA, PANATHINAIKOS AKTOR ATHENS, EA7 EMPORIO ARMANI MILAN,
                                 FC BARCELONA, PARTIZAN MOZZART BET BELGRADE, REAL MADRID, LDLC ASVEL VILLEURBANNE, OLYMPIACOS PIRAEUS, CRVENA ZVEZDA MERIDIANBET BELGRADE,
                                 ANADOLU EFES ISTANBUL

            Column format:
            - code: text (3-letter uppercase team code, PRIMARY KEY)
            - name: text (full team name, uppercase)

            Use this table when questions involve teams or team names.
            Join with games for match results.
            Join with players_teams for team rosters.
        """
    ),
]
