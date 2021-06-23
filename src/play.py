import game.gameplay

'''
def test_tic_tac_toe():
    ttt = game.board.TicTacToeBoard()
    print(ttt.players)
    
    ttt.display()
    print(ttt.find_winner())
    print(ttt.is_terminal_state())
    ttt.update_state("X", 0, 0)
    ttt.update_state("X", 0, 1)
    ttt.update_state("X", 0, 2)
    ttt.display()
    print(ttt.find_winner())
    print(ttt.is_terminal_state())
    
    ttt = game.board.TicTacToeBoard()
    ttt.update_state("O", 0, 0)
    ttt.update_state("X", 0, 1)
    ttt.update_state("O", 0, 2)
    ttt.update_state("O", 1, 0)
    ttt.update_state("X", 1, 1)
    ttt.update_state("O", 1, 2)
    ttt.update_state("X", 2, 0)
    ttt.update_state("O", 2, 1)
    ttt.update_state("X", 2, 2)
    ttt.display()
    print(ttt.find_winner())
    print(ttt.is_terminal_state())
'''
if __name__ == "__main__":
    #test_tic_tac_toe()
    #ttt = game.gameplay.TicTacToe(ai_players=["O"])
    #ttt = game.gameplay.TicTacToe(ai_players=[])
    #ttt.start()

    c4 = game.gameplay.Connect4(ai_players=["O"])
    c4.start()