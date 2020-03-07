import itertools as it

from model.items import Board, Player, Move
from model.generator import MovesGenerator


class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = Player.white
        self.player_iterator = it.cycle([Player.red, Player.white])
        self.piece_to_continue = None
        # todo: endgame observer?

    def get_possible_moves(self):
        gen = MovesGenerator(self.current_player, self.board, self.piece_to_continue)
        return gen.generate()

    def move(self, move: Move):
        self.board.move(move.piece, move.dest)
        if move.is_capturing:
            self.board.pick_up(move.captured_piece)

        if move.following_move:
            self.piece_to_continue = move.piece
        else:
            self.piece_to_continue = None
            self._change_player()

    def get_board(self):
        return self.board()

    def _change_player(self):
        self.current_player = next(self.player_iterator)

    def _is_end_game(self):
        # todo:
        print(f"Game ends. {self.current_player} player wins.")


if __name__ == '__main__':
    b = Game()
    print('end')
