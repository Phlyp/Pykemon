import system_calls as sys

import sqlite3
import random
from database import db_name, team
from playerManager import current_player
import teamManager

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

class pokemon:
    team_id = 0
    name = ""

    def __init__(self):
        pass
    
    def get_hp(self):
        return cursor.execute("SELECT health FROM team WHERE team_id = ?", (self.team_id,)).fetchone()[0]
    
    def set_hp(self, new_hp):
        cursor.execute("UPDATE team SET health = ? WHERE team_id = ?", (new_hp, self.team_id))
        conn.commit()

player_pokemon = pokemon()
bot_pokemon = pokemon()

def choose_pokemon():
    teamManager.list_team(current_player.id)

    des = int(input("Please use the Keys 1-6 + ENTER to choose which pokemon to send into battle! "))
    while des < 1 or des > 6:
        print("Invalid input given!")
        des = input("Please use the Keys 1-6 + ENTER to choose which pokemon to send into battle! ")
    player_pokemon.team_id = cursor.execute("SELECT team_id FROM team WHERE player_id = ? AND pokemon_order = ?", (current_player.id, des)).fetchone()[0]
    hp = cursor.execute("SELECT health FROM team WHERE team_id = ?", (player_pokemon.team_id,)).fetchone()[0]
    if hp < 1:
        sys.clear()
        print("You can't choose a pokemon who has already feinted!")
        choose_pokemon()
        return
    cursor.execute("""SELECT pokemon.name FROM team
        INNER JOIN pokemon ON team.pokedex_number = pokemon.pokedex_number 
        WHERE team.team_id = ?""", (player_pokemon.team_id,))
    player_pokemon.name = cursor.fetchone()[0]

def choose_bot_pokemon():
    alive_pokemon = cursor.execute("SELECT team_id FROM team WHERE player_id = 0 AND health > 0").fetchall()
    bot_pokemon.team_id = random.choice(alive_pokemon)[0]
    cursor.execute("""SELECT pokemon.name FROM 
        team INNER JOIN pokemon ON team.pokedex_number = pokemon.pokedex_number 
        WHERE team.team_id = ?""", (bot_pokemon.team_id,))
    bot_pokemon.name = cursor.fetchone()[0]

def choose_attack():
    pokedex_number = cursor.execute("SELECT pokedex_number FROM team WHERE team_id = ?", (player_pokemon.team_id,)).fetchone()[0]
    basic_attack = "Tackle"

    type0 = "basic"
    (type1, type2) = cursor.execute("SELECT type1, type2 FROM pokemon WHERE pokedex_number = ?", (pokedex_number,)).fetchone()

    basic_damage = cursor.execute("SELECT attack FROM pokemon WHERE pokedex_number = ?", (pokedex_number,)).fetchone()[0]
    special_damage = cursor.execute("SELECT sp_attack FROM pokemon WHERE pokedex_number = ?", (pokedex_number,)).fetchone()[0]

    sp_attack1 = cursor.execute("SELECT Attack FROM attacks WHERE Type = ?", (type1,)).fetchone()[0]
    if type2 is not None:
        sp_attack2 = cursor.execute("SELECT Attack FROM attacks WHERE Type = ?", (type2,)).fetchone()[0]

        sys.clear()
        print("It's your turn!")
        print(f"You: {player_pokemon.name: <10} hp: {player_pokemon.get_hp(): <10} Enemy: {bot_pokemon.name: <10} hp: {bot_pokemon.get_hp()}")
        print(f" 1. {basic_attack: <13} type: {type0: <10} damage: {basic_damage}")
        print(f" 2. {sp_attack1: <13} type: {type1: <10} damage: {special_damage}")
        print(f" 3. {sp_attack2: <13} type: {type2: <10} damage: {special_damage}")
        print(" 4. Go back")
        des = input("Please use the Keys 1-4 + ENTER to choose your attack! ")

        if des == "1":
            attack(basic_attack, basic_damage, player_pokemon, bot_pokemon)
        elif des == "2":
            attack(sp_attack1, special_damage, player_pokemon, bot_pokemon)
        elif des == "3":
            attack(sp_attack2, special_damage, player_pokemon, bot_pokemon)
        elif des == "4":
            return
        else:
            print("Invalid Input given!")
    else:
        sys.clear()
        print("It's your turn!")
        print(f"You: {player_pokemon.name: <10} hp: {player_pokemon.get_hp(): <10} Enemy: {bot_pokemon.name: <10} hp: {bot_pokemon.get_hp()}")
        print(f" 1. {basic_attack: <13} type: {type0: <10} damage: {basic_damage}")
        print(f" 2. {sp_attack1: <13} type: {type1: <10} damage: {special_damage}")
        print(" 3. Go back")
        des = input("Please use the Keys 1-3 + ENTER to choose your attack! ")
        
        if des == "1":
            attack(basic_attack, basic_damage, player_pokemon, bot_pokemon)
        elif des == "2":
            attack(sp_attack1, special_damage, player_pokemon, bot_pokemon)
        elif des == "3":
            return
        else:
            print("Invalid Input given!")
        
def attack(attack_name, damage, attacking_pokemon=pokemon, defending_pokemon=pokemon):
    sys.clear()
    print(f"{attacking_pokemon.name} used {attack_name}!")
    sys.wait_for_keypress()
    defending_pokemon.set_hp(defending_pokemon.get_hp() - damage)
    if defending_pokemon.get_hp() <= 0:
        print(f"{defending_pokemon.name} feinted!")
        sys.wait_for_keypress()
        defending_player_id = cursor.execute("SELECT player_id FROM team WHERE team_id = ?", (defending_pokemon.team_id,)).fetchone()[0]

        # Check Win
        if check_win(defending_player_id):
            return

        if defending_player_id != 0:
            sys.clear()
            print("Your Pokemon feinted! You must choose a new Pokemon!")
            choose_pokemon()
        else:
            choose_bot_pokemon() 

def bot_attack():
    pokedex_number = cursor.execute("SELECT pokedex_number FROM team WHERE team_id = ?", (bot_pokemon.team_id,)).fetchone()[0]
    basic_damage = cursor.execute("SELECT attack FROM pokemon WHERE pokedex_number = ?", (pokedex_number,)).fetchone()[0]
    basic_attack = "Tackle"
    attack(basic_attack, basic_damage, bot_pokemon, player_pokemon)

def check_win(player_id):
    end = True
    hp_values = cursor.execute("SELECT health FROM team WHERE player_id = ?", (player_id,)).fetchall()
    for hp in hp_values:
        if hp[0] > 0:
            end = False
    
    if end:
        is_bot = cursor.execute("SELECT is_bot FROM players WHERE player_id = ?", (player_id,)).fetchone()[0]
        if is_bot:
            sys.clear()
            print("You Won!")
            sys.wait_for_keypress()
        else:
            sys.clear()
            print("You Lost!")
            sys.wait_for_keypress()
        global game_over
        game_over = True
    return end


def fight_engine():
    #initial set up for fight
    teamManager.create_random_team(0)
    choose_bot_pokemon()
    teamManager.heal_team(current_player.id)
    choose_pokemon()

    global game_over
    game_over = False

    while True:
        sys.clear()
        print("It's your turn!")
        print(f"You: {player_pokemon.name: <10} hp: {player_pokemon.get_hp(): <10} Enemy: {bot_pokemon.name: <10} hp: {bot_pokemon.get_hp()}")
        print(" 1. Attack \n 2. Choose a different Pokemon \n 3. Run")
        des = input("Please use the Keys 1-3 + ENTER to choose what to do next! ")
        sys.clear()

        if des == "1":
            choose_attack()
        elif des == "2":
            choose_pokemon()
        elif des == "3":
            return
        else:
            print("Invalid input given!")
        
        if game_over:
            game_over = False
            return
        
        sys.clear()
        print("It's the Enemy's turn!")
        print(f"You: {player_pokemon.name: <10} hp: {player_pokemon.get_hp(): <10} Enemy: {bot_pokemon.name: <10} hp: {bot_pokemon.get_hp()}")
        sys.wait_for_keypress()
        bot_attack()

        if game_over:
            game_over = False
            return

    