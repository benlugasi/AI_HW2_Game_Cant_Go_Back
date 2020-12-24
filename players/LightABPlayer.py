"""
MiniMax Player with AlphaBeta pruning with light heuristic
"""
from players.AbstractPlayer import AbstractPlayer
import SearchAlgos
import utils
#TODO: you can import more modules, if needed


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time,
                                penalty_score)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        self.alphaBeta = SearchAlgos.AlphaBeta(self.utility, self.succ, self.perform_move, self.goal,
                                               self.heuristic_function, self.revert_move)

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
        self.score = players_score
        cur_state = Player.PlayerState(board=self.board, playerToMove=1, fruit_life=self.fruit_life, fruit_taken=0,
                                       penalty_taken=0)
        depth = 4
        self.fruit_life = max(0, self.fruit_life - 1)
        last_valid_move = self.alphaBeta.search(state=cur_state, depth=depth, maximizing_player=1)
        last_valid_move = last_valid_move[1]
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
        print(f"LightABPlayer depth: {depth}")
        return last_valid_move

    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        rival_prev_pos = utils.getPlayerPos(self.board, 2)
        self.board[rival_prev_pos] = -1
        assert self.board[pos] not in [-1, 1, 2]
        self.board[pos] = 2
        assert utils.count_val(self.board, 2) == 1

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
            assert self.board[fruit_pos] not in [-1, 1, 2]  # then fruit is still a live
            self.board[fruit_pos] = fruit_val

    # ######## helper functions in class ##########
    # ##### Helper Class: PlayerState - a game state  ######
    class PlayerState:
        def __init__(self, board, playerToMove, fruit_life, fruit_taken, penalty_taken):
            self.playerToMove = playerToMove
            self.pos = utils.getPlayerPos(board, playerToMove)
            self.rival_pos = utils.getPlayerPos(board, utils.nextTurn(playerToMove))
            self.fruit_life = fruit_life
            self.fruit_taken = fruit_taken
            self.penalty_taken = penalty_taken

    ########## helper functions for AlphaBeta algorithm ##########

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
        self.score[state.playerToMove - 1] = self.score[
                                                 state.playerToMove - 1] + fruit_taken - penalty_taken  # the fruit was on my pos + penalty if there any

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
        assert (self.goal(state))
        return self.score[0] - self.score[1]

    def state_score(self, board, pos):
        num_steps_available = 0
        for d in self.directions:
            i = pos[0] + d[0]
            j = pos[1] + d[1]

            # check legal move
            if 0 <= i < len(board) and 0 <= j < len(board[0]) and (board[i][j] not in [-1, 1, 2]):
                num_steps_available += 1

        if num_steps_available == 0:
            return -1
        else:
            return 4 - num_steps_available

    def heuristic_function(self, state):  # 4 parameters: curr_score, md from fruits, fruits value, is reachable fruit
        """
        see ex4 in dry part
        """
        max_fruit_val_min_dist = 0
        for fruit_pos in self.fruits_on_board_dict:
            fruit_val = self.board[fruit_pos]
            dist_from_fruit = max(utils.mDist(state.pos, fruit_pos), 1)
            is_reachable = 0
            if dist_from_fruit <= state.fruit_life:
                is_reachable = 1
            max_fruit_val_min_dist = max(max_fruit_val_min_dist, (fruit_val/dist_from_fruit)*is_reachable)

        if not self.fruits_on_board_dict:
            max_fruit_val = 0
        else:
            max_fruit_pos = max(self.fruits_on_board_dict)
            max_fruit_val = self.board[max_fruit_pos] + 1
        return self.state_score(self.board, state.pos) + max_fruit_val_min_dist/(max_fruit_val + 1)
