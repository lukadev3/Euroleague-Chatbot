def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        code TEXT PRIMARY KEY,
        name TEXT,
        age INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        code TEXT PRIMARY KEY,
        name TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        round INTEGER,
        group_name TEXT,
        date TEXT,
        time TEXT,
        home_team_code TEXT,
        home_team_score INTEGER,
        away_team_code TEXT,
        away_team_score INTEGER,
        FOREIGN KEY(home_team_code) REFERENCES teams(code),
        FOREIGN KEY(away_team_code) REFERENCES teams(code)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players_average_stats (
        player_code TEXT PRIMARY KEY,
        games_played INTEGER,
        minutes_played REAL,
        off_reb_pct REAL,
        def_reb_pct REAL,
        reb_pct REAL,
        assists_ratio REAL,
        turnovers_ratio REAL,
        two_pt_attempts_ratio REAL,
        three_pt_attempts_ratio REAL,
        ft_rate REAL,
        FOREIGN KEY(player_code) REFERENCES players(code)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players_teams (
        player_code TEXT,
        team_code TEXT,
        PRIMARY KEY(player_code, team_code),
        FOREIGN KEY(player_code) REFERENCES players(code),
        FOREIGN KEY(team_code) REFERENCES teams(code)
    )
    """)

    conn.commit()

