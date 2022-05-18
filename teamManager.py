import sqlite3
import database
import random
import pandas as pd

sqlite_con = sqlite3.connect(database.db_name)
sqlite_cursor = sqlite_con.cursor()

def createRandomTeam():
    print("Creating random Team!")
    sqlite_cursor.execute("SELECT * FROM pokemon")
    rows = len(sqlite_cursor.fetchall())

    for i in range(6):
        rand = random.randint(0, rows)
        sqlite_cursor.execute("SELECT hp FROM pokemon WHERE pokedex_number = %i" %rand)
        hp = sqlite_cursor.fetchone()[0]
        sqlite_cursor.execute("INSERT INTO team(player_id, pokemon_order, pokedex_number, health, remaining_light, remaining_special) VALUES(?,?,?,?,?,?)", (1, i+1, rand, hp, 8, 3))
    sqlite_con.commit()

def deleteTeam():
    sqlite_cursor.execute("DELETE FROM team")
    sqlite_con.commit()
    
def listTeam():
    team = pd.read_sql('SELECT * FROM team', sqlite_con)
    pokemon_pd = pd.read_sql('SELECT * FROM pokemon', sqlite_con)
    
    print("Your team is currently comprised of: ", end="")
    for id in team['pokedex_number']:
        print(pokemon_pd['name'][id], end=", ")

def teamSize():
    sqlite_cursor.execute("SELECT * FROM team WHERE player_id = 1")
    team_size = len(sqlite_cursor.fetchall())
    return team_size