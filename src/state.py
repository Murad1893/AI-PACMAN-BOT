from utility_functions import *
import time, os
import traceback
import sys
from gameflow import *

class Agent:
    #returns the index of the agent if any.
    def __init__(self, index=0):
        self.index = index

class movement:
    #Strings defined for the direction (POLES)
    up = 'up'
    down = 'down'
    right = 'right'
    left = 'left'
    STOP = 'Stop'

    #In case, pacman is going in a certain direction, its poles relative to it are defined below:
    left_dir = {up: left, down: right, right:  up, left:  down, STOP:  STOP}
    right_dir = dict([(y,x) for x, y in list(left_dir.items())]) #right is the reverse of left
    reverse_dir = {up: down, down: up, right: left, left: right, STOP: STOP}

class location:

#takes in the initial position of the Pacman and its initial direction as the argument
    def __init__(self, coord, direction):
        self.coord = coord #coords
        self.direction = direction #direction of movement

    #UTILITY FUNCTIONS
    def get_coord(self):
        return (self.coord)

    def get_dir(self):
        return self.direction

    def isInteger(self):
        x,y = self.coord
        return x == int(x) and y == int(y)

    #converts position to direction vector to implement position on the pacman graph
    def produce_successor(self, vector):

        x, y= self.coord
        dx, dy = vector
        direction = Actions.vec_to_dir(vector)
        if direction == movement.STOP:
            direction = self.direction # There is no stop direction
        return location((x + dx, y+dy), direction)

class AgentState:

    #agent_states hold the state of an agent (location, speed, scared, etc).
    def __init__( self, startLocation, is_pac ):
        self.start = startLocation
        self.location = startLocation
        self.is_pac = is_pac #is the agent Pacman or ghost?
        self.scared_timer = 0 #time until the ghost can be eaten

    def copy( self ):
        state = AgentState( self.start, self.is_pac )
        state.location = self.location
        state.scared_timer = self.scared_timer #time until which the agent would be eatable
        return state

    #UTILITY FUNCTIONS
    def get_coord(self):
        if self.location == None: return None
        return self.location.get_coord()

    def get_dir(self):
        return self.location.get_dir()

class Grid:

    def __init__(self, width, height, initialValue=False, bitRepresentation=None):
        if initialValue not in [False, True]: raise Exception('Grids can only contain booleans')
        self.CELLS_PER_INT = 30 #cells per pixel
        #dimensions of the maze
        self.width = width
        self.height = height
        self.data = [[initialValue for y in range(height)] for x in range(width)] #initializing array for the maze
        if bitRepresentation:
            self.unpack_bits(bitRepresentation)

    def __getitem__(self, i):
        return self.data[i]

    def copy(self): #returns a copy of the grid (deep_copy)
        g = Grid(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    def deep_copy(self):
        return self.copy()

    def shallow_copy(self): #pointers to the grid passed
        g = Grid(self.width, self.height)
        g.data = self.data
        return g

    def count(self, item =True ): #returns number of items in the data
        return sum([x.count(item) for x in self.data])

    def as_list(self, key = True): #return the Grid as a list
        list = []
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == key: list.append( (x,y) )
        return list

    def cell_index_to_coord(self, index):
        x = index / self.height
        y = index % self.height
        return x, y

    def unpack_bits(self, bits):
        cell = 0
        for packed in bits:
            for bit in self.unpack_int(packed, self.CELLS_PER_INT):
                if cell == self.width * self.height: break
                x, y = self.cell_index_to_coord(cell)
                self[x][y] = bit
                cell += 1

    def unpack_int(self, packed, size):
        flag = []
        if packed < 0: raise ValueError("must be a positive integer")
        for i in range(size):
            n = 2 ** (self.CELLS_PER_INT - i - 1)
            if packed >= n:
                flag.append(True)
                packed -= n
            else:
                flag.append(False)
        return flag

class Actions:
    # movement
    _directions = {movement.up: (0, 1),
                   movement.down: (0, -1),
                   movement.right:  (1, 0),
                   movement.left:  (-1, 0),
                   movement.STOP:  (0, 0)}

    directions_as_list = list(_directions.items())

    TOLERANCE = .001 #for transition of pacman between the grids

    def reverse_dir(action):
        if action == movement.up:
            return movement.down
        if action == movement.down:
            return movement.up
        if action == movement.right:
            return movement.left
        if action == movement.left:
            return movement.right
        return action
    reverse_dir = staticmethod(reverse_dir)

    def vec_to_dir(vector):
        dx, dy = vector
        if dy > 0:
            return movement.up
        if dy < 0:
            return movement.down
        if dx < 0:
            return movement.left
        if dx > 0:
            return movement.right
        return movement.STOP
    vec_to_dir = staticmethod(vec_to_dir)

   #returning the direction as a vector, incorporated with the speed
    def direction_from_vector(direction, speed = 1.0):
        dx, dy =  Actions._directions[direction]
        return (dx * speed, dy * speed)
    direction_from_vector = staticmethod(direction_from_vector)

    #location is the current game_state of an agent
    def get_possible_moves(location, walls):
        possible = [] #initialized empty
        x, y = location.coord #gets the current coord of Pacman
        x_int, y_int = int(x + 0.5), int(y + 0.5)

        # In between grid points, all agents must continue straight
        if (abs(x - x_int) + abs(y - y_int)  > Actions.TOLERANCE):
            return [location.get_dir()]

        for dir, vec in Actions.directions_as_list:
            dx, dy = vec
            next_y = y_int + dy
            next_x = x_int + dx
            #if the coords are not of the walls, then append to possible
            if not walls[next_x][next_y]: possible.append(dir)

        return possible

    get_possible_moves = staticmethod(get_possible_moves)

class game_state_data: #data pertaining to each state of the game

    def __init__( self, prevState = None ):
        if prevState != None:
            #MAINTAINING THE PREVIOUS STATE IN ORDER TO COMPARE
            self.coin = prevState.coin.shallow_copy()
            self.big_coin = prevState.big_coin[:]
            self.agent_states = self.copy_agent_states( prevState.agent_states )
            self.maze = prevState.maze #previous maze maze
            self._eaten = prevState._eaten
            self.score = prevState.score

        #MAINTAINING STATES FOR THE AGENT
        self.coin_eaten = None
        self._coinAdded = None
        self.big_food_Eaten = None
        self.agent_moved = None #checking if the agent has moved from previous position
        self._lose = False #game lost
        self.win = False #game won
        self.score_change = 0

    def deep_copy( self ): #DEEP COPYING
        state = game_state_data( self )
        state.coin = self.coin.deep_copy()
        state.maze = self.maze.deep_copy()
        state.agent_moved = self.agent_moved
        state.coin_eaten = self.coin_eaten
        state._coinAdded = self._coinAdded
        state.big_food_Eaten = self.big_food_Eaten
        return state

    def copy_agent_states( self, agent_states ):
        copied_states = []
        for agentState in agent_states:
            copied_states.append( agentState.copy() )
        return copied_states

    def initialize( self, maze, numghost_agents ):
        #creating the game_state from the maze (INITIAL STATE)
        self.coin = maze.coin.copy()
        #self.big_coin = []
        self.big_coin = maze.big_coin[:]
        self.maze = maze
        self.score = 0
        self.score_change = 0

        self.agent_states = []
        ghosts_count = 0
        for is_pac, coord in maze.agent_coord:
            if not is_pac:
                if ghosts_count == numghost_agents: continue # Max ghosts reached already
                else: ghosts_count += 1
            self.agent_states.append( AgentState( location( coord, movement.STOP), is_pac) )
        self._eaten = [False for a in self.agent_states] #Checking that agent is eaten or not (as pacman can eat the agents)
