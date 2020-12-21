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
        self.minimax = SearchAlgos.MiniMax(self.utility, self.succ, self.perform_move, self.goal, self.heuristic_function, self.revert_move)
        #TODO: initialize more fields, if needed, and the Minimax algorithm from SearchAlgos.py

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
        self.fruit_life = min(len(self.board), len(self.board[0]))

    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        start = time.time()
        cur_state = Player.PlayerState(board=self.board, playerToMove=1, score=players_score, fruit_life=self.fruit_life)
        depth = 1
        self.fruit_life = max(0, self.fruit_life-1)
        last_valid_move = self.minimax.search(cur_state, depth, 1, time_limit)[1]
        if last_valid_move is None:
            return None
        while True:
            depth += 1
            time_elapsed = time.time() - start
            move = self.minimax.search(state=cur_state, depth=depth, maximizing_player=1, time_limit=time_limit-time_elapsed)[1]
            if move is not None:
                last_valid_move = move
            else:
                assert (utils.count_val(self.board, 1) == 1)
                self.board[self.pos] = -1
                assert (utils.count_val(self.board, 1) == 0)
                i = self.pos[0] + last_valid_move[0]
                j = self.pos[1] + last_valid_move[1]
                new_pos = (i, j)
                assert self.board[new_pos] not in [-1, 1, 2]
                self.board[new_pos] = 1
                assert utils.count_val(self.board, 1) == 1
                self.pos = new_pos
                return last_valid_move

    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        # rival (3,3) -> pos(3,4)
        rival_prev_pos = utils.getPlayerPos(self.board, 2)
        self.fruit_life = max(0, self.fruit_life - 1)
        self.board[rival_prev_pos] = -1
        i = rival_prev_pos[0] + pos[0]
        j = rival_prev_pos[1] + pos[1]
        new_pos = (i, j)
        assert self.board[new_pos] not in [-1, 1, 2]
        self.board[new_pos] = 2
        assert utils.count_val(self.board, 2) == 1

    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        # translate the fruit's position from np.where to location on board
        np_fruits_pos = np.where(self.board > 2)
        ghost_fruits = tuple(ax[0] for ax in np_fruits_pos)

        for fruit_pos in ghost_fruits:
            if fruit_pos not in fruits_on_board_dict:
                self.board[fruit_pos] = 0

        for fruit_pos, fruit_val in fruits_on_board_dict.items():
            assert self.board[fruit_pos] not in [-1, 1, 2]  # then fruit is still a live
            self.board[fruit_pos] = fruit_val


    # _______ helper functions in class _______
    class PlayerState:
        def __init__(self, board, playerToMove, score, fruit_life):
            self.playerToMove = playerToMove
            self.pos = utils.getPlayerPos(board, playerToMove)
            self.rival_pos = utils.getPlayerPos(board, utils.nextTurn(playerToMove))
            self.score = score
            self.fruit_life = fruit_life

    # _______helper functions for MiniMax algorithm _________
    def goal(self, state):
        return not utils.playerCanMove(self.board, state.pos)

    def succ(self, state, maximizing_player):  # ->List(directions)
        succ_states = []
        if state.playerToMove == maximizing_player:  # Maximizing
            pos = state.pos
        else:  # Minimizing
            pos = state.rival_pos
        for d in self.directions:
            i = pos[0] + d[0]
            j = pos[1] + d[1]
            if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and (
                    self.board[i][j] not in [-1, 1, 2]):  # then move is legal
                succ_states.append(d)
        return succ_states

    def perform_move(self, state, d, maximizing_player):  # ->succ_state
        if state.playerToMove == maximizing_player:  # Maximizing
            pos = state.pos
            rival_pos = state.rival_pos
        else:  # Minimizing
            pos = state.rival_pos
            rival_pos = state.pos
        i = pos[0] + d[0]
        j = pos[1] + d[1]
        new_pos = (i, j)

        self.board[state.pos] = -1
        self.board[new_pos] = state.playerToMove

        new_player_to_move = utils.nextTurn(state.playerToMove)
        new_fruit_life = max(0, state.fruit_life - 1)

        new_pos_val = 0
        if new_fruit_life > 0:
            new_pos_val = self.board[new_pos]
        penalty = 0
        if not utils.playerCanMove(self.board, new_pos) and utils.playerCanMove(self.board, rival_pos):
            penalty = self.penalty_score
        new_score = state.score
        new_score[state.playerToMove - 1] += new_pos_val - penalty  # the fruit was on my pos + penalty if there any

        return Player.PlayerState(self.board, new_player_to_move, new_score, new_fruit_life)

    def revert_move(self, state, next_state):
        penalty = 0
        if not utils.playerCanMove(self.board, next_state.rival_pos) and utils.playerCanMove(self.board,
                                                                                             next_state.pos):
            penalty = self.penalty_score

        fruit_val = next_state.score[state.playerToMove - 1] - state.score[state.playerToMove - 1] + penalty

        self.board[next_state.rival_pos] = fruit_val
        self.board[state.pos] = state.playerToMove

    def utility(self, state):
        assert (self.goal(state))
        return state.score[0] - state.score[1]

    def heuristic_function(self, state):  # 4 parameters: curr_score, md from fruits, fruits value, is reachable fruit
        """
        Gets the state
        Returns heuristic function based on below:
        1.Gap between players score
        2. Distance from an (3)is-reachable fruit
        4. Manaheten Distance
        """
        my_potential_score = 0
        rival_potential_score = 0

        for fruit_pos in np.where(self.board > 2):
            my_dist_from_fruit = utils.mDist(state.pos, fruit_pos)
            rival_dist_from_fruit = utils.mDist(state.rival_pos, fruit_pos)
            if my_dist_from_fruit < rival_dist_from_fruit and my_dist_from_fruit <= state.fruit_life:
                my_potential_score += self.board[fruit_pos]
            elif rival_dist_from_fruit < my_dist_from_fruit and rival_dist_from_fruit <= state.fruit_life:
                rival_potential_score += self.board[fruit_pos]
        return (state.score[0] + my_potential_score) - (rival_potential_score + state.score[1])

