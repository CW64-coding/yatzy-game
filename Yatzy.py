# This file will run a Maxi Yatzy game.
# Developed just for fun and Python/Vim coding practice.

# Rules of Yatzy used for this game:-
#   * 6 dice, 3 rolls per round (unused rolls are saved and accumulate)
#   * player can choose order to assign scores (within current section)
#   * Bonus is achieved with score of >=75 in 'Upper' section
#   * The same number can be used in hands
#       e.g. three 6's and 2 6's is also a full house


from random import randint  # needed for dice rolls
import pandas as pd         # the scoresheet will be displayed as DataFrame
import re                   # regular expressions used to check some inputs
import time                 # for pausing and better user readability
from itertools import combinations as combo     # for finding sets

t = 0           # variable for pauses, set to 0 while testing

class Player():     # Player class holds name and counter of extra rolls
    def __init__(self, name, extra_rolls=0):
        self.n = name
        self.e = extra_rolls

def game_setup():       # function to set number of players & get names
    while True:
        global n        # ensures 'n' is accessible outside function
        n = input("Number of players (2-6): ")
        try:
            n = int(n)
        except ValueError:
            print("Valid integer please. Try again: ")
            continue
        if (2 <= n <= 6):
            break
        else:
            print("Invalid range. Try again (2-6): ")

    global players
    players = []
    for i in range(1, n+1):
        name_input = ""
        while True:
            name_input = input(f"Player {i} name: ")
            if name_input != "" and name_input not in players:
                break
            else:
                print("Invalid or name already taken. Please try again: ")
        players.append(Player(name = name_input))

game_setup()
       
# names of the different potential scores and respective codes
upper_rows = ["One's", "Two's", "Three's",
                "Four's", "Five's", "Six's"]

lower_rows = ["1 pair", "2 pairs", "3 pairs",
                "3 of a kind", "4 of a kind", "5 of a kind",
                "Small straight", "Big straight", "Full straight",
                "Full House (3+2)", "Villa (3+3)", "Tower (4+2)",
                "Chance", "MAXI YATZY"]

lower_codes = ["1p", "2p", "3p", "3k", "4k", "5k", "ss", "bs", "fs",
                "fh", "vi", "tw", "ch", "my"]

scoresheet = pd.DataFrame(index = upper_rows, columns = [P.n for P in players])


# function calculates possible scores from the current roll
# then returns the players choice and the respective score
def score(dice, section, player): 
    if section == upper_rows:
        score_choice = {}
        for i in range(len(upper_rows)):
            score_choice[section[i]] = sum([x for x in dice if x == (i+1)])
        print()
        print("Possible scores:-","\n")
        print(score_choice,"\n")
        time.sleep(t)
        print("Make a selection, type 1-6. E.g. for 'Four's', enter: 4")
        print("(Note you can only choose a free option)")
        print()
        while True:
            try:
                choice = int(input("Choose: ")) - 1     # -1 to match PC counting
                if choice not in range(6):
                    print("Try again, type between 1-6: ")
                elif pd.notna(scoresheet.loc[section[choice], player.n]):
                    print("Score already filled-in, please choose again.\n")
                else:
                    return section[choice], score_choice[section[choice]]
            except (ValueError, IndexError):
                print("Try again, type between 1-6: ")
                continue
    elif section == lower_rows:
        score_choice = {}

        # we create a dictionary with the dice and their roll counts
        dice_count = {x: dice.count(x) for x in set(dice)}
        
        # a list of dice appearing frequency MOD 2 times
        # using tuples in order to do the calc, so must convert to str
        # will convert back afterwards
        all_pairs = [tuple(str(x))*(dice_count[x] // 2)
                        for x in dice_count]
        
        # eg. [1,1,1,1,2,3] -> [('1','1'), ('1','1'), ('1','1')]
        # so we use list(set()) for a unique list of tuples
        # sorting  saves codes in the later cases
        all_pairs = sorted(list(set(all_pairs)))

        # then loop through the tuples and concatenate the values as int
        all_pairs = [int(x) for tup in all_pairs for x in tup]


        score_choice["1 pair"] = {
            # sorted added for easier user readability
            "Dice": [x for x in set(all_pairs)],
            "Score": [0] if all_pairs == [] else 
                    [2*x for x in set(all_pairs)]}
                                 
        score_choice["2 pairs"] = {
            "Dice": list(set(combo(all_pairs, 2))),
            "Score": [0] if len(all_pairs) < 2
                else [2*sum(x) for x in set(combo(all_pairs, 2))]}
        

        score_choice["3 pairs"] = {
            "Dice": list(combo(all_pairs, 3)),
        # 0/1 item so no set required, output is either [] or [x]
        # therefore below we can use double sum to give [0] or [sum()] 
            "Score": [2*sum([sum(x) for x in combo(all_pairs, 3)])]}
        
        # same process as above for 'all_pairs'
        all_triples = [tuple(str(x))*(dice_count[x] // 3) for x in dice]
        all_triples = sorted(list(set(all_triples)))
        all_triples = [int(x) for tup in all_triples for x in tup]

        score_choice["3 of a kind"] = {
            "Dice": list(set(all_triples)),
            "Score": [0] if all_triples == [] 
                        else [3*x for x in set(all_triples)]}
        

        all_quads = [x for x in dice_count if dice_count[x] > 3]

        score_choice["4 of a kind"] = {
            "Dice": all_quads, "Score": [4*sum(all_quads)]}


        five_kind = [x for x in dice_count if dice_count[x] >= 5]

        score_choice["5 of a kind"] = {
            "Dice": five_kind, "Score": [5*sum(five_kind)]}


        score_choice["Small straight"] = {
            "Dice": ([1,2,3,4,5]
                if all(x in dice for x in [1,2,3,4,5]) else []),
            "Score": ([15] 
                if all(x in dice for x in [1,2,3,4,5]) else [0])}

        score_choice["Big straight"] = {
            "Dice": ([2,3,4,5,6]
                if all(x in dice for x in [2,3,4,5,6]) else []),
            "Score": ([20] 
                if all(x in dice for x in [2,3,4,5,6]) else [0])}

        score_choice["Full straight"] = {
            "Dice": ([1,2,3,4,5,6] if len(dice_count) == 6 else []),
            "Score": ([25] if len(dice_count) == 6 else [0])}


        if all_triples == [] or len(all_pairs) < 2:
            full_house = []
        else:
            full_house = list(combo(([x for x in all_triples]
                + [y for y in all_pairs if y not in all_triples]), 2))

        score_choice["Full House (3+2)"] = {
            "Dice": full_house,
            "Score": [sum([3*x[0]+2*x[1] for x in full_house])]}
                        
        
        score_choice["Villa (3+3)"] = {
            "Dice": list(combo(all_triples, 2)),
            # list is [] or 1 item only
            # so below we can use double sum to give [0] or [sum()] 
            "Score": [3*sum([sum(x) for x in combo(all_triples, 2)])]}


        tower = list(combo(all_quads 
                + len(all_quads)*[x for x in set(all_pairs)
                if (x not in all_quads) or (dice_count[x] == 6)], 2))
                # latter case in 'or' allows case of Yatzy
                # len(all_quads) = 0 if no quads so ensure tower = []

        score_choice["Tower (4+2)"] = {
            "Dice": tower, "Score": [sum([4*x[0]+2*x[1] for x in tower])]}


        score_choice["Chance"] = {
            "Dice": sorted(dice), "Score": [sum(dice)]}


        score_choice["MAXI YATZY"] = {
            "Dice": dice if len(dice_count) == 1 else [],
            "Score": [100] if len(dice_count) == 1 else [0]}

        print()
        print()
        print("Possible scores   = [Dice used]                    [Score]:-","\n")
        
        for key in score_choice.keys():
            # adjustments ensure table is aligned visually for the user
            print(key.ljust(18), end = "= ")
            print(str(score_choice[key]["Dice"]).ljust(30), end=" ")
            print(score_choice[key]["Score"]) 
        time.sleep(t)

        print()
        print()
        print("Make a selection, use this code:")
        print("(...only the highest possible score per chosen row will be taken, of course!)")
        print()
        for i in range(len(lower_codes)):
            print((lower_codes[i] + ": " + lower_rows[i]).ljust(20), end="\t")
            if ((i+1) % 3 == 0) and (i != 0):
                print()
        print()            
        print()
        print("(Note you can only choose a free option)")
        print()

        while True:
            code = input("Choose from code list (e.g. '4k'): ").lower()      
            try:
                choice = lower_rows[lower_codes.index(code)]
                if pd.notna(scoresheet.loc[choice, player.n]):
                    print("Score already fixed, please choose again.")
                    print()
                else:
                    return choice, score_choice[choice]["Score"]
            except (ValueError, KeyError): 
                print("Try again, type a code from the list above.")
                print()
    else:
        print("Unexpected 'section' error...")


def update_score(player):       # function to update score after user has chosen
    dice = [*current_roll.values()]     # dictionary's values in a list 
    row, points = score(dice, section, player)
    if section == upper_rows:
        scoresheet.loc[row, player.n] = points
    else:
        scoresheet.loc[row, player.n] = max(points, default = 0)


def re_roll():          # function re-rolls the dice as per user choice
    dice_to_reroll = ""
    # while loop ensures user input is combo of "A"-"F" (no repeats)
    while not re.search(r"""
            ^                      # fixed start position
              (?!                  # negative lookahead i.e. ensure no match for...
              .*(.).*\1)           # anything/1 char/anything/same 1 char 
              [A-F]{1,6}           # then match A-F 1-6 times (but no repeat due to above)
            $"""                   # fixed end position
            , dice_to_reroll
            , re.VERBOSE):          # re.VERBOSE allows above indenting/comments

        dice_to_reroll = input("""
            Enter a string of dice to RE-ROLL.
            (For example, to re-roll all except dice B & C enter: ADEF)
            Enter now: """).upper()
    
    for letter in dice_to_reroll:
       current_roll[letter] = randint(1,6)

# function that rolls 6 die, 3 times, calling re_roll() if user wants 
# then the function allows user to use extra rolls (with re_roll())
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
            2) re-roll (from A-F state which dice to re-roll)""")
        print("-"*72)
        
        choice = input("Type '1' to lock in or '2' to re-roll: ")
        while choice not in ["1", "2"]:
            print("Invalid entry, try again: ","\n")
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
            elif choice in ["y", "yes"]:
                re_roll()
                print()
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

# function plays the game, calling roll for each player each round
# then printing the updated scoresheet as the game progresses 
def play_Yatzy():
    print()
    print("LET YATZY BEGIN!!!")
    print()
    global scoresheet           # otherwise scoresheet is a new local variable
    print(scoresheet)
    print()
    print("(Note - 'NaN' is a blank placeholder)")

    global section
    section = upper_rows      # for separating the game sections
    for i in range(6):
        for j in range(n):
            print()
            print(f"Round {i+1} - {players[j].n}")
            print("="*72)
            roll(players[j])
            print("="*72)
    scoresheet.loc["Subtotal - Upper"] = 0
    scoresheet.loc["Bonus"] = 0
    for P in players:
        scoresheet.loc["Subtotal - Upper", P.n] = scoresheet[P.n].sum()
        if scoresheet.loc["Subtotal - Upper", P.n] >= 75:
            scoresheet.loc["Bonus", P.n] = 50
    scoresheet.loc["------"] = "---"
    time.sleep(t)

    print()
    print("="*72)
    print("*"*72)
    print("Scores so far...")
    print()
    time.sleep(t*2)
    print(scoresheet)
    print("*"*72)
    print("="*72)
    time.sleep(t*4)
  
    section = lower_rows
    print()
    print()
    time.sleep(t)
    print(scoresheet)
    print("*"*72)
    print("="*72)
    print()
    print()
    time.sleep(t)

    print("Final section...")
    print() 
    ss_lower = pd.DataFrame(index = lower_rows, columns = [p.n for p in players])
    scoresheet = pd.concat([scoresheet, ss_lower])
    print(scoresheet)
    time.sleep(t)
    
    print()
    print()
    print("-"*72)
    
    # for each round for each player, print out the round then call roll()
    for i in range(6, 6+len(section)):
        for j in range(n):
            print()
            print(f"Round {i+1} - {players[j].n}")
            print("="*72)
            roll(players[j])
            print("="*72)
    time.sleep(t)

    scoresheet.loc["------"] = "---"
    scoresheet.loc["Subtotal - Lower"] = 0
    scoresheet.loc["======"] = "==="
    scoresheet.loc["Grand total"] = 0
    scoresheet.loc["Subtotal - Lower"] = scoresheet.loc[lower_rows].sum()
    scoresheet.loc["Grand total"] = scoresheet.loc[
        ["Subtotal - Upper", "Bonus", "Subtotal - Lower"]].sum()

    print()
    print("="*72)
    print("*"*72)
    print("FINAL SCORES...")
    print()
    time.sleep(t*4)
    print(scoresheet)
    print()
    print("*"*72)
    print("="*72)
    print()


play_Yatzy()
