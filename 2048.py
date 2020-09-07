"""
Clone of 2048 game.
"""

import poc_2048_gui, random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    lastmerge = 0
    size = len(line)
    nonzeros = [number for number in line if number != 0]
    numcount = len(nonzeros)
    
    for entry in range(1, numcount):
        if nonzeros[entry - 1] == nonzeros[entry]:
            nonzeros[entry - 1] *= 2
            nonzeros[entry] = 0
            lastmerge = entry - 1
       
    merged = [value for value in nonzeros if value != 0]
    numcount = len(merged)
    
    zeros = [0 for count in range(size - numcount)]
    merged = merged + zeros

    return merged

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    def gen_start(self, start_cell, direction, num_steps):
        """
        Generate the starting rows/columns for moving when a move is made
        """
        row_list = []
        row_entry = []
        col_entry = []
        for step in range(num_steps):
            row_entry.append(start_cell[0] + step * direction[0])
            col_entry.append(start_cell[1] + step * direction[1])
        row_list = list(zip(row_entry, col_entry))    
        return row_list    

    def __init__(self, grid_height, grid_width):
        self.height = grid_height
        self.width = grid_width
        self.board = [[0 for entry in range(grid_width)] for count in range(grid_height)]
        self.iter_start = {UP: self.gen_start((0, 0), (0, 1), grid_width),
                           DOWN: self.gen_start((grid_height - 1, 0), (0, 1), grid_width), 
                           LEFT: self.gen_start((0, 0), (1, 0), grid_height), 
                           RIGHT: self.gen_start((0, grid_width - 1), (1, 0), grid_height)}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self.board = [[0 for entry in range(self.width)] for count in range(self.height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        full_str = ' '.join([str((self.board[row][col]) for col in self.width) + "/n" for row in self.height])
        return full_str

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        iterations = 0
        row_list = []
        merge_values = []
        merged_list = []
        if (direction == UP) or (direction == DOWN):
            iterations = self.get_grid_height()
        else:
            iterations = self.get_grid_width()
        for entry in range(len(self.iter_start[direction])): #for each starting cell in the row or column that provides starting cells
            row_entry = self.iter_start[direction][entry][0]
            col_entry = self.iter_start[direction][entry][1]
            row_list = self.gen_start(self.iter_start[direction][entry], OFFSETS[direction], iterations)#generate the column or row to merge in the proper direction as a list of tuples
            for value in row_list:
                row_entry = value[0]
                col_entry = value[1]
                merge_values.append(self.board[row_entry][col_entry])                       
            merged_list = merge(merge_values)
            merge_values = []
            counter = 0
            for value in row_list:
                self.board[value[0]][value[1]] = merged_list[counter]
                counter += 1
            counter = 0
        self.new_tile()    
                                    
          

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        insert_value = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
        while (True):
            zeros = 0
            for entry in range(self.height):
                for count in range(self.width):
                    if self.board[entry][count] == 0:
                        zeros += 1
            if zeros == 0:
                print "Game Over"
                quit()
            zeros = 0    
            selected_row = random.randint(0, self.height - 1)
            selected_column = random.randint(0, self.width - 1)
            if self.board[selected_row][selected_column] == 0:
                self.board[selected_row][selected_column] = insert_value
                break
            

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.board[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.board[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))