"""
Monte Carlo Tic-Tac-Toe Player
"""
#Must be run in codeskulptor2

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 10         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial (board, player):
    """
    Runs through a whole game, with the given player making the first move.
    Alternates with each player making random moves until someone wins or a draw happens.
    Does not return anything, modifies the given board.
    """
    mover = player
    while (board.check_win() == None): #plays until someone wins, or the game is a draw
        empties = board.get_empty_squares()
        selection = random.choice(empties) 
        board.move(selection[0], selection[1], mover) #make a move into a random empty square
        mover = provided.switch_player(mover)  #swap player

def mc_update_scores(scores, board, player):
    """
    Scores the given board. If the given player won, each tile the player
    used gets a constant added to it, and each tile the loser used gets a constant
    subtracted from the corresponding tile in the score grid. If the given player lost
    then instead the player gets their scores subtracted in the score grid and the winner
    gets their scores added. Empty tiles get a score of 0, and if the game was a draw
    the score of each tile is 0. Directly modifies the score grid, does not return anything.
    """
    rows = range(board.get_dim())
    cols = range(board.get_dim())
    current = SCORE_CURRENT
    other = SCORE_OTHER
    other_player = provided.switch_player(player)
    
    if (board.check_win() == provided.DRAW): #if the game is a draw don't add anything to scores
        for row in rows:
            for col in cols:
                scores[row][col] += 0
    else:
        if (board.check_win() == player): #making sure we subtract from opponent scores if the player wins
            other *= -1
        else:                             #making sure we subtract player scores if the player loses
            current *= -1
        for row in rows:                  #updating scores over the board
            for col in cols:
                if board.square(row, col) == player:
                    scores[row][col] += current
                elif board.square(row, col) == other_player:
                    scores[row][col] += other
                else:
                    scores[row][col] += 0         
            
        
#mc_update_scores(scores, use_board, provided.PLAYERX) #test
def get_best_move(board, scores):
    """
    Looks over the scores of empty tiles and returns the tile with the highest score
    as a tuple. If there is a tie for highest score, the function randomly returns one of the
    tied tiles.
    """
    empties = board.get_empty_squares()
    length = range(len(empties))
    max = scores[empties[0][0]][empties[0][1]]
    best_tiles = []
    
    for entry in length: #iterating over empty cells and seeing which has the highest score
        if scores[empties[entry][0]][empties[entry][1]] >= max:
            max = scores[empties[entry][0]][empties[entry][1]]
    for entry in length:
        if scores[empties[entry][0]][empties[entry][1]] == max:
            best_tiles.append(empties[entry])  #adding cells that have the max score to a list
    return random.choice(best_tiles)        #randomly selecting cell among the ones with a max score
    
def mc_move(board, player, trials):
    """
    Does a monte carlo simulation to determine which should be the next move. Does a certain number 
    of trials, scores the moves of the trials, then chooses the highest scoring move to do. 
    """
    size = board.get_dim()
    counter = 0
    scores = [[0 for count in range(size)] for value in range(size)]
    while (counter < trials): #doing all the trials starting from current state of board
        copied_board = board.clone()
        mc_trial(copied_board, player)
        mc_update_scores(scores, copied_board, player) #scoring all the trials
        counter += 1
    return get_best_move(board, scores)    #returning whichever cell had the best score

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
