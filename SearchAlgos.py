"""Search Algos: MiniMax, AlphaBeta
"""
import time
import utils
from utils import ALPHA_VALUE_INIT, BETA_VALUE_INIT



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
        self.goal = goal

    def search(self, state, depth, maximizing_player):
        pass


class MiniMax(SearchAlgos):
    def __init__(self, utility, succ, perform_move, goal, heuristic_function, revert_move):
        super().__init__(utility, succ, perform_move, goal)
        self.heuristic_function = heuristic_function
        self.revert_move = revert_move

    def rbMinimax_rec(self, state, depth, maximizing_player,remaining_time):
        if remaining_time <= 0:
            return None
        start = time.time()
        if self.goal(state):
            return [self.utility(state), state]
        if depth == 0:
            return [self.heuristic_function(state), state]
        # init for the recursion
        children = self.succ(state, maximizing_player) #(0,1),(1,0)...
        if state.playerToMove == maximizing_player:
            curMaxState = [float('-inf'), state]
            for c in children:
                time_elapsed = time.time() - start
                new_state = self.perform_move(state, c, maximizing_player)
                child_value = self.rbMinimax_rec(new_state, depth - 1, maximizing_player, remaining_time - time_elapsed)
                self.revert_move(state, new_state)
                if child_value is None:
                    return None
                if child_value[0] > curMaxState[0]:
                    curMaxState = [child_value[0], new_state]
            return curMaxState
        else:
            curMinState = [float('inf'), state]
            for c in children:
                time_elapsed = time.time() - start
                new_state = self.perform_move(state, c, maximizing_player)
                child_value = self.rbMinimax_rec(new_state, depth - 1, maximizing_player, remaining_time - time_elapsed)
                self.revert_move(state, new_state)
                if child_value is None:
                    return None
                if child_value[0] < curMinState[0]:
                    curMinState = [child_value[0], new_state]
            return curMinState

    def search(self, state, depth, maximizing_player, time_limit = float('inf')):
        """Start the MiniMax algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        result = self.rbMinimax_rec(state, depth, maximizing_player, time_limit)
        if result is None:
            return None
        result_state = result[1]
        if result_state.playerToMove == maximizing_player:  # Maximizing
            result_pos = result_state.pos
        else:  # Minimizing
            result_pos = result_state.rival_pos
        return result[0], utils.getDir(state.pos, result_pos)


class AlphaBeta(SearchAlgos):
    def __init__(self, utility, succ, perform_move, goal, heuristic_function, revert_move):
        super().__init__(utility, succ, perform_move, goal)
        self.heuristic_function = heuristic_function
        self.revert_move = revert_move

    def alpha_beta(self, state, depth, maximizing_player, alpha, beta, time_limit):
        if time_limit <= 0:
            return None  #
        start = time.time()
        if self.goal(state):
            return [self.utility(state), state]
        if depth == 0:
            return [self.heuristic_function(state), state]
        # init for the recursion
        children = self.succ(state, maximizing_player)  # (0,1),(1,0)...
        if state.playerToMove == maximizing_player:
            curMaxState = [float('-inf'), state]
            for c in children:
                time_elapsed = time.time() - start
                new_state = self.perform_move(state, c, maximizing_player)
                child_value = self.alpha_beta(new_state, depth - 1, maximizing_player, alpha, beta, time_limit - time_elapsed)
                self.revert_move(state, new_state)
                if child_value is None:
                    return None
                if child_value[0] > curMaxState[0]:
                    curMaxState = [child_value[0], new_state]
                alpha = max(curMaxState[0], alpha)
                if curMaxState[0] >= beta:
                    return [float('inf'), new_state]
            return curMaxState
        else:
            curMinState = [float('inf'), state]
            for c in children:
                time_elapsed = time.time() - start
                new_state = self.perform_move(state, c, maximizing_player)
                child_value = self.alpha_beta(new_state, depth - 1, maximizing_player, alpha, beta, time_limit - time_elapsed)
                self.revert_move(state, new_state)
                if child_value is None:
                    return None
                if child_value[0] < curMinState[0]:
                    curMinState = [child_value[0], new_state]
                beta = min(curMinState[0], beta)
                if curMinState[0] <= alpha:
                    return [float('-inf'), new_state]
            return curMinState



    def search(self, state, depth, maximizing_player, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT, time_limit = float('inf')):
        """Start the AlphaBeta algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param alpha: alpha value
        :param: beta: beta value
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        result = self.alpha_beta(state=state, depth=depth, maximizing_player=maximizing_player, alpha=alpha, beta=beta, time_limit=time_limit)
        if result is None:
            return None
        result_state = result[1]
        if result_state.playerToMove == maximizing_player:
            result_pos = result_state.pos
        else: # minimizing
            result_pos = result_state.rival_pos
        return result[0], utils.getDir(state.pos, result_pos)
