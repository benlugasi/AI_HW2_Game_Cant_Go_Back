"""
Player for the competition
"""

from players.AbstractPlayer import AbstractPlayer
import SearchAlgos
import numpy as np
import time
import utils


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time, penalty_score)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        self.alphaBeta = SearchAlgos.AlphaBeta(self.utility, self.succ, self.perform_move, self.goal, self.heuristic_function, self.revert_move)
        self.remaining_time = game_time


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
        self.fruit_life = 2 * min(len(self.board), len(self.board[0]))

    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        start = time.time()
        time_frame = self.calc_time_frame(self.board)
        self.score = players_score
        time_frame_epsilon = 0.01
        time_frame = time_frame - time_frame_epsilon # attempt to suit the time to the global limit
        time_limit_epsilon = 0.05
        time_limit = time_limit - time_limit_epsilon
        time_frame = min(time_frame, time_limit)

        cur_state = Player.PlayerState(board=self.board, playerToMove=1, fruit_life=self.fruit_life, fruit_taken=0,
                                       penalty_taken=0)
        depth = 1
        self.fruit_life = max(0, self.fruit_life - 1)
        last_valid_move = self.alphaBeta.search(state=cur_state, depth=depth, maximizing_player=1,
                                                time_limit=time_frame)
        if last_valid_move is None:
            for d in self.directions:
                i = self.pos[0] + d[0]
                j = self.pos[1] + d[1]
                new_pos = (i, j)
                if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[new_pos] not in [-1, 1, 2]:
                    self.board[self.pos] = -1
                    self.board[new_pos] = 1
                    self.pos = new_pos
                    self.remaining_time -= time.time() - start
                    return d
        else:
            last_valid_move = last_valid_move[1]
        while depth < len(self.board) * len(self.board[0]):  # total number of possible steps on the board
            depth += 1
            time_elapsed = time.time() - start
            move = self.alphaBeta.search(state=cur_state, depth=depth, maximizing_player=1,
                                         time_limit=time_frame - time_elapsed)
            if move is not None:
                last_valid_move = move[1]
            else:
                break
       # assert (utils.count_val(self.board, 1) == 1)
        self.board[self.pos] = -1
       # assert (utils.count_val(self.board, 1) == 0)
        i = self.pos[0] + last_valid_move[0]
        j = self.pos[1] + last_valid_move[1]
        new_pos = (i, j)
       # assert self.board[new_pos] not in [-1, 1, 2]
        self.board[new_pos] = 1
       # assert utils.count_val(self.board, 1) == 1
        self.pos = new_pos
        self.remaining_time -= (time.time() - start)
        return last_valid_move

    def calc_time_frame(self, board):
        moveable_squares = len(np.where(board == 0)[0]) + len(np.where(board > 2)[0])
        total_squares = len(self.board) * len(self.board[0])
        return (moveable_squares*self.remaining_time) / (2*total_squares)

    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        rival_prev_pos = utils.getPlayerPos(self.board, 2)
        self.board[rival_prev_pos] = -1
      #  assert self.board[pos] not in [-1, 1, 2]
        self.board[pos] = 2
      #  assert utils.count_val(self.board, 2) == 1

    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        self.fruits_on_board_dict = fruits_on_board_dict
        for fruit_pos in utils.getFruitsOnBoard(self.board):
            if len(fruits_on_board_dict) == 0 or fruit_pos not in fruits_on_board_dict:
                self.board[fruit_pos] = 0

        for fruit_pos, fruit_val in fruits_on_board_dict.items():
          #  assert self.board[fruit_pos] not in [-1, 1, 2]  # then fruit is still a live
            self.board[fruit_pos] = fruit_val

    # ##### Helper Class: PlayerState - a game state  ######
    class PlayerState:
        def __init__(self, board, playerToMove, fruit_life, fruit_taken, penalty_taken):
            self.playerToMove = playerToMove
            self.pos = utils.getPlayerPos(board, playerToMove)
            self.rival_pos = utils.getPlayerPos(board, utils.nextTurn(playerToMove))
            self.fruit_life = fruit_life
            self.fruit_taken = fruit_taken
            self.penalty_taken = penalty_taken

    # ########## helper functions for the competing algorithm ##########

    def goal(self, state):
        return not utils.playerCanMove(self.board, state.pos)

    def succ(self, state, maximizing_player):  # ->List(directions)
        succ_states = []
        for d in self.directions:
            i = state.pos[0] + d[0]
            j = state.pos[1] + d[1]
            if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and (
                    self.board[i][j] not in [-1, 1, 2]):  # then move is legal
                succ_states.append(d)
        return succ_states

    def perform_move(self, state, d, maximizing_player):  # ->succ_state
        i = state.pos[0] + d[0]
        j = state.pos[1] + d[1]
        new_pos = (i, j)

        self.board[state.pos] = -1

        new_player_to_move = utils.nextTurn(state.playerToMove)
        new_fruit_life = max(0, state.fruit_life - 1)

        fruit_taken = 0
        if new_fruit_life > 0:
            fruit_taken = self.board[new_pos]

        self.board[new_pos] = state.playerToMove
        penalty_taken = 0
        if not utils.playerCanMove(self.board, new_pos) and utils.playerCanMove(self.board, state.rival_pos):
            penalty_taken = self.penalty_score
        self.score[state.playerToMove - 1] = self.score[state.playerToMove - 1] + fruit_taken - penalty_taken  # the fruit was on my pos + penalty if there any

        return Player.PlayerState(self.board, new_player_to_move, new_fruit_life, fruit_taken, penalty_taken)

    def revert_move(self, state, next_state):
        if next_state.rival_pos in self.fruits_on_board_dict:  # reverts pos from fruit dictionary
            self.board[next_state.rival_pos] = self.fruits_on_board_dict[next_state.rival_pos]
        else:
            self.board[next_state.rival_pos] = 0
        self.board[state.pos] = state.playerToMove  # reverts pos to states pos
        self.score[state.playerToMove - 1] = self.score[
                                                 state.playerToMove - 1] - next_state.fruit_taken + next_state.penalty_taken  # reverts score

    def utility(self, state):
       # assert (self.goal(state))
        return self.score[0] - self.score[1]

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

        for fruit_pos in utils.getFruitsOnBoard(self.board):
            my_dist_from_fruit = utils.mDist(state.pos, fruit_pos)
            rival_dist_from_fruit = utils.mDist(state.rival_pos, fruit_pos)
            if my_dist_from_fruit < rival_dist_from_fruit and my_dist_from_fruit <= state.fruit_life:
                my_potential_score += self.board[fruit_pos]
            elif rival_dist_from_fruit < my_dist_from_fruit and rival_dist_from_fruit <= state.fruit_life:
                rival_potential_score += self.board[fruit_pos]
        return (self.score[0] + my_potential_score) - (rival_potential_score + self.score[1])
