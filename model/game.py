import itertools as it

from model.items import Board, Player, Move
from model.generator import MovesGenerator


class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = Player.white
        self.player_iterator = it.cycle([Player.red, Player.white])
        self.following_move = None
        # todo: endgame observer?

    def get_possible_moves(self):
        if self.following_move:
            following_move = self.following_move
            self.following_move = None
            return following_move

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

        if move.following_move:
            self.following_move = {move.piece: [move.following_move]}
        else:
            self.following_move = None
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
