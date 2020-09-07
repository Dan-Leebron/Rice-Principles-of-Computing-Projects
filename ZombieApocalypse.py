"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        return (zombie for zombie in self._zombie_list)

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        return (human for human in self._human_list)
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        rows = self.get_grid_height()
        cols = self.get_grid_width()
        visited = poc_grid.Grid(rows, cols)
        distance_field = [[rows * cols for col in range(cols)] for row in range(rows)]
        boundary = poc_queue.Queue()
        
        if entity_type == HUMAN:
            for human in self.humans():
                person = human
                boundary.enqueue(person)
                distance_field[person[0]][person[1]] = 0
                visited.set_full(person[0], person[1])
        else:
            for zombie in self.zombies():
                person = zombie
                boundary.enqueue(person)
                distance_field[person[0]][person[1]] = 0
                visited.set_full(person[0], person[1])
                
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]) and self.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue((neighbor[0], neighbor[1]))
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
                              
        
        return distance_field
     
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        blocked = self.get_grid_height() * self.get_grid_width() #getting the distance value of obstacles
        new_positions = []
        for human in self.humans(): #calculate move for each human
            moves = self.eight_neighbors(human[0], human[1]) #getting list of up to 8 possible moves
            moves.append((human[0], human[1]))
            potential_moves = []
            distance = zombie_distance_field[human[0]][human[1]]
            for move in moves: #storing potential move if the distance is the max but not that of an obstacle
                if zombie_distance_field[move[0]][move[1]] < blocked:
                    if zombie_distance_field[move[0]][move[1]] > distance:
                        potential_moves = [move]
                        distance = zombie_distance_field[move[0]][move[1]]
                    elif zombie_distance_field[move[0]][move[1]] == distance: #getting multiple moves if valid
                        potential_moves.append(move)       
                    
            new_positions.append(random.choice(potential_moves))
        self._human_list = new_positions                         
            
            
            
    
    def move_zombies(self, human_distance_field): #essentially the same as move_humans, but in 4 directions not 8
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        blocked = self.get_grid_height() * self.get_grid_width()
        new_positions = []
        for zombie in self.zombies():
            moves = self.four_neighbors(zombie[0], zombie[1])
            moves.append((zombie[0], zombie[1]))
            potential_moves = [moves[0]]
            distance = human_distance_field[moves[0][0]][moves[0][1]]
            
            for move in moves:
                if human_distance_field[move[0]][move[1]] < blocked:
                    if human_distance_field[move[0]][move[1]] < distance:
                        potential_moves = [move]
                        distance = human_distance_field[move[0]][move[1]]
                    elif human_distance_field[move[0]][move[1]] == distance:
                        potential_moves.append(move)
                    
            new_positions.append(random.choice(potential_moves))
            
        self._zombie_list = new_positions    
        
# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))