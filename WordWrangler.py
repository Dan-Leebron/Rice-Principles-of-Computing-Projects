"""
Student code for Word Wrangler game
"""
# avoiding use of set, sorted, or sort to focus on ordered lists and recursion

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"
codeskulptor.set_timeout(15)

# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    newlist = [list1[0]]
    comparison = list1[0]
    for item in list1:
        if comparison != item:
            newlist.append(item)
            comparison = item
    return newlist

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    intersection = []
    for item in list1:
        if item in list2:
            intersection.append(item)
    return intersection

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    merged_list = []
    
    while len(list1) != 0 or len(list2) != 0:
        if len(list1) == 0:
            merged_list = merged_list + list2
            list2 = []
        elif len(list2) == 0:
            merged_list = merged_list + list1
            list1 = []
        elif list1[0] <= list2[0]:
            merged_list.append(list1[0])
            list1.remove(list1[0])
        else:
            merged_list.append(list2[0])
            list2.remove(list2[0])
            
    return merged_list

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) == 1:
        return list1
    else:
        half_length = len(list1)/2
        half1 = merge_sort(list1[:half_length])
        half2 = merge_sort(list1[half_length:])
        return merge(half1, half2)

# Function to generate all strings for the word wrangler game
def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """

    if word == "":
        return [""]
    
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        new_words = []
        for item in rest_strings:
            for letter in range(len(item) + 1):
                new_words.append(item[:letter] + first + item[letter:])
        return rest_strings + new_words
           


# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    word_list = []
    words = codeskulptor.file2url(WORDFILE)
    netfile = urllib2.urlopen(words)
    for line in netfile.readlines():
        word_list.append(line[:-1])   
    return word_list

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()
