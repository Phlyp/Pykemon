from calendar import c
import string
from sys import meta_path
import sqlalchemy as db
import sqlite3 as sdb
import pandas as pd
import random
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

db_name = "Data\pokemon.sqlite"
engine = db.create_engine('sqlite:///' + db_name)
con = engine.connect()
meta_data = db.MetaData(bind=engine)
db.MetaData.reflect(meta_data)

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
    base.metadata.create_all(engine)

    pokemon_data = pd.read_csv("Data/pokemon.csv", encoding='utf8')
    pokemon_data.to_sql("pokemon", engine, index=False, if_exists="replace")
    


    
def createRandomTeam():
    # meta_data = db.MetaData(bind=engine)
    # db.MetaData.reflect(meta_data)
    pokemon_table = meta_data.tables['pokemon']
    team_table = meta_data.tables['team']
    
    rows = db.select([db.func.count()]).select_from(pokemon_table).scalar()
    for i in range(5):
        rand = random.randint(0, rows)
        insert_stmt = db.insert(team_table).values(pokemon_id=i, pokedex_number=rand)
        # print(insert_stmt)
        con.execute(insert_stmt)

def deleteTeam():
    team_table = meta_data.tables['team']
    query = db.select([team_table])
    con.execute(db.delete(team_table))
    
def listTeam():
    team = pd.read_sql_table('team', engine)
    pokemon_pd = pd.read_sql_table('pokemon', engine)
    
    print("Your team is currently comprised of: ", end="")
    for id in team['pokedex_number']:
        print(pokemon_pd['name'][id], end=", ")
