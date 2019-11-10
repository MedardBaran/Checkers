from enum import Enum
import string as st
import numpy as np
import itertools as it


class Player(Enum):
    white = 'n'  # and goes south
    red = 's'  # and goes north


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

    def get_diagonal_fields(self, max_dist=7, min_dist=1, direction='nwse'):
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


class Game:
    # region def.__init__()
    def __init__(self):
        self._init_board()
        for p in Player:
            self._init_pieces(p)

    # todo: endgame observer?

    def _init_board(self):
        self.board = np.empty((8, 8), dtype=BoardMember)
        for r, c in it.product(range(8), range(8)):
            av = not (r + c + 1) % 2
            self.board[r, c] = EmptyField(r, c, av)

    def _init_pieces(self, player):
        starting_rows = self.board[:3] if player == Player.white else self.board[-3:]
        for (addr, field) in np.ndenumerate(starting_rows):
            if field.available:
                starting_rows[addr] = Piece(field.row, field.col, player)

    # endregion def.__init__()

    def get_board(self):
        return self.board

    def move(self, piece_addr, dest):
        # move obj
        self.board[piece_addr], self.board[dest] = self.board[dest], self.board[piece_addr]

        # update addr
        self.board[piece_addr].addr = piece_addr
        self.board[dest].addr = dest

        self._delete_pieces_between(dest, piece_addr)

    def get_possible_moves(self, piece) -> dict:
        """
        :return: {id: address}
        """
        moves = {}
        captures = {}
        direction = piece.player.value

        # check captures
        addresses = piece.get_diagonal_fields(max_dist=1, direction=direction)
        for addr in addresses:
            if self._is_capture_allowed(piece, addr):
                capture_id = len(captures) + 1
                captures[capture_id] = addr
                # todo: allow back piece capture
            elif self._is_move_allowed(piece, addr):
                move_id = len(moves) + 1
                moves[move_id] = addr

        # todo: create capturing paths and select the longest

        # example moves from (3,6): [(4,5), (4,7)]
        # example captures from (3,6): [[(5,4)], [(5,8), (6,7)]] so returns only [(5,8), (6,7)]
        return moves if not captures else captures

    def get_movable_pieces(self, player):
        pieces = {}
        for row in self.board:
            for item in row:
                if not isinstance(item, Piece) or not item.player == player: continue
                possible_moves = self.get_possible_moves(item)
                if possible_moves:
                    pieces[item.addr] = possible_moves

        if not pieces: pass # todo: endgame
        return pieces

    def _is_move_allowed(self, piece, addr):
        return isinstance(self.board[addr], EmptyField)

    def _is_capture_allowed(self, piece, addr):
        dir = _vector_sum(addr, piece.addr, reverse_addrs=True)

        field_behind = _vector_sum(piece.addr, dir, dir)
        if not _is_on_board(*field_behind):
            return False

        av = isinstance(addr, Piece) and \
             addr.player != piece.player and \
             isinstance(self.board[field_behind], EmptyField)
        return av

    def _delete_pieces_between(self, addr1, addr2):
        diff = _vector_sum(addr1, addr2, reverse_addrs=True)
        dist = abs(diff[0])
        dir = diff[0]/dist, diff[1]/dist

        for i in range(1, dist):
            addr_between = _vector_sum(addr1, dir)
            field_between = self.board[addr_between]

            if isinstance(field_between, Piece):
                self.board[addr_between] = EmptyField(*addr_between, available=True)
                field_between.decr_items_counter()
                break

    def _addr_to_id(self, addrs):
        res = {}

        for addr in list(addrs):
            res[self.board[addr].id] = addr

        return res


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
    print(b.get_board())
    p = Piece
