"""
MiniMax Player
"""
from numpy.core._multiarray_umath import ndarray

from players.AbstractPlayer import AbstractPlayer
import numpy as np
import time
import SearchAlgos
import utils
#TODO: you can import more modules, if needed


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time, penalty_score)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        self.minimax = SearchAlgos.MiniMax(self.utility, self.succ, self.perform_move, self.goal, self.turn, self.heuristic_function) # TODO: think about performmove
        #TODO: initialize more fields, if needed, and the Minimax algorithm from SearchAlgos.py

    class PlayerState:
        def __init__(self, board, playerToMove, score):
            self.board = board
            self.playerToMove = playerToMove
            self.pos = np.where(board == playerToMove)
            self.score = score

    def playerCanMove(self, board, pos):
        for d in self.directions:
            i = pos[0] + d[0]
            j = pos[1] + d[1]
            if 0 <= i < len(board) and 0 <= j < len(board[0]) and (board[i][j] not in [-1, 1, 2]):  # then move is legal
                return True
        return False

    def goal(self, state):
        return not self.playerCanMove(state.board,state.pos)

    def turn(self, state):
        return state.playerToMove

    def utility(self, state):
        assert(self.goal(state))
        return state.score[0] - state.score[1]

    def succ(self, state, playerToMove):  # ->List(states)
        succ_states = []
        for d in self.directions:
            i = state.pos[0] + d[0]
            j = state.pos[1] + d[1]
            if 0 <= i < len(state.board) and 0 <= j < len(state.board[0]) and (state.board[i][j] not in [-1, 1, 2]):  # then move is legal
                new_state = self.perform_move(state, d, playerToMove)
                succ_states.append(new_state)
        return succ_states

    def nextTurn(self,current_turn):
        return current_turn % 2 + 1

    def perform_move(self, state, d, playerToMove):  # ->succ_state
        i = state.pos[0] + d[0]
        j = state.pos[1] + d[1]
        new_pos = (i, j)
        penalty = 0
        new_board = state.board
        new_board[state.pos] = -1
        new_board[new_pos] = playerToMove
        new_player_to_move = self.nextTurn(playerToMove)
        new_player_to_move_pos = utils.getPlayerPos(new_board, new_player_to_move)
        if not self.playerCanMove(new_board, new_pos) and self.playerCanMove(new_board, new_player_to_move_pos):
            penalty = self.penalty_score
        new_score = state.score
        new_score[playerToMove - 1] += state.board[new_pos] + penalty  # the fruit was on my pos + penalty if there any
        return Player.PlayerState(new_board, new_player_to_move, new_score)

    def heuristic_function(self, state):  # 4 parameters: curr_score, md from fruits, fruits value, is reachable fruit
        heuristic_val = state.score[0]-state.score[1]
        my_potential_score = 0
        rival_potential_score = 0
        my_pos = state.playerToMove
        rival_pos = np.where(state.board == self.nextTurn(state.playerToMove))
        for fruit_pos in np.where(state.board > 2):
            my_dist_from_fruit = self.mDist(my_pos, fruit_pos)
            rival_dist_from_fruit = self.mDist(rival_pos, fruit_pos)
            if rival_dist_from_fruit < my_dist_from_fruit <= len(state.board):
                my_potential_score += state.board[fruit_pos]
            elif my_dist_from_fruit < rival_dist_from_fruit <= len(state.board):
                rival_potential_score += state.board[fruit_pos]
        return heuristic_val + my_potential_score - rival_potential_score

    def mDist(self, pos1, pos2):
        return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, a 2D matrix of the board.
        No output is expected.
        """
        self.board = board
        self.pos = utils.getPlayerPos(board, 1)

    def count_val(self, board,val):
        counter = len(np.where(board == val)[0])
        return counter

    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        start = time.time()
        cur_state = Player.PlayerState(self.board, 1, players_score)
        depth = 1
        move = self.minimax.search(cur_state, depth, 1, time_limit)[1]
        while True:
            try:   # TODO: handle when finished before max depth
                depth += 1
                time_elapsed = time.time() - start
                move = self.minimax.search(cur_state, depth, 1, time_limit-time_elapsed)[1]
            except TimeoutError:
                assert (self.count_val(self.board, 1) == 1)
                self.board[self.pos] = -1
                assert (self.count_val(self.board, 1) == 0)
                i = self.pos[0] + move[0]
                j = self.pos[1] + move[1]
                new_pos = (i, j)
                assert self.board[new_pos] not in [-1, 1, 2]
                self.board[new_pos] = 1
                assert self.count_val(self.board, 1) == 1
                self.pos = new_pos
                return move

    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        # rival (3,3) -> pos(3,4)
        rival_prev_pos = utils.getPlayerPos(self.board, 2)
        self.board[rival_prev_pos] = -1
        i = rival_prev_pos[0] + pos[0]
        j = rival_prev_pos[1] + pos[1]
        new_pos = (i, j)
        assert self.board[new_pos] not in [-1, 1, 2]
        self.board[new_pos] = 2
        assert self.count_val(self.board, 2) == 1


        #TODO: erase the following line and implement this function.
        raise NotImplementedError

    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        #TODO: erase the following line and implement this function. In case you choose not to use it, use 'pass' instead of the following line.
        raise NotImplementedError


    ########## helper functions in class ##########
    #TODO: add here helper functions in class, if needed


    ########## helper functions for MiniMax algorithm ##########
    #TODO: add here the utility, succ, and perform_move functions used in MiniMax algorithm