"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set
def combinations(iterable, r): #can't use itertools because codeskulptor does not support it
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = range(r)
    yield tuple(pool[i] for i in indices)
    while True:
        #for i in reversed(range(r)):
        for i in range(r - 1, -1, -1):  
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    uniques = set(hand)
    max_value = 0
    max_index = 0
    for num in uniques:
        value = num * hand.count(num)
        if (value > max_value):
            max_index = num
            max_value = value
    return max_value

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    hands = num_die_sides * num_free_dice
    tot_score = 0
    die_sides = [side + 1 for side in range(num_die_sides)]
    sequences = gen_all_sequences(die_sides, num_free_dice)
    for combo in sequences:
        tot_score += score(held_dice + combo)
    if num_free_dice == 0:
        return score(held_dice)
    return tot_score / float(len(sequences))    

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    possible_set = set([()])
    hand_size = range(len(hand) + 1)
    for length in hand_size:
        combos = combinations(hand, length)
        for combo in combos:
            possible_set.add(combo)
    return possible_set

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    hands = gen_all_holds(hand)
    hand_size = len(hand)
    max_score = 0.0
    max_hand = ()
    for i in hands:
        if (expected_value(i, num_die_sides, hand_size - len(i)) >= max_score):
            max_score = expected_value(i, num_die_sides, hand_size - len(i))
            max_hand = i
    return (max_score, max_hand)

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()

import poc_holds_testsuite
poc_holds_testsuite.run_suite(gen_all_holds)
                                       