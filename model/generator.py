from model.items import EmptyField, Piece, King, Move, EndGameEvent
from collections import OrderedDict
import itertools as it


class MovesGenerator:
    def __init__(self, player, board, piece=None):
        self.player = player
        self.board = board
        self.max_length = 0
        self.pieces = []
        self.specific_piece = piece

    def generate(self):
        if self.specific_piece:
            self.pieces = [self.specific_piece]
        else:
            self.pieces = self._get_pieces()

        captures = self._get_captures()
        if self._any_available(captures):
            return captures

        moves = self._get_moves()
        if self._any_available(moves):
            return moves

        raise EndGameEvent(self.player.opponent)

    def _get_pieces(self):
        pieces = []
        for row in self.board():
            for item in row:
                if isinstance(item, Piece) and item.player == self.player:
                    pieces.append(item)
        return pieces

    def _get_captures(self):
        all_captures = OrderedDict()

        for piece in self.pieces:
            generator = _CapturesFinder(piece, self.board)
            captures = generator.generate()

            if captures:
                all_captures[piece] = captures

        all_captures = self._remove_all_but_longest(all_captures)

        return all_captures

    def _get_moves(self):
        all_moves = OrderedDict()

        for piece in self.pieces:
            generator = _MovesFinder(piece, self.board)
            moves = generator.generate()

            if moves:
                all_moves[piece] = moves

        return all_moves

    def _any_available(self, all_moves):
        for piece, moves in all_moves.items():
            if moves != []:
                return True
        return False

    def _remove_all_but_longest(self, captures_dict):
        if not captures_dict:
            return captures_dict

        max_len = max([len(i) for i in list(it.chain.from_iterable(captures_dict.values()))])

        longest = {}
        for piece, captures_list in captures_dict.items():
            captures = [c for c in captures_list if len(c) == max_len]
            if captures:
                longest[piece] = captures

        return longest


class _Finder:
    def __init__(self, piece, board):
        self.piece = piece
        self.board = board

    def generate(self):
        raise NotImplementedError()

    @staticmethod
    def _get_fields_between(addr1, addr2):
        fields = []
        r1, c1 = addr1
        r2, c2 = addr2

        assert abs(r2-r1) == abs(c2-c1), f"{addr1} -> {addr2}, impossible move."

        length = abs(r2-r1)
        direction = (int((r2-r1)/length), int((c2-c1)/length))

        for i in range(1, length):
            field = _vector_sum(addr1, *(direction, )*i)
            fields.append(field)
        return fields


class _CapturesFinder(_Finder):
    def generate(self):
        reachable = self.piece.get_my_diagonal_neighbours(max_dist=self.piece.max_distance+1,
                                                          min_dist=2, direction='nwse')
        result = []

        for destination in reachable:
            target = self._get_piece_to_capture(destination)
            if target is None: continue

            this_capture = Move(self.piece, destination, captured_piece=target)
            following_captures = self._find_following_captures(this_capture)

            if following_captures:
                for following_capture in following_captures:
                    capture = this_capture.clone()
                    capture.following_move = following_capture
                    result.append(capture)
            else:
                result.append(this_capture)

        return result

    def _get_piece_to_capture(self, destination):
        possible_victims = []
        addrs_between = self._get_fields_between(self.piece.addr, destination)
        for addr in addrs_between:
            field = self.board()[addr]

            is_occupied = isinstance(field, Piece) or isinstance(field, King)
            is_occupied_by_other_player = hasattr(field, "player") and field.player != self.piece.player

            if is_occupied and not is_occupied_by_other_player:
                return None
            elif is_occupied and is_occupied_by_other_player:
                possible_victims.append(field)

        is_destination_empty = isinstance(self.board()[destination], EmptyField)
        if len(possible_victims) == 1 and is_destination_empty:
            return possible_victims[0]
        else:
            return None

    def _find_following_captures(self, previous):
        board = self.board.clone()
        board.move(previous.piece.clone(), previous.dest)
        board.pick_up(previous.captured_piece)
        piece = board()[previous.dest]

        generator = _CapturesFinder(piece, board)
        captures = generator.generate()

        return captures


class _MovesFinder(_Finder):
    def generate(self):
        moves = []
        dir_to_move = 'nwse' if isinstance(self.piece, King) else self.piece.player.value

        addrs = self.piece.get_my_diagonal_neighbours(max_dist=self.piece.max_distance, direction=dir_to_move)

        for addr in addrs:
            if self._has_clear_path(destination=addr):
                move = Move(self.piece, addr)
                moves.append(move)

        return moves

    def _has_clear_path(self, destination):
        addrs_between = self._get_fields_between(self.piece.addr, destination)

        for addr in [*addrs_between, destination]:
            field = self.board()[addr]
            is_occupied = isinstance(field, Piece) or isinstance(field, King)
            if is_occupied:
                return False
        return True


def _vector_sum(basic_addr, *addrs, reverse_addrs=False):
    temp = []
    if reverse_addrs:
        for addr in addrs:
            temp.append([-1 * i for i in addr])
    else:
        temp = addrs

    return tuple([sum(addr) for addr in zip(basic_addr, *temp)])
