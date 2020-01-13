# This file will run a Maxi Yatzy game.
# Developed just for fun and Python/vim coding practice.

# Rules of Yatzy used for this game:-
#   * 6 dice, 3 rolls per round (unused rolls are saved and accumulate)
#   * player can choose order to assign scores (within current section)
#   * Bonus is achieved with score of >=75 in 'Upper' section


from random import randint           # needed for dice rolls
import pandas as pd     # the scoresheet will be displayed as DataFrame
import re               # regular expressions used to check some inputs
import time             # for pausing and better user readability


t = 0               # variable for pauses, set to 0 while I'm testing

class Player():
    def __init__(self, name, extra_rolls=0):
        self.n = name
        self.e = extra_rolls

# TODO finish looking at classes, whether you need more, finish
# scoresheet for 'upper'


def game_setup():       # function to set number of players & get names
    while True:
        global n        # ensures 'n' is accessible outside function
        n = input("Number of players (2-6):")
        try:
            n = int(n)
        except ValueError:
            print("Valid integer please. Try again.")
            continue
        if (2 <= n <= 6):
            break
        else:
            print("Invalid range. Try again (2-6).")
            break

    global players
    players = []
    for i in range(1, n+1):
        name_input = ""
        while True:
            name_input = input(f"Player {i} name: ")))
            if name_input != "" and name_input not in players:
                break
            else:
                print("Invalid or name already taken. Please try again.")
        players.append(Player(name = name_input))

game_setup()
        
upper_rows = ["One's", "Two's", "Three's",
                "Four's", "Five's", "Six's"]    # Add subtotal/bonus later

lower_rows = ["1 pair", "2 pairs", "3 pairs",
                "3 of a kind", "4 of a kind", "5 of a kind",
                "Small straight", "Big straight", "Full straight",
                "Full House (2+3)", "Villa (3+3)", "Tower (2+4)",
                "Chance", "MAXI YATZY"]         # Add subtotal/bonus later


scoresheet = pd.DataFrame(index = upper_rows, columns = [P.n for P in players])

# TODO add lower_rows

print()
print("LET YATZY BEGIN!!!")
print()
print(scoresheet)

def score(dice, section, player):
    if section == upper_rows:
        score_choice = {}
        for i in range(6):
            score_choice[section[i]] = sum([x for x in dice if x == (i+1)])
        print()
        print("Possible scores:-","\n")
        print(score_choice,"\n")
        time.sleep(t)
        print("Make a selection, type 1-6. E.g. for 'Four's', enter: 4")
        print("(Note you can only choose a free option)")
        while True:
            choice = int(input("Choose: ")) - 1     # -1 to match PC counting
            if pd.notna(scoresheet.loc[section[choice], player.n]):
                print("Score already fixed, please choose again.")
            else:
                return section[choice], score_choice[section[choice]]
        
    else:
        print("Lower section not coded yet...")





def update_score(player):
    dice = [*current_roll.values()]     # dictionary's values in a list 
    row, points = score(dice, section, player)
    scoresheet.loc[row, player.n] = points

def re_roll():
    dice_to_reroll = ""
    while not re.search(r"[A-F]{1,6}", dice_to_reroll):
        dice_to_reroll = input("""Enter a string of dice to RE-ROLL.
    (For example, to re-roll all except dice B & C enter: ADEF)
    Enter now: """).upper()
    
    for letter in dice_to_reroll:
       current_roll[letter] = randint(1,6)



def roll(player):
    global current_roll
    current_roll = dict(zip(["A","B","C","D","E","F"],
                            [randint(1,6) for _ in range(6)]))

    for i in range(3):
        print()
        print(f"Roll {(i+1)} =")
        time.sleep(t)
        print(current_roll,"\n")
        time.sleep(t)
        if i == 2:      # ensures options not offered in final roll
            break
        print(f"""Options:
            1) lock in current roll, save {(2-i)} extra rolls
            2) re-roll (from A-F state which dice to KEEP, if any)""")
        print("-"*72)
        
        choice = input("Type '1' to lock in or '2' to re-roll: ")
        while choice not in ["1", "2"]:
            print("Invalid entry, try again.","\n")
            choice = input("Type '1' to lock in or '2' to re-roll.")
        print()
        
        if choice == "2":
            re_roll()
        else:
            player.e += (2-i)
            break



    print("-"*72)
    print(f"You have {player.e} extra rolls remaining.")
    if choice != "1" and player.e > 0:
        while player.e > 0:
            print(f"Would you like to use one of your {player.e} remaining extra rolls?")
            choice = input("Yes/No: ").lower()
            if choice not in ["y", "yes", "n", "no"]:
                print("Please enter a valid answer.")
                continue
            else:
                if choice in ["y", "yes"]:
                    re_roll()
                    print(f"Extra Roll =")
                    time.sleep(t)
                    print(current_roll,"\n")
                    time.sleep(t)
                    player.e -= 1
                else:
                    break
    update_score(player)
    print()
    print(scoresheet)
    print()
    time.sleep(t)


def play_Yatzy():
    global section
    section = upper_rows      # for separating the game sections
    for i in range(6):
        for j in range(n):
            print()
            print(f"Round {i+1} - {players[j].n}")
            print("="*72)
            roll(players[j])
            print("="*72)

    scoresheet.loc["Subtotal"] = 0
    scoresheet.loc["Bonus"] = 0
    for P in players:
        scoresheet.loc["Subtotal", P.n] = scoresheet[P.n].sum()
        if scoresheet.loc["Subtotal", P.n] >= 75:
            scoresheet.loc["Bonus", P.n] = 50


    print()
    print("="*72)
    print("*"*72)
    print("FINAL SCORES...")
    print()
    time.sleep(t)
    print(scoresheet)
    print("*"*72)
    print("="*72)
 
    for P in players:
        print(P.n, "final score =", (scoresheet.loc["Subtotal", P.n] + scoresheet.loc["Bonus", P.n]))
play_Yatzy()


# TODO next = complete update_score function










