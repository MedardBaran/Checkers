import itertools as it

from model.items import Board, Player, Move, EndGameEvent
from model.generator import MovesGenerator


class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = Player.white
        self.player_iterator = it.cycle([Player.red, Player.white])
        self.piece_to_continue = None

        self.winner = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is EndGameEvent:
            self.winner = exc_value.args[0]
            return True

    def get_possible_moves(self):
        gen = MovesGenerator(self.current_player, self.board, self.piece_to_continue)
        return gen.generate()

    def move(self, move: Move):
        piece = move.piece

        self.board.move(piece, move.dest)
        if move.is_capturing:
            self.board.pick_up(move.captured_piece)

        if self._can_be_upgraded(piece):
            self.board.put(piece.upgrade())

        if move.following_move:
            self.piece_to_continue = piece
        else:
            self.piece_to_continue = None
            self._change_player()

    def get_board(self):
        return self.board()

    def continues(self):
        return self.winner is None

    def _change_player(self):
        self.current_player = next(self.player_iterator)

    def _can_be_upgraded(self, piece):
        last_row = 0 if piece.player == Player.red else 7

        has_reached_last_row = piece.row == last_row
        is_piece = hasattr(piece, 'upgrade')

        return has_reached_last_row and is_piece


if __name__ == '__main__':
    b = Game()
    print('end')
