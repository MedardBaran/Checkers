import copy
import itertools as it
import string as st
from enum import Enum

import numpy as np

class Player(Enum):
    white = 'n'  # and move south
    red = 's'    # and move north


class BoardMember:
    def __init__(self, row: int, col: int, available: bool):
        self.row = row
        self.col = col
        self.available = available

    @property
    def addr(self):
        return self.row, self.col

    @addr.setter
    def addr(self, new_addr):
        self.row, self.col = new_addr

    def get_my_diagonal_neighbours(self, max_dist=7, min_dist=1, direction='nwse'):
        """
        example: get all +'s for field 'adr'

        -  -  -  -  +  -  -  -
        -  -  -  -  -  +  -  +
        -  -  -  -  -  - adr -
        -  -  -  -  -  +  -  +
        -  -  -  -  +  -  -  -
        -  -  -  +  -  -  -  -
        -  -  +  -  -  -  -  -
        -  +  -  -  -  -  -  -
        """
        ne, nw, se, sw = [(1, 1)], [(1, -1)], [(-1, 1)], [(-1, -1)]
        n, s = ne + nw, se + sw
        nwse = n + s
        dirs = dict(zip(['nwse', 'n', 's', 'nw', 'ne', 'sw', 'se'],
                        [nwse, n, s, nw, ne, sw, se]))

        result = []
        for dist, dr in it.product(range(min_dist, max_dist + 1), dirs[direction]):
            r = self.row + dr[0] * dist
            c = self.col + dr[1] * dist
            if _is_on_board(r, c):
                result.append((r, c))
        return result


class EmptyField(BoardMember):
    def __repr__(self):
        return "  "


class Piece(BoardMember):
    items_created = dict([(i, 0) for i in Player])

    def __init__(self, row, col, player):
        super().__init__(row, col, True)
        self.player = player
        self.max_distance = 1
        self.id = st.ascii_lowercase[Piece.items_created[player]]
        Piece.items_created[player] += 1

    def __repr__(self):
        return f"{self.player.name[0]}P"

    def __del__(self):
        Piece.items_created[self.player] -= 1

    def upgrade(self):
        return King(self.row, self.col, self.player)


class King(Piece):
    def __init__(self, row, col, player):
        super().__init__(row, col, player)
        self.max_distance = 7
        Piece.items_created[player] -= 1

    def __repr__(self):
        return f"{self.player.name[0]}K"


class Board:
    def __init__(self):
        self.board = np.empty((8, 8), dtype=BoardMember)
        self._init_fields()
        for player in Player:
            self._init_pieces(player)

    def __repr__(self):
        view = ""
        for row in self.board:
            view = view + ",".join([item.__repr__() for item in row]) + "\n"
        return view

    def _init_fields(self):
        for row, col in it.product(range(8), range(8)):
            available = not (row + col + 1) % 2
            self.board[row, col] = EmptyField(row, col, available)

    def _init_pieces(self, player):
        starting_rows = self.board[:3] if player == Player.white else self.board[-3:]
        for (addr, field) in np.ndenumerate(starting_rows):
            if field.available:
                starting_rows[addr] = Piece(field.row, field.col, player)

    def __call__(self):
        return self.board

    def pick_up(self, item: BoardMember):
        self.board[item.addr] = EmptyField(*item.addr, available=True)
        return item

    def move(self, item: BoardMember, dest):
        assert self.board[dest].available
        item = self.pick_up(item)
        self.put(item, dest)

    def put(self, item: BoardMember, addr):
        self.board[addr] = item
        item.addr = addr

    def clone(self):
        return copy.deepcopy(self.board)


class Move:
    def __init__(self, piece: BoardMember, dest: BoardMember, captured_piece: BoardMember = None, following_move=None):
        self.piece = piece
        self.dest = dest
        self.captured_piece = captured_piece
        self.is_capturing = captured_piece is not None
        self.following_move = following_move

    def __repr__(self):
        return f"{self.piece}: {self.piece.addr} -> {self.dest}"

    def get_len(self):
        n = 1
        move = self
        while move.following_move is not None:
            move = self.following_move
            n += 1
        return n

    def get_captured_piece(self):
        return self.captured_piece

    # Composite pattern
    def set_following_move(self, following_move):
        self.following_move = following_move

    def clone(self):
        return Move(self.piece, self.dest, self.captured_piece, self.following_move)


def _is_on_board(r, c):
    return 0 <= r <= 7 and 0 <= c <= 7
