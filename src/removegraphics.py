import time
import pacman


#for suppressing the display
class null_graphic:
    def initialize(self, state, isBlue = False):
        pass

    def update(self, state):
        pass

    def end(self):
        time.sleep(SLEEP_TIME)

    def draw(self, state):
        print(state)

    def finish(self):
        pass
