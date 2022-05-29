import os
import string
from sys import meta_path
import sqlalchemy as db
import sqlite3 as sdb
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

db_name = os.path.join("Data","db.sqlite")
engine = db.create_engine('sqlite:///' + db_name)
conn = engine.connect()
meta_data = db.MetaData(bind=engine)
db.MetaData.reflect(meta_data)

sqlite_conn = sdb.connect(db_name)
sqlite_cursor = sqlite_conn.cursor()

class pokemon(base):
    __tablename__ = "pokemon"
    pokemon_id = db.Column(db.Integer, primary_key = True)

class bots(base):
    __tablename__ = 'bots'
    bot_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    teamsize = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    def __init__(self, bot_id: int, name: string, teamsize: int, difficutly: int) -> None:
        self.bot_id = bot_id
        self.name = name
        self.teamsize = teamsize
        self. difficulty = difficutly

class computer(base):
    __tablename__ = 'computer'
    computer_id = db.Column(db.Integer, primary_key = True)

    def __init__(self, computer_id: int) -> None:
        self.computer_id = computer_id

class player(base):
    __tablename__ = 'player'
    player_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    level = db.Column(db.Integer)
    computer_id = db.Column(db.Integer, db.ForeignKey('computer.computer_id'))

    def __init__(self, player_id: int, name: string, pokemon_computer_id: int) -> None:
        self.player_id = player_id
        self.name = name
        self.pokemon_computer_id = pokemon_computer_id

class team(base):
    __tablename__ = 'team'
    pokemon_id = db.Column(db.Integer, primary_key = True)
    pokedex_number = db.Column(db.Integer)

    def __init__(self, pokemon_id: int, pokedex_number: int) -> None:
        self.id = pokemon_id
        self.pokedex_number = pokedex_number

def initialise():
    # base.metadata.create_all(engine)

    pokemon_data = pd.read_csv("Data/pokemon.csv", encoding='utf8')
    pokemon_data.to_sql("pokemon", sqlite_conn, index=False, if_exists="replace")

    pokemon_attacks = pd.read_csv("Data/attacks.csv")
    pokemon_attacks.to_sql("attacks", sqlite_conn, index=False, if_exists="replace")

    sqlite_cursor.execute("""CREATE TABLE IF NOT EXISTS players(
        player_id INTEGER PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE,
        is_bot INTEGER,
        xp INTEGER,
        level INTEGER,
        dollars INTEGER,
        high_score INTEGER,
        CHECK(is_bot IN (0,1)))""")

    sqlite_cursor.execute("""CREATE TABLE IF NOT EXISTS team(
        team_id INTEGER PRIMARY KEY,
        player_id INTEGER,
        pokemon_order INTEGER,
        pokedex_number INTEGER,
        health INTEGER,
        remaining_light INTEGER,
        remaining_special INTEGER,
        FOREIGN KEY (player_id) REFERENCES players(player_id))""")
    
    sqlite_cursor.execute("INSERT OR REPLACE INTO players VALUES(0, 'bot', 1, 0, 0, 0, 0)")
    sqlite_conn.commit()
    

def table_exists(name):
    sqlite_cursor.execute(''' SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name=? ''', (name,))
    if sqlite_cursor.fetchone()[0]==1:
        return True 
    else:
        return False


