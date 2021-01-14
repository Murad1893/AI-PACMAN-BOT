from state import Agent
from state import Actions
from state import movement
import random
from utility_functions import coords_distance
import utility_functions

class ghost_agent( Agent ):
    def __init__( self, index ):
        self.index = index

    def get_move( self, state ): #return an action
        dist = self.get_probability_distribution (state) #evaluating the probabilities of attacking or fleeing using factors as distance from pacman etc.
        if len(dist) == 0:
            return movement.STOP
        else:
            return utility_functions.select_from_probability_distribution( dist )

#GHOST THAT CHOOSES AN ACTION RANDOMLY
class random_ghost( ghost_agent ):
    def get_probability_distribution ( self, state ):
        dist = utility_functions.Counter()
        for a in state.get_legal_moves( self.index ): dist[a] = 1.0
        dist.normalize()
        return dist

#GHOST THAT CHOOSES AN ACTION SMARTLY
class directional_ghost( ghost_agent ):
    def __init__( self, index, prob_attack=0.8, prob_scared=0.8 ):
        self.index = index
         #setting the probabilities for the ghost to flee or attack
        self.prob_attack = prob_attack
        self.prob_scared = prob_scared

    def get_probability_distribution ( self, state ):
        # Read variables from state
        ghost_state = state.get_ghost_state( self.index )
        legal_move = state.get_legal_moves( self.index )
        coord = state.get_ghost_coord( self.index )
        is_scared = ghost_state.scared_timer > 0

        speed = 1
        if is_scared: speed = 0.5

        action_vectors = [Actions.direction_from_vector( a, speed ) for a in legal_move]
        new_coords = [( coord[0]+a[0], coord[1]+a[1] ) for a in action_vectors] #ghost positions
        pacman_position = state.get_pacman_coord() #pacman positions

        # Select best actions given the state
        distances_from_pacman = [coords_distance( coord, pacman_position ) for coord in new_coords]
        if is_scared: #choose the position with the max distance from pacman and start to flee there
            max_score = max( distances_from_pacman )
            best_probablilty = self.prob_scared
        else: #choose the positions with the min distance from pacman and start to attack there
            max_score = min( distances_from_pacman )
            best_probablilty = self.prob_attack
        best_actions = [action for action, distance in zip( legal_move, distances_from_pacman ) if distance == max_score]

        # Construct distribution
        dist = utility_functions.Counter()
        for a in best_actions: dist[a] = best_probablilty / len(best_actions)
        for a in legal_move: dist[a] += ( 1-best_probablilty ) / len(legal_move)
        dist.normalize()
        return dist
