import os
from db import create_tables
from transform import transform_data
import sqlite3

db_file = "../euroleague.db"  
conn = sqlite3.connect(db_file)


def write_to_sqlite(df, table_name):
    df.to_sql(table_name, conn, if_exists="replace", index=False)

def load_data(season):
    if not os.path.exists(db_file):
        create_tables()
    
    players, players_average_stats, teams, games, players_teams = transform_data(season)
    write_to_sqlite(players, "players")
    write_to_sqlite(teams, "teams")
    write_to_sqlite(games, "games")
    write_to_sqlite(players_average_stats, "players_average_stats")
    write_to_sqlite(players_teams, "players_teams")
