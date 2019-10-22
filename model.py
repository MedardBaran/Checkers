from enum import Enum
import string as st
import numpy as np
from itertools import product


class Player(Enum):
    white = 0
    red = 1


class Field:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return "    "


class Piece(Field):
    items_created = dict([(i, 0) for i in Player])

    def __init__(self, row, col, player):
        super().__init__(row, col)
        self.player = player
        self.id = st.ascii_lowercase[Piece.items_created[player]]
        Piece.items_created[player] += 1

    def __repr__(self):
        return " " + str(self.player.value) + self.id + " "
        # return " 0 " if self.player == Player.red else " O "


class King(Piece):
    pass


class Game:
    def __init__(self):
        self._init_board()
        for p in Player:
            self._init_pieces(p)


        # # fill all available with Field
        # self.board[1::2, ::2] = Field()
        # self.board[::2, 1::2] = Field()
        #
        # # change available Fields in 3 first rows into Player as placeholder...
        # self.board[1:3:2, ::2] = Player.white
        # self.board[:3:2, 1::2] = Player.white
        # self.board[-3::2, ::2] = Player.red
        # self.board[-2::2, 1::2] = Player.red
        #
        # # ...to create new instance of Piece for each Player
        # for (addr, item) in np.ndenumerate(self.board):
        #     if isinstance(item, Player):
        #         self.board[addr] = Piece(item)

    def _init_board(self, size=8):
        self.board = np.empty((size, size), dtype=object)
        for r, c in product(range(size), range(size)):
            self.board[r, c] = Field(r, c) if not (r + c + 1) % 2 else None

    def _init_pieces(self, player):
        arr = self.board[:3] if player == Player.white else self.board[-3:]
        for (addr, item) in np.ndenumerate(arr):
            if isinstance(item, Field):
                arr[addr] = Piece(item.row, item.col, player)

    def get_board(self):
        return self.board

    def move(self, piece, to):
        pass

    def get_possible_moves(self, piece):
        pass


if __name__ == '__main__':
    b = Game()
    print(b.get_board())
