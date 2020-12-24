import operator
import numpy as np
import os

# instead of 'None', write the real initialization value, learned in class.
# hint: you can use np.inf
ALPHA_VALUE_INIT = float('-inf')
BETA_VALUE_INIT = float('inf')


def get_directions():
    """Returns all the possible directions of a player in the game as a list of tuples.
    """
    return [(1, 0), (0, 1), (-1, 0), (0, -1)]


def tup_add(t1, t2):
    """
    returns the sum of two tuples as tuple.
    """
    return tuple(map(operator.add, t1, t2))


def get_board_from_csv(board_file_name):
    """Returns the board data that is saved as a csv file in 'boards' folder.
    The board data is a list that contains: 
        [0] size of board
        [1] blocked poses on board
        [2] starts poses of the players
    """
    board_path = os.path.join('boards', board_file_name)
    board = np.loadtxt(open(board_path, "rb"), delimiter=" ")

    # mirror board
    board = np.flipud(board)
    i, j = len(board), len(board[0])
    blocks = np.where(board == -1)
    blocks = [(blocks[0][i], blocks[1][i]) for i in range(len(blocks[0]))]
    start_player_1 = np.where(board == 1)
    start_player_2 = np.where(board == 2)

    if len(start_player_1[0]) != 1 or len(start_player_2[0]) != 1:
        raise Exception('The given board is not legal - too many start locations.')

    start_player_1 = (start_player_1[0][0], start_player_1[1][0])
    start_player_2 = (start_player_2[0][0], start_player_2[1][0])

    return [(i, j), blocks, [start_player_1, start_player_2]]


def getPlayerPos(board, player):
    pos_np = np.where(board == player)
    return tuple(ax[0] for ax in pos_np)


def nextTurn(current_turn):
    return (current_turn % 2) + 1


def playerCanMove(board, pos):
    for d in get_directions():
        i = pos[0] + d[0]
        j = pos[1] + d[1]
        if 0 <= i < len(board) and 0 <= j < len(board[0]) and (board[i][j] not in [-1, 1, 2]):  # then move is legal
            return True
    return False


#  gets pos1 & pos2
#  returns the relative distance between pos2 and pos1 in directions tuple
def getDir(pos1, pos2):
    result_pos = pos2[0]-pos1[0], pos2[1]-pos1[1]
   # assert(result_pos in [(-1, 0), (1, 0), (0, 1), (0, -1)])
    return result_pos


#  counts the number of val appearances on board
def count_val(board, val):
    counter = len(np.where(board == val)[0])
    return counter


# returns the Manheten Distance between pos2 and pos1
def mDist(pos1, pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])


def getFruitsOnBoard(board):
    np_fruit_list = np.where(board > 2)
    fruit_list = []
    if len(np_fruit_list[0]) == 0:
        return fruit_list
    elif len(np_fruit_list[0]) == 1:
        fruit_list.append((np.asscalar(np_fruit_list[0]), np.asscalar(np_fruit_list[1])))  # appending tuple
        return fruit_list
    else:
        for i in range(len(np_fruit_list[0])):
            fruit_list.append(tuple(ax[i] for ax in np_fruit_list))
        return fruit_list