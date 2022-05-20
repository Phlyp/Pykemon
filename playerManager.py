import database
import sqlite3

conn = sqlite3.connect(database.db_name)
cursor = conn.cursor()
start_dollars = 1000

class currentPlayer:
    id = 1
    name = "player"

def create_new_player():
    name = input("Please enter a name for your new player: ")

    cursor.execute("SELECT COUNT(*) FROM players WHERE name = ?", (name,))
    while cursor.fetchone()[0] > 0:
        name = input("Name already exists! Please enter a new name: ")
        cursor.execute("SELECT COUNT(*) FROM players WHERE name = ?", (name,))

    cursor.execute("INSERT INTO players(name, is_bot, xp, level, dollars, high_score) VALUES(?,0,0,0,?,0)", (name, start_dollars))
    conn.commit()
    player_id = cursor.execute("SELECT player_id FROM players WHERE name = ?", (name,)).fetchone()[0]
    currentPlayer.id = player_id
    currentPlayer.name = cursor.execute("SELECT name FROM players WHERE player_id = ?", (player_id,)).fetchone()

def change_current_player():
    cursor.execute("SELECT COUNT(*) FROM players WHERE is_bot = 0")
    total_rows = cursor.fetchone()
    print("These are the current players:")
    cursor.execute("SELECT player_id,name,xp,level,dollars,high_score FROM players WHERE is_bot = 0")
    players = cursor.fetchall()
    for row in players:
        print(f" {row[0]}. Name: {row[1]}, Xp: {row[2]}, Level: {row[3]}, Dollars: {row[4]}, High Score: {row[5]}")

    id = int(input(f"Please use the Keys 1-{total_rows} + ENTER to select your player: " ))
    cursor.execute("SELECT COUNT(*) FROM players WHERE player_id = ?", (id,))
    while cursor.fetchone()[0] == 0:
        print("Error: Player does not exist!")
        id = int(input(f"Please use the Keys 1-{total_rows} + ENTER to select your player: "))
        cursor.execute("SELECT COUNT(*) FROM players WHERE player_id = ?", (id,))

    currentPlayer.id = id
    currentPlayer.name = cursor.execute("SELECT name FROM players WHERE player_id = ?", (id,)).fetchone()
    print("Hello %s!"%currentPlayer.name)

def get_player_info():
    info = cursor.execute("SELECT player_id,name,xp,level,dollars,high_score FROM players WHERE player_id = ?", (currentPlayer.id,)).fetchone()
    print(f" {info[0]}. Name: {info[1]}, Xp: {info[2]}, Level: {info[3]}, Dollars: {info[4]}, High Score: {info[5]}")

def delete_all_players():
    cursor.execute("DELETE FROM players WHERE is_bot = 0")
    conn.commit()
    create_new_player()