"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(20)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

print SCORES[provided.PLAYERX]
def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    winner = board.check_win() #establishing the base cases for when the game is ended
    if winner == provided.PLAYERX:
        return (1, (-1, -1))
    elif winner == provided.PLAYERO:
        return (-1, (-1, -1))
    elif winner == provided.DRAW:
        return (0, (-1, -1))
    
    else: #otherwise seeing the least bad move that can be made accross the empty squares
        empties = board.get_empty_squares()
        player2 = provided.switch_player(player)
        move_scores = []
        for square in empties: #looking at all the empty squares
            copy = board.clone() #making a copy so we don't modify the board until we figure out the best move
            copy.move(square[0], square[1], player)
            submove = mm_move(copy, player2) #recursively figuring out the potential game states after the first move is made
            move_scores.append((submove[0] * SCORES[player], submove[1], square)) #scoring the game and associating the score with the empty square
            if submove[0] == SCORES[player]: #if the game states following a move provide a winning score, make that move
                return (submove[0], square)
        max_move = max(move_scores) #because we multiplied the score by the player, we can always look for the max
        return (max_move[0], max_move[2]) #choosing the highest scoring move

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)