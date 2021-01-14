from utility_functions import coords_distance
from state import movement
import random, utility_functions

from state import Agent

class reflex_agent(Agent):

    # A reflex agent chooses action at each phase by using the evaluation function given below
    def get_move(self, game_state):

        def remove_stop(List):  # shows the legal moves
            return [x for x in List if x != 'Stop']  # removing the stop action, as the pacman is not allowed to stop

        # Collect legal moves and successor states
        legal_moves = remove_stop(game_state.get_legal_moves())

        scores = [self.reflex_evaluator(game_state, action) for action in
                  legal_moves]  # Choose the best action amongs the list of possible moves
        max_score = max(scores)  # max of the scores array is extracted
        max_score_indexs = [index for index in range(len(scores)) if
                       scores[index] == max_score]  # get indexes of the max_score in the score array
        random_index = random.choice(
            max_score_indexs)  # as there can be multiple max_scores that are the same, hence we chose any one randomly
        return legal_moves[random_index]

    def reflex_evaluator(self, current_game_state, action):  # This evaluation function is only for the Reflex agent

        # returns a score,the higher the score from reflex_evaluator the better
        # information taken into consideration from current state: remaining coin(new_coin), Pacman position after moving (new_coord), ScaredTimes of the ghosts

        next_game_state = current_game_state.produce_pac_successor(action)
        loc = next_game_state.get_pacman_coord()  # taking the pacman position after moving
        coin = next_game_state.get_coin()  # taking the remaining coin
        ghosts = next_game_state.get_ghost_states() # taking the ghost states
        walls = next_game_state.get_walls()

        dmap = walls.copy()
        stk = utility_functions.Queue()
        stk.push(loc)
        dmap[loc[0]][loc[1]] = 0
        dis = 0
        while not stk.isEmpty():  # Using BFS inorder to find the closest coin available
            x , y = stk.pop()
            dis = dmap[x][y] + 1
            if coin[x][y]:
                break;
            for v in [(0, 1) , (1, 0) , (0 , -1) , (-1 , 0)]:
                xn = x + v[0]
                yn = y + v[1]
                if dmap[xn][yn] == False:
                    dmap[xn][yn] = dis
                    stk.push((xn, yn))
        if(coin.count() == 0):
            dis = 1
        score = 1 - dis
        for ghost in ghosts:
            if ghost.scared_timer == 0:  # active ghost poses danger to the pacman
                score -= 100 ** (1.6 - coords_distance(ghost.get_coord(), loc))
            else:  # bonus points for having a scared ghost
                score += 25
        score -= 30 * coin.count() # bonus points for eating a coin
        return score  # next_game_state.get_score()

def multiAgent_evaluator(current_game_state):

    # The implementation involves a simple breath-first-search that terminates at the closest food near pacman

    # checking if the game is won or lost
    if current_game_state.pac_won():
        return 10000
    elif current_game_state.pac_lost():
        return -10000

    loc = current_game_state.get_pacman_coord() # getting current location
    coin = current_game_state.get_coin() # getting the coin locations
    walls = current_game_state.get_walls() # getting the wall locations
    dmap = walls.copy()
    stk = utility_functions.Queue()
    stk.push(loc)
    dmap[loc[0]][loc[1]] = 0
    dis = 0
    while not stk.isEmpty():  # Using BFS inorder to find the closest coin available
        x , y = stk.pop()
        dis = dmap[x][y] + 1
        if coin[x][y]:
            break;
        for v in [(0, 1) , (1, 0) , (0 , -1) , (-1 , 0)]:
            xn = x + v[0]
            yn = y + v[1]
            if dmap[xn][yn] == False:
                dmap[xn][yn] = dis
                stk.push((xn, yn))
    if(coin.count() == 0):
        dis = 1
    score = 1 - dis
    ghosts = current_game_state.get_ghost_states() # getting ghost states
    for ghost in ghosts:
        if ghost.scared_timer == 0:  # active ghost poses danger to the pacman
            score -= 100 ** (1.6 - coords_distance(ghost.get_coord(), loc))
        else:  # bonus points for having a scared ghost
            score += 25
    score -= 30 * coin.count()  # bonus points for eating a coin
    return score

class mutli_agent_search(Agent):
    # Some variables and methods that are publically available to all Minimax, alpha_beta_agent, and expecti_max_agent
    def __init__(self, evalFn='multiAgent_evaluator', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.reflex_evaluator = utility_functions.lookup(evalFn, globals())
        self.depth = int(depth)  # the depth till which the game_state will be evaluated. The more the depth, the more accurate the result, however, time taken would be greater as more branches would be traversed

class minimax_agent(mutli_agent_search):
    # MINIMAX AGENT
    def get_move(self, game_state):
        # makes use of current game_state to return the proper action, given the depth and the evaluation function to be used.
        # all the agents have been tested without an evaluation function to see how they compare against the reflex agent

        # MAIN CODE
        num_agent = game_state.get_num_agents()  # pacman + ghosts
        action_score = []  # stores the legal move and their scores

        def remove_stop(List):  # shows the legal moves
            return [x for x in List if x != 'Stop']  # removing the stop action, as the pacman is not allowed to stop

        def miniMax(s, iteration_count):  # default depth is '2'
            # print(iteration_count)
            if iteration_count >= self.depth * num_agent or s.pac_won() or s.pac_lost():  # returning the score in case of agent count exceeding the depth for which the evaluation has to be done.
                return self.reflex_evaluator(s)  # using the evaluationFunnction to return the score
            if iteration_count % num_agent != 0:  # Ghost min (e.g 0,5,10 % 5 would be 0 which the index for the Pacman)
                result = 1e10  # +ve infinity

                # get_legal_moves is returning the legal actions for the agent specified. Index 0 represents Pacman and Index 1 onwards represents Ghosts
                for a in remove_stop(s.get_legal_moves(iteration_count % num_agent)):
                    successor_data = s.produce_successor(iteration_count % num_agent,
                                               a)  # generating the successor  game_state for the action specified
                    result = min(result, miniMax(successor_data,
                                                  iteration_count + 1))  # as the agent will minimize, hence choses the result with the minimum benefit
                return result
            else:  # Pacman Max
                result = -1e10  # -ve infinity
                for a in remove_stop(s.get_legal_moves(iteration_count % num_agent)):
                    successor_data = s.produce_successor(iteration_count % num_agent, a)  # same as above
                    result = max(result, miniMax(successor_data,
                                                  iteration_count + 1))  # the pacman will try to maximize the result hence will chose the one with the max benefit
                    if iteration_count == 0:
                        action_score.append(result)
                return result

        result = miniMax(game_state, 0);  # initialiteration_count is 0
        # print (remove_stop(game_state.get_legal_moves(0)), action_score)
        return remove_stop(game_state.get_legal_moves(0))[
            action_score.index(max(action_score))]  # returning the action having the max score

class alpha_beta_agent(mutli_agent_search):
    # ALPHA BETA AGENT
    def get_move(self, game_state):
        # Main Code
        num_agent = game_state.get_num_agents()
        action_score = []

        def remove_stop(List):
            return [x for x in List if x != 'Stop']

        # introduced two factor, alpha and beta here, in order to prune and not traverse all gamestates
        def alpha_beta(s, iteration_count, alpha, beta):
            if iteration_count >= self.depth * num_agent or s.pac_won() or s.pac_lost():
                return self.reflex_evaluator(s)
            if iteration_count % num_agent != 0:  # Ghost min
                result = 1e10
                for a in remove_stop(s.get_legal_moves(iteration_count % num_agent)):
                    successor_data = s.produce_successor(iteration_count % num_agent, a)
                    result = min(result, alpha_beta(successor_data, iteration_count + 1, alpha, beta))
                    beta = min(beta, result)  # beta holds the minimum of the path travered till the root
                    if beta < alpha:  # Pruning. If beta is lesser than alpha, then we need not to traverse the other state
                        break
                return result
            else:  # Pacman Max
                result = -1e10
                for a in remove_stop(s.get_legal_moves(iteration_count % num_agent)):
                    successor_data = s.produce_successor(iteration_count % num_agent, a)
                    result = max(result, alpha_beta(successor_data, iteration_count + 1, alpha, beta))
                    alpha = max(alpha, result)  # alpha holds the maxmimum of the path travered till the root
                    if iteration_count == 0:
                        action_score.append(result)
                    if beta < alpha:  # Prunning
                        break
                return result

        result = alpha_beta(game_state, 0, -1e20, 1e20)  # alpha and beta are set to -ve and +ve infinity as shown
        return remove_stop(game_state.get_legal_moves(0))[action_score.index(max(action_score))]

class expecti_max_agent(mutli_agent_search):
    # EXPECTIMAX AGENT
    def get_move(self, game_state):
        # Main Code
        num_agent = game_state.get_num_agents()
        action_score = []

        def remove_stop(List):
            return [x for x in List if x != 'Stop']

        def expect_minimax(s, iteration_count):
            if iteration_count >= self.depth * num_agent or s.pac_won() or s.pac_lost():
                return self.reflex_evaluator(s)
            if iteration_count % num_agent != 0:  # Ghost min
                successor_score = []
                for a in remove_stop(s.get_legal_moves(iteration_count % num_agent)):
                    successor_data = s.produce_successor(iteration_count % num_agent, a)
                    result = expect_minimax(successor_data, iteration_count + 1)
                    successor_score.append(result)
                avg_score = sum([float(x) / len(successor_score) for x in
                                    successor_score])  # maintaing the average of the scores instead of the max or min
                return avg_score
            else:  # Pacman Max
                result = -1e10
                for a in remove_stop(s.get_legal_moves(iteration_count % num_agent)):
                    successor_data = s.produce_successor(iteration_count % num_agent, a)
                    result = max(result, expect_minimax(successor_data, iteration_count + 1))
                    if iteration_count == 0:
                        action_score.append(result)
                return result

        result = expect_minimax(game_state, 0);
        return remove_stop(game_state.get_legal_moves(0))[action_score.index(max(action_score))]
