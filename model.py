from enum import Enum
import string as st
import numpy as np


class Field:
    def __repr__(self):
        return "   "


class Player(Enum):
    black = 0
    white = 1


class Piece(Field):
    items_created = dict([(i, 0) for i in list(Player)])

    def __init__(self, player):
        self.player = player
        self.id = st.ascii_lowercase[Piece.items_created[player]]
        Piece.items_created[player] += 1

    def __repr__(self):
        return " " + self.id + " "
        # return " 0 " if self.player == Player.black else " O "


class King(Piece):
    pass


class Board:
    def __init__(self):
        self.board = np.empty((8, 8), dtype=object)

        # fill all available with Field
        self.board[1::2, ::2] = Field()
        self.board[::2, 1::2] = Field()

        # change available Fields in 3 first rows into Player placeholder...
        self.board[1:3:2, ::2] = Player.black
        self.board[:3:2, 1::2] = Player.black
        self.board[-3::2, ::2] = Player.white
        self.board[-2::2, 1::2] = Player.white

        # ...to create new instance of Piece for each Player
        for (addr, item) in np.ndenumerate(self.board):
            if isinstance(item, Player):
                self.board[addr] = Piece(item)

    def print(self):
        print(self.board)

    def check_if_available(self):
        pass

    def return_possible_moves(self):
        pass


if __name__ == '__main__':
    b = Board()
    print(b.board)
