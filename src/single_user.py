from state import Agent
from state import movement
import random

#Keys for the controlling the pacman by the user
class keyboard_agent(Agent):
    # NOTE: Arrow keys also work.
    left_key  = 'a'
    right_key  = 'd'
    up_key = 'w'
    down_key = 's'
    end = 'q'

    def __init__( self, index = 0 ):

        self.last_move = movement.STOP
        self.index = index
        self.keys = []

    def get_move( self, state):
        from gamegraphics import keys_waiting
        from gamegraphics import keys_pressed
        keys = keys_waiting() + keys_pressed()
        if keys != []:
            self.keys = keys

        legal = state.get_legal_moves(self.index)
        move = self.getMove(legal)

        if move == movement.STOP:
            # Try to move in the same direction as before
            if self.last_move in legal:
                move = self.last_move

        if (self.end in self.keys) and movement.STOP in legal: move = movement.STOP

        if move not in legal:
            move = random.choice(legal)

        self.last_move = move
        return move

    def getMove(self, legal):
        move = movement.STOP
        if   (self.left_key in self.keys or 'Left' in self.keys) and movement.left in legal:  move = movement.left
        if   (self.right_key in self.keys or 'Right' in self.keys) and movement.right in legal: move = movement.right
        if   (self.up_key in self.keys or 'Up' in self.keys) and movement.up in legal:   move = movement.up
        if   (self.down_key in self.keys or 'Down' in self.keys) and movement.down in legal: move = movement.down
        return move
