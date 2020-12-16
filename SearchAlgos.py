"""Search Algos: MiniMax, AlphaBeta
"""
import time

from utils import ALPHA_VALUE_INIT, BETA_VALUE_INIT

#TODO: you can import more modules, if needed


class SearchAlgos:
    def __init__(self, utility, succ, perform_move, goal=None):
        """The constructor for all the search algos.
        You can code these functions as you like to, 
        and use them in MiniMax and AlphaBeta algos as learned in class
        :param utility: The utility function.
        :param succ: The succesor function.
        :param perform_move: The perform move function.
        :param goal: function that check if you are in a goal state.
        """
        self.utility = utility
        self.succ = succ
        self.perform_move = perform_move

    def search(self, state, depth, maximizing_player):
        pass


class MiniMax(SearchAlgos):
    def __init__(self, utility, succ, perform_move, goal, turn, heuristic_function):
        SearchAlgos.__init__(utility, succ, perform_move, goal)
        self.turn = turn
        self.heuristic_function = heuristic_function

    def rbMinimax_rec(self, state, depth, maximizing_player, remaining_time):
        if remaining_time <= 0:
            raise TimeoutError
        start = time.time()
        if self.goal(state):
            return [self.utility(state, maximizing_player), state]
        if depth == 0:
            return [self.heuristic_function(state, maximizing_player), state]

        # init for the recursion
        state_to_return = state
        playerToMove = self.turn(state)  # Turn
        children = self.succ(state, playerToMove)

        if playerToMove == maximizing_player:
            curMax = [float('-inf'), state_to_return]
            for c in children:
                time_elapsed = time.time() - start
                child_value = self.rbMinimax_rec(c, depth - 1, playerToMove, remaining_time - time_elapsed)
                if child_value[0] > curMax[0]:
                    curMax = child_value
            return curMax
        else:
            curMin = [float('inf'), state_to_return]
            for c in children:
                time_elapsed = time.time() - start
                peform
                child_value = self.rbMinimax_rec(c, depth - 1, playerToMove, remaining_time - time_elapsed)
                if child_value[0] < curMin[0]:
                    curMin = child_value
            return curMin

    def search(self, state, depth, maximizing_player, time_limit = float('-inf')):
        """Start the MiniMax algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        result_state = self.rbMinimax_rec(state, depth, maximizing_player, time_limit)[1]
        return result_state[0], self.getDir(state.pos, result_state.pos)

    def getDir(self, pos1, pos2):
        assert(pos2[0]-pos1[0] in [-1, 0, 1] and pos2[1]-pos1[1] in [-1, 0, 1])
        return pos2[0]-pos1[0], pos2[1]-pos1[1]


class AlphaBeta(SearchAlgos):
    def search(self, state, depth, maximizing_player, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT):
        """Start the AlphaBeta algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param alpha: alpha value
        :param: beta: beta value
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        #TODO: erase the following line and implement this function.
        raise NotImplementedError
