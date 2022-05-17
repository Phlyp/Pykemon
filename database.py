import string
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

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
    team_id = db.Column(db.Integer, primary_key = True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'))

    def __init__(self, team_id: int, player_id: int) -> None:
        self.team_id = team_id
        self.player_id = player_id

def initialise(name):
    db_name = name
    engine = db.create_engine('sqlite:///' + db_name)
    base.metadata.create_all(engine)