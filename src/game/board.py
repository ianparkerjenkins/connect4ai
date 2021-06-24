import numpy as np 
from abc import ABC
from typing import Tuple


def _coords_have_k_in_a_row(coords: list, k: int) -> bool:
    """ Determines if there are k coordinates of indices in a row.
    """
    coords_set = set(coords)
    for coord in coords_set:
        for seq in _sequences_of_k_from_coordinate(coord, k):
            if seq <= coords_set:
                return True
    return False

def _sequences_of_k_from_coordinate(coord: Tuple[int, int], k: int): #TODO : return typing
    """ Creates 4 dummy sets that represents k sequential indices in
     4 directions from a given coordingate tuple. 
    """
    horizontal = set([(coord[0], coord[1] + j) for j in range(k)])
    verticle = set([(coord[0] + j, coord[1]) for j in range(k)])
    up_diagonal = set([(coord[0] + j, coord[1] + j) for j in range(k)])
    down_diagonal = set([(coord[0] - j, coord[1] + j) for j in range(k)])
    return horizontal, verticle, up_diagonal, down_diagonal


class GameBoard(ABC):
    """ A generic game board for an (m,n,k) game.
    https://en.wikipedia.org/wiki/M,n,k-game
    """

    players = ["X", "O"]
    blank = "."

    def __init__(self, m, n, k):
        """ Initializes an empty game board for an (m,n,k) game. 
        """
        self.num_rows = m
        self.num_cols = n
        self.win_condition = k
        self.state = np.full((m,n), self.blank)

    def find_winner(self): # -> Union[str, None]
        """ Method to determine if the state of the game is in a completed 
        state and who won the game. 

        Returns ``None`` if no player has won the game. 
        """
        for p in self.players:
            player_coords = [tuple(el) for el in np.stack(np.where(self.state == p)).T.tolist()]
            if _coords_have_k_in_a_row(player_coords, self.win_condition):
                return p
        return None

    def is_terminal_state(self):
        if self.find_winner() is None and not np.all(self.state != self.blank):
            return False
        else:
            return True

    def update_state(self, player: str, i: int, j: int):
        assert player in self.players, player
        if i > self.num_rows or j > self.num_cols or i < 0 or j < 0 :
            print("\n This position is not on the board ")
            return False

        if self.state[i,j] == self.blank:
            self.state[i,j] = player
            return True
        else:
            print("\n You cannot play in this position again ")
            return False

    def display(self):
        print(self.state)



class Connect4Board(GameBoard):

    def update_state(self, player: str, col: int):
        assert player in self.players, player
        j = col
        for i in range(self.num_rows-1, -1, -1):
            if i > self.num_rows or j > self.num_cols or i < 0 or j < 0 :
                print("\n This position is not on the board ")
                return False

            if self.state[i,j] == self.blank:
                self.state[i,j] = player
                return True
