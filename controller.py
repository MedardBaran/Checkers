from model import *
from terminalView import *

# todo: wybrany warcab powinien byc oznaczony w momencie wyboru pola docelowego


class Controller:
    def __init__(self):
        self.game = Game()
        self.dialog = Dialog()

    def start_game(self):
        self.dialog.show_intro()
        self._play()

    def _play(self):
        while True:
            possible_moves = self.game.get_possible_moves()
            selected_move = self._ask_about_next_move(possible_moves)
            self.game.move(selected_move)
            if self._is_end_game():
                winner = self.game.current_player
                self.dialog.show_ending(winner)
                break

    def _ask_about_next_move(self, possible_moves):
        # todo: refactor!

        id_field_translator = IdFieldTranslator(possible_moves)

        movable_pieces = id_field_translator.pieces_dict()
        self._print_board(movable_pieces)

        # ask about piece
        possible_answers = id_field_translator.piece_ids()
        piece_id = self.dialog.get_piece(possible_answers)
        selected_piece = id_field_translator.id_to_piece(piece_id)

        # print moves
        reachable_fields = id_field_translator.moves_dict(piece_id)
        self._print_board(reachable_fields)

        # ask about destination
        possible_answers = id_field_translator.move_ids(selected_piece)
        move_id = self.dialog.get_dest(possible_answers)

        return id_field_translator.id_to_move(move_id, selected_piece)

    def _print_board(self, fields_with_id=None):
        if fields_with_id is None:
            fields_with_id = {}

        print_board(self.game.get_board(), fields_with_id)

    def _is_end_game(self):
        # todo: calculate endgame
        return False


class IdFieldTranslator:
    def __init__(self, possible_moves):
        self.possible_moves = possible_moves

    def _pieces(self):
        pieces = list(self.possible_moves.keys())
        piece_addrs = [piece.addr for piece in pieces]
        ids = 'abcdefghijkl'

        return zip(piece_addrs, ids)

    def _moves(self, piece):
        moves = self.possible_moves[piece]
        reachable_destinations = [move.dest for move in moves]
        ids = '123456789ABCDEFG'

        return zip(reachable_destinations, ids)

    def pieces_dict(self):
        return dict(self._pieces())

    def moves_dict(self, piece_id):
        piece = self.id_to_piece(piece_id)
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
        self.whose_turn_msg = ""
        self.select_piece_msg = "Please enter piece id you would like to move..."
        self.select_destination_msg = "Now please enter number with destination field or 0 to select different piece..."
        self.exit_confirmation_msg = "Are you sure you want to exit?"
        self.end_msg = "And the winner is... "

    def show_intro(self):
        print(self.intro_msg)

    def show_ending(self, player):
        color = str(player).split(".")[-1].capitalize()
        print(self.end_msg)

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


if __name__ == '__main__':
    c = Controller()
    c.start_game()
