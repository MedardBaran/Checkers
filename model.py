from enum import Enum
import string as st
import numpy as np
from itertools import product


class Player(Enum):
    white = 0
    red = 1


class BoardMember:
    def __init__(self, row: int, col: int, available: bool):
        self.row = row
        self.col = col
        self.available = available


class EmptyField(BoardMember):
    pass


class Piece(BoardMember):
    items_created = dict([(i, 0) for i in Player])

    def __init__(self, row, col, player):
        super().__init__(row, col, True)
        self.player = player
        self.id = st.ascii_lowercase[Piece.items_created[player]]
        Piece.items_created[player] += 1


class King(BoardMember):
    pass


class Game:
    def __init__(self):
        self._init_board()
        for p in Player:
            self._init_pieces(p)

    def _init_board(self, size=8):
        self.board = np.empty((size, size), dtype=object)
        for r, c in product(range(size), range(size)):
            av = not (r + c + 1) % 2
            self.board[r, c] = EmptyField(r, c, av)

    def _init_pieces(self, player):
        starting_rows = self.board[:3] if player == Player.white else self.board[-3:]
        for (addr, field) in np.ndenumerate(starting_rows):
            if field.available:
                starting_rows[addr] = Piece(field.row, field.col, player)

    def get_board(self):
        return self.board

    def move(self, piece, to):
        pass

    def get_possible_moves(self, piece):
        pass


if __name__ == '__main__':
    b = Game()
    print(b.get_board())
