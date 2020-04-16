# Yatzy Game
## Introduction
This repository contains code I have written purely for practice of Python, Vim and Git/GitHub usage.

The code runs a text-based user-input style game of Maxi Yatzy, as a fun way to explore several programming concepts.

When the code is run, a text input-based game for 2-6 players is initiated.

All code is purely my own, developed from scratch through trial-and-error and basic online research.


### Game background: Maxi Yatzy (aka "Swedish Yatzhee")
Maxi Yatzy is Yahtzee with an extra die, more ways to score points and a feature where you can save extra rolls for later. I have not adopted the exact Maxi Yatzy rules as e.g. my game allows a '5 of a kind' to also be used as a 'Full House' (3 of a kind and a pair - of the same value).

Assuming the reader is familiar with Yatzhee/Yatzy, below are the variations of my version compared to 'regular' Yatzhee:-
* 6 dice instead of 5, and hence several extra scoring combinations on the scoreboard
* players can choose to forfeit one or two of the maximum 3 possible rolls in a turn and instead save up re-rolls that can be used in later turns
* players can choose to score a combination at any time (within the current section - 'Upper' or 'Lower'), scoring does not follow the order of the scoreboard
* bonus points are scored if a player achieves a minimum subtotal of 75+ points in the Upper section.
* in the Lower section - set combinations can be of the same die value e.g. a roll of 3-3-4-3-3-1 could be scored as:-
  1. 4 of a kind (4 x '3') = 12 pts
  1. 2 pair (2 x '3' + 2 x '3') = 12 pts
  1. 3 of a kind (3 x '3') = 9 pts
  1. 1 pair (2 x '3') = 6 pts
