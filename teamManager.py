import sqlite3
from database import db_name
import random
import pandas as pd

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

def create_random_team(player_id):
    delete_team(player_id)
    if player_id != 0: print("Creating random Team!")
    cursor.execute("SELECT * FROM pokemon")
    rows = len(cursor.fetchall())

    for i in range(6):
        rand = random.randint(1, rows)
        cursor.execute("SELECT hp FROM pokemon WHERE pokedex_number = ?", (rand,))
        hp = cursor.fetchone()[0]
        cursor.execute("INSERT OR REPLACE INTO team(player_id, pokemon_order, pokedex_number, health, remaining_light, remaining_special) VALUES(?,?,?,?,?,?)", (player_id, i+1, rand, hp, 8, 3))
    conn.commit()

def delete_all_teams():
    cursor.execute("DELETE FROM team")
    conn.commit()

def delete_team(player_id):
    cursor.execute("DELETE FROM team WHERE player_id = ?", (player_id,))
    conn.commit()

def heal_team(player_id):
    cursor.execute("""UPDATE team
        SET health = (SELECT hp FROM pokemon WHERE pokedex_number = team.pokedex_number)
        WHERE player_id = ?""", (player_id,))
    conn.commit()
    
def list_team(player_id):
    if team_size(player_id) == 0:
        print("You have no Team!")
        return

    cursor.execute("""SELECT team.pokemon_order, pokemon.name, team.health, pokemon.attack, pokemon.defense, pokemon.type1, pokemon.type2
        FROM team INNER JOIN pokemon 
        ON team.pokedex_number = pokemon.pokedex_number 
        WHERE team.player_id = ?
        ORDER BY team.pokemon_order""", (player_id,))
    team = cursor.fetchall()

    
    print("Your team is currently comprised of: ")
    for row in team:
        if row[6] == None:
            print(f" {row[0]}. {row[1]: <10} hp: {row[2]: <4} attack: {row[3]: <4} defense: {row[4]: <4} type: {row[5]}")
        else:
            print(f" {row[0]}. {row[1]: <10} hp: {row[2]: <4} attack: {row[3]: <4} defense: {row[4]: <4} type: {row[5]} & {row[6]}")

def team_size(player_id):
    cursor.execute("SELECT * FROM team WHERE player_id = ?", (player_id,))
    team_size = len(cursor.fetchall())
    return team_size