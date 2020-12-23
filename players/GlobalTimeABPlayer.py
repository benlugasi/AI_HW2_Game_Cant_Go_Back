"""
MiniMax Player with AlphaBeta pruning and global time
"""
from players.AbstractPlayer import AbstractPlayer
import SearchAlgos
import numpy as np
import time
import utils


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time, penalty_score) # keep the inheritance of the parent's (AbstractPlayer) __init__()
        self.alphaBeta = SearchAlgos.AlphaBeta(self.utility, self.succ, self.perform_move, self.goal, self.heuristic_function, self.revert_move)
        self.remaining_time = game_time

    #  def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, a 2D matrix of the board.
        No output is expected.
        """

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
        time_frame = time_frame - time_frame_epsilon
        # time_limit_epsilon = 0.05
        # time_limit = time_limit - time_limit_epsilon
        # time_frame = min(time_frame, time_limit)

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
                    print(f"(2) compete random depth: {depth} time frame: {time_frame}")
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
        print(f"compete depth: {depth} time frame: {time_frame}")
        return last_valid_move

    def calc_time_frame(self, board):
        moveable_squares = len(np.where(board == 0)[0]) + len(np.where(board > 2)[0])
        total_squares = len(self.board) * len(self.board[0])
        return (moveable_squares * self.remaining_time) / (2 * total_squares)

    # def set_rival_move(self, pos):
    #     """Update your info, given the new position of the rival.
    #     input:
    #         - pos: tuple, the new position of the rival.
    #     No output is expected
    #     """
    #     AbstractPlayer.set_rival_move(self, pos=pos)