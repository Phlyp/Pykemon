import os
import system_calls as sys

from zmq import PLAIN
import database
import teamManager as team
import playerManager as player
import fightManager as fight

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

clear = lambda: os.system('cls')

def game_engine():
    while True:
        sys.clear()
        print(f"Hello {player.current_player.name}, what would you like to do?")
        print(" 1. Player Settings \n 2. Edit your team \n 3. Fight!\n 4. Exit!")
        des = input("Please use the Keys 1-4 + ENTER to choose what to do next! ")
        sys.clear()

        if des == "1":
            player_settings()
        elif des == "2":
            team_settings()
        elif des == "3":
            if team.team_size(player.current_player.id) == 0:
                print("You must first create your team!")
                sys.wait_for_keypress()
            else:
                fight.fight_engine()
        elif des == "4":
            print("Goodbye!")
            quit()
        else:
            print("invalid input given!")

def player_settings():
    while True:
        sys.clear()
        print(f"Hello {player.current_player.name}, what would you like to do?")
        print(" 1. Get player info \n 2. Create new player \n 3. Change current player \n 4. Delete all players \n 5. Back to main menu")
        des = input("Please use the Keys 1-5 + ENTER to choose what to do next! ")
        sys.clear()

        if des == "1":
            player.get_player_info()
            sys.wait_for_keypress()
        elif des == "2":
            player.create_new_player()
        elif des == "3":
            player.change_current_player()
        elif des == "4":
            player.delete_all_players()
            team.delete_all_teams()
        elif des == "5":
            print("")
            break
        else:
            print("invalid input given!")
    
def team_settings():
    while True:
        sys.clear()
        print(f"Hello {player.current_player.name}, what would you like to do?")
        print(" 1. Choose your own Team\n 2. Create a random Team \n 3. List Team \n 4. Heal team \n 5. Back to main menu")
        des = input("Please use the Keys 1-4 + ENTER to choose what to do next! ")
        sys.clear()

        if des == "1":
            print("Not implemented!")
            sys.wait_for_keypress()
        elif des == "2":
            team.create_random_team(player.current_player.id)
            team.list_team(player.current_player.id)
            sys.wait_for_keypress()
        elif des == "3":
            team.list_team(player.current_player.id)
            sys.wait_for_keypress()
        elif des == "4":
            team.heal_team(player.current_player.id)
            print("Healing team!")
            sys.wait_for_keypress()
        elif des == "5":
            print("")
            break
        else:
            print("invalid input given!")
        print("\n") 



if __name__ == "__main__":
    is_new_session = not database.table_exists("team")
    database.initialise()
    sys.clear()
    print("Welcome to Pykemon!\n")
    sys.wait_for_keypress()

    if is_new_session:
        sys.clear()
        print("As you are starting Pykemon for the first time, you must first create a player!")
        player.create_new_player()
    else:
        sys.clear()
        print("Select your Player:")
        player.change_current_player()

    game_engine()