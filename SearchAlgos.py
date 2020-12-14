"""Search Algos: MiniMax, AlphaBeta
"""
from utils import ALPHA_VALUE_INIT, BETA_VALUE_INIT
import math
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

    def __init__(self,utility, succ, perform_move, goal, heuristic_function):
        self.utility = utility
        self.succ = succ
        self.perform_move = perform_move
        self.goal = goal
        self.heuristic_function = heuristic_function

    def search(self, state, depth, maximizing_player):
        """Start the MiniMax algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        if self.goal(state):
            return self.utility(state, maximizing_player)
        if depth == 0:
            return self.heuristic_function(state, maximizing_player)

        playerToMove = self.perform_move(state)
        children = self.succ(state, playerToMove)
        if playerToMove == maximizing_player:
            curMax = float('-inf')
            for c in children:
                child_value = self.search(c, depth-1, playerToMove)
                curMax = max(child_value, curMax)
            return curMax
        else:
            curMin = float('inf')
            for c in children:
                child_value = self.search(c, depth-1, playerToMove)
                curMin = min(child_value, curMin)
            return curMin


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
