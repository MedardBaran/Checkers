from model import *
from terminalView import *


class Controller:
    def __init__(self):
        self.game = Game()
        self.board = self.game.get_board()
        self.next_turn = Player.red

        print_board(self.board)


if __name__ == '__main__':
    c = Controller()
    print("available moves for red b", c.game.get_possible_moves(c.board[5, 2]))
