from model.game import Game
from terminalView import *


class Controller:
    def __init__(self):
        self.game = Game()
        self.dialog = Dialog()

    def start_game(self):
        self.dialog.show_intro()
        self._play()

    def _play(self):
        with self.game:
            while self.game.continues():
                possible_moves = self.game.get_possible_moves()
                selected_move = self._get_next_move(possible_moves)
                self.game.move(selected_move)

        self.dialog.show_ending(self.game.winner)

    def _get_next_move(self, possible_moves):
        id_field_translator = IdFieldTranslator(possible_moves)
        piece = self._get_next_piece(id_field_translator)
        # todo: if its capturing chain, there is no point of selecting piece.
        # todo: also if there is only one to be selected - do not ask
        move = self._get_destination(piece, id_field_translator)
        # todo: if only one destination - single enter will work
        return move

    def _get_next_piece(self, translator):
        movable_pieces = translator.pieces_dict()
        self._print_board(movable_pieces)
        piece_id = self.dialog.get_piece(movable_pieces.values())
        return translator.id_to_piece(piece_id)

    def _get_destination(self, piece, translator):
        reachable_fields = translator.moves_dict(piece)
        # todo: add selected piece to reachable_fields to highlight it properly
        self._print_board(reachable_fields)
        move_id = self.dialog.get_dest(reachable_fields.values())
        return translator.id_to_move(move_id, piece)

    def _print_board(self, fields_with_id=None):
        if fields_with_id is None:
            fields_with_id = {}

        print_board(self.game.get_board(), fields_with_id)


class IdFieldTranslator:
    def __init__(self, possible_moves):
        self.possible_moves = possible_moves

    def _pieces(self):
        return [(piece.addr, piece.id) for piece in list(self.possible_moves.keys())]

    def _moves(self, piece):
        # todo: strange numbers location (1 far from 2, 1 next to 3)
        # todo: when capture chain and first move is mandatory, its id is not always == 1
        moves = self.possible_moves[piece]
        reachable_destinations = [move.dest for move in moves]
        ids = '123456789ABCDEFG'

        return zip(reachable_destinations, ids)

    def pieces_dict(self):
        return dict(self._pieces())

    def moves_dict(self, piece):
        return dict(self._moves(piece))

    def piece_ids(self):
        return [p[1] for p in self._pieces()]

    def move_ids(self, piece):
        return [m[1] for m in self._moves(piece)]

    def id_to_piece(self, id):
        id_to_addr = dict([(p[1], p[0]) for p in self._pieces()])
        addr_to_piece = dict([(p.addr, p) for p in self.possible_moves.keys()])
        return addr_to_piece[id_to_addr[id]]

    def id_to_move(self, id, piece):
        id_to_addr = dict([(m[1], m[0]) for m in self._moves(piece)])
        addr_to_move = dict([(m.dest, m) for m in self.possible_moves[piece]])
        return addr_to_move[id_to_addr[id]]


class Dialog:
    def __init__(self):
        self.intro_msg = "Hello. That's intro with tutorial."  # todo: intro
        self.whose_turn_msg = ""  # todo:
        self.select_piece_msg = "Please enter piece id you would like to move..."
        self.select_destination_msg = "Now please enter number with destination field or 0 to select different piece..."
        self.exit_confirmation_msg = "Are you sure you want to exit?"
        self.end_suffix = " player is the winner! Congratulations!!"

    def show_intro(self):
        print(self.intro_msg)

    def show_ending(self, player):
        print(player.name.capitalize(), self.end_suffix)

    def get_piece(self, available):
        while True:
            print(self.select_piece_msg)
            piece = str(input()).lower()
            if piece in available:
                return piece

    def get_dest(self, available):
        while True:
            print(self.select_destination_msg)
            dest = str(input()).upper()
            if dest in available:
                return dest
            # todo: click 0 to return to select capture not working


if __name__ == '__main__':
    c = Controller()
    c.start_game()
