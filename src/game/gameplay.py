from abc import ABC

from game.board import GameBoard, Connect4Board
from ai.move_search import MnkGameAi, Connect4GameAi

class Game(ABC):

    def __init__(self, m: int, n: int, k: int, board_type=GameBoard, ai_type=MnkGameAi, ai_players=None, **kwargs):
        self.board = board_type(m, n, k)
        self.turn = 0
        if ai_players is not None and len(ai_players) > 0:
            self.ai = ai_type(ai_players[0])
            self.ai_players = ai_players
        else:
            self.ai_players = []
    
    def start(self):
        print("\t ~~~ Let's play a game ~~~ \n")
        print(f" You are  {self.board.players[self.turn]} ")
        self.move()

    def move(self):
        self.board.display()
        
        current_player = self.board.players[self.turn]
        print(f" Player {current_player}'s turn ")

        if current_player in self.ai_players:
            x, y = self.ai.move_search(current_player, self.board)
        else:
            x = input(" Input the (x) coordinate you want to play at : ")
            y = input(" Input the (y) coordinate you want to play at : ")
        
        if self.board.update_state(current_player, int(x), int(y)):
            self._increment_turn()
        
        if self.board.is_terminal_state():
            winner = self.board.find_winner()
            print(f" Player {winner} has won the game")
            self.board.display()
        else:
            print()
            self.move()

    def _increment_turn(self):
        if self.turn == len(self.board.players) - 1:
            self.turn = 0
        else:
            self.turn += 1


class TicTacToe(Game):

    def __init__(self, **kwargs):
        """ 
        """
        Game.__init__(self, 3, 3, 3, ai_players=kwargs["ai_players"])


class Connect4(Game):

    def __init__(self, **kwargs):
        """ 
        """
        Game.__init__(self, 6, 7, 4, board_type=Connect4Board, ai_type=Connect4GameAi, ai_players=kwargs["ai_players"])

    def move(self):
        self.board.display()
        
        current_player = self.board.players[self.turn]
        print(f" Player {current_player}'s turn ")

        if current_player in self.ai_players:
            y = self.ai.move_search(current_player, self.board)
        else:
            y = input(" Input the column you want to play in : ")
        
        if self.board.update_state(current_player, int(y)):
            self._increment_turn()
        
        if self.board.is_terminal_state():
            winner = self.board.find_winner()
            self.board.display()
            print(f" Player {winner} has won the game")
        else:
            print()
            self.move() 