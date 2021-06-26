import numpy as np
from copy import deepcopy
from typing import Tuple 


def _sequences_of_k_from_coordinate(coord: Tuple[int, int], k: int): #TODO : return typing
    """ Creates 4 dummy sets that represents k sequential indices in
     4 directions from a given coordingate tuple. 
    """
    horizontal = set([(coord[0], coord[1] + j) for j in range(k)])
    verticle = set([(coord[0] + j, coord[1]) for j in range(k)])
    up_diagonal = set([(coord[0] + j, coord[1] + j) for j in range(k)])
    down_diagonal = set([(coord[0] - j, coord[1] + j) for j in range(k)])
    return horizontal, verticle, up_diagonal, down_diagonal



class MnkGameAi:

    def __init__(self, player, max_search_depth=7):
        self.player = player
        self.max_search_depth = max_search_depth 

    def valid_actions(self, state: np.ndarray):
        return [coord for coord, space in np.ndenumerate(state) if space == "."] # assuming this is the blank space

    def action_result(self, board, player, action):
        new_board = deepcopy(board)
        new_board.update_state(player, action[0], action[1])
        return new_board
        
    def evaluate_state(self, state, k):
        X_coords = [tuple(el) for el in np.stack(np.where(state == "X")).T.tolist()]
        blank_coords = [tuple(el) for el in np.stack(np.where(state == ".")).T.tolist()]

        X_and_blanks = X_coords + blank_coords
        Xset = set(X_coords)
        Xbset = set(X_and_blanks)
        X_score = 0
        for i in X_and_blanks:
            for seq in _sequences_of_k_from_coordinate(i, k):
                if seq <= Xbset:
                    ratio = len(seq & Xset)/k
                    X_score = max(X_score, ratio)
        return X_score            

    def move_search(self, player, board):
        board_ = deepcopy(board)
        if player == "O":
            value, move = self._min_value(board_, -float("inf"), float("inf"), 0)
        else:
            value, move = self._max_value(board_, -float("inf"), float("inf"), 0)
        print(move)
        return move

    def _max_value(self, board, alpha, beta, depth):
        if board.is_terminal_state() and board.find_winner() is not None:
            if board.find_winner() == "X":
                return 1, None
            else:
                return -1, None
            
        depth += 1
        val = -float("inf")
        move = None

        if depth > self.max_search_depth:
            return self.evaluate_state(board.state, board.win_condition), move
        
        actions = self.valid_actions(board.state)
        for act in actions:
            val_, act_ = self._min_value(self.action_result(board, "X", act), alpha, beta, depth)
            if val_ > val :
                val, move = val_, act
                alpha = max( alpha , val )
            if val >= beta :
                return val, move   

        return val, move


    def _min_value(self, board, alpha, beta, depth):
        if board.is_terminal_state() and board.find_winner() is not None:
            if board.find_winner() == "X":
                return 1, None
            else:
                return -1, None

        depth += 1
        val = float("inf")
        move = None 

        if depth > self.max_search_depth:
            return self.evaluate_state(board.state, board.win_condition), move

        actions = self.valid_actions(board.state)
        for act in actions:
            val_, act_ = self._max_value(self.action_result(board, "O", act), alpha, beta, depth)
            if val_ < val :
                val, move = val_, act
                beta = min( beta , val )
            if val <= alpha :
                return val, move

        return val, move


    

class Connect4GameAi(MnkGameAi):

    def valid_actions(self, state: np.ndarray):
        blanks_row, blanks_col = np.where(state == ".")
        return np.unique(blanks_col)#[coord for coord, space in np.ndenumerate(state) if space == "."] # assuming this is the blank space

    def action_result(self, board, player, action):
        new_board = deepcopy(board)
        new_board.update_state(player, action)
        return new_board

    def evaluate_state(self, state, k):
        X_coords = [tuple(el) for el in np.stack(np.where(state == "X")).T.tolist()]
        O_coords = [tuple(el) for el in np.stack(np.where(state == "O")).T.tolist()]
        blank_coords = [tuple(el) for el in np.stack(np.where(state == ".")).T.tolist()]

        X_and_blanks = X_coords + blank_coords
        Xset = set(X_coords)
        Xbset = set(X_and_blanks)
        X_score = 0
        for i in X_and_blanks:
            for seq in _sequences_of_k_from_coordinate(i, k):
                if seq <= Xbset:
                    ratio = len(seq & Xset)/k
                    X_score = max(X_score, ratio)

        '''
        O_and_blanks = O_coords + blank_coords
        Oset = set(O_coords)
        Obset = set(O_and_blanks)
        O_score = 0
        for i in O_and_blanks:
            for seq in _sequences_of_k_from_coordinate(i, k):
                if seq <= Obset:
                    ratio = len(seq & Oset)/k
                    O_score = max(O_score, ratio)
        '''
        return X_score# - O_score   