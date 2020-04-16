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

class Player():
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
        
upper_rows = ["One's", "Two's", "Three's",
                "Four's", "Five's", "Six's"]    # Add subtotal/bonus later

lower_rows = ["1 pair", "2 pairs", "3 pairs",
                "3 of a kind", "4 of a kind", "5 of a kind",
                "Small straight", "Big straight", "Full straight",
                "Full House (3+2)", "Villa (3+3)", "Tower (4+2)",
                "Chance", "MAXI YATZY"]         # Add grand total

lower_codes = ["1p", "2p", "3p", "3k", "4k", "5k", "ss", "bs", "fs",
                "fh", "vi", "tw", "ch", "my"]


scoresheet = pd.DataFrame(index = upper_rows, columns = [P.n for P in players])


print()
print("LET YATZY BEGIN!!!")
print()
print(scoresheet)
print()
print("(Note - 'NaN' is a blank placeholder)")

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
        print("(...and only the maximum score will be taken, of course!)")
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
        
        all_pairs = list(set(x for x in dice if dice.count(x) >= 2))

        score_choice["1 pair"] = {
            "Dice": all_pairs,
            "Score": ([0] if all_pairs == []
                else [2*x for x in all_pairs])}
        
        
        two_pairs = list(set([x for x in combo(all_pairs
                    + list(set([x for x in dice
                                if dice.count(x) >= 4])), 2)]))

        score_choice["2 pairs"] = {
            "Dice": two_pairs,
            "Score": ([0] if len(two_pairs) == 0
                else [2*(x[0]+x[1]) for x in two_pairs])}
        

        three_pairs = ([x for x in combo(all_pairs, 3)]
                        if len(set(dice)) > 1
                        else [(x, x, x) for x in set(dice)])
        
        score_choice["3 pairs"] = {
            "Dice": three_pairs,
            "Score": ([0] if three_pairs == []
                else [2*(x[0]+x[1]+x[2]) for x in three_pairs])}
        

        all_triples = sorted(list(set(x for x in dice
                        if dice.count(x) >= 3)), reverse=True)
        
        score_choice["3 of a kind"] = {
            "Dice": all_triples,
            "Score": ([0] if all_triples == []
                else [3*x for x in all_triples])}
        

        all_quads = list(set([x for x in dice if dice.count(x) >= 4]))

        score_choice["4 of a kind"] = {
            "Dice": all_quads,
            "Score": ([0] if all_quads == []
                else [4*x for x in all_quads])}


        five_kind = list(set([x for x in dice if dice.count(x) >= 5]))

        score_choice["5 of a kind"] = {
            "Dice": five_kind,
            "Score": ([0] if five_kind == []
                else [5*x for x in five_kind])}


        score_choice["Small straight"] = {
            "Dice": ([1,2,3,4,5]
                if all(x in dice for x in [1,2,3,4,5])
                else []),
            "Score": ([15] 
                if all(x in dice for x in [1,2,3,4,5])
                else [0])}

        score_choice["Big straight"] = {
            "Dice": ([2,3,4,5,6]
                if all(x in dice for x in [2,3,4,5,6])
                else []),
            "Score": ([20] 
                if all(x in dice for x in [2,3,4,5,6])
                else [0])}

        score_choice["Full straight"] = {
            "Dice": ([1,2,3,4,5,6]
                if len(set(dice)) == 6
                else []),
            "Score": ([21]
                if len(set(dice)) == 6
                else [0])}


        if (len(set(dice)) == 1):
            full_house = [2*[x for x in all_triples]]
        elif (all_triples == [] or len(all_pairs) < 2):
            full_house = []
        else:
            full_house = list(combo(([x for x in all_triples]
                + [y for y in all_pairs if y not in all_triples]), 2))


        score_choice["Full House (3+2)"] = {
            "Dice": full_house,
            "Score": ([0] if full_house == []
                            else [3*x[0]+2*x[1] for x in full_house])}
                        
        
        if (len(set(dice)) == 1):
            villa = [2*[x for x in all_triples]]
        else:
            villa = list(combo(all_triples, 2))

        score_choice["Villa (3+3)"] = {
            "Dice": villa,
            "Score": ([0] if villa == []
                            else [3*x[0] + 3*x[1] for x in villa])}


        if (all_quads == []):
           tower = []
        elif (len(set(dice)) == 1):
            tower = [2*[x for x in all_quads]]
        else:
            tower = list(combo(all_quads + 
                    [x for x in all_pairs if x not in all_quads], 2))
                

        score_choice["Tower (4+2)"] = {
            "Dice": tower,
            "Score": ([0] if tower == []
                            else [4*x[0] + 2*x[1] for x in tower])}


        score_choice["Chance"] = {"Dice": dice, "Score": [sum(dice)]}


        yatzy = [] if len(set(dice)) > 1 else dice

        score_choice["MAXI YATZY"] = {
            "Dice": yatzy,
            "Score": ([0] if yatzy == [] else [100])}

        print()
        print()
        print("Possible scores   = [Dice used]                    [Score]:-","\n")
        
        for key in score_choice.keys():
            print(key.ljust(18), end = "= ")
            print(str(score_choice[key]["Dice"]).ljust(30), end=" ")
            print(score_choice[key]["Score"]) 
        time.sleep(t)

        print()
        print()
        print("Make a selection, use this code:")
        print()
        code_choices = list(zip(lower_codes, lower_rows))
        for i in range(1, len(code_choices)+1):
            print(code_choices[i-1], end="\t")
            if (i % 3 == 0) and not (i == 1):
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


def update_score(player):
    dice = [*current_roll.values()]     # dictionary's values in a list 
    row, points = score(dice, section, player)
    if section == upper_rows:
        scoresheet.loc[row, player.n] = points
    else:
        scoresheet.loc[row, player.n] = max(points, default = 0)

def re_roll():
    dice_to_reroll = ""
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
            else:
                if choice in ["y", "yes"]:
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
    global scoresheet           # otherwise scoresheet is a new local variable
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
   
    section = lower_rows
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
