#PACMAN AGENT TYPE
REFLEX = "reflex_agent"
MINIMAX = "minimax_agent"
ALPHA = "alpha_beta_agent"
EXPECTIMAX = "expecti_max_agent"

#maze
TEST = "testClassic"
MINI = "minimaxClassic"
SMALL = "smallClassic"
TRAPPED = "trappedClassic"
ORIGINAL = "originalClassic"

class Game:

    # manages the control flow, requesting actions from agents.
    def __init__( self, agents, display, rules, s_index=0):
        self.agent_crash = False
        self.agents = agents
        self.display = display
        self.rules = rules
        self.s_index = s_index
        self.game_finish = False
        self.move_history = []
        import io
        self.agent_out = [io.StringIO() for agent in agents]

    def get_progress(self): #Checking whether the game is over or not
        if self.game_finish:
            return 1.0
        else:
            return self.rules.get_progress(self)

    def run( self ):
        self.display.initialize(self.state.data)
        self.numMoves = 0

        # inform learning agents of the game start
        for i in range(len(self.agents)):
            agent = self.agents[i]
            if ("registerInitialState" in dir(agent)):
                agent.registerInitialState(self.state.deep_copy())

        agent_index = self.s_index
        numAgents = len( self.agents )

        while not self.game_finish:
            # Fetch the next agent
            agent = self.agents[agent_index]
            move_time = 0
            skip_action = False
            # Generate an observation of the state
            if 'observationFunction' in dir( agent ):
                observation = agent.observationFunction(self.state.deep_copy())
            else:
                observation = self.state.deep_copy()

            # Solicit an action
            action = agent.get_move(observation)

            # Execute the action
            self.move_history.append( (agent_index, action) )
            self.state = self.state.produce_successor( agent_index, action )

            # Change the display
            self.display.update( self.state.data )

            # Allow for game specific conditions (winning, losing, etc.)
            self.rules.process(self.state, self)
            # Track progress
            if agent_index == numAgents + 1: self.numMoves += 1
            # Next agent
            agent_index = ( agent_index + 1 ) % numAgents

        self.display.finish()
