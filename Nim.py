"""
A simple Monte Carlo solver for Nim
http://en.wikipedia.org/wiki/Nim#The_21_game
"""

import random
import codeskulptor
codeskulptor.set_timeout(20)

MAX_REMOVE = 3
TRIALS = 10000

def evaluate_position(num_items):
    """
    Monte Carlo evalation method for Nim
    """
    win_pct = [0]
    for move in range(MAX_REMOVE):
        items = num_items
        counter = 0
        sub_item = items - (move + 1)
        wins = 0
        while (counter < TRIALS):
            trial_item = sub_item
            player = 1
            while (trial_item > 0):
                trial_item -= random.randint(1,MAX_REMOVE)
                player += 1
            if (player % 2 == 1):
                wins += 1
            counter += 1
        win_pct.append(wins)    
    return win_pct.index(max(win_pct))


def play_game(start_items):
    """
    Play game of Nim against Monte Carlo bot
    """
    
    current_items = start_items
    print "Starting game with value", current_items
    while True:
        comp_move = evaluate_position(current_items)
        current_items -= comp_move
        print "Computer choose", comp_move, ", current value is", current_items
        if current_items <= 0:
            print "Computer wins"
            break
        player_move = int(input("Enter your current move"))
        current_items -= player_move
        print "Player choose", player_move, ", current value is", current_items
        if current_items <= 0:
            print "Player wins"
            break

play_game(10)
        
    
                 
    