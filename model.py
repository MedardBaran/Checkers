from enum import Enum
import string as st
import numpy as np
import itertools as it


class Player(Enum):
    white = 'n'  # and goes south
    red = 's'  # and goes north

# region Pieces
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

    def get_my_diagonal_fields(self, max_dist=7, min_dist=1, direction='nwse'):
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
    pass


class Piece(BoardMember):
    items_created = dict([(i, 0) for i in Player])

    def __init__(self, row, col, player):
        super().__init__(row, col, True)
        self.player = player
        self.id = st.ascii_lowercase[Piece.items_created[player]]
        Piece.items_created[player] += 1

    def decr_items_counter(self):
        Piece.items_created[self.player] -= 1
        # todo: notify endgame observer.


class King(BoardMember):
    # todo: class and its moves to be implemented...
    pass
# endregion Pieces


class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = Player.white
        # todo: endgame observer?

    def get_possible_moves(self, player=None):
        pass

    def move(self, possible_move):
        pass

    def _delete_pieces_between(self, move):
        pass


class Board:
    def __init__(self):
        self.board = np.empty((8, 8), dtype=BoardMember)
        self._init_fields()
        for player in Player:
            self._init_pieces(player)

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

    def move(self, item: BoardMember, dest: BoardMember):
        assert dest.available == True
        item = self.pick_up(item)
        self.put(item, dest)

    def put(self, item: BoardMember, addr: BoardMember):
        self.board[addr] = item
        item.addr = addr


class Move:
    last_id = 0

    def __init__(self, piece: BoardMember, dest: BoardMember, is_capturing: bool, following_move=None):
        self.piece = piece
        self.dest = dest
        self.is_capturing = is_capturing
        self.following_move = following_move
        self.id = self._generate_id()

    def get_len(self):
        n = 1
        move = self
        while move.following_move is not None:
            move = self.following_move
            n += 1
        return n

    def set_following_move(self, following_move):
        self.following_move = following_move

    def clone(self):
        return Move(self.piece, self.dest, self.is_capturing)

    @classmethod
    def _generate_id(cls):
        cls.last_id += 1
        return chr(96 + cls.last_id)

    @classmethod
    def restart_id_generator(cls):
        cls.last_id = 0


class PossibleMoves:
    """list of tuples, where (piece, piece.addr, piece.id, destination.addr, destination.id)"""
    def __init__(self, player, board):
        self.player = player
        self.board = board
        self.possible_moves = []

    def __call__(self):
        return self.possible_moves

    def get_movable_pieces(self):
        pieces = {}
        for row in self.board:
            for item in row:
                if not isinstance(item, Piece) or not item.player == self.player: continue
                possible_moves = self.get_possible_moves(item)
                if possible_moves:
                    pieces[item] = possible_moves

        if not pieces: pass # todo: endgame
        return pieces

    def get_reachable_fields(self, piece):
        pass

    def piece_id_to_addr(self, id):
        pass

    def dest_id_to_addr(self, id):
        pass

    def _id_generator(self):
        pass

    def get_possible_moves(self, piece) -> list:
        """
        :return:
        """
        moves = []
        captures = []
        direction = piece.player.value

        # check captures
        addresses = piece.get_my_diagonal_fields(max_dist=1, direction=direction)
        for addr in addresses:
            if self._is_capture_allowed(piece, addr):
                captures.append(addr)
                # todo: allow back piece capture
            elif self._is_move_allowed(piece, addr):
                moves.append(addr)

        # todo: create capturing paths and select the longest

        # example moves from (3,6): [(4,5), (4,7)]
        # example captures from (3,6): [[(5,4)], [(5,8), (6,7)]] so returns only [(5,8), (6,7)]
        return moves if not captures else captures

    def get_all_possible_moves(self, player):
        pieces = {}

    def _is_move_allowed(self, piece, addr):
        return isinstance(self.board[addr], EmptyField)

    def _is_capture_allowed(self, piece, addr):
        dir = _vector_sum(addr, piece.addr, reverse_addrs=True)

        field_behind = _vector_sum(piece.addr, dir, dir)
        if not _is_on_board(*field_behind):
            return False

        av = (isinstance(addr, Piece) and
             addr.player != piece.player and
             isinstance(self.board[field_behind], EmptyField))
        return av


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
    p = Piece
