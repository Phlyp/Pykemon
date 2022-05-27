import os

def clear():
    os.system('cls')

def wait_for_keypress():
    input("press ENTER to continue")

def get_number(question):
    while True:
        try:
            user_input = input(question)
            user_input = int(user_input)
            return user_input
        except:
            print("Invaldid Input!")
