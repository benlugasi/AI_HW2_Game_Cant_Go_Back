"""
MiniMax Player with AlphaBeta pruning and global time
"""
from players.AbstractPlayer import AbstractPlayer
import SearchAlgos
import time
import utils


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time, penalty_score) # keep the inheritance of the parent's (AbstractPlayer) __init__()
        self.alphaBeta = SearchAlgos.AlphaBeta(self.utility, self.succ, self.perform_move, self.goal,
                                               self.heuristic_function, self.revert_move)
        #TODO: initialize more fields, if needed, and the AlphaBeta algorithm from SearchAlgos.py


    #def set_game_params(self, board):
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
        #TODO: erase the following line and implement this function.
        raise NotImplementedError


    # def set_rival_move(self, pos):
    #     """Update your info, given the new position of the rival.
    #     input:
    #         - pos: tuple, the new position of the rival.
    #     No output is expected
    #     """
    #     AbstractPlayer.set_rival_move(self, pos=pos)

    def make_move(self,time_limit, player_score):
     raise NotImplementedError



    # #TODO: erase the following line and implement this function. In case you choose not to use this function,
    # # use 'pass' instead of the following line.
    #     AbstractPlayer.update_fruits(self,fruits_on_board_dict=fruits_on_board_dict)


    ########## helper functions in class ##########
    #TODO: add here helper functions in class, if needed


    ########## helper functions for AlphaBeta algorithm ##########
    #TODO: add here the utility, succ, and perform_move functions used in AlphaBeta algorithm