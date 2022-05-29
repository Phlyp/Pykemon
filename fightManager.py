from tokenize import Special
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
    pokedex_number = 0

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

    decision = sys.get_number("Please use the Keys 1-6 + ENTER to choose which pokemon to send into battle! ")
    while decision < 1 or decision > 6:
        print("Invalid input given!")
        decision = int(input("Please use the Keys 1-6 + ENTER to choose which pokemon to send into battle! "))
    player_pokemon.team_id = cursor.execute("SELECT team_id FROM team WHERE player_id = ? AND pokemon_order = ?", (current_player.id, decision)).fetchone()[0]
    hp = cursor.execute("SELECT health FROM team WHERE team_id = ?", (player_pokemon.team_id,)).fetchone()[0]
    if hp < 1:
        sys.clear()
        print("You can't choose a pokemon who has already fainted!")
        choose_pokemon()
        return
    cursor.execute("""SELECT pokemon.name FROM team
        INNER JOIN pokemon ON team.pokedex_number = pokemon.pokedex_number 
        WHERE team.team_id = ?""", (player_pokemon.team_id,))
    player_pokemon.name = cursor.fetchone()[0]

    cursor.execute("""SELECT pokemon.pokedex_number FROM team
        INNER JOIN pokemon ON team.pokedex_number = pokemon.pokedex_number 
        WHERE team.team_id = ?""", (player_pokemon.team_id,))
    player_pokemon.pokedex_number = cursor.fetchone()[0]

def choose_bot_pokemon():
    alive_pokemon = cursor.execute("SELECT team_id FROM team WHERE player_id = 0 AND health > 0").fetchall()
    bot_pokemon.team_id = random.choice(alive_pokemon)[0]
    cursor.execute("""SELECT pokemon.name FROM 
        team INNER JOIN pokemon ON team.pokedex_number = pokemon.pokedex_number 
        WHERE team.team_id = ?""", (bot_pokemon.team_id,))
    bot_pokemon.name = cursor.fetchone()[0]
    cursor.execute("""SELECT pokemon.pokedex_number FROM team
        INNER JOIN pokemon ON team.pokedex_number = pokemon.pokedex_number 
        WHERE team.team_id = ?""", (bot_pokemon.team_id,))
    bot_pokemon.pokedex_number = cursor.fetchone()[0]

def choose_attack():
    pokedex_number = player_pokemon.pokedex_number
    (total_light, total_special) = (8,6)
    basic_attack = "Tackle"

    type0 = "basic"
    (type1, type2) = cursor.execute("SELECT type1, type2 FROM pokemon WHERE pokedex_number = ?", (player_pokemon.pokedex_number,)).fetchone()

    remaining_light = cursor.execute("SELECT remaining_light FROM team WHERE team_id = ?", (player_pokemon.team_id,)).fetchone()[0]
    remaining_special = cursor.execute("SELECT remaining_special FROM team WHERE team_id = ?", (player_pokemon.team_id,)).fetchone()[0]

    sp_attack1 = cursor.execute("SELECT Attack FROM attacks WHERE Type = ?", (type1,)).fetchone()[0]
    if type2 is not None:
        sp_attack2 = cursor.execute("SELECT Attack FROM attacks WHERE Type = ?", (type2,)).fetchone()[0]

        sys.clear()
        print("It's your turn!")
        print(f"You: {player_pokemon.name: <10} hp: {player_pokemon.get_hp(): <10} Enemy: {bot_pokemon.name: <10} hp: {bot_pokemon.get_hp()}")
        print(f" 1. {basic_attack: <13} type: {type0: <10} remaining: {remaining_light}/{total_light}")
        print(f" 2. {sp_attack1: <13} type: {type1: <10} remaining: {remaining_special}/{total_special}")
        print(f" 3. {sp_attack2: <13} type: {type2: <10} remaining: {remaining_special}/{total_special}")
        print(" 4. Go back")

        while True:
            decision = input("Please use the Keys 1-4 + ENTER to choose your attack! ")
            if decision == "1":
                if remaining_light < 0:
                    print("No basic attacks remaining!")
                    continue
                attack(basic_attack, type0, player_pokemon, bot_pokemon)
                break
            elif decision == "2":
                if remaining_special < 0:
                    print("No special attacks remaining!")
                    continue
                attack(sp_attack1, type1, player_pokemon, bot_pokemon)
                break
            elif decision == "3":
                if remaining_special < 0:
                    print("No special attacks remaining!")
                    continue
                attack(sp_attack2, type2, player_pokemon, bot_pokemon)
                break
            elif decision == "4":
                return 1
            else:
                print("Invalid Input given!")
    else:
        sys.clear()
        print("It's your turn!")
        print(f"You: {player_pokemon.name: <10} hp: {player_pokemon.get_hp(): <10} Enemy: {bot_pokemon.name: <10} hp: {bot_pokemon.get_hp()}")
        print(f" 1. {basic_attack: <13} type: {type0: <10} remaining: {remaining_light}/{total_light}")
        print(f" 2. {sp_attack1: <13} type: {type1: <10} remaining: {remaining_special}/{total_special}")
        print(" 3. Go back")
        decision = ""

        while True:
            decision = input("Please use the Keys 1-3 + ENTER to choose your attack! ")
            if decision == "1":
                if remaining_light < 0:
                    print("No basic attacks remaining!")
                    continue
                attack(basic_attack, type0, player_pokemon, bot_pokemon)
                break
            elif decision == "2":
                if remaining_special < 0:
                    print("No special attacks remaining!")
                    continue
                attack(sp_attack1, type1, player_pokemon, bot_pokemon)
                break
            elif decision == "3":
                return 1
            else:
                print("Invalid Input given!")
    return 0
        
def attack(attack_name, type, attacking_pokemon=pokemon, defending_pokemon=pokemon):
    sys.clear()
    print(f"{attacking_pokemon.name} used {attack_name}!")
    sys.wait_for_keypress()

    # decrement remaining attack counter
    if type == "basic":
        remaining_light = cursor.execute("SELECT remaining_light FROM team WHERE team_id = ?", (attacking_pokemon.team_id,)).fetchone()[0]
        cursor.execute("UPDATE team SET remaining_light = ? WHERE team_id = ?", (remaining_light-1, attacking_pokemon.team_id))
    else:
        remaining_special = cursor.execute("SELECT remaining_special FROM team WHERE team_id = ?", (attacking_pokemon.team_id,)).fetchone()[0]
        cursor.execute("UPDATE team SET remaining_special = ? WHERE team_id = ?", (remaining_special-1, attacking_pokemon.team_id))
    conn.commit()

    # calculate damage
    # base damage
    attack = 1
    defense = 1
    if type == "basic":
        attack = cursor.execute("SELECT attack FROM pokemon WHERE pokedex_number = ?", (attacking_pokemon.pokedex_number,)).fetchone()[0]
        defense = cursor.execute("SELECT defense FROM pokemon WHERE pokedex_number = ?", (defending_pokemon.pokedex_number,)).fetchone()[0]
    else:
        attack = cursor.execute("SELECT sp_attack FROM pokemon WHERE pokedex_number = ?", (attacking_pokemon.pokedex_number,)).fetchone()[0]
        defense = cursor.execute("SELECT sp_defense FROM pokemon WHERE pokedex_number = ?", (defending_pokemon.pokedex_number,)).fetchone()[0]
    
    level_multiplier = 110 / 5 + 2
    power = 60
    base_damage = level_multiplier * power * (attack/defense) / 50 + 2

    # type damage
    type_damage = 1
    if type != "basic":
        (defending_type1, defending_type2) = cursor.execute("SELECT type1, type2 FROM pokemon WHERE pokedex_number = ?", (defending_pokemon.team_id,)).fetchone()
        type1_column = "against_" + defending_type1
        against_type1 = cursor.execute("SELECT %s FROM attacks WHERE type = ?" %(type1_column), (type,)).fetchone()[0]
        against_type2 = 1
        if defending_type2 is not None:
            type2_column = "against_" + defending_type2
            against_type2 = cursor.execute("SELECT %s FROM attacks WHERE type = ?" %(type2_column), (type,)).fetchone()[0]
        type_damage = max(against_type1, against_type2, against_type1*against_type2)
    
    # critical multiplier
    critical_mult = 1
    if random.random() < 1/10:
        print("A critical hit!")
        critical_mult = 2
    
    # random multiplier
    random_mult = random.randint(85,100) / 100

    # final damage
    damage = int(base_damage * type_damage * critical_mult * random_mult)
    print(f"{attacking_pokemon.name} did {damage} damage!")
    sys.wait_for_keypress()   

    defending_pokemon.set_hp(defending_pokemon.get_hp() - damage)

    # check if pokemon feinted
    if defending_pokemon.get_hp() <= 0:
        print(f"{defending_pokemon.name} fainted!")
        sys.wait_for_keypress()
        defending_player_id = cursor.execute("SELECT player_id FROM team WHERE team_id = ?", (defending_pokemon.team_id,)).fetchone()[0]

        # Check Win
        if check_win(defending_player_id):
            return

        if defending_player_id != 0:
            sys.clear()
            print("Your Pokemon fainted! You must choose a new Pokemon!")
            choose_pokemon()
        else:
            choose_bot_pokemon() 

def bot_attack():
    pokedex_number = cursor.execute("SELECT pokedex_number FROM team WHERE team_id = ?", (bot_pokemon.team_id,)).fetchone()[0]
    basic_damage = cursor.execute("SELECT attack FROM pokemon WHERE pokedex_number = ?", (pokedex_number,)).fetchone()[0]
    basic_attack = "Tackle"
    type = "basic"
    attack(basic_attack, type, bot_pokemon, player_pokemon)

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
    teamManager.reset_team(current_player.id)
    choose_pokemon()

    global game_over
    game_over = False 

    player_pokemon_speed = cursor.execute("SELECT speed FROM pokemon WHERE pokedex_number = ?", (player_pokemon.pokedex_number,)).fetchone()[0]
    bot_pokemon_speed = cursor.execute("SELECT speed FROM pokemon WHERE pokedex_number = ?", (bot_pokemon.pokedex_number,)).fetchone()[0]
    
    if bot_pokemon_speed > player_pokemon_speed:
        sys.clear()
        print("It's the Enemy's turn!")
        print(f"You: {player_pokemon.name: <10} hp: {player_pokemon.get_hp(): <10} Enemy: {bot_pokemon.name: <10} hp: {bot_pokemon.get_hp()}")
        sys.wait_for_keypress()
        bot_attack()

    while True:
        while True:
            sys.clear()
            print("It's your turn!")
            print(f"You: {player_pokemon.name: <10} hp: {player_pokemon.get_hp(): <10} Enemy: {bot_pokemon.name: <10} hp: {bot_pokemon.get_hp()}")
            print(" 1. Attack \n 2. Choose a different Pokemon \n 3. Run")
            decision = input("Please use the Keys 1-3 + ENTER to choose what to do next! ")
            sys.clear()

            if decision == "1":
                if choose_attack() == 0:
                    break
            elif decision == "2":
                choose_pokemon()
                break
            elif decision == "3":
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

    