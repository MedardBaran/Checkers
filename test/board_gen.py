import itertools as it

import numpy as np

from controller import Controller
from model.items import BoardMember, Player, King, Piece, Board


class BoardLayout:
    """
        ; f01;    ; f03;    ; f05;    ; f07
     f10;    ; f12;    ; f14;    ; f16;
        ; f21;    ; f23;    ; f25;    ; f27
     f30;    ; f32;    ; f34;    ; f36;
        ; f41;    ; f43;    ; f45;    ; f47
     f50;    ; f52;    ; f54;    ; f56;
        ; f61;    ; f63;    ; f65;    ; f67
     f70;    ; f72;    ; f74;    ; f76;

    Creates pieces to be injected into Tailored Board.
    Possible kwargs:
        - keys: see table above,
        - vals: 'wP' := White Piece
                'wK' := White King
                'rP' := Red Piece
                'rK' := Red King
    """

    def __init__(self, **kwargs):
        self.pieces = {}

        to_set_up = self._filter_kwargs(**kwargs)
        for addr, piece_config in to_set_up.items():
            _, row, col = addr
            row, col = int(row), int(col)
            player, piece_class = self._translate_piece_config(piece_config)

            self.pieces[(row, col)] = piece_class(row, col, player)

    def __call__(self):
        """
        Get pieces to be injected into Tailored Board
        :return: dict: {addr tuple: piece instance}
        """
        return self.pieces

    def _filter_kwargs(self, **kw):
        available_keys = ['f' + str(row) + str(col) for row, col in it.product(range(8), range(8))
                          if not (row + col + 1) % 2]
        available_vals = [color + piece_type for color, piece_type in it.product(['W', 'R'], ['P', 'K'])]

        return {key: val.upper() for (key, val) in kw.items()
                if key in available_keys and val.upper() in available_vals}

    def _translate_piece_config(self, piece_config):
        pcolor, ptype = piece_config

        player = Player.white if pcolor == 'W' else Player.red
        piece_cls = Piece if ptype == 'P' else King
        return player, piece_cls


class TailoredBoard(Board):
    def __init__(self, board_layout):
        self.board = np.empty((8, 8), dtype=BoardMember)
        self._init_fields()

        pieces_dict = board_layout()
        for addr, piece in pieces_dict.items():
            self.board[addr] = piece


def start_test_scenario(board_layout):
    c = Controller()
    c.game.board = TailoredBoard(board_layout)
    c.start_game()


if __name__ == '__main__':
    layout = BoardLayout(f23='wK', f34='rP', f63='rP')
    start_test_scenario(layout)
