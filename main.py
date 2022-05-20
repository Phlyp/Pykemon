import os

from zmq import PLAIN
import database
import teamManager as team
import playerManager as player

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
pygame.init()

def wait_for_keypress():
    input("press ENTER to continue")

clear = lambda: os.system('cls')

def game_engine():
    while True:
        clear()
        print(" 1. Player Settings \n 2. Edit your team \n 3. Fight!\n 4. Exit!")
        des = input("Please use the Keys 1-4 + ENTER to choose what to do next! ")
        clear()

        if des == "1":
            player_settings()
        elif des == "2":
            team_settings()
        elif des == "3":
            fight_sim()
            wait_for_keypress()
        elif des == "4":
            print("Goodbye!")
            quit()
        else:
            print("invalid input given!")

def player_settings():
    while True:
        clear()
        print("Hello %s, what would you like to do?"%player.currentPlayer.name)
        print(" 1. Get player info \n 2. Create new player \n 3. Change current player \n 4. Delete all players \n 5. Back to main menu")
        des = input("Please use the Keys 1-5 + ENTER to choose what to do next! ")
        clear()

        if des == "1":
            player.get_player_info()
            wait_for_keypress()
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
        clear()
        print(" 1. Choose your own Team\n 2. Create a random Team \n 3. List Team \n 4. Back to main menu")
        des = input("Please use the Keys 1-2 + ENTER to choose what to do next! ")
        clear()

        if des == "1":
            print("Not implemented!")
            wait_for_keypress()
        elif des == "2":
            team.create_random_team(player.currentPlayer.id)
            team.list_team(player.currentPlayer.id)
            wait_for_keypress()
        elif des == "3":
            team.list_team(player.currentPlayer.id)
            wait_for_keypress()
        elif des == "4":
            print("")
            break
        else:
            print("invalid input given!")
        print("\n") 

def fight_sim():
    if team.team_size(player.currentPlayer.id) == 0:
        print("You must first create your team!")
    else:
        print("Not implemented!")



if __name__ == "__main__":
    is_new_session = not database.table_exists("team")
    database.initialise()
    clear()
    print("Welcome to Pykemon!\n")
    wait_for_keypress()

    if is_new_session:
        clear()
        print("As you are starting Pykemon for the first time, you must first create a player!")
        wait_for_keypress()
        player.create_new_player()

    game_engine()