import os
import database

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame


database.initialise("Data\pokemon.sqlite")

print("Welcome to Pykemon!\n")


def game_engine():
    while True:
        print(" 1. Choose your Team \n 2. Fight!\n 3. Exit!")
        des = input("Please use the Keys 1-3 to choose what to do next!")

        if des == "1":
            choose_team()
        elif des == "2":
            fight_sim()
        elif des == "3":
            print("Goodbye!")
            quit()
        else:
            print("invalid input given!")

    
def choose_team():
    print("Not implemented!")

def fight_sim():
    print("Not implemented!")



if __name__ == "__main__":
    game_engine()