import sqlite3
import database
import random
import pandas as pd

conn = sqlite3.connect(database.db_name)
cursor = conn.cursor()

def create_random_team():
    print("Creating random Team!")
    cursor.execute("SELECT * FROM pokemon")
    rows = len(cursor.fetchall())

    for i in range(6):
        rand = random.randint(0, rows)
        cursor.execute("SELECT hp FROM pokemon WHERE pokedex_number = ?", (rand,))
        hp = cursor.fetchone()[0]
        cursor.execute("INSERT INTO team(player_id, pokemon_order, pokedex_number, health, remaining_light, remaining_special) VALUES(?,?,?,?,?,?)", (1, i+1, rand, hp, 8, 3))
    conn.commit()

def delete_team():
    cursor.execute("DELETE FROM team")
    conn.commit()
    
def list_team():

    cursor.execute("SELECT team.pokemon_order, pokemon.name FROM pokemon INNER JOIN team ON pokemon.pokedex_number = team.pokedex_number ORDER BY team.pokemon_order")
    team = cursor.fetchall()
    pokemon_pd = pd.read_sql('SELECT * FROM pokemon', conn)
    
    print("Your team is currently comprised of: ",)
    for row in team:
        print(" %i. %s" %(row[0], row[1]))

def team_size():
    cursor.execute("SELECT * FROM team WHERE player_id = 1")
    team_size = len(cursor.fetchall())
    return team_size