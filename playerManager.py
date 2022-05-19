import database
import sqlite3

conn = sqlite3.connect(database.db_name)
cursor = conn.cursor()

class currentPlayer:
    id = 1
    name = "player"

def create_new_player():
    name = input("Please enter a name for your new player: ")

    cursor.execute("SELECT COUNT(*) FROM players WHERE name = ?", (name,))
    while cursor.fetchone()[0] > 0:
        name = input("Name already exists! Please enter a new name: ")
        cursor.execute("SELECT COUNT(*) FROM players WHERE name = ?", (name,))

    cursor.execute("INSERT INTO players(name, is_bot, level, high_score) VALUES(?,0,0,0)", (name,))
    conn.commit()
    player_id = cursor.execute("SELECT player_id FROM players WHERE name = ?", (name,)).fetchone()[0]
    currentPlayer.id = player_id
    currentPlayer.name = cursor.execute("SELECT name FROM players WHERE player_id = ?", (player_id,)).fetchone()

def change_current_player():
    cursor.execute("SELECT COUNT(*) FROM players WHERE is_bot = 0")
    rows = cursor.fetchone()
    print("These are the current players:")
    cursor.execute("SELECT player_id,name,level,high_score FROM players WHERE is_bot = 0")
    players = cursor.fetchall()
    for row in players:
        print(" %i. Name: %s, Level: %i, High Score: %i" %(row[0], row[1], row[2], row[3]))

    id = int(input("Please use the Keys 1-%i + ENTER to select your player: " %rows))
    cursor.execute("SELECT COUNT(*) FROM players WHERE player_id = ?", (id,))
    while cursor.fetchone()[0] == 0:
        print("Error: Player does not exist!")
        id = int(input("Please use the Keys 1-%i + ENTER to select your player: " %rows))
        cursor.execute("SELECT COUNT(*) FROM players WHERE player_id = ?", (id,))

    currentPlayer.id = id
    currentPlayer.name = cursor.execute("SELECT name FROM players WHERE player_id = ?", (id,)).fetchone()
    print("Hello %s!"%currentPlayer.name)

def get_player_info():
    info = cursor.execute("SELECT * FROM players WHERE player_id = ?", (currentPlayer.id,)).fetchone()
    print("Id: %i, Name: %s, Level: %i, High Score: %i" %(info[0], info[1], info[3], info[4]))

def delete_all_players():
    cursor.execute("DELETE FROM players WHERE is_bot = 0")
    conn.commit()
    create_new_player()