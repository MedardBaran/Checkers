import copy
import itertools as it
import string as st
from collections import OrderedDict
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

    def set_following_move(self, following_move):
        self.following_move = following_move

    def clone(self):
        return Move(self.piece, self.dest, self.captured_piece, self.following_move)


class MovesGenerator:
    def __init__(self, player, board):
        self.player = player
        self.board = board()
        self.max_length = 0

    def generate(self):
        """
        Return the list of all possible moves to be done in one turn by single player. Contains the multiple captures
        to do by single piece in a row.
        :return: dict, key: Piece, value: [Moves]
        """
        moves = OrderedDict()

        for piece in self._get_pieces():
            possible_moves = self._get_possible_moves_per_piece(piece)
            if possible_moves:
                moves[piece] = possible_moves

        moves = self._filter_captures(moves)
        moves = self._filter_longest_moves(moves)
        return moves

    def _get_pieces(self):
        pieces = []
        for row in self.board:
            for item in row:
                if isinstance(item, Piece) and item.player == self.player:
                    pieces.append(item)
        return pieces

    def _get_possible_moves_per_piece(self, piece) -> list:
        # todo: add recurrent function to calculate next moves... include board copy as argument
        captures = self._get_captures(piece)

        if captures:
            return captures
        else:
            moves = self._get_moves(piece)
            return moves

    def _get_captures(self, piece):
        captures = []
        addrs = piece.get_my_diagonal_neighbours(max_dist=piece.max_distance+1, min_dist=2, direction='nwse')

        for addr in addrs:
            target = self._get_piece_to_capture(piece, addr)
            if target is not None:
                capture = Move(piece, addr, captured_piece=target)
                captures.append(capture)

        if captures:
            return captures

    def _get_moves(self, piece):
        # fixme: ta metoda zwraca wiele niemozliwych ruchow...
        moves = []
        dir_to_move = piece.player.value
        addrs = piece.get_my_diagonal_neighbours(max_dist=piece.max_distance, direction=dir_to_move)

        for addr in addrs:
            if self._is_move_allowed(piece, addr):
                move = Move(piece, addr)
                moves.append(move)

        return moves

    def _is_move_allowed(self, piece, destination):
        addrs_between = self._get_fields_between(piece.addr, destination)

        for addr in [*addrs_between, destination]:
            field = self.board[addr]
            is_occupied = isinstance(field, Piece) or isinstance(field, King)
            if is_occupied:
                return False
        return True

    def _get_piece_to_capture(self, attacker: Piece, destination: tuple):
        possible_victims = []
        addrs_between = self._get_fields_between(attacker.addr, destination)
        for addr in addrs_between:
            field = self.board[addr]

            is_occupied = isinstance(field, Piece) or isinstance(field, King)
            is_occupied_by_other_player = hasattr(field, "player") and field.player != attacker.player

            if is_occupied and not is_occupied_by_other_player:
                return None
            elif is_occupied and is_occupied_by_other_player:
                possible_victims.append(field)

        is_destination_empty = isinstance(self.board[destination], EmptyField)
        if len(possible_victims) == 1 and is_destination_empty:
            return possible_victims[0]
        else:
            return None

    def _get_fields_between(self, addr1, addr2):
        fields = []
        r1, c1 = addr1
        r2, c2 = addr2

        assert abs(r2-r1) == abs(c2-c1)

        length = abs(r2-r1)
        direction = (int((r2-r1)/length), int((c2-c1)/length))

        for i in range(1, length):
            field = _vector_sum(addr1, *(direction, )*i)
            fields.append(field)
        return fields

    def _filter_captures(self, moves):
        for move_list in moves.values():
            for move in move_list:
                if move.is_capturing:
                    moves = self._remove_moves_leave_captures(moves)
                    break
        return moves

    def _remove_moves_leave_captures(self, moves):
        new_moves = OrderedDict()
        for piece, moves_list in moves.items():
            captures = [move for move in moves_list if move.is_capturing]
            if captures:
                new_moves[piece] = captures

        return new_moves

    def _filter_longest_moves(self, moves):
        # todo: find longest capture/move and filter ...
        return moves


class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = Player.white
        self.player_iterator = it.cycle([Player.red, Player.white])
        self.next_move = None
        # todo: endgame observer?

    def get_possible_moves(self):
        if self.next_move:
            return self.next_move

        gen = MovesGenerator(self.current_player, self.board)
        moves = gen.generate()
        if not moves:
            self._change_player()
            self._is_end_game()

        return moves

    def move(self, move: Move):
        self.board.move(move.piece, move.dest)
        if move.is_capturing:
            self.board.pick_up(move.captured_piece)

        if self.next_move:
            self.next_move = move.following_move
        else:
            self._change_player()

    def get_board(self):
        return self.board.board

    def _change_player(self):
        self.current_player = next(self.player_iterator)

    def _is_end_game(self):
        # todo:
        print(f"Game ends. {self.current_player} player wins.")


def _vector_sum(basic_addr, *addrs, reverse_addrs=False):
    temp = []
    if reverse_addrs:
        for addr in addrs:
            temp.append([-1 * i for i in addr])
    else:
        temp = addrs

    return tuple([sum(addr) for addr in zip(basic_addr, *temp)])


def _is_on_board(r, c):
    return 0 <= r <= 7 and 0 <= c <= 7


if __name__ == '__main__':
    b = Game()
    print('end')
