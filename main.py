import os
import database
import teamManager as team

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame


def game_engine():
    while True:
        print(" 1. Choose your Team \n 2. Fight!\n 3. Exit!")
        des = input("Please use the Keys 1-3 + ENTER to choose what to do next! ")

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
    team.deleteTeam()
    print(" 1. Choose your own Team\n 2. Create a random Team")
    des = input("Please use the Keys 1-2 + ENTER to choose what to do next! ")
    if des == "1":
        print("Not implemented!")
    elif des == "2":
        team.createRandomTeam()

    team.listTeam()
    print("\n") 

def fight_sim():
    if team.teamSize() == 0:
        print("You must first create your team!")
    else:
        print("Not implemented!")



if __name__ == "__main__":
    database.initialise()
    print("Welcome to Pykemon!\n")

    game_engine()